# Chirality Framework: A Semantic Calculator

[![PyPI](https://img.shields.io/pypi/v/chirality-framework.svg)](https://pypi.org/project/chirality-framework/)
[![Python versions](https://img.shields.io/pypi/pyversions/chirality-framework.svg)](https://pypi.org/project/chirality-framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Publish](https://github.com/sgttomas/chirality-framework/actions/workflows/python-publish.yml/badge.svg)](https://github.com/sgttomas/chirality-framework/actions/workflows/python-publish.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/tag/sgttomas/chirality-framework?sort=semver&label=release)](https://github.com/sgttomas/chirality-framework/tags)

**Version: 17.1.0** | **Status: Active Development**

The Chirality Framework is a "semantic calculator" designed to execute a fixed, canonical algorithm for structured problem-solving. It transforms a set of base matrices through a multi-stage semantic pipeline, producing a series of derived matrices that represent a complete traversal of a "semantic valley" from problem to evaluation.

The value of this project is in the unique, insightful **output** of the calculation and the **observability** of the process, not in the flexibility of the code.

## Core Concept: The Asset-Based Canonical Pipeline

The framework's logic is driven by a canonical pipeline that is orchestrated using a set of version-controlled, maintainer-authored text files called "prompt assets." All semantic interpretation is performed by an LLM guided by these assets.

The primary operations involve:
1.  **Mechanical Construction (Stage 1):** The framework mechanically constructs the initial input for a cell, for example by creating term pairs for a semantic dot product. For Matrix D, this involves creating a sentence from a hard-coded formula. This stage does not use an LLM.
2.  **Semantic Resolution (Stage 2):** For operations like semantic multiplication, an LLM, guided by an "operator" prompt asset, resolves the initial input into a single, concise concept.
3.  **Combined Ontological Lensing (Stage 3):** The output from the previous stage is interpreted by an LLM guided by a "lensing" prompt asset. This single, powerful call synthesizes the content through the simultaneous perspectives of the cell's row, column, and the station's overall purpose (provided by a "station brief" asset).

For a complete technical description, see the **[Canonical Algorithm Documentation](docs/ALGORITHM.md)**.

For a complete technical description, see the **[Canonical Algorithm Documentation](docs/ALGORITHM.md)**.

## The Ontological Modality Path

The sequence of stations in the semantic valley is not arbitrary; it follows a deep, underlying pattern of cognitive modalities. This path describes the *type* of work being done at each stage, revealing a structured cycle of systematic processing, epistemic (knowledge-based) evaluation, and alethic (truth-based) assessment.

| Modality | Station | Operation |
| :--- | :--- | :--- |
| `Problem` | 1. Problem Statement | `[A], [B]` |
| `Systematic` | 2. Requirements | `[C] = [A] * [B]` |
| `Process` | 3. Objectives | `[D] = [A] + [F]` |
| `Epistemic` | 4. Verification | `[K] = [D]^T, [X] = [K] * [J]` |
| `Epistemic` | 5. Validation | `[Z] = shift([X])` |
| `Process` | 6. Evaluation | `[G], [P], [T], [E]` |
| `Alethic` | 7. Assessment | `[M] = [R] x [E]` |
| `Epistemic` | 8. Implementation | `[W] = [M] x [X]` |
| `Alethic` | 9. Integration | `[U] = [W] x [P]` |
| `Alethic` | 10. Reflection | `[N] = [U] x [H]` |
| `Resolution` | 11. Resolution | `Final = synth([N])` |

**Clarifications:**
- **X/Z Modality:** Both Verification (S4) and Validation (S5) are `Epistemic`. S4 strictly precedes S5.
- **E Modality:** Evaluation (S6) is a `Process` modality, not Epistemic.

For a detailed explanation of this conceptual architecture, see the **[Project Philosophy Documentation](docs/PHILOSOPHY.md)**.

## Quick Start: The End-to-End Workflow

The recommended way to use the framework is to compute the entire pipeline and view the results in the generated HTML viewer.

### Prerequisites
- Python 3.9+
- An OpenAI API key set as the `OPENAI_API_KEY` environment variable
- **Note**: The framework uses OpenAI's Responses API exclusively (not Chat Completions API)

### Step 1: Compute the Full Pipeline
This command runs the entire semantic pipeline (Matrices C through E), generates snapshots of every matrix (including the base matrices A, B, and J), and creates detailed trace files for debugging.

```bash
# Install with OpenAI support (requires OpenAI SDK >=1.50.0)
pip install 'chirality-framework[openai]'

# Set your API key (add to your shell profile for persistence)
export OPENAI_API_KEY="sk-..."

# Run the full pipeline with the OpenAI resolver
python3 -m chirality.cli compute-pipeline --resolver openai --snapshot-jsonl --include-base
```
This will create two directories, `snapshots/<run_id>/` and `traces/<run_id>/`, containing the output files.

### Step 2: Render and View the Results
This command reads the generated snapshots and creates a self-contained HTML file to display all the matrices in an elegant, readable format.

```bash
# Render the latest run and open it in your browser
python3 -m chirality.cli render-viewer --latest --open
```
This will create a `viewer-output/` directory containing the `index.html` and `style.css` files and automatically open the page for you. You can change the output location with `--output-dir`.

## Advanced Usage

### App Integration Mode (Producer Contract)
For automation by external apps (e.g., chirality-app), use app mode to write a manifest and contract snapshots with a single JSON result to stdout.

```
python3 -m chirality.cli compute-pipeline \
  --resolver echo \
  --out runs/my-run-1 \
  --problem-file problem.json \
  --max-seconds 900
```

- Writes per-cell JSONL snapshots for `C`, `D`, `X`, `E` under `runs/<run_id>/snapshots/` with format `cells-jsonl-v1`.
- Writes `runs/<run_id>/index.json` last and atomically with checksums, sizes, and record counts.
- Prints exactly one JSON line to stdout on success: `{ "run_id": "...", "manifest": "runs/<run_id>/index.json" }`.
- Exit codes: `0` success; `2` invalid args; `3` timeout; `4` I/O; `5` resolver; `1` general.
- Backward compatibility: also dual-writes legacy snapshots for all computed matrices to `snapshots/<run_id>/` for the built-in viewer.

### App Mode (Chirality App Integration)

- Generate a run:

  `python3 -m chirality.cli compute-pipeline --resolver <echo|openai> --out runs/<run_id> --problem-file problem.json --max-seconds 900`

- Output:
  - `runs/<run_id>/index.json`
  - `runs/<run_id>/snapshots/{C,D,X,E}.jsonl`

- Stdout (last line):

  `{"run_id":"<run_id>","manifest":"runs/<run_id>/index.json"}`

- Contract:
  - Manifest `framework_schema_version = "1.0.0"`
  - Each matrix entry includes `path`, `format:"cells-jsonl-v1"`, `records`, `sha256`, `bytes`
  - JSONL rows include `id, matrix, row, col, row_label, col_label, station, text, citations, refs, meta.order`

### Using Framework Artifacts (chirality-app)

- Set `CHIRALITY_RUNS_DIR=/absolute/path/to/chirality-framework/runs` in chirality-app `.env.local`
- Ingest: `POST /api/agent/run` with body `{"framework_run_id":"<run_id>"}` (optionally include `"enable_rag": true`)
- Export: `GET /api/agent/export/<run_id>` with header `X-Role: approver`

### Computing Individual Matrices
The `compute-matrix` command allows you to compute and snapshot any single matrix, automatically handling its prerequisites.

```bash
# Compute just the final Evaluation matrix (E)
python3 -m chirality.cli compute-matrix E --resolver openai --snapshot-jsonl

# Snapshot a base matrix for reference
python3 -m chirality.cli compute-matrix A --snapshot-jsonl
```

### Inspecting a Single Cell
For detailed debugging, the `compute-cell` command lets you observe the new canonical pipeline for any single cell in a matrix.

```bash
# Observe the computation of cell C[0,0] with verbose output
python3 -m chirality.cli compute-cell C --i 0 --j 0 --resolver openai --verbose --trace
```

### Viewing Options
The `render-viewer` command has several options for customizing the output:

```bash
# Render a specific run with a custom title
python3 -m chirality.cli render-viewer --run-id "<run_id>" --title "My Analysis"

# Render with the "Elements" style for a more code-like view
python3 -m chirality.cli render-viewer --latest --style elements

# Disable the default value sanitization to see raw output
python3 -m chirality.cli render-viewer --latest --style elements --no-sanitize-values
```

## Common CLI Commands

- Compute full pipeline (dev): `python3 -m chirality.cli compute-pipeline --resolver echo --snapshot-jsonl --include-base -v`
- App-mode run (artifacts): `python3 -m chirality.cli compute-pipeline --resolver echo --out runs/my-run-1 --problem-file problem.json --max-seconds 900`
- Render latest viewer: `python3 -m chirality.cli render-viewer --latest --open`
- Inspect a cell: `python3 -m chirality.cli compute-cell C --i 0 --j 0 -v`

See full CLI Quick Reference in `docs/API_REFERENCE.md#cli-reference`.

## Development

To set up the development environment and run tests, please refer to the instructions in `CONTRIBUTING.md`.

Additional docs:
- `docs/INTERFACE.md`: Producer mirror of the chirality-app contract (app mode).
- `GEMINI.md`: Guidance for using Gemini/AI assistants with this repo.
 - `CLAUDE.md`: Guidance for using Claude Code with this repo.
 - `AGENTS.md`: Notes for agentic coding assistants working on this project.
