# Implementation note

Working V1 scope: Deterministic property-style fuzzing for JSON-schema tool contracts, including invalid-call generation and failure shrinking.

Verified with `python -m unittest discover -s tests -v`.

Known boundary: V1 covers object, array, string, integer, number, boolean and enum constraints; regex patterns and cross-field schema logic are not implemented.
