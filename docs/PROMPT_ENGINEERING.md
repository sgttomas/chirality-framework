# Prompt Engineering Guide for the Chirality Framework

**Version: 2.0 (Asset-Based Architecture)**

This guide provides the official methodology for authoring and managing the semantic assets that drive the Chirality Framework. In the current architecture, all semantic content is externalized into version-controlled markdown files, giving the maintainer full control over the framework's reasoning and voice.

## Overview: The Prompt Asset Architecture

The framework's semantic engine has been refactored to separate semantic content from code. All prompts are now assembled from immutable, maintainer-authored assets.

-   **Source of Truth:** The `chirality/prompt_assets/` directory.
-   **Integrity and Versioning:** The `chirality/prompt_assets/metadata.yml` file, which registers every asset, its version, and its checksum.
-   **Assembly:** The `PromptBuilder` code reads these assets and assembles them according to a fixed, canonical pipeline. It only substitutes placeholders; it does not alter semantic content.

---

## The Core Assets and Their Roles

The entire semantic output of the framework is controlled by the interplay of the following assets.

### 1. The System Prompt (`system.md`)

-   **Purpose:** This is the global frame for all LLM interactions. It sets the persona of the LLM (e.g., "a semantic interpreter"), its core mission (e.g., "to generate reliable knowledge"), and the fundamental rules of engagement (e.g., "prioritize semantics over mechanics").
-   **Usage:** This asset is included at the beginning of every LLM call.

### 2. Station Briefs (`station/*.md`)

-   **Purpose:** This is a critical new concept. Each file (e.g., `evaluation.md`, `objectives.md`) provides the specific semantic context for a **Station** in the semantic valley. It tells the LLM the *purpose* of the work it is about to perform.
-   **Authoring Tip:** A good station brief describes the station's goal, its relationship to the previous station, and the kind of thinking the LLM should adopt (e.g., for "Evaluation," the brief would focus on establishing frameworks for judging quality and reliability).

### 3. Operator Assets (`ops/operators/*.md`)

-   **Purpose:** These assets define the exact instructions for a specific Stage 2 semantic operation.
    -   `multiply.md`: Defines how to find the "semantic intersection" of multiple terms.
    -   `elementwise.md`: A variant of multiplication for Matrix F.
    -   `shift.md`: Defines the context shift from Verification to Validation for Station Z.
-   **Authoring Tip:** The quality of the examples in `multiply.md` is crucial for guiding the LLM to the correct level of abstraction.

### 4. The Lensing Asset (`ops/lensing/combined.md`)

-   **Purpose:** This is the template for the unified, single-call combined lensing operation. It is the heart of the Stage 3 interpretation pipeline.
-   **Placeholders:** This asset uses placeholders to orchestrate the interpretation:
    -   `{{station_brief}}`: Where the full text of the relevant Station Brief is injected.
    -   `{{content}}`: The input text from Stage 2 that needs to be interpreted.
    -   `{{row_label}}` & `{{col_label}}`: The specific ontological lenses to apply.

---

## The Canonical Assembly Pipeline

The `PromptBuilder` assembles these assets in a fixed order.

1.  **For Stage 2 Operations (e.g., Multiplication):**
    -   `system.md`
    -   `ops/operators/multiply.md` (with the `{{terms}}` placeholder substituted)

2.  **For Stage 3 (Combined Lensing):**
    -   `system.md`
    -   `ops/lensing/combined.md` (with `{{station_brief}}`, `{{content}}`, `{{row_label}}`, and `{{col_label}}` placeholders substituted)
    -   For Validation (Z), include `ops/operators/shift.md` as part of the assembly before the combined template if your template relies on it.

**Note:** The Station Brief is **inlined** into the lensing prompt via the `{{station_brief}}` placeholder; it is not sent as a separate message. This creates a single, powerful, context-rich prompt for the most critical interpretation step.

---

## Authoring Guide for Maintainers

### Writing Effective Station Briefs

Your goal is to ground the LLM. A good brief should:
-   Clearly state the name and purpose of the Station (e.g., "You are at the Station of Verification.").
-   Explain what kind of cognitive work is done here (e.g., "Your goal is not to create new ideas, but to check the internal consistency of existing objectives.").
-   Describe how this station relates to the one before it.

### Authoring the `combined.md` Lensing Template

This is the most important asset for controlling the quality of the framework's output. A successful template will weave the placeholders into a narrative that guides the LLM.

**Example Structure:**

> You are an expert semantic interpreter. Your task is to synthesize a final narrative for a cell in a matrix.
>
> **Your Goal:**
> {{station_brief}}
>
> **The Content to Interpret:**
> "{{content}}"
>
> **Apply the following ontological lenses:**
> 1.  **Column Perspective:** Interpret the content through the lens of `{{col_label}}`.
> 2.  **Row Perspective:** Interpret the content through the lens of `{{row_label}}`.
>
> **Final Synthesized Narrative:**
> Now, combine the content and both perspectives into a final, integrated narrative that fulfills the goal of the station. The narrative should be clear, concise, and directly address the station's purpose.

### Managing Assets and Ensuring Integrity

The `chirality/prompt_assets/metadata.yml` file is the manifest for all semantic assets.
-   **Workflow:** When you edit any `.md` asset file, you **must** update its corresponding entry in `metadata.yml` with the new `sha256` checksum, `size_bytes`, `last_modified` timestamp, and an updated `version` number.
-   **Integrity:** The `PromptRegistry` will fail to initialize if any asset does not match its checksum in the metadata file. This guarantees that the executed semantics are always the version-controlled, intended semantics.
