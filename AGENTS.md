# Repository Guidelines for AI Agents

This document provides essential, high-level guidance for AI coding assistants working on this repository. For more detailed instructions, see `GEMINI.md` or `CLAUDE.md`.

## Architecture Overview

The framework executes a fixed, canonical algorithm. Its logic is driven by an **asset-based prompt system**, where all semantic instructions are defined in version-controlled markdown files, not in the Python code.

-   **Prompt Assets**: All semantic content is in `chirality/prompt_assets/`. This includes the `system.md` prompt, `station_briefs/`, and `ops/` templates for operators and lensing.
-   **Orchestration**: The `chirality/lib/` directory contains the logic for assembling prompts (`prompt_builder.py`) based on a defined `strategies.py`.
-   **Execution**: The core pipeline logic in `chirality/core/operations.py` calls this assembly system and the `llm_client.py` to perform its work.

## The Canonical Pipeline

The framework follows a strict, three-stage process for all semantic computations:

1.  **Stage 1 (Mechanical Construction)**: The framework code mechanically assembles the initial input. For Matrix D, the construction formula is hard-coded in `operations.py`.
2.  **Stage 2 (Semantic Resolution)**: An LLM, guided by an `operator` asset, resolves the input into a concise concept.
3.  **Stage 3 (Combined Lensing)**: An LLM, guided by a `lensing` asset and a `station_brief`, interprets the Stage 2 output through ontological lenses.

-   **Z-Matrix Exception**: Matrix Z uses a special, single-stage path, employing a dedicated lensing asset (`ops/lensing/shift.md`) that performs its context shift.

## Critical Policies for AI Agents

Adherence to these policies is mandatory.

### 1. Prompt Authoring Policy

-   **AI agents must NEVER author or edit the semantic content of any prompt asset** in `chirality/prompt_assets/`. This content is owned exclusively by the human maintainer.
-   Your role is to implement the code that *orchestrates* these assets. If the maintainer provides new text for a prompt, your job is to place it in the correct file and update the `metadata.yml` manifest.

### 2. Immutable Files Policy

-   Under no circumstances should you ever modify `chirality/normative_spec.txt`. This file is the canonical semantic specification of the framework.

### 3. LLM API Policy

-   **Approved API**: The OpenAI resolver **MUST** use the `client.responses.create()` method.
-   **Forbidden API**: The `client.chat.completions.create()` API is strictly prohibited. CI checks will fail if its usage is detected.
-   **Configuration**: All LLM parameters (model, temperature, etc.) are defined centrally in `chirality/core/llm_config.py`. Do not add per-station or user-configurable overrides.

### 4. Placeholder Policy

-   The prompt system uses a fixed set of placeholders. Any additions require code changes to `prompt_builder.py`.
-   **Allowed Placeholders**: `{{row_label}}`, `{{col_label}}`, `{{content}}`, `{{station_brief}}`, `{{station_id}}`, and `{{terms}}`.

## Day-to-Day Commands

-   **Testing**: `pytest -v` (uses mocks, no live LLM calls).
-   **Type Checking**: `mypy chirality/`
-   **Formatting**: `black chirality/ tests/`
-   **Full Pipeline (Echo)**: `python3 -m chirality.cli compute-pipeline --resolver echo --snapshot-jsonl --include-base -v`