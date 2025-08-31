# Changelog

All notable changes to the Chirality Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [16.0.0] - 2025-08-31

### Added
- Universal, metadata-rich 5-stage provenance schema for all matrices (C, F, D):
  - stage_1_construct, stage_2_semantic, stage_3_column_lensed, stage_4_row_lensed, stage_5_final_synthesis.
- RichResult response type across resolvers with text, terms_used, warnings, and resolver metadata (modelId, latencyMs, promptHash, createdAt, phase).
- Universal Neo4j exporter with a single UNWIND-based Cypher that persists all five stages, rich metadata, and full context.
- Run/session scoping in exporter: (:Run {id}) nodes with (:Run)-[:CONTAINS]->(:Cell|:Stage) relationships; CLI generates a run_id per invocation for Neo4j exports.

### Changed
- Standardized API naming for D: `compute_cell_D`, `compute_matrix_D` (previously `synthesize_*`).
- Centralized prompt construction in `chirality/core/prompts.py` using explicit builders; resolver no longer exposes `assemble_prompt`.
- CLI verbose flows now display universal lensing steps: Column → Row → Final.

### Removed
- Backward compatibility shims and legacy fields/methods:
  - Removed `apply_ontological_lens` and any `assemble_prompt` usage.
  - Removed legacy provenance keys: `stage_1_products`, `stage_2_resolved`, `stage_3_lensed`, `stage_1_synthesis`.
  - Exporter no longer accepts legacy formats; provenance must be dict-shaped per stage with text/texts, terms_used, warnings, metadata.

### BREAKING CHANGES
- Provenance schema and resolver API changed:
  - Per-stage provenance is now dict-shaped and mandatory.
  - D functions renamed to `compute_*`; the CLI no longer accepts a custom `--problem` for D (canonical problem only).
- Export graph schema changed:
  - Universal five-stage pipeline with new labels and properties.
  - Run scoping added; existing queries should include `(:Run)` where appropriate.

## [15.0.2] - 2025-08-29

### Changed
- Refactored versioning to use `VERSION.md` as a single source of truth, removing hardcoded versions from the CLI and documentation.
- Updated core concept description from "deterministic" to "procedurally-rigorous methodology on a stochastic process" to more accurately reflect the architecture.

### Fixed
- Removed all outdated "CF14" version identifiers from current documentation and code for consistency.
- Renamed `CF14ValidationError` to `FrameworkValidationError` to align with the current project branding.

## [15.0.1] - 2025-08-29

### Fixed
- Corrected `.env` loading to ensure proper environment variable handling.
- Fixed a bug in the JSONL tracer to ensure accurate trace output.
- Resolved a missing import for Neo4j integration.

### Changed
- Enabled dual output for JSONL traces and Neo4j working memory for enhanced observability.

### Added
- Completed API reference documentation.
- Added a comprehensive prompt engineering guide.
- Included Neo4j query examples for advanced analysis.
- Added a tutorial for new users.

## [15.0.0] - 2025-08-29

### Added
- **Core Algorithm**: Introduced a three-stage interpretation pipeline (Combinatorial, Semantic Resolution, Ontological Lensing).
- **CLI**: Added a new `compute-cell` command with flags for verbosity, tracing, and Neo4j export.

### Changed
- **Major Architectural Refactoring**: This is a complete rewrite with a new CLI, simplified types, and different import paths. The project is transformed from a flexible framework into a fixed "semantic calculator" algorithm.

### BREAKING CHANGES
- This release is a complete architectural rewrite and is not backward-compatible.
- The CLI has been completely changed, with `compute-cell` as the new primary command.
- All import paths have been updated due to the new structure.
