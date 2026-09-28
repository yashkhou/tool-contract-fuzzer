# Architecture

A schema generator creates deterministic valid calls. Mutators derive invalid siblings. The runner records invariant failures and the shrinker repeatedly removes structure while preserving the failure predicate.

## Design constraints

- deterministic offline behavior
- explicit machine-readable inputs and outputs
- small standard-library surface area
- failures are surfaced rather than hidden

## V1 limitation

V1 covers object, array, string, integer, number, boolean and enum constraints; regex patterns and cross-field schema logic are not implemented.
