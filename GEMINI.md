# GEMINI.md

Guidance for using Google Gemini (or similar AI coding assistants) with this repository.

## Project Overview

Chirality Framework is a semantic calculator implementing a fixed 3‑stage interpretation pipeline. It focuses on a canonical algorithm and predictable outputs rather than framework flexibility.

- Quick start: see `README.md`
- Tutorial: `docs/TUTORIAL.md`
- CLI Quick Reference: `docs/API_REFERENCE.md#cli-reference`
- App contract (producer): `docs/INTERFACE.md`

## Day‑to‑Day Commands

Testing and quality:

```bash
pytest -v               # uses mocks (no live LLM calls)
mypy chirality/         # strict typing
black chirality/ tests/ # formatting
```

CLI (common):

```bash
# Single cell (deterministic echo)
python3 -m chirality.cli compute-cell C --i 0 --j 0 -v

# One matrix with legacy snapshot
python3 -m chirality.cli compute-matrix X --resolver echo --snapshot-jsonl -v

# Full pipeline (dev mode)
python3 -m chirality.cli compute-pipeline --resolver echo --snapshot-jsonl --include-base -v

# App mode (artifacts for chirality-app)
python3 -m chirality.cli compute-pipeline \
  --resolver echo \
  --out runs/my-run-1 \
  --problem-file problem.json \
  --max-seconds 900
```

## App Integration (Producer Contract)

App mode writes:
- `runs/<run_id>/index.json` (atomic, last)
- `runs/<run_id>/snapshots/{C,D,X,E}.jsonl` (cells-jsonl-v1)

Stdout (last line only):
```json
{"run_id":"<run_id>","manifest":"runs/<run_id>/index.json"}
```

Manifest includes `framework_schema_version: "1.0.0"`, and per‑matrix `path`, `format`, `records`, `sha256`, `bytes`.

## Resolver Notes

- Default for development: `echo` (deterministic, no API calls).
- OpenAI resolver optional: install extras `pip install 'chirality-framework[openai]'` and set `OPENAI_API_KEY`.
- Tests must use mocks (`tests/mocks.py`); do not introduce live LLM calls in tests.

## Contribution Guardrails

- Style: Black; Types: mypy (strict) — see `pyproject.toml`.
- Naming: prefer `compute_cell_*`, `compute_matrix_*` (avoid deprecated `synthesize_*`).
- Provenance keys: `stage_1_construct` through `stage_5_final_synthesis`.
- Do not change canonical matrices (`chirality/core/matrices.py`) unless updating the spec.
- Secrets: never commit keys; use environment variables or `.env` (not committed).
- Conventional Commits for messages, e.g., `docs(cli): ...`, `feat(exporter): ...`.

## Suggested Workflow for Changes

1. Read relevant docs (`README.md`, `docs/TUTORIAL.md`, `docs/API_REFERENCE.md`).
2. Make focused edits; keep changes minimal and aligned with existing patterns.
3. Run `pytest -v`, `mypy`, and (optionally) `black` locally.
4. For CLI features, add/update tests under `tests/` (use mocks, no network).
5. If adding artifacts/manifest logic, ensure atomic writes and integrity fields.

## Common Pitfalls

- Printing extra lines in app mode: ensure the CLI prints only the final JSON line on success.
- Omitting `records/sha256/bytes` in the manifest: app ingestion requires these.
- Writing to non‑atomic files: always write temp + `os.replace`.
- Forgetting run‑relative paths in `index.json` (must be relative to `runs/<run_id>/`).
