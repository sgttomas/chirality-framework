# GEMINI.md

Guidance for using Google Gemini (or similar AI coding assistants) with this repository.

**NOTE:** This project is undergoing a code migration to a Domain-Driven Design (DDD) architecture. As a result, some file paths in the documentation may be outdated. Additionally, a major refactoring is planned for the implementation of Phase 2.

## Project Overview

Chirality Framework is a "semantic calculator" that implements a fixed, canonical algorithm. Its core logic is driven by an **asset-based prompt system**, where all semantic instructions are defined in version-controlled markdown files, not in the Python code. The framework executes a multi-stage pipeline featuring a unified **Combined Lensing** step for all semantic interpretation. The framework is implemented in two phases:

-   **Phase 1**: Computes matrices A-Z, establishing the foundational semantic relationships. This phase uses a unique conversational system prompt to prime the LLM's understanding of the semantic operations.
-   **Phase 2**: Computes tensors M, W, U, and N, which build upon the foundational matrices to create higher-order semantic structures. This phase uses the normative implementation of Phase 1 as its system prompt.

-   Quick start: see `README.md`
-   Normative Specification: `chirality/normative_spec.txt`
-   Phase 1 System Prompt: `chirality/normative_system_prompt_Phase1.txt`
-   Phase 1 Normative Implementation: `chirality/normative_implementation_chirality-framework_Phase1.txt`
-   Algorithm details: `docs/ALGORITHM.md` (Note: This file is referenced in the documentation but does not exist in the `docs` directory.)
-   Prompting system: `docs/PROMPT_ENGINEERING.md` (Note: This file is referenced in the documentation but does not exist in the `docs` directory.)
-   CLI Reference: `docs/API_REFERENCE.md#cli-reference` (Note: This file is referenced in the documentation but does not exist in the `docs` directory.)

## Key Architectural Concepts for AI Agents

To contribute effectively, it is critical to understand the new asset-based architecture.

### 1. The Prompt Asset System (`chirality/prompt_assets/`)

-   **Source of Truth**: All semantic content (the "why" and "how" of the interpretation) lives in `.md` files within this directory. The Python code is just an engine that orchestrates these assets.
-   **Asset Types**:
    -   `system.md`: The global prompt prepended to all LLM calls.
    -   `station_briefs/`: One file per station (e.g., `requirements.md`) that defines the station's purpose.
    -   `ops/operators/`: Instructions for Stage 2 semantic resolutions (e.g., `multiply.md`).
    -   `ops/lensing/`: Templates for Stage 3 combined lensing (e.g., `combined.md`, `shift.md`).
-   **Registry & Integrity**: `metadata.yml` acts as a manifest, mapping asset IDs to files and their SHA256 checksums. The system will fail if a file is modified without its checksum being updated in the manifest.

### 2. The Core Pipeline Logic

-   **Stage 1 (Mechanical)**: The framework code mechanically assembles the initial input. For Matrix D, the formula `A(i,j) + " applied to frame the problem; " + F(i,j) + " to resolve the problem."` is **hard-coded** in `chirality/application/services/pipeline_service.py`.
-   **Stage 2 (Semantic Resolution)**: The LLM, guided by an `operator` asset, resolves the initial input into a concise concept.
-   **Stage 3 (Combined Lensing)**: The LLM, guided by a `lensing` asset and a `station_brief`, interprets the Stage 2 output through ontological lenses.
-   **Z-Matrix Path**: Matrix Z follows a special path. It bypasses Stage 2 and uses a dedicated lensing asset (`ops/lensing/shift.md`) in Stage 3 to perform its context shift.
-   **Shim Files**: You may encounter `_shim.py` files in the `chirality/core/` directory. These are temporary files created during the DDD migration and should not be modified.

### 3. Two-Phase Prompting Strategy

-   **Phase 1**: Uses a conversational history as a system prompt to get the LLM into the right "frame of mind" to understand and perform the semantic operations. The prompt is stored in `chirality/normative_system_prompt_Phase1.txt`.
-   **Phase 2**: Uses the normative implementation of Phase 1 (up to Matrix E) as the system prompt. In this phase, the tensors are constructed cell-by-cell without a rolling context window. The normative implementation is stored in `chirality/normative_implementation_chirality-framework_Phase1.txt`.

### 4. Phase 2: Tensor Operations

Phase 2 introduces a new semantic operation, the **semantic cross product (×)**, which creates higher-dimensional tensors by generating nested hierarchies of meaning. This is used to compute the following tensors:

-   **Tensor M**: [R] × [E]
-   **Tensor W**: [M] × [X]
-   **Tensor U**: [W] × [P]
-   **Tensor N**: [U] × [H]

### 5. The Prompt Assembly Logic (`chirality/infrastructure/prompts/builder.py`)

-   `strategies.py`: This module is the "brain" that maps a given component (e.g., "C") and stage (e.g., "combined_lens") to a list of prompt asset IDs. It also contains the logic for the special Z-path and for retrieving station metadata.
-   `prompt_builder.py`: This module assembles the final prompt message sent to the LLM. It fetches asset content from the registry, substitutes placeholders, and prepends the `system.md` prompt.
-   **Placeholders**: The system supports a fixed set of placeholders: `{{terms}}`, `{{content}}`, `{{row_label}}`, `{{col_label}}`, `{{station_brief}}`, and `{{station_id}}`. No other placeholders will work without code changes.

## Day-to-Day Commands

Testing and quality:

```bash
pytest -v               # uses mocks (no live LLM calls)
mypy chirality/         # strict typing
black chirality/ tests/ # formatting
```

CLI (common):

```bash
# Full pipeline (dev mode)
python3 -m chirality.cli compute-pipeline --resolver echo --snapshot-jsonl --include-base -v

# App mode (artifacts for chirality-app)
python3 -m chirality.cli compute-pipeline \
  --resolver echo \
  --out runs/my-run-1 \
  --problem-file problem.json \
  --max-seconds 900
```

## Contribution Guardrails

-   **CRITICAL API USAGE**: The OpenAI resolver **MUST** use the `client.responses.create()` method. The `client.chat.completions.create()` API is forbidden.
-   **Immutable Files**: Never modify `chirality/normative_spec.txt` or `chirality/normative_implementation_chirality-framework_Phase1.txt`.
-   **Prompt Authoring**: As an AI, you must **NEVER** author or change the semantic content of the prompt assets. Only the maintainer can do this. You may only propose changes to the code that orchestrates these assets.
-   **Provenance Keys**: The canonical keys are `stage_1_construct`, `stage_2_semantic`, `stage_3_combined_lensed`.

## Suggested Workflow for Changes

1.  **Analyze the Request**: Understand whether the request involves changing the framework's mechanics (code) or its semantics (prompt assets).
2.  **For Code Changes**: Read the relevant modules in `chirality/application/services/` and `chirality/infrastructure/`. Propose changes that align with the existing canonical pipeline and asset-based architecture.
3.  **For Semantic Changes**: Remind the user that only they can author semantic content. If they provide new content, your job is to implement it by creating/updating the `.md` files and the `metadata.yml` manifest.
4.  **Testing**: Ensure any proposed code changes are accompanied by updates to the tests in `tests/`. Use the mock/echo resolver for all tests.
5.  **Validation**: Run `pytest -v`, `mypy`, and `black` locally before finalizing any proposal.