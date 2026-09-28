from __future__ import annotations

import random
from copy import deepcopy


def _bounds(schema: dict, integer: bool) -> tuple[float, float]:
    lo = schema.get("minimum", 0)
    hi = schema.get("maximum", 100 if integer else 10)
    if "exclusiveMinimum" in schema:
        lo = schema["exclusiveMinimum"] + (1 if integer else 1e-6)
    if "exclusiveMaximum" in schema:
        hi = schema["exclusiveMaximum"] - (1 if integer else 1e-6)
    if lo > hi:
        raise ValueError("numeric schema has no valid values")
    return lo, hi


def value(schema: dict, rng: random.Random):
    if "const" in schema:
        return schema["const"]
    if "enum" in schema:
        if not schema["enum"]:
            raise ValueError("enum must not be empty")
        return rng.choice(schema["enum"])
    t = schema.get("type", "object")
    if t == "object":
        required = set(schema.get("required", []))
        return {
            key: value(subschema, rng)
            for key, subschema in schema.get("properties", {}).items()
            if key in required or rng.random() > 0.35
        }
    if t == "array":
        lo = int(schema.get("minItems", 0))
        hi = min(int(schema.get("maxItems", max(lo, 3))), max(lo, 3))
        if hi < lo:
            raise ValueError("array schema has maxItems < minItems")
        return [value(schema.get("items", {}), rng) for _ in range(rng.randint(lo, hi))]
    if t == "string":
        lo = int(schema.get("minLength", 0))
        hi = int(schema.get("maxLength", max(lo, 12)))
        if hi < lo:
            raise ValueError("string schema has maxLength < minLength")
        n = rng.randint(lo, min(hi, max(lo, 12)))
        return "s" * n
    if t == "integer":
        lo, hi = _bounds(schema, True)
        return rng.randint(int(lo), int(hi))
    if t == "number":
        lo, hi = _bounds(schema, False)
        return round(rng.uniform(float(lo), float(hi)), 6)
    if t == "boolean":
        return bool(rng.getrandbits(1))
    if t == "null":
        return None
    raise ValueError(f"unsupported schema type: {t!r}")


def _wrong_type(t: str):
    return {"object": [], "array": {}, "string": 1, "integer": "1", "number": "1", "boolean": 0, "null": False}.get(t, None)


def _scalar_invalid_variants(schema: dict, good):
    t = schema.get("type")
    if "const" in schema:
        yield "const-mismatch", object()
    if "enum" in schema:
        sentinel = "__outside_enum__"
        if sentinel not in schema["enum"]:
            yield "enum-outside", sentinel
    if t == "string":
        if int(schema.get("minLength", 0)) > 0:
            yield "below-minLength", "" * 0
        if "maxLength" in schema:
            yield "above-maxLength", "x" * (int(schema["maxLength"]) + 1)
    if t in ("integer", "number"):
        if "minimum" in schema:
            yield "below-minimum", schema["minimum"] - 1
        if "maximum" in schema:
            yield "above-maximum", schema["maximum"] + 1
        if "exclusiveMinimum" in schema:
            yield "at-exclusiveMinimum", schema["exclusiveMinimum"]
        if "exclusiveMaximum" in schema:
            yield "at-exclusiveMaximum", schema["exclusiveMaximum"]
    if t == "array":
        if int(schema.get("minItems", 0)) > 0:
            yield "below-minItems", []
        if "maxItems" in schema:
            yield "above-maxItems", [None] * (int(schema["maxItems"]) + 1)
    if t:
        yield "wrong-type", _wrong_type(t)


def invalid_variants(schema: dict, good):
    out = []
    t = schema.get("type")
    if t == "object" and isinstance(good, dict):
        for key in schema.get("required", []):
            if key in good:
                candidate = dict(good)
                candidate.pop(key)
                out.append((f"missing-required:{key}", candidate))
        for key, subschema in schema.get("properties", {}).items():
            if key not in good:
                continue
            for reason, invalid in _scalar_invalid_variants(subschema, good[key]):
                candidate = deepcopy(good)
                candidate[key] = invalid
                out.append((f"{reason}:{key}", candidate))
        if schema.get("additionalProperties") is False:
            candidate = dict(good)
            candidate["__unexpected__"] = True
            out.append(("additional-property", candidate))
    else:
        out.extend(_scalar_invalid_variants(schema, good))
    return out


def cases(schema: dict, seed: int = 0, count: int = 10):
    rng = random.Random(seed)
    for i in range(count):
        good = value(schema, rng)
        yield {"id": f"valid-{i}", "valid": True, "value": good}
        for reason, bad in invalid_variants(schema, good):
            yield {"id": f"invalid-{i}-{reason}", "valid": False, "value": bad}


def shrink(obj, predicate):
    cur = obj
    while True:
        if isinstance(cur, dict):
            opts = [{k: v for k, v in cur.items() if k != drop} for drop in list(cur)]
        elif isinstance(cur, list):
            opts = [cur[:i] + cur[i + 1 :] for i in range(len(cur))]
        elif isinstance(cur, str) and len(cur) > 1:
            opts = [cur[: max(1, len(cur) // 2)]]
        elif isinstance(cur, int) and cur:
            opts = [cur // 2, 0]
        else:
            opts = []
        nxt = next((candidate for candidate in opts if predicate(candidate)), None)
        if nxt is None:
            return cur
        cur = nxt
