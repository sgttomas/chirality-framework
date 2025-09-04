# Chirality Framework Interface (Producer Mirror)

This document mirrors the canonical interface contract defined in the chirality-app project. The chirality-app INTERFACE.md is the source of truth for the consumer. This file summarizes the constraints the chirality-framework (producer) implements to satisfy that contract.

- Canonical reference: maintained in chirality-app (INTERFACE.md)
- Producer version: framework_schema_version = "1.0.0"

## App Mode CLI (Producer)

Command (app mode):

```
chirality compute-pipeline \
  --resolver <echo|openai> \
  --out runs/<run_id> \
  --problem-file <path/to/problem.json> \
  --max-seconds 900
```

- `--out`: output run directory (must be `runs/<run_id>`, `<run_id>` matches `^[a-z0-9-_]{1,64}$`). If omitted, a valid run_id may be auto-generated and returned in stdout JSON.
- `--problem-file`: JSON with `{ "title": string, "statement": string }` (metadata-only in v1.0.0).
- `--max-seconds`: best‑effort timeout (checked at operation boundaries).
- `--resolver`: `echo` (deterministic) or `openai`.

Stdout on success (single line, final):

```
{"run_id":"<run_id>","manifest":"runs/<run_id>/index.json"}
```

## Producer Guarantees

- Manifest atomicity: `index.json` is written last and only if the run completes successfully.
- Paths in manifest: relative to `runs/<run_id>/`.
- Stdout hygiene: only the final JSON line on success. Informational logs go to stderr or require `--verbose`.
- Exit codes:
  - 0: success
  - 2: invalid arguments
  - 3: timeout
  - 4: I/O error
  - 5: resolver error
  - 1: general/unexpected

## Manifest (index.json)

Top-level fields:
- `run_id`, `created_at`, `tool` `{name, version}`, `framework_schema_version` ("1.0.0"),
- `problem` `{title, statement}`, `durations` `{ total_ms }`,
- `matrices`: object mapping matrix code to file metadata.

Per-matrix metadata (required matrices: C, D, X, E):
- `path`: `snapshots/<M>.jsonl`
- `format`: `cells-jsonl-v1`
- `records`: integer line count
- `sha256`: hex digest of file bytes
- `bytes`: file size in bytes

Producer may include additional non-breaking fields; consumer must ignore unknown fields.

## Snapshot Format: cells-jsonl-v1

One JSON object per cell per line. Fields:
- `id`: `"{matrix}:r{row}:c{col}"`
- `matrix`: one of `C`, `D`, `X`, `E`
- `row`: integer index; `col`: integer index
- `row_label`, `col_label`: verbatim labels from matrix axes
- `station`: exact `Matrix.station` string (e.g., "Problem Requirements", "Solution Objectives", "Verification", "Evaluation")
- `text`: final cell text
- `citations`: array (may be empty)
- `refs`: array (may be empty)
- `meta`: object (must include `order`: integer); additional fields allowed

## Backward Compatibility

- Legacy snapshot format and the static viewer remain supported outside of app mode.
- App mode writes into `runs/<run_id>/snapshots/` using `cells-jsonl-v1` and a manifest at `runs/<run_id>/index.json`.

