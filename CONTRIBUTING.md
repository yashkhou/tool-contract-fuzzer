# Contributing

Changes to generation or mutation behavior should include deterministic seeded regression tests.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python3 -m compileall -q src tests
```
