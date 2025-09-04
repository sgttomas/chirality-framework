# Repository Guidelines

## Project Structure & Module Organization
- Source: `chirality/` (core code), `chirality/core/*` (algorithm, resolvers, tracer, exporter).
- CLI: `chirality/cli.py` (`compute-cell`, `compute-matrix`, `compute-pipeline`, `render-viewer`, `info`).
- Tests: `tests/` (unit tests, mocks); Docs: `docs/`.
- Versioning: `VERSION.md`; packaging: `pyproject.toml`.

## Build, Test, and Development Commands
- Build distributions: `python3 -m build`.
- Run tests: `.venv/bin/pytest -v`.
- Run full pipeline & view results: `python3 -m chirality.cli compute-pipeline --snapshot-jsonl && python3 -m chirality.cli render-viewer --latest --open`.
- Tracing: add `--trace` or `--trace-only` to generate JSONL files in `traces/`.
- Snapshots: add `--snapshot-jsonl` to generate matrix snapshots in `snapshots/`.

## Coding Style & Naming Conventions
- Python 3.9+; format with Black. Type‑check with mypy (strict in `pyproject.toml`).
- Naming: use `compute_cell_*`, `compute_matrix_*`; avoid deprecated `synthesize_*`.
- Provenance (dict per stage): `stage_1_construct`, `stage_2_semantic`, `stage_3_column_lensed`, `stage_4_row_lensed`, `stage_5_final_synthesis`.

## Testing Guidelines
- Framework: `pytest`; use `tests/mocks.py` (no live LLM calls).
- Assert on universal provenance fields and final values. Put new tests in `tests/core/`.

## Commit & Pull Request Guidelines
- Conventional Commits examples:
  - `feat(exporter): add run‑scoped stages`
  - `fix(cli): print run_id when exporting`
- PRs optional for solo work; include a short summary and breaking notes if used.

## Security & Configuration Tips
- Secrets: never commit keys; use `.env` or OIDC (Trusted Publishing).
- Neo4j: set `NEO4J_URI/USER/PASSWORD`; exporter creates constraints/indexes automatically.

## Architecture Overview (Quick)
- Algorithm: 3 stages with universal lensing (Column → Row → Final).
- D matrix: mechanical sentence (semantic addition) + universal lensing.
- Exporter: writes Matrix/Cell/Stage and Run nodes; filter queries by `(:Run {id})` when analyzing.
