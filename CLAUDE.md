# Guidance for AI Assistants (Claude)

**NOTE:** This project has a unique architecture. Do not assume standard coding practices. Read this guide carefully.

## Core Philosophy: "Conversation as Program"

This framework's primary purpose is to execute a **"Conversation as Program."** The Python code is merely a **Control-Plane** or **Orchestrator** that runs the "real" program: a sequence of prompts that form a single, continuous dialogue with an LLM.

- **Your Goal:** Your primary goal is to help the user manage and refactor the **Control-Plane** (`.py` files) and the **Data-Plane** (the `.md` prompt assets).
- **The Program is the Transcript:** The dialogue history is the program's state. The LLM relies on this history for context.
- **The LLM is the Runtime:** All semantic operations happen inside the LLM based on the conversational flow.

## Key Architectural Concepts

Refer to `ARCHITECTURE.md` for a full breakdown. Key points for you are:

1.  **The "Pure History" Model:**
    - The `DialogueOrchestrator` builds a single, growing transcript string.
    - **CRITICAL:** We do **NOT** inject the output of a previous LLM call into the prompt for the next call (e.g., no `{{content}}` placeholders for prior results).
    - Prompts are static instructions that rely on the LLM's ability to understand the preceding turns in the conversation.

2.  **The Prompt Asset System (`chirality/infrastructure/prompts/assets/`)**
    - **Source of Truth:** All semantic instructions (the "why" and "how") live in `.md` files. The Python code only sequences these assets.
    - **Your Role:** You must **NEVER** author or change the semantic content of these prompt assets. Only the user can do this. Your job is to wire them up in the orchestrator.
    - **Structure:** There is one `.md` file per LLM call, organized by matrix and stage (e.g., `phase1/C/mechanical.md`).

3.  **The Correct API: OpenAI Responses API**
    - **MANDATORY:** The framework **MUST** use the `client.responses.create()` method.
    - **FORBIDDEN:** The `client.chat.completions.create()` API and the `messages=[...]` array format are strictly forbidden. All architectural guards will fail if they are used.
    - **Correct Signature:** The adapter call uses `instructions` (for the system prompt) and `input` (for the conversational transcript).
      ```python
      # Correct Usage
      call_responses_api(
          instructions=system_prompt_text,
          input=full_transcript_string
      )
      ```

4.  **No Metadata in the Transcript:**
    - The conversational transcript sent to the LLM must be pure semantic content.
    - It **must not** contain any framework metadata like SHAs, timestamps, sources, modes, or data-drop headers like `<<<BEGIN...>>>`.
    - All provenance data is captured exclusively in Python trace objects.

5.  **Data-Drops for Code-Only Steps:**
    - When a non-LLM operation occurs (e.g., transposing a matrix), the orchestrator adds a `role: user` turn to the conversation that presents the result in clean, natural language, ready for the next LLM step.

## Day-to-Day Commands

- **Run the full Phase 1 pipeline:**
  ```bash
  # Ensure the lens catalog exists first
  python3 -m chirality.interfaces.cli lenses ensure

  # Run the main dialogue
  python3 -m chirality.interfaces.cli phase1-dialogue-run --lens-mode=auto
  ```
- **Testing:**
  ```bash
  # Run all tests
  pytest -v

  # Run critical architectural guards
  python3 tests/test_architecture_guards.py
  python3 tests/test_clean_transcript.py
  ```

## Contribution Guardrails

- **CRITICAL API USAGE:** Use `client.responses.create(instructions=..., input=...)`. Never use `client.chat.completions.create()`.
- **Immutable Files:** Never modify `chirality/normative_spec.txt` or `chirality/normative_system_prompt_Phase1.txt`.
- **Prompt Authoring:** As an AI, you must **NEVER** author or change the semantic content of the prompt assets.
- **Pure Transcripts:** Do not add any metadata to the conversational history that is sent to the LLM.
