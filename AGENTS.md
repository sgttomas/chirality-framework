# Repository Guidelines

## Project Structure & Module Organization
- Source: `chirality/` (core code), `chirality/lib/*` (prompt system), `chirality/core/*` (algorithm, llm client, tracer, exporter).
- Prompt Assets: `chirality/prompt_assets/*` (maintainer-authored semantic content).
- CLI: `chirality/cli.py` (`compute-cell`, `compute-matrix`, `compute-pipeline`, `render-viewer`, `info`).
- Tests: `tests/` (unit tests, mocks); Docs: `docs/`.
- Versioning: `VERSION.md`; packaging: `pyproject.toml`.

## Build, Test, and Development Commands
- Build distributions: `python3 -m build`.
- Run tests: `.venv/bin/pytest -v`.
- Run full pipeline & view results: `python3 -m chirality.cli compute-pipeline --snapshot-jsonl && python3 -m chirality.cli render-viewer --latest --open`.
- Tracing: add `--trace` or `--trace-only` to generate JSONL files in `traces/`.
- Snapshots: add `--snapshot-jsonl` to generate matrix snapshots in `snapshots/`.

### App Integration Mode (Producer Contract)
- Contract snapshots + manifest for external apps (e.g., chirality-app):
  - `python3 -m chirality.cli compute-pipeline --resolver echo --out runs/<run_id> --problem-file problem.json --max-seconds 900`
  - On success, stdout last line only: `{ "run_id": "<run_id>", "manifest": "runs/<run_id>/index.json" }`.
  - Exit codes: `0` success; `2` invalid args; `3` timeout; `4` I/O; `5` resolver; `1` general.
  - Writes per-cell JSONL for `C,D,X,E` under `runs/<run_id>/snapshots/` and a manifest `index.json` (atomic, last).
  - Backward compatibility: also writes legacy full-matrix snapshots for all computed matrices under `snapshots/<run_id>/` for the built-in viewer.

## Coding Style & Naming Conventions
- Python 3.9+; format with Black. Type‑check with mypy (strict in `pyproject.toml`).
- Naming: use `compute_cell_*`, `compute_matrix_*`; avoid deprecated `synthesize_*`.
- Provenance (dict per stage): `stage_1_construct`, `stage_2_semantic`, `stage_3_combined_lensed`.

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

## Immutable Files Policy
- Do not modify `chirality/normative_spec.txt` under any circumstances. If changes are desired, notify the maintainer with a proposed edit; the maintainer will apply approved updates. This file encodes semantic canon and is outside agent change authority.

## Prompt Authoring Policy
- All prompts (including system prompts, station briefs, and any semantic instructions) are part of the normative specification.
- Only the maintainer may author or edit semantic content of prompts. LLM agents must NEVER write or change prompt semantics.
- LLM agents may propose prompt structuring changes (e.g., variable interpolation, templating, or context assembly order) but must not implement them without explicit maintainer direction.
- Each station must have its own station brief to ground the LLM; the maintainer authors these briefs (not the agent). The E station brief is especially critical and is owned by the maintainer.

## Prompt Assets Policy
- Location: All prompt assets live under `chirality/prompt_assets/` and are owned by the maintainer.
- Integrity: Assets are declared in `chirality/prompt_assets/metadata.yml` with `id`, `path`, `sha256`, `version`, `last_modified`, and `size_bytes`. The prompt registry validates checksums and sizes on load.
- Placeholders: Only explicitly present placeholders are substituted. Allowed placeholders: `{{row_label}}`, `{{col_label}}`, `{{content}}`, `{{station_brief}}`, and `{{terms}}` (if referenced by an operator asset). No other implicit context is injected.
- Stations vs Components: Station briefs are keyed by station (Requirements, Objectives, Verification, Validation, Evaluation). Components (C, D, F, X, Z, E, etc.) are used to select the correct station brief internally.
- No optionality: No exemplars, ontology cards, env overrides, or per-station configs. The semantic valley is a canonical algorithm; we implement a single approach.

## LLM API Policy
- Approved API: Use the OpenAI Responses API exclusively. Chat Completions is prohibited.
- Single wrapper: All LLM calls must go through `chirality/core/llm_client.py` (Responses API wrapper). Do not instantiate SDK clients or call APIs elsewhere.
- Global config only: Model, `temperature`, `top_p`, and optional `seed` are defined centrally in `chirality/core/llm_config.py`. Do not add per-station or per-stage decoding configs.
- Response format: Always request `response_format: { type: "json_object" }` and expect a single JSON object with keys `text`, `terms_used`, and `warnings` (as specified by the frontend INTERFACE). Do not post-process or truncate the `text` field.
- Token policy: Do not impose artificial output caps. Compute a safe `max_output_tokens` from the model’s remaining context if required by the API, but do not truncate or otherwise edit model output.
- No prompt edits by agents: Agents must not change prompt semantics. Only maintainer-authored assets in `chirality/prompt_assets/` are used by the prompt builder.
- Enforcement: CI checks MUST fail if any use of Chat Completions is detected (see CI step below). PRs violating this policy will be rejected.

## Canonical Pipeline Policy
- Combined Lensing Only: All matrices use a single unified “Combined Lensing” call (row × col × station). Legacy column/row/synthesis lensing helpers and calls are removed.
- Stage 2: C, X, E use semantic multiply; F uses element-wise; D uses mechanical addition (no LLM); Z uses Validation combined lens (shift semantics embedded).
- Context Passing: Never inject problem statements or unrelated context. Only placeholders present in assets are substituted.
- Provenance: Every LLM call records asset ids/hashes/versions, strategy="combined", station (inferred from the station brief asset), prompt hash, model/decoding params, and timings.

### CI Enforcement Snippet (GitHub Actions)
Add a job that fails on any Chat Completions usage (excluding docs):

```yaml
name: Policy Checks

on: [push, pull_request]

jobs:
  enforce-llm-api-policy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install ripgrep
        run: sudo apt-get update && sudo apt-get install -y ripgrep
      - name: Forbid Chat Completions usage
        run: |
          set -e
          if rg -n "chat\\.completions|ChatCompletion" --hidden \
               --glob '!**/docs/**' --glob '!**/.venv/**' --glob '!**/venv/**' ; then
            echo "Forbidden Chat Completions usage detected. Use the Responses API via llm_client.py." >&2
            exit 1
          else
            echo "No forbidden Chat Completions usage found."
          fi
```

### Alternative Local Check (optional)
Run locally to catch issues before committing:

```bash
if rg -n 'chat\.completions|ChatCompletion' --hidden --glob '!**/docs/**' --glob '!**/.venv/**' --glob '!**/venv/**'; then
  echo "Forbidden Chat Completions usage detected. Use the Responses API via llm_client.py." >&2
  exit 1
fi
```

## Architecture Overview (Quick)
- Algorithm: A canonical pipeline featuring a unified **Combined Lensing** step for all semantic interpretation.
- Prompts: All prompts are assembled from version-controlled, maintainer-authored assets in `chirality/prompt_assets/`.
- D matrix: Follows the canonical pipeline: a mechanical sentence construction followed by Combined Lensing.
- Exporter: writes Matrix/Cell/Stage and Run nodes; filter queries by `(:Run {id})` when analyzing.

See also:
- `docs/INTERFACE.md`: producer mirror of the chirality-app contract (app mode specifics).
