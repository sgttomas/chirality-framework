# The Philosophy of the Chirality Framework

This document outlines the core philosophy and conceptual architecture of the Chirality Framework. It is intended for developers, architects, and researchers who wish to understand the "why" behind the framework's design.

## 1. The Semantic Calculator

The Chirality Framework is not a general-purpose, flexible platform. It is a **"semantic calculator"**: a tool that executes a fixed, canonical algorithm to produce insightful, structured outputs. Its primary design principles are:

-   **Simplicity Over Abstraction:** The code is a direct translation of the algorithm.
-   **Directness Over Indirection:** The flow of control is linear and explicit.
-   **Observability is Paramount:** The entire process is designed to be transparent and auditable.

The value of the framework is in the unique, insightful **output** of the calculation, not in the flexibility of the code itself.

## 2. The Semantic Valley as a Cognitive Workflow

The 11 stations of the semantic valley are not merely a sequence of computations; they represent a structured cognitive workflow for moving from a problem to a state of reliable knowledge. This workflow follows a specific, repeating pattern of ontological modalities, revealing a deep structure in the problem-solving process.

## 3. The Ontological Modality Path: A Detailed Mapping

The "About" section of the framework describes a high-level philosophical path:
`Problem → Systematic → Process → Epistemic → Epistemic → Process → Alethic → Epistemic → Alethic → Alethic → Resolution`

This path has a precise 1:1 mapping to the 11 stations of the semantic valley. It describes the *type* of cognitive work being performed at each stage.

---

### The Mapping Explained

*   **`Problem` -> S1: Problem Statement**
    *   **Operation:** `[A], [B]`
    *   **Analysis:** This is the axiomatic starting point. It defines the ontological axes and the fundamental terms upon which all subsequent reasoning is built. It is the ground truth for the problem space.

*   **`Systematic` -> S2: Requirements**
    *   **Operation:** `[C] = [A] * [B]`
    *   **Analysis:** The semantic dot product is a **systematic** enumeration of all possible interactions between the problem's axioms (A) and its decision basis (B). It ensures that no potential requirement is overlooked before the process of semantic interpretation begins.

*   **`Process` -> S3: Objectives**
    *   **Operation:** `[D] = [A] + [F]`
    *   **Analysis:** The construction of Matrix D is a purely mechanical **process**. It follows a rigid formula to combine elements from A and F into a set of objective statements. This stage is procedural, not interpretive.

*   **`Epistemic` -> S4: Verification**
    *   **Operation:** `[K] = [D]^T, [X] = [K] * [J]`
    *   **Analysis:** This is the first major **epistemic** (knowledge-based) check. It verifies that the objectives (D, transposed into K) are internally consistent and correct according to the judgment criteria (J). It asks, "Are our objectives well-formed and logically sound?"

*   **`Epistemic` -> S5: Validation**
    *   **Operation:** `[Z] = shift([X])`
    *   **Analysis:** This is the second **epistemic** check, which strictly follows Verification. The `shift` operation is an LLM-driven reframing of the verified knowledge in `X` into a new context, `Z`. It is not a simple procedural transformation but a knowledge-based re-interpretation. It asks, "Now that we know the objectives are correct, what do they mean in the context of solving the *right* problem?"

*   **`Process` -> S6: Evaluation**
    *   **Operation:** `[G], [P], [T], [E]`
    *   **Analysis:** This station is a **process** step that gathers and structures the inputs for the subsequent alethic assessments. It is not an epistemic evaluation itself but a procedural preparation. The matrices `G`, `P`, and `T` are prepared for the computation of `E`.

*   **`Alethic` -> S7: Assessment**
    *   **Operation:** `[M] = [R] x [E]`
    *   **Analysis:** This marks the transition to **alethic** (truth-based) modalities. The "semantic cross product" (`x`) is introduced, which applies the fundamental modes of truth and assessment (from R) to the evaluated objectives (E). This stage moves beyond correctness to assess the deeper truth and applicability of the solution.

*   **`Epistemic` -> S8: Implementation**
    *   **Operation:** `[W] = [M] x [X]`
    *   **Analysis:** This is a grounding step. It applies our verified, **epistemic** framework (X) to our alethic assessment (M). This ensures that our deep "truth" claims are still grounded in and consistent with our verified, knowledge-based objectives.

*   **`Alethic` -> S9: Integration**
    *   **Operation:** `[U] = [W] x [P]`
    *   **Analysis:** The first of the final **alethic** checks. It applies the "Validity Parameters" (P) to the implemented framework (W), ensuring the solution is integrated and coherent.

*   **`Alethic` -> S10: Reflection**
    *   **Operation:** `[N] = [U] x [H]`
    *   **Analysis:** The final **alethic** check. It applies "Consistency" checks (H) to the integrated result (U), ensuring the solution holds up under final reflection.

*   **`Resolution` -> S11: Resolution**
    *   **Operation:** `Final = synth([N])`
    *   **Analysis:** The final output, representing a state of reliable knowledge that has been systematically constructed, procedurally defined, and rigorously checked against both epistemic and alethic criteria.

## 4. Executor Grouping (Internal)

For implementation purposes, the 11 stations are grouped into 9 execution units. This is an internal detail that maps the conceptual stations to the practical execution flow.

-   **G1:** S1 (Problem Statement)
-   **G2:** S2 (Requirements)
-   **G3:** S3 (Objectives)
-   **G4:** S4, S5 (Verification & Validation)
-   **G5:** S6 (Evaluation)
-   **G6:** S7 (Assessment)
-   **G7:** S8 (Implementation)
-   **G8:** S9, S10 (Integration & Reflection)
-   **G9:** S11 (Resolution)
