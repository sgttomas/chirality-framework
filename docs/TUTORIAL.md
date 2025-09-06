# Chirality Framework Tutorial

This tutorial will guide you through the primary end-to-end workflow of the Chirality Framework, from installation to generating and viewing a full set of matrices.

For a compact list of commands and options, see the CLI Quick Reference in `docs/API_REFERENCE.md#cli-reference`.

## 1. Installation

First, install the framework from PyPI. It's recommended to do this in a virtual environment. To use the OpenAI resolver, you must install the `[openai]` extra.

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the framework with OpenAI support
pip install 'chirality-framework[openai]'
```

## 2. Set Your OpenAI API Key

The framework requires a valid OpenAI API key to perform semantic computations. Set it as an environment variable in your shell.

```bash
# Add this line to your .bashrc, .zshrc, or other shell profile for persistence
export OPENAI_API_KEY="sk-..."
```

## 3. Compute the Full Semantic Pipeline

The easiest way to get started is to compute all matrices in the semantic valley at once using the `compute-pipeline` command. This command will:
- Compute all matrices from C through E using the canonical pipeline, which features a single-call "Combined Lensing" step for all semantic interpretations.
- Create JSONL "snapshot" files for each matrix, which are clean summaries of the final state.
- Create detailed "trace" files for debugging every computation step.

Run the following command in your terminal:

```bash
python3 -m chirality.cli compute-pipeline --resolver openai --snapshot-jsonl --trace-only --include-base
```
- `--resolver openai`: Specifies that we want to use the live OpenAI API for semantic resolution.
- `--snapshot-jsonl`: Enables the creation of the summary snapshot files.
- `--trace-only`: Enables detailed tracing and disables any potential Neo4j database export.
- `--include-base`: Also creates snapshots for the foundational matrices (A, B, J).

After the command completes, you will have two new directories:
- `snapshots/<run_id>/`: Contains the clean summary files (e.g., `C-....jsonl`, `D-....jsonl`).
- `traces/<run_id>/`: Contains the highly detailed debug trace files.

### App Integration Mode (Optional)
If you need to automate runs from another application, use app mode to produce a manifest and per-cell snapshots:

```
python3 -m chirality.cli compute-pipeline \
  --resolver echo \
  --out runs/tutorial-run-1 \
  --problem-file problem.json \
  --max-seconds 900
```

This writes per-cell JSONL snapshots for `C`, `D`, `X`, `E` under `runs/<run_id>/snapshots/` and a manifest `runs/<run_id>/index.json` (written last, atomically). The CLI prints exactly one JSON line to stdout on success with the `run_id` and manifest path. For backward compatibility, legacy full-matrix snapshots for all computed matrices are also written under `snapshots/<run_id>/` and can be rendered with the viewer.

## 4. Render and View the Results

Now that you have the snapshot files, you can generate a self-contained HTML viewer to see the matrices in an elegant, readable format.

Run the following command:

```bash
python3 -m chirality.cli render-viewer --latest --open
```
- `--latest`: Automatically finds the most recent run directory in `snapshots/`.
- `--open`: Automatically opens the generated HTML file in your default web browser.

This will create a new `viewer-output/` directory containing `index.html` and `style.css`. Your browser should open to a page displaying all the computed matrices, from A to E, in their canonical order.

## 5. (Optional) Inspecting Snapshots with `jq`

The snapshot files are simple, single-line JSON objects, which makes them easy to inspect from the command line with a tool like `jq`.

```bash
# Find your latest run ID
RUN_ID=$(ls -t snapshots | head -n 1)

# Pretty-print the snapshot for Matrix C
jq . snapshots/$RUN_ID/C-*.jsonl

# Extract just the cell values from Matrix E
jq -r '.cells[].value' snapshots/$RUN_ID/E-*.jsonl

# Get the shape of Matrix X
jq '.shape' snapshots/$RUN_ID/X-*.jsonl
```

That's it! You have successfully run the entire Chirality Framework pipeline and visualized the results.
