# Project Roadmap

**Status Last Updated**: September 6, 2025

## Current Status: Full Semantic Resolution Operational

The project has completed a major architectural refactoring to externalize all semantic content and streamline the core pipeline. The old three-stage lensing process has been replaced with a more powerful and coherent **Combined Lensing** pipeline.

**Major Milestone Achieved (v17.1.1)**: The framework now successfully performs complete semantic resolution with the OpenAI Responses API and reliable CI/CD infrastructure. All critical integration issues have been resolved:
- ✅ OpenAI Responses API compatibility fixed (input parameter, response parsing)
- ✅ Semantic tracing system restored (critical for coherence diagnostics)
- ✅ Complete pipeline validation (C through E matrices) with authentic semantic transformation
- ✅ All 81 tests passing with production-ready package build

This transformation into a fully asset-based, canonical algorithm is now complete. The core logic is stable, and the semantic content is now fully owned and version-controlled by the maintainer in the `chirality/prompt_assets/` directory.



## Next Development Priorities

With the new asset-based architecture in place, future work can focus on improving semantic quality and extending the pipeline.

### High Priority
*   **Semantic Asset Tuning**: Iteratively refine the content of the `.md` files in `chirality/prompt_assets/` (especially the Station Briefs and the `combined.md` lensing template) to improve the coherence and insight of the final output.
*   **Online Testing Suite**: Add `@pytest.mark.online` tests that validate against the live OpenAI Responses API to catch any regressions in semantic quality.
*   **Extended Semantic Valley**: Implement the next matrices in the canonical sequence (M, W, U, N), which will involve implementing the "Semantic Cross Product" operation.

### Medium Priority  
*   **Performance Optimization**: Profile the new `PromptBuilder` and `llm_client` to identify any performance bottlenecks.
*   **Tracing Analytics**: Build tools to analyze and visualize `JSONLTracer` output to better understand the new pipeline's behavior.

### Low Priority
*   **Additional Export Formats**: CSV, Excel, or other matrix export options.
*   **Advanced CLI Features**: Batch processing or other usability enhancements.

The core algorithm is stable and production-ready. All future work builds on this solid foundation.

## Production Hardening Plan

This plan captures the remaining work to move from a robust prototype to a production-grade, continuously validated system. Each item includes scope and concrete outcomes.

### 1) Test Coverage Expansion
- **Neo4j Export Integration Tests**: Exercise `Neo4jWorkingMemoryExporter` end-to-end against a test Neo4j instance.
  - Validate graph schema (Matrix/Cell/Stage nodes; CONTAINS/HAS_STAGE rels).
  - Assert idempotency and uniqueness constraints; verify stage ordering via timestamps.
  - Add a `--dry-run` mode stub to simulate writes for CI.
- **Tracer Rotation & Dedupe Tests**: Generate large traces to trigger rotation; assert file rollover and no duplicates with dedupe on.
  - Include concurrency smoke test (ThreadPoolExecutor) to ensure locking behavior.
- **CLI Snapshot Tests (Verbose)**: Snapshot “stage-by-stage” output for `compute-cell` (C, and minimal F/D) to detect regressions in UX.
- **Optional Online Tests**: Gate with `@pytest.mark.online` and `OPENAI_API_KEY`.
  - Small, stable set of cells; assert JSON contract and non-empty `text`.

### 2) Error Handling & Reporting
- **Resolver Error Propagation**: Distinguish hard failures (raise) vs soft warnings (attach to provenance).
  - Return structured errors up the call stack; surface in CLI with clear messages.
- **CLI Failure Modes**: Add `--fail-on-error` to exit non‑zero on Stage 2/3 failures or invalid outputs.
  - Print remediation tips (env vars, network, rate limits) in verbose mode.
- **Provenance Warnings**: Ensure any model/output validation issues are recorded in `warnings` and optionally highlighted in CLI.

### 3) Configuration & Resilience
- ✅ **Centralized Config**: All LLM configuration (model, temperature, etc.) is now centralized and hardcoded in `chirality/core/llm_config.py`. This aligns with the principle of a single, canonical implementation.
- **Backoff & Limits**: The retry logic in `llm_client.py` should be reviewed for production readiness.

### 4) CI/CD & Packaging
- **CI Pipeline**: GitHub Actions workflow to run lint, type-check, and tests on PRs and main.
  - Lint: `ruff` or `flake8`; Type-check: `mypy` (target core modules); Tests: `pytest -q` (skip `@online`).
  - Cache dependencies; artifact snapshots for CLI verbose outputs and trace samples.
- **Dependency Hygiene**: Pin minimal versions; provide `requirements-dev.txt` and extras; document installation matrix.
- **Release Automation**: Tag-driven version checks; build/publish to an internal index or PyPI when ready.

### 5) Usability & DX Improvements
- **CLI Enhancements**:
  - `info` prints A/B/J axes explicitly (row/col labels and station names).
  - `--dry-run` for Neo4j exporter (log-only, no DB writes).
  - `--summary` to print staged highlights (without full provenance block).
- **Examples & Guides**:
  - Add short, copy‑paste examples for common flows (compute single cell with tracing/export; full C→F→D run).
  - Troubleshooting appendix: common resolver/exporter errors and quick fixes.

### Acceptance (Production-Ready)
- Green CI on PRs and main; unit + integration tests stable and fast.
- CLI communicates failures clearly; `--fail-on-error` behaves as expected.
- Configurable resolver and tracer/export behavior documented and discoverable.
- Neo4j export validated with schema checks; `--dry-run` safe for CI.
- Docs updated to reflect UX and configuration; examples runnable as-is.
