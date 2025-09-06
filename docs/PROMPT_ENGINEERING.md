# Prompt Engineering Guide for the Chirality Framework

**Version: 3.0 (Asset-Based Architecture)**

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

-   **Purpose:** This is the global frame for all LLM interactions. It sets the persona of the LLM, its core mission, its operational principles, and its non-negotiable output contract (JSON).
-   **Usage:** This asset is prepended to every LLM call made in Stage 2 and Stage 3 of the pipeline.

### 2. Station Briefs (`station_briefs/*.md`)

-   **Purpose:** Each file provides the specific semantic context for a **Station** in the semantic valley. It tells the LLM the *purpose* of the work it is about to perform at that station.
-   **Authoring Tip:** A good station brief describes the station's goal, its relationship to the previous station, and the kind of thinking the LLM should adopt (e.g., for "Verification," the brief would focus on checking for internal correctness).

### 3. Operator Assets (`ops/operators/*.md`)

-   **Purpose:** These assets define the exact instructions for a specific Stage 2 semantic operation.
    -   `multiply.md`: Defines how to find the "semantic intersection" of multiple terms (for matrices C, X, E).
    -   `elementwise.md`: A variant of multiplication for the single pairs in Matrix F.

### 4. Lensing Assets (`ops/lensing/*.md`)

-   **Purpose:** These templates guide the Stage 3 interpretation pipeline.
    -   `combined.md`: The standard template for the unified, single-call combined lensing operation.
    -   `shift.md`: A special-purpose lensing template used only for Matrix Z, which handles the context shift from Verification to Validation.

### Placeholders

The prompt asset system uses a limited set of placeholders to inject context.

-   `{{terms}}`: Used in Stage 2 operator assets (`multiply.md`, `elementwise.md`) to inject the list of terms to be resolved.
-   `{{content}}`: Used in Stage 3 lensing assets to inject the text produced by the previous stage.
-   `{{row_label}}` & `{{col_label}}`: Used in Stage 3 lensing assets to provide the ontological lenses.
-   `{{station_brief}}`: Used in Stage 3 lensing assets to inject the full text of the relevant station brief.
-   `{{station_id}}`: Used in Stage 3 lensing assets to provide the clean name of the current station (e.g., "Validation").

---

## The Canonical Assembly Pipeline

The `PromptBuilder` assembles these assets in a fixed order.

1.  **For Stage 2 Operations (e.g., Multiplication):**
    -   `system.md`
    -   `ops/operators/multiply.md` (with the `{{terms}}` placeholder substituted)

2.  **For Stage 3 (Standard Lensing):**
    -   `system.md`
    -   `ops/lensing/combined.md` (with `{{station_brief}}`, `{{content}}`, `{{row_label}}`, `{{col_label}}`, and `{{station_id}}` placeholders substituted)

3.  **For Stage 3 (Z-Matrix Shift Lensing):**
    -   `system.md`
    -   `ops/lensing/shift.md` (with `{{content}}`, `{{row_label}}`, `{{col_label}}`, and `{{station_id}}` placeholders substituted)

---

## Authoring Guide for Maintainers

### Writing Effective Station Briefs

Your goal is to ground the LLM. A good brief should:
-   Clearly state the name and purpose of the Station (e.g., "You are at the Station of Verification.").
-   Explain what kind of cognitive work is done here (e.g., "Your goal is not to create new ideas, but to check the internal consistency of existing objectives.").
-   Describe how this station relates to the one before it (e.g., "Building on the Objectives you just framed...").

### Managing Assets and Ensuring Integrity

The `chirality/prompt_assets/metadata.yml` file is the manifest for all semantic assets.
-   **Workflow:** When you edit any `.md` asset file, you **must** update its corresponding entry in `metadata.yml` with the new `sha256` checksum and `size_bytes`. It is also good practice to update the `version` and `last_modified` timestamp.
-   **Integrity:** The `PromptRegistry` will fail to initialize if any asset does not match its checksum in the metadata file. This guarantees that the executed semantics are always the version-controlled, intended semantics.