# API Reference - Chirality Framework

**Comprehensive reference for the Chirality Framework Semantic Calculator API**

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Core Types](#core-types)
3. [Canonical Matrices](#canonical-matrices)
4. [Core Operations](#core-operations)
5. [Resolvers](#resolvers)
6. [Observability (Tracing, Snapshots, Exporting)](#observability)
7. [Viewer Generator](#viewer-generator)
8. [Validation](#validation)
9. [CLI Reference](#cli-reference)

---

## Core Operations

This section details the functions for computing each matrix in the semantic valley.

### Cell-Level Operations
These functions implement the core pipeline for a single cell.

- `compute_cell_C(i, j, A, B, resolver, ...)`: Computes a cell of Matrix C using the full 5-stage pipeline.
- `compute_cell_F(i, j, J, C, resolver, ...)`: Computes a cell of Matrix F.
- `compute_cell_D(i, j, A, F, resolver, ...)`: Computes a cell of Matrix D.
- `compute_cell_X(i, j, K, J, resolver, ...)`: Computes a cell of Matrix X using the full 5-stage pipeline.
- `compute_cell_Z(i, j, X, resolver, ...)`: Computes a cell of Matrix Z using the 2-stage station shift pipeline.
- `compute_cell_E(i, j, G, T, resolver, ...)`: Computes a cell of Matrix E using the full 5-stage pipeline.

### Matrix-Level Operations
These are convenience wrappers that compute entire matrices by iterating over the cell-level functions.

- `compute_matrix_C(A, B, resolver, ...)`
- `compute_matrix_F(J, C, resolver, ...)`
- `compute_matrix_D(A, F, resolver, ...)`
- `compute_matrix_K(D)`
- `compute_matrix_X(K, J, resolver, ...)`
- `compute_matrix_Z(X, resolver, ...)`
- `compute_matrix_T_from_B(B)`
- `compute_matrix_G(Z)`
- `compute_array_P(Z)`
- `compute_matrix_E(G, T, resolver, ...)`

---

## Observability (Tracing, Snapshots, Exporting)

### JSONLTracer
Records the detailed, stage-by-stage execution of every cell computation.

```python
from chirality.core.tracer import JSONLTracer

tracer = JSONLTracer(thread_id="my-run-123")
# ... use tracer in compute calls ...
tracer.close()
```

### MatrixSnapshotWriter
Writes snapshots in two formats:

- Legacy matrix JSONL (single JSON object with embedded cells), suitable for the built-in HTML viewer.
- Per-cell `cells-jsonl-v1` (one JSON object per line), suitable for app integrations.

```python
from chirality.exporters.snapshot_exporter import MatrixSnapshotWriter

writer = MatrixSnapshotWriter(run_id="my-run-123")

# Legacy format (single JSON object, used by viewer)
writer.write_matrix(computed_matrix, "openai")

# App format (one JSON per line, cells-jsonl-v1)
writer.write_matrix_cells_jsonl(computed_matrix, Path("runs/my-run-123/snapshots"), f"{computed_matrix.name}.jsonl")
```

### Neo4jWorkingMemoryExporter
Exports the full, 5-stage provenance of every cell to a Neo4j graph database.

```python
from chirality.exporters.working_memory_exporter import Neo4jWorkingMemoryExporter

with Neo4jWorkingMemoryExporter(run_id="my-run-123") as exporter:
    # ... use exporter in compute calls ...
```

---

## Viewer Generator

Functions for rendering the static HTML viewer from snapshot files.

```python
from chirality.viewer.render import render_page, write_assets, load_snapshots_for_run

run_dir = "snapshots/my-run-123"
snapshots = load_snapshots_for_run(run_dir)
html = render_page(snapshots, "my-run-123", "My Title")
write_assets(html, "viewer/")
```

---
... (rest of the original content) ...

## Manifest Exporter

Generates `runs/<run_id>/index.json` with checksums, bytes, and record counts for snapshots.

```python
from pathlib import Path
from chirality.exporters.manifest_exporter import ManifestExporter

run_dir = Path("runs/my-run-123")
exporter = ManifestExporter(run_dir, "chirality-framework", "1.2.3", framework_schema_version="1.0.0")
matrices = {
    "C": (run_dir / "snapshots/C.jsonl", "cells-jsonl-v1"),
    "D": (run_dir / "snapshots/D.jsonl", "cells-jsonl-v1"),
    "X": (run_dir / "snapshots/X.jsonl", "cells-jsonl-v1"),
    "E": (run_dir / "snapshots/E.jsonl", "cells-jsonl-v1"),
}
manifest_path = exporter.write_manifest("my-run-123", {"title": "T", "statement": "S"}, {"total_ms": 12345}, matrices)
```

The manifest is written atomically and only after all referenced files exist.

## CLI: App Mode

The `compute-pipeline` command supports an app integration mode:

- `--out runs/<run_id>`: output directory (run_id validated).
- `--problem-file`: problem metadata JSON.
- `--max-seconds`: best‑effort timeout.
- Success prints exactly one JSON line: `{ "run_id": "...", "manifest": "runs/<run_id>/index.json" }`.
- Exit codes: `0` ok, `2` invalid args, `3` timeout, `4` I/O, `5` resolver, `1` general.

In app mode, per-cell snapshots for `C`, `D`, `X`, `E` are written to `runs/<run_id>/snapshots/` and a manifest is created. For backward compatibility, full legacy snapshots for all computed matrices are also written to `snapshots/<run_id>/`.

## CLI Reference

Quick reference for all CLI commands and common options. See also the dedicated app-mode section below.

- `chirality compute-cell <C|F|D|K|X|Z|G|P|T|E> --i <row> --j <col> [options]`
  - Options: `--resolver <echo|openai>`, `--api-key <key>` (or `OPENAI_API_KEY`), `--trace/--no-trace`, `--neo4j-export/--no-neo4j-export`, `--trace-only`, `--verbose/-v`.
  - Purpose: Compute a single cell and show staged provenance.

- `chirality compute-matrix <A|B|J|C|F|D|K|X|Z|G|P|T|E> [options]`
  - Options: `--resolver <echo|openai>`, `--api-key <key>`, `--trace/--no-trace`, `--neo4j-export/--no-neo4j-export`, `--trace-only`, `--snapshot-jsonl`, `--verbose/-v`.
  - Purpose: Compute a full matrix (handles prerequisites) and optionally write legacy snapshots.

- `chirality compute-pipeline [options]`
  - Developer mode: `--resolver <echo|openai>`, `--api-key <key>`, `--trace-only`, `--snapshot-jsonl`, `--include-base`, `--only "C,F,D"`, `--verbose/-v`.
  - App mode (producer contract): `--out runs/<run_id>`, `--problem-file problem.json`, `--max-seconds <int>`. Writes `runs/<run_id>/index.json` and per‑cell JSONL snapshots for `C,D,X,E`; stdout last line is `{"run_id":"<run_id>","manifest":"runs/<run_id>/index.json"}`. See “CLI: App Mode”.

- `chirality render-viewer [--run-id <id> | --latest] [options]`
  - Options: `--source-dir <dir>` (default `snapshots`), `--output-dir <dir>` (default `viewer-output`), `--title <text>`, `--include "A,C,F"`, `--style <tables|elements>`, `--no-sanitize-values`, `--open`.
  - Purpose: Generate static HTML to view legacy snapshots.

- `chirality info`
  - Purpose: Print version and canonical matrix/station info.

Exit codes (where applicable): `0` success; `2` invalid args; `3` timeout; `4` I/O; `5` resolver; `1` general.
