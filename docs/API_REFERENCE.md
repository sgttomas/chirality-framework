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
Writes a clean, final-state summary of a computed matrix to a JSONL file.

```python
from chirality.exporters.snapshot_exporter import MatrixSnapshotWriter

writer = MatrixSnapshotWriter(run_id="my-run-123")
writer.write_matrix(computed_matrix, "openai")
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