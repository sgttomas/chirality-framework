# Chirality Framework: A Semantic Calculator

[![PyPI](https://img.shields.io/pypi/v/chirality-framework.svg)](https://pypi.org/project/chirality-framework/)
[![Python versions](https://img.shields.io/pypi/pyversions/chirality-framework.svg)](https://pypi.org/project/chirality-framework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Publish](https://github.com/sgttomas/chirality-framework/actions/workflows/python-publish.yml/badge.svg)](https://github.com/sgttomas/chirality-framework/actions/workflows/python-publish.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/tag/sgttomas/chirality-framework?sort=semver&label=release)](https://github.com/sgttomas/chirality-framework/tags)

**Version: 19.1.0** | **Status: Phase 2 Ready**

The Chirality Framework is a meta-ontological, system-agnostic methodology for mapping the solution space to a problem statement in the context of knowledge work. It creates structured semantic relationships that serve as "semantic anchors" to guide LLMs through problem-solving stages across a "semantic valley."

The framework employs two distinct phases with fundamentally different prompting strategies:
- **Phase 1** (Matrices A-E): Uses conversational prompting to build semantic understanding
- **Phase 2** (Tensors M-N): Uses Phase 1 implementation as system prompt for modular cell-by-cell construction

## Core Architecture: Two-Phase Semantic Computation

### Phase 1: Conversational Semantic Pipeline (Matrices A-E)
Phase 1 uses a conversational dialogue history as the system prompt to create semantic understanding. The dialogue builds the concept of semantic multiplication through examples, develops key concepts organically, and establishes modal ontologies through iterative refinement. This creates a "semantic state" in the LLM that enables proper interpretation.

**Three-Stage Pipeline with Rolling Context:**
1. **Mechanical Construction (Stage 1):** Framework mechanically constructs initial input (e.g., term pairs for semantic dot product)
2. **Semantic Resolution (Stage 2):** LLM resolves concepts via operation-specific strategies
3. **Combined Lensing (Stage 3):** Unified semantic operation combining row × column × station perspectives

### Phase 2: Modular Tensor Construction (Tensors M-N)
Phase 2 uses the complete Phase 1 implementation (through Matrix E) as the system prompt, then constructs tensors cell-by-cell WITHOUT rolling context. The modular design of the tensors facilitates this approach, with each cell computed independently using semantic cross products to create hierarchical structures.

For a complete technical description, see the **[Canonical Algorithm Documentation](docs/ALGORITHM.md)**.

## The Ontological Modality Path

The sequence of stations in the semantic valley is not arbitrary; it follows a deep, underlying pattern of cognitive modalities. This path describes the *type* of work being done at each stage, revealing a structured cycle of systematic processing, epistemic (knowledge-based) evaluation, and alethic (truth-based) assessment.

| Modality | Station | Operation |
| :--- | :--- | :--- |
| `Problem` | 1. Problem Statement | `[A], [B]` |
| `Systematic` | 2. Requirements | `[C] = [A] · [B]` |
| `Process` | 3. Objectives | `[D] = [A] + [F]` |
| `Epistemic` | 4. Verification | `[K] = [D]^T, [X] = [K] · [J]` |
| `Epistemic` | 5. Validation | `[Z] = shift([X])` |
| `Process` | 6. Evaluation | `[G], [P], [T], [E] = [G] · [T]` |
| `Alethic` | 7. Assessment | `[M] = [R] × [E]` |
| `Epistemic` | 8. Implementation | `[W] = [M] × [X]` |
| `Alethic` | 9. Reflection | `[U] = [W] × [P]` |
| `Alethic` | 10. Resolution | `[N] = [U] × [H]` |

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
