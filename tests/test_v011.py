import random
import unittest

from tool_contract_fuzzer.core import cases, invalid_variants, value


class BoundaryGenerationTests(unittest.TestCase):
    def test_generator_honors_numeric_and_length_bounds(self):
        rng = random.Random(7)
        schema = {
            "type": "object",
            "required": ["n", "name"],
            "properties": {
                "n": {"type": "integer", "minimum": 5, "maximum": 8},
                "name": {"type": "string", "minLength": 3, "maxLength": 5},
            },
        }
        for _ in range(20):
            generated = value(schema, rng)
            self.assertLessEqual(5, generated["n"])
            self.assertLessEqual(generated["n"], 8)
            self.assertLessEqual(3, len(generated["name"]))
            self.assertLessEqual(len(generated["name"]), 5)

    def test_invalid_cases_target_boundaries(self):
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["n"],
            "properties": {"n": {"type": "integer", "minimum": 2, "maximum": 4}},
        }
        good = {"n": 3}
        reasons = {reason for reason, _ in invalid_variants(schema, good)}
        self.assertIn("below-minimum:n", reasons)
        self.assertIn("above-maximum:n", reasons)
        self.assertIn("additional-property", reasons)

    def test_case_generation_is_seed_deterministic(self):
        schema = {"type": "integer", "minimum": 1, "maximum": 9}
        self.assertEqual(list(cases(schema, seed=42, count=4)), list(cases(schema, seed=42, count=4)))


if __name__ == "__main__":
    unittest.main()
