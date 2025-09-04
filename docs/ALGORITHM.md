# The Chirality Framework Canonical Algorithm

## 1. Overview & Philosophy: The "Semantic Calculator"

The Chirality Framework is implemented as a fixed algorithm, not a flexible platform. Its purpose is to function as a "semantic calculator," taking canonical, unchanging inputs (Matrices A and B) and executing a procedurally rigorous methodology with fixed ontological structure to produce a series of insightful, structured outputs (Matrices C, F, D, etc.).

The core design principles are:
- **Simplicity Over Abstraction:** The code is a direct translation of the algorithm.
- **Directness Over Indirection:** The flow of control is linear and explicit.
- **Observability is Paramount:** The process is designed to be fully transparent through detailed tracing and a cell-first CLI.

## 2. The Canonical Matrices

The algorithm begins with two fixed, axiomatic matrices. The authoritative source for these matrices is the code itself, located in `chirality/core/matrices.py`. These definitions are based on the final normative specification (14.2.1.1).

*   **`MATRIX_A` (3x4): The Problem Statement Matrix.** Defines the ontological axes for Normative, Operative, and Evaluative perspectives against Guiding, Applying, Judging, and Reviewing functions.
*   **`MATRIX_B` (4x4): The Decision Basis Matrix.** Defines the ontological axes for levels of knowledge (Data, Information, Knowledge, Wisdom) against logical attributes (Necessity, Sufficiency, Completeness, Consistency).
*   **`MATRIX_J` (3x4): The Judgment Matrix.** A truncated version of Matrix B, used in later stages.

## 3. The Core Algorithm: The Three-Stage Interpretation Pipeline

The "secret sauce" of the Chirality Framework is the process by which new meaning is generated for a cell at a specific matrix coordinate `(i, j)`. This is a three-stage pipeline:

### Stage 1: Combinatorial (Mechanical)
This stage is purely mechanical and does not involve an LLM. It combines the terms from the input matrices according to the specified operation (e.g., for a dot product, it generates all the `A[i,k] * B[k,j]` word pairs).

*   **Input:** Raw terms from source matrices.
*   **Output:** A list of string pairs (e.g., `["Direction * Essential Facts", "Implementation * Critical Context", ...]`).

### Stage 2: Semantic Resolution (First Meaning Layer)
An LLM resolves each raw word pair from Stage 1 into a single, concise concept. This is the first layer of meaning generation.

*   **Input:** A single word pair (e.g., `"Direction * Essential Facts"`).
*   **Output:** A resolved concept (e.g., `"Guiding Imperatives"`).

### Stage 3: Ontological Lensing (Deep Interpretation)
The resolved concepts from Stage 2 are combined and then interpreted through a universal, three-step lensing process applied to all matrices:

1) Column lens → 2) Row lens → 3) Final synthesis.

*   **Input:** The combined concepts and the ontological context (e.g., `content: "Guiding Imperatives, Applied Context..."`, `row: "Normative"`, `col: "Necessity (vs Contingency)"`).
*   **Output:** A final, synthesized narrative that explains the meaning of the content within that specific ontological context, after column and row perspectives are applied.

## 4. Sequence of Operations

The calculator performs the following sequence of operations, with each step building on the last:

1.  **Compute Matrix C (Requirements):** `C = A * B`
    *   Each cell `C(i,j)` is computed using the full 3-stage pipeline on the dot product of row `i` from `A` and column `j` from `B`.
2.  **Compute Matrix F (Functions):** `F = J ⊙ C`
    *   Each cell `F(i,j)` is computed using an element-wise multiplication of `J(i,j)` and `C(i,j)`, which is then processed through the Semantic Resolution and Lensing stages.
3.  **Compute Matrix D (Solution Objectives):** `D = A + F`
    *   Each cell `D(i,j)` is computed by mechanically forming the sentence: `"A(i,j) applied to frame the problem of generating reliable knowledge; F(i,j) to resolve the problem."`. This serves as Stage 2, and the result is passed to the universal lensing process.
4.  **Compute Matrix K (Pre-Verification Transform):** `K = D^T`
    *   Matrix K is the transpose of Matrix D, transforming Solution Objectives for verification.
5.  **Compute Matrix X (Verification):** `X = K * J`
    *   Each cell `X(i,j)` is computed using the full 3-stage pipeline on the dot product of row `i` from `K` and column `j` from `J`.
6.  **Compute Matrix Z (Validation):** `Z = shift(X)`
    *   Each cell `Z(i,j)` uses a lean 2-stage pipeline: direct extraction of `X(i,j)` content (Stage 1), then station context shift from Verification to Validation (Stage 2). No lensing stages.
7.  **Compute Matrix T (Evaluation Criteria):** `T = (B[0:3,:])^T`
    *   Matrix T is derived from a slice of Matrix B, not from J. The first 3 rows of B (Data, Information, Knowledge) are sliced and transposed to create T (4×3).
8.  **Compute Matrix G (Evaluation Input):** `G = Z[0:3,:]`
    *   Matrix G is the first 3 rows of Z, representing validated objectives for evaluation.
9.  **Compute Array P (Evaluation Context):** `P = Z[3,:]`
    *   Array P is the fourth row of Z extracted as a 1×4 matrix for evaluation context.
10. **Compute Matrix E (Evaluation):** `E = G * T`
    *   Each cell `E(i,j)` is computed using the full 3-stage pipeline on the dot product of row `i` from `G` and column `j` from `T`.

## 5. Observability

The entire process is designed to be transparent through a suite of CLI tools that provide different levels of detail.

*   **HTML Viewer (Primary Interface):** The recommended way to observe the results is via the static HTML viewer. It displays all matrices from a given run in a clean, readable format. Generate it by running `compute-pipeline` and then `render-viewer`.
*   **Matrix Snapshots (Data Output):** For machine-readable output, the `compute-pipeline` and `compute-matrix` commands can generate JSONL "snapshot" files for each matrix. These files contain the final state and are the data source for the HTML viewer.
*   **Tracing (Deep Debugging):** For maximum detail, the `--trace` or `--trace-only` flags will generate a detailed JSONL file for each cell computation, recording the inputs and outputs of every single stage in the pipeline.
*   **Neo4j (Graph Analysis):** For advanced structural analysis, the `--neo4j-export` flag writes the full, five-stage provenance of each cell to a Neo4j graph database, correlated by a unique `run_id`.

## 6. Provenance: Pipeline-Specific Field Structures

Different matrices use different provenance structures based on their processing pipeline:

### 6.1 Full 5-Stage Provenance (Matrices C, F, D, X, E)
The third stage (Ontological Lensing) is a universal three-step process (Column → Row → Final). For full observability and graph export, provenance splits this into three separate fields:

- `stage_1_construct`: Mechanical setup of inputs.
  - C: list of k-products `A[i,k] * B[k,j]` (texts)
  - F: element-wise pair `J[i,j] * C[i,j]` (text)
  - D: formula reference `A[i,j] + F[i,j]` (text)
  - X: list of k-products `K[i,k] * J[k,j]` (texts)
  - E: list of k-products `G[i,k] * T[k,j]` (texts)
- `stage_2_semantic`: First meaning layer produced from Stage 1 content.
  - C: resolved concepts for each k-product (texts)
  - F: resolved concept for the element-wise pair (text)
  - D: mechanical synthesis sentence (semantic addition) (text)
  - X: resolved concepts for each k-product (texts)
  - E: resolved concepts for each k-product (texts)
- `stage_3_column_lensed`: Column-perspective interpretation of Stage 2 content (text)
- `stage_4_row_lensed`: Row-perspective interpretation of Stage 2 content (text)
- `stage_5_final_synthesis`: Integrated narrative fusing column and row perspectives (text)

### 6.2 Lean 2-Stage Provenance (Matrix Z)
Matrix Z uses a simplified pipeline for station context shift:

- `stage_1_construct`: Direct extraction of source content.
  - Z: verification content from `X[i,j]` (text)
- `stage_2_semantic`: Station shift operation result.
  - Z: validation-contextualized content (text)
- `stage_3_column_lensed`: Empty (for exporter compatibility)
- `stage_4_row_lensed`: Empty (for exporter compatibility)  
- `stage_5_final_synthesis`: Empty (for exporter compatibility)

Notes
- These field names match the canonical schema enforced in code (`chirality/core/provenance_schema.py`) and used by the Neo4j exporter.
- Tracing emits step-aligned events (e.g., `lensing:column`, `lensing:row`, `lensing:final`) which correspond to the last three provenance fields.

## 7. Verification (K and X)

Beyond D (Solution Objectives), the Verification stage introduces two derived matrices:

- K = D^T (transpose of D)
  - Size: 4×3. Structural transpose only (no new semantic computation).
  - Axes: rows are D’s columns; columns are D’s rows.
  - Purpose: prepares objectives for verification against criteria in J.

- X = K * J (Verification)
  - Size: 4×4. Computed with the same 3‑stage pipeline as C: combinatorial → semantic → lensing.
  - Station: Verification. Lensing remains universal (Column → Row → Final).
  - Axes: rows = K row labels; columns = J column labels.

These definitions mirror the CLI "info" output and README quick reference for parity and clarity.

## 8. Evaluation (G, T, P, and E)

Beyond Z (Validation), the Evaluation stage introduces four matrices:

- T = (B[0:3,:])^T (Evaluation Criteria)
  - Size: 4×3. Derived from slice and transpose of Matrix B (not J).
  - Axes: rows are B's columns; columns are first 3 B rows (Data, Information, Knowledge).
  - Purpose: provides evaluation criteria grounded in observable knowledge levels.

- G = Z[0:3,:] (Evaluation Input)  
  - Size: 3×4. First 3 rows of the Validation matrix Z.
  - Axes: rows = first 3 Z row labels; columns = Z column labels.
  - Purpose: validated objectives ready for evaluation.

- P = Z[3,:] (Evaluation Context)
  - Size: 1×4. Fourth row of Z extracted as evaluation perspective.
  - Axes: row = fourth Z row label; columns = Z column labels.
  - Purpose: provides validation context for evaluation operations.

- E = G * T (Evaluation)
  - Size: 3×3. Computed with the same 3-stage pipeline as C and X: combinatorial → semantic → lensing.
  - Station: Evaluation. Lensing remains universal (Column → Row → Final).
  - Axes: rows = G row labels; columns = T column labels.
