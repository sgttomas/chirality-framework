# API Reference - Chirality Framework

**Comprehensive reference for the Chirality Framework Semantic Calculator API**

## Table of Contents

1.  [Installation & Setup](#installation--setup)
2.  [Core Operations](#core-operations)
3.  [LLM Client and Configuration](#llm-client-and-configuration)
4.  [Observability (Tracing, Snapshots, Exporting)](#observability)
5.  [CLI Reference](#cli-reference)

---

## Core Operations

This section details the primary functions for computing matrices and the new, canonical cell-level API.

### Matrix-Level Operations (`chirality.core.operations`)

These high-level functions orchestrate the computation of an entire matrix, calling the `CellResolver` for each cell according to the canonical pipeline.

-   `compute_matrix_C(A, B, resolver, ...)`
-   `compute_matrix_F(J, C, resolver, ...)`
-   `compute_matrix_D(A, F, resolver, ...)`
-   And so on for all computed matrices (X, Z, E).

### Cell-Level API (`chirality.core.cell_resolver.CellResolver`)

This is the new, refactored API for executing the stages of the canonical pipeline. The `CellResolver` uses a `PromptBuilder` internally to assemble prompts from the maintainer-authored assets.

-   `run_stage2_multiply(terms: list[str], component_id: str) -> RichResult`: Performs semantic multiplication on a list of terms (C/X/E).
-   `run_stage2_elementwise(terms: list[str], component_id: str) -> RichResult`: Performs element-wise semantic multiplication (F).
-   `run_stage2_addition(parts: list[str]) -> str`: Performs mechanical string concatenation (no LLM call).
-   `run_combined_lens(content: str, component_id: str, row_label: str, col_label: str) -> RichResult`: Performs the unified row, column, and station interpretation in a single LLM call. For Matrix Z, this method is still called, but the underlying strategy maps it to a special-purpose lensing prompt that performs the context shift.

### Prompt Strategy API (`chirality.lib.strategies.PromptStrategy`)

-   `plan(stage: str, component_id: str) -> list[str]`: Returns the list of prompt asset IDs for a given stage and component.
-   `get_station_brief_id(component_id: str) -> str`: Gets the asset ID for a component's station brief.
-   `get_station_meta(component_id: str) -> dict`: Returns metadata about the station, including its `name`, `ordinal`, and the `total` number of stations.

---

## LLM Client and Configuration

-   **`chirality.core.llm_client.py`**: Provides a single `call_responses(...)` function, which is the exclusive wrapper for the OpenAI Responses API. All LLM calls in the framework route through this client. Chat Completions is not used anywhere in this codebase.
    -   **Requirements**: OpenAI SDK >=1.50.0 
    -   **API Compatibility**: Uses `input` parameter instead of `prompt`, implements robust response parsing for `output_text` with fallback to `output[].content[].text`
    -   **JSON Format**: Relies on system prompt JSON contract rather than API `response_format` parameter (temporarily removed due to SDK compatibility)
-   **`chirality.core.llm_config.py`**: Defines the global, hardcoded configuration for the LLM, including model name, temperature, and other decoding parameters. There are no per-station or user-configurable overrides.

---

## Observability (Tracing, Snapshots, Exporting)

This functionality remains largely the same, but the provenance data recorded has been updated.

-   **Provenance Structure**: The provenance for each cell now follows a simpler, 3-stage structure:
    -   `stage_1_construct`: The initial mechanical inputs.
    -   `stage_2_semantic`: The result from the first LLM call (e.g., `run_stage2_multiply`).
    -   `stage_3_combined_lensed`: The final narrative from the `run_combined_lens` call.
-   **Asset Provenance**: For each LLM call, the provenance now includes a list of the prompt assets used (ID, version, and sha256 hash), ensuring full auditability.

---

## CLI Reference

The CLI commands and their flags remain the same, but their behavior and output have been updated to reflect the new canonical pipeline.

-   `chirality compute-cell <C|F|D|X|Z|E> --i <row> --j <col> --verbose`
    -   **Updated Purpose**: The verbose output now displays the new 2-stage LLM pipeline, showing the result of the "Semantic Resolution" stage and the final "Combined Lensing" stage.

-   `chirality compute-matrix <A|B|J|C|F|D|K|X|Z|G|P|T|E> [options]`
    -   Computes a full matrix using the new canonical pipeline.

-   `chirality compute-pipeline [options]`
    -   Runs the entire sequence of matrix computations using the new canonical pipeline.

(Other commands like `render-viewer` and `info` remain unchanged in their function.)
