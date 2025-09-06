# GEMINI.md

Guidance for using Google Gemini (or similar AI coding assistants) with this repository.

## Project Overview

Chirality Framework is a semantic calculator implementing a canonical pipeline that features a unified **Combined Lensing** step for all semantic interpretation. It focuses on a canonical algorithm and predictable outputs rather than framework flexibility.

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

- **CRITICAL**: Per maintainer directive, the OpenAI resolver MUST use the `client.responses.create()` method. The `client.chat.completions.create()` API must NOT be used.
- Default for development: `echo` (deterministic, no API calls).
- OpenAI resolver optional: install extras `pip install 'chirality-framework[openai]'` and set `OPENAI_API_KEY`.
- Tests must use mocks (`tests/mocks.py`); do not introduce live LLM calls in tests.

## Contribution Guardrails

- Style: Black; Types: mypy (strict) — see `pyproject.toml`.
- Naming: prefer `compute_cell_*`, `compute_matrix_*` (avoid deprecated `synthesize_*`).
- Provenance keys: `stage_1_construct`, `stage_2_semantic`, `stage_3_combined_lensed`.
- Do not change canonical matrices (`chirality/core/matrices.py`) unless updating the spec.
- Secrets: never commit keys; use environment variables or `.env` (not committed).
- Conventional Commits for messages, e.g., `docs(cli): ...`, `feat(exporter): ...`.

## Suggested Workflow for Changes

1.  **Analyze the Request**: Understand whether the request involves changing the framework's mechanics (code) or its semantics (prompt assets).
2.  **For Code Changes**: Read the relevant modules in `chirality/core/` and `chirality/lib/`. Propose changes that align with the existing canonical pipeline and asset-based architecture.
3.  **For Semantic Changes**: Propose changes to the maintainer for the content of files in `chirality/prompt_assets/`. Do not edit these files directly. Reference the **Prompt Authoring Policy**.
4.  **Testing**: Ensure any proposed code changes are accompanied by updates to the tests in `tests/`. Use the mock/echo resolver for all tests.
5.  **Validation**: Run `pytest -v`, `mypy`, and `black` locally before finalizing any proposal.

## Common Pitfalls

- Printing extra lines in app mode: ensure the CLI prints only the final JSON line on success.
- Omitting `records/sha256/bytes` in the manifest: app ingestion requires these.
- Writing to non‑atomic files: always write temp + `os.replace`.
- Forgetting run‑relative paths in `index.json` (must be relative to `runs/<run_id>/`).

## Immutable Files Policy
- **Normative Specification**: Under no circumstances should you ever modify `chirality/normative_spec.txt`. The semantics of the framework are canonical and must not be changed. If you believe a change is required, you must notify the user and explain your reasoning. The user will be responsible for making any approved changes.

## Prompt Authoring Policy
- All prompts (including system prompts, station briefs, and any semantic instructions) are part of the normative specification.
- Only the user (maintainer) may author or edit the semantic content of prompts. As an LLM agent, I must NEVER write or change prompt semantics.
- I may only propose changes to prompt *structure* (e.g., variable interpolation, templating, or context assembly order) and must not implement them without explicit user direction.
- Each station must have its own station brief to ground the LLM; the user authors these briefs. The E station brief is especially critical and is owned by the user.