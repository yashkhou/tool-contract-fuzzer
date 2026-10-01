> [!IMPORTANT]
> **This project now lives in [agent-reliability-lab](https://github.com/yashkhou/agent-reliability-lab/tree/main/packages/tool-contract-fuzzer).** Its full history was moved there and this repository is archived.
>
> `pip install "git+https://github.com/yashkhou/agent-reliability-lab#subdirectory=packages/tool-contract-fuzzer"`


# tool-contract-fuzzer

Deterministic property-style fuzzing for JSON-schema tool contracts, including invalid-call generation and failure shrinking.

## What it does

- generates valid values for a practical JSON Schema subset
- produces targeted invalid variants such as missing required keys and wrong types
- runs invariants against generated calls with reproducible seeds
- shrinks failing dictionaries, lists, strings and integers into smaller repro cases

## Quick start

```bash
PYTHONPATH=src python -m tool_contract_fuzzer examples/schema.json --seed 7 --count 4
```

No model API, network service, or third-party package is required.

## Architecture

A schema generator creates deterministic valid calls. Mutators derive invalid siblings. The runner records invariant failures and the shrinker repeatedly removes structure while preserving the failure predicate.

See [`docs/architecture.md`](docs/architecture.md) for the data model and trade-offs.

## V1 boundary

V1 covers object, array, string, integer, number, boolean and enum constraints; regex patterns and cross-field schema logic are not implemented.

## Development

```bash
python -m unittest discover -s tests -v
```

MIT licensed.


## v0.1.1

**Boundary-aware schema generation.** Generators now honor common numeric/string/array bounds and invalid cases deliberately probe boundary, enum, type, required-field, and additional-property failures.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```
