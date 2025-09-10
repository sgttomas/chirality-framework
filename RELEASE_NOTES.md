# Release Notes: Version 20.0.0

**Release Date:** 2025-09-10
**Codename:** Architectural Purity

## Overview

Version 20.0.0 represents a fundamental architectural rewrite of the Chirality Framework. This release moves the project from a conventional Python application to a true **"Conversation as Program"** model, where the core logic is expressed as a pure, auditable, and semantically-clean dialogue with a Large Language Model.

The Python codebase has been refactored into a robust **Control-Plane** responsible only for orchestrating this conversation, while all semantic instructions and data reside in a version-controlled **Data-Plane**. This release introduces major improvements in architectural clarity, testability, provenance, and philosophical alignment.

## Major Architectural Changes

- **Adoption of the "Pure History" Model:** The framework now operates on a single, continuous conversational transcript. The LLM relies exclusively on the preceding dialogue for context, eliminating complex template injection and making the process more robust and transparent.

- **Complete OpenAI Responses API Migration:** All calls to the legacy Chat Completions API (`client.chat.completions.create`) have been purged. The framework now exclusively uses the `client.responses.create` endpoint with the `instructions` and `input` contract, ensuring a clean separation of the system prompt from the conversational transcript.

- **Strict Metadata Purge from LLM Transcript:** All framework-level metadata (e.g., SHAs, timestamps, sources, modes) has been completely removed from the dialogue sent to the LLM. The LLM now sees only pure semantic content (instructions, matrices, lenses). All provenance data is captured exclusively in Python-side trace objects.

- **Canonical Data-Drop Pattern:** All non-LLM operations (e.g., matrix transpose, slicing) now leave a footprint in the conversation as a clean, metadata-free `<<<BEGIN DERIVED MATRIX>>>` block. This makes every step in the pipeline, whether code- or LLM-driven, a visible and auditable part of the dialogue.

- **Formalized DDD Structure:** The architecture is now formally described using Domain-Driven Design (DDD) principles, including Bounded Contexts for Lens Management and Conversation Execution, and an Anti-Corruption Layer (ACL) for the OpenAI adapter. See the new `ARCHITECTURE.md` for full details.

## New Features & Systems

- **Comprehensive Lens Management System:** A complete, standalone system for managing semantic lenses has been implemented.
    - **Lens Catalog:** A meta-pipeline can now pre-generate a full `lens_catalog.json` for all stations.
    - **On-the-Fly Generation:** A new `lens_mode="auto"` allows the framework to generate missing lenses dynamically during a run.
    - **Overrides & Caching:** On-the-fly generated lenses are cached in `lens_overrides.json` with full provenance, and this cache takes precedence over the main catalog, allowing for robust A/B testing.
- **New CLI Commands:** The command-line interface has been expanded with a full suite of tools for managing the lens system: `chirality lenses ensure|refresh|show|meta|source|clear-overrides`.

## Testing & Architectural Enforcement

- **Architectural Guardrails:** The CI/CD pipeline is now protected by a new suite of blocking tests that programmatically enforce the architecture. These guards prevent the use of forbidden APIs, inline prompts, and metadata leaks into the transcript.
- **Semantic Contract Tests:** A new layer of testing has been introduced to validate the *conversation itself*. These tests assert the correct turn order, check for the presence and resolution of semantic operators, and verify the structural integrity of data-drops.

## Documentation Overhaul

- **New `ARCHITECTURE.md`:** A new, definitive document has been created that describes the "Conversation as Program" model and the full DDD-based design.
- **Updated AI & Contributor Guides:** `GEMINI.md`, `CLAUDE.md`, and `CONTRIBUTING.md` have been completely rewritten to reflect the new architecture, API contracts, and testing philosophy.
- **Refactored `README.md`:** The main README is now a clean, high-level entry point with an updated Quick Start guide.

## Deprecations & Removals

- All legacy components have been removed from the codebase, including `CellResolver`, `PromptBuilder`, `PromptStrategy`, and all `_compute_matrix_*` methods.
- All old prompt assets that mixed instructions with metadata have been removed in favor of the new, clean, single-purpose assets.
