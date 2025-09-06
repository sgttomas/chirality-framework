# The Chirality Framework Canonical Algorithm

## 1. Overview & Philosophy: The "Semantic Calculator"

The Chirality Framework is implemented as a fixed algorithm, not a flexible platform. Its purpose is to function as a "semantic calculator," taking canonical, unchanging inputs and executing a procedurally rigorous methodology to produce insightful, structured outputs.

The core design principles are:
-   **Simplicity Over Abstraction:** The code is a direct translation of the algorithm.
-   **Directness Over Indirection:** The flow of control is linear and explicit.
-   **Observability is Paramount:** The process is designed to be fully transparent.

## 2. The Canonical Matrices

The algorithm begins with fixed, axiomatic matrices defined in `chirality/core/matrices.py`.

*   **`MATRIX_A` (3x4): The Problem Statement Matrix.**
*   **`MATRIX_B` (4x4): The Decision Basis Matrix.**
*   **`MATRIX_J` (3x4): The Judgment Matrix.** (A subset of Matrix B).

## 3. The Canonical Pipeline

The core of the framework is the process by which new meaning is generated for each cell. This is a pipeline that moves from mechanical combination to semantic interpretation.

### Stage 1: Combinatorial (Mechanical)

This stage is purely mechanical and does not involve an LLM. It combines the terms from the input matrices according to the specified operation (e.g., for a dot product, it generates all the `A[i,k] * B[k,j]` word pairs).

*   **Input:** Raw terms from source matrices.
*   **Output:** A list of string pairs or a mechanically constructed sentence.

### Stage 2: Semantic Resolution (LLM Call #1)

For operations involving semantic multiplication (`*` or `⊙`), an LLM resolves the raw terms from Stage 1 into a single, concise concept. This is the first layer of meaning generation.

**Implementation Note:** The framework uses OpenAI's Responses API exclusively (not Chat Completions API) with JSON output format enforced through system prompts rather than API parameters.

*   **Input:** A list of term pairs (e.g., `["Values * Necessary", "Actions * Contingent"]`).
*   **Output:** A resolved concept or sentence (depending on the operator), which then becomes the input to Stage 3.

### Stage 3: Combined Ontological Lensing (LLM Call #2)

This is the primary interpretation step. The output from Stage 2 (or the mechanical sentence from Stage 1, in the case of Matrix D) is interpreted through a single, powerful, combined lens. A single LLM call processes the content through three simultaneous perspectives:

1.  **The Column Lens:** The ontological meaning of the cell's column.
2.  **The Row Lens:** The ontological meaning of the cell's row.
3.  **The Station Context:** The purpose of the current station in the semantic valley (provided by a **Station Brief** asset).

*   **Input:** The content to be interpreted and the full cell context (row/column labels, station brief).
*   **Output:** A final, synthesized narrative that integrates the content with its full ontological and situational context.

## 4. Sequence of Operations

The calculator performs the following sequence of operations, with each step building on the last. All LLM-driven computations now use the canonical pipeline described above.

1.  **Compute Matrix C (Requirements):** `C = A * B`
2.  **Compute Matrix F (Functions):** `F = J ⊙ C`
3.  **Compute Matrix D (Solution Objectives):** `D = A + F` (Mechanical Stage 1, then Combined Lensing)
4.  **Compute Matrix K (Pre-Verification Transform):** `K = D^T` (No LLM)
5.  **Compute Matrix X (Verification):** `X = K * J`
6.  **Compute Matrix Z (Validation):** `Z = shift(X)` (A single, Z-specific Combined Lensing call that performs the context shift from Verification to Validation)
7.  **Compute Matrix T (Evaluation Criteria):** `T = (B[0:3,:])^T` (No LLM)
8.  **Compute Matrix G (Evaluation Input):** `G = Z[0:3,:]` (No LLM)
9.  **Compute Array P (Evaluation Context):** `P = Z[3,:]` (No LLM)
10. **Compute Matrix E (Evaluation):** `E = G * T`

## 5. Provenance

With the move to a simpler, more powerful pipeline, the provenance structure has also been simplified.

-   `stage_1_construct`: Contains the mechanical inputs (e.g., list of product pairs).
-   `stage_2_semantic`: Contains the output of the first LLM call (the resolved concepts).
-   `stage_3_combined_lensed`: Contains the final narrative output from the combined lensing call.

This structure provides a clear, auditable trail of the new canonical pipeline for every cell.
