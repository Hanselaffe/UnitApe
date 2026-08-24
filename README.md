# UnitApe

UnitApe is a small static-analysis utility that generates explicit `unittest` skeletons for top-level classes in Python source files.

## 2026 refresh

The maintenance refresh fixes several problems in the original prototype:

- generated files now contain real line breaks and valid Python syntax;
- source code is parsed with `ast` only and is never imported or executed during generation;
- unconditional `assertTrue(True)` placeholders are replaced with explicit `@unittest.skip(...)` TODOs so generated suites cannot create false confidence;
- output filenames include both source-module and class names to reduce collisions;
- existing files are not overwritten unless `--overwrite` is given;
- deterministic recursive file ordering and clearer error handling;
- Windows-safe core module `unitape_core.py` with the historical `UnitApe.py` entry point retained for compatibility;
- standard-library unit tests; no third-party dependencies.

## Requirements

- Python 3.10+

## Usage

```bash
python UnitApe.py path/to/source.py path/to/tests
```

or for a whole directory:

```bash
python UnitApe.py path/to/project path/to/generated-tests
```

To intentionally replace generated files:

```bash
python UnitApe.py path/to/project path/to/generated-tests --overwrite
```

The implementation can also be imported directly:

```python
import unitape_core
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Important limitation

UnitApe creates reviewable test skeletons, not complete tests. It deliberately does not guess expected behavior and does not automatically import or execute the analyzed application. Every skipped placeholder must be replaced with a behavior-focused assertion before it contributes real test coverage.
