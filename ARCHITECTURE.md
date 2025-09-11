# Chirality Framework Architecture

## 1. Core Philosophy: "Conversation as Program"

The Chirality Framework is not a traditional Python application. Its architecture is designed to serve a single purpose: to execute a **"Conversation as Program."**

- **The Program Is the Transcript:** The *actual program* is the sequence of version-controlled prompt assets and the resulting dialogue transcript. The final output is an artifact of this structured conversation.
- **The Code Is the Control-Plane:** The Python codebase is a deterministic **Orchestrator** or **Control-Plane**. Its only job is to run the "real" program (the conversation) reliably and verifiably.
- **The LLM Is the Runtime:** The Large Language Model is the runtime environment where the semantic program executes.

This philosophy mandates a strict separation of concerns, which is implemented using a Domain-Driven Design (DDD) structure.

## 2. Architecture by DDD Layers & Bounded Contexts

The codebase is organized into canonical DDD layers, which map to specific Bounded Contexts (BCs) with clear responsibilities.

```
+----------------+      +-----------------+      +----------------+
|   Interfaces   |----->|   Application   |----->|  Infrastructure|
| (The "Button") |      | (The Director)  |      | (The "Real World")|
+----------------+      +-------+---------+      +----------------+
                                |
                                | Uses
                                v
                          +-------------+
                          |   Domain    |
                          | (The "Rules") |
                          +-------------+
```

### The `domain` Layer (The "Rules of the Game")

This layer represents the pure, abstract concepts of the Chirality Framework. It has no knowledge of LLMs, files, or APIs.

- **Responsibilities:**
    - Defines the **Canonical Models** (axiomatic matrices A, B, J) in `matrices/canonical.py`.
    - Defines the core **Value Objects** (`Matrix`, `Cell`) in `types.py`.
    - Defines the logical rules for matrix combination via **Preflight Checks** in `preflight.py`.

### The `infrastructure` Layer (The "Real World" & The "Script")

This layer handles all interaction with the outside world and contains the physical prompt assets. It is the **Data-Plane**.

- **Responsibilities:**
    - **Domain Resource Repository (The Prompts):** The `prompts/assets/` directory holds the `.md` prompt files. These are logically part of the domain but physically stored in infrastructure. The `prompts/registry.py` loads and manages them.
    - **Anti-Corruption Layer (ACL):** The `llm/openai_adapter.py` is the *only* file that communicates with the OpenAI Responses API, protecting the domain from external service details.
    - **Persistence Repositories:** Code that reads/writes `artifacts/` files, such as `lens_catalog.json`, `lens_overrides.json`, and the final output traces.

### The `application` Layer (The "Director")

This is the **Control-Plane**. It orchestrates the entire process, using rules from the `domain` and tools from `infrastructure`.

- **Responsibilities:**
    - **Conversation Execution BC:** The `phase1/dialogue_run.py` file contains the `DialogueOrchestrator`, which directs the A->E conversational chain. It sequences prompts, manages the dialogue history, and executes code-only steps (e.g., transpose).
    - **Lens Management BC:** The `lenses/` directory contains the `LensResolver` and its helpers. This is a specialized service for managing the creation, caching, and resolution of lenses according to the `catalog` vs. `auto` modes.

### The `interfaces` Layer (The "Power Button")

The outermost layer, providing the entry point for a user to run the program.

- **Responsibilities:**
    - The `cli.py` file defines the command-line interface (e.g., `chirality phase1-dialogue-run`), parses arguments, and triggers the `DialogueOrchestrator`.

### The `Observability & Governance` Cross-Cutting Concern

This is not a single directory but a collection of components whose purpose is to enforce the architecture.

- **Responsibilities:**
    - **Architectural Guardrails:** `tests/test_architecture_guards.py` and `scripts/guard_*.py` enforce rules like "no inline prompts" and "Responses API only."
    - **Semantic Contract Tests:** `tests/test_clean_transcript.py` and other tests that validate the content and order of the conversation itself, ensuring the LLM dialogue adheres to the specified rules.

## 3. The "Pure History" Model & Data Flow

The framework operates on a "Pure History" model to maintain semantic integrity.

- **The Transcript is Sacred:** The conversational history sent to the LLM contains only pure semantic content (instructions, matrices, lenses). It **must not** contain any framework metadata (e.g., `system_sha`, `source: catalog`, `mode: cross`).
- **Prompts are Static Assets:** Each `.md` file is a complete, static user turn. The orchestrator's job is to sequence them.
- **No `{{content}}` Placeholders:** The orchestrator never injects the output of a previous LLM turn into the prompt for the next turn. The LLM is expected to derive this context from the conversation history.
- **Metadata Placeholders are Allowed:** Prompts *can* contain placeholders for out-of-band data needed for an operation, such as `{{lens}}` (from the lens catalog) or `{{row_name}}` (metadata for the instruction).
- **Data-Drops for Code Operations:** When a non-LLM operation occurs (e.g., transposing Matrix K), the orchestrator adds a new `role: user` turn to the conversation that presents the result in a clean, metadata-free block (`<<<BEGIN DERIVED MATRIX>>>...`). This makes the code-only step a visible and auditable part of the conversation.
- **Provenance is External:** All metadata (SHAs, timestamps, lens sources, etc.) is captured exclusively in the Python trace objects and is never exposed to the LLM.

## 4. Semantic‑First + Out‑of‑Band Normalization

Phase‑1 now separates creative generation from structured extraction:

- **Stage A (Semantic, Markdown)**: Prompts produce clean, human‑readable matrices. Transcript is free of framework metadata and JSON constraints.
- **Stage B (Normalization, Strict JSON)**: A reusable normalizer prompt converts the Stage‑A text into a single JSON object that matches the strict schema exactly. Local validation is applied with one diff‑driven retry. A deterministic GitHub‑table parser is used as a first pass to reduce model calls.

Provenance and failure behavior:
- Each normalized object carries a `_provenance.stage_a_sha256` hash of the Stage‑A text to enable idempotent re‑normalization and audit.
- Missing/invalid structure fails loudly and is reported in a per‑stage `validation` block emitted by the extractor (kept out of DB ingest).

Transport & contracts:
- Adapter uses OpenAI Responses API with typed message parts (`type: "input_text"`).
- JSON is enabled only for JSON‑expecting calls; semantic stages run free‑form.
- For reasoning models (e.g., GPT‑5), unsupported parameters like `top_p` are omitted automatically by the adapter.

CLI support:
- `--relaxed-json` keeps the transcript clean and saves `phase1_relaxed_output.json`.
- `--extract-structured` runs the normalizer immediately to produce `phase1_structured.json` and `phase1_structured_matrices.json` for DB ingest.
- `phase1-extract` normalizes a saved relaxed run later (e.g., in CI/CD).
- `--stop-at C_interpreted` enables quick Stage‑A checks for Matrix C.
