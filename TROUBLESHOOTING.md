# Troubleshooting Production Runs (Phase‑1 / Responses API)

This document captures what we changed, why, and how to triage failures when running a Phase‑1 production smoke using the OpenAI Responses API with structured outputs.

## Summary

- Phase‑1 runs semantic‑first (markdown) and normalizes out‑of‑band to strict JSON.
- The adapter uses typed message parts and enforces JSON only for JSON‑expecting calls.
- Local validation + one retry ensures strict compliance; a deterministic table parser reduces model use.

## Environment & Secrets

- The API key is loaded from `.env` (root):
  - CLI (`chirality/interfaces/cli.py`) calls `load_dotenv()` at startup.
  - Adapter (`LLMClient.__init__`) also calls `load_dotenv()` before reading `OPENAI_API_KEY`.
- Verify loaded key:
  - `python - <<'PY' ... get_client() ... PY` prints “Client initialized. Key present: True”.

## Adapter Architecture (openai_adapter.py)

- Canonical path: `client.responses.create(**api_params)` with:
  - `instructions`: system text.
  - `input`: typed message parts array.
  - `text`: structured outputs config (see below).
- Fallback path: Minimal raw POST to `/v1/responses` only when the SDK rejects parameters (e.g., `TypeError('...response_format...')`).
  - Uses `httpx` if present; else stdlib `urllib`.
  - Timeouts: connect 10s, read 60s, write 10s (and pool 10s when using httpx).
  - One retry on 5xx with small jitter; 4xx fails fast.
- Output extraction: prefer `resp.output_text`; fallback to envelope content extraction.
- Usage normalization: robust extraction of token counts (input/output/total/cached).

## Structured Outputs & Validation

- JSON is enabled via `json_object` for JSON‑expecting calls; semantic stages run free‑form.
- Strict validation happens locally after parsing; on failure the extractor retries once with a compact diff‑driven note.
- A deterministic GitHub‑table parser bypasses the model when markdown tables match canonical labels and dimensions.

## Typed Messages & Content Types

- Input uses typed parts: `[{"role":"user","content":[{"type":"input_text","text": "..."}]}]`.
  - Server rejected `{type:"text"}` with: “Invalid value: 'text'. Supported values include 'input_text' ...”. We fixed this by switching to `input_text`.

## Phase‑1 Orchestration Changes (dialogue_run.py)

- For each stage and for auto lenses:
  - We call `get_strict_response_format(matrix, step)` from `json_schema_converter` as the single source of truth.
  - We map this to the `text` configuration for SDK calls (json_object for basic; json_schema planned, see issue above).
  - Prompt “JSON tails” remain as guidance only; server enforcement is via `text`.
- Transcript is system in `instructions`; conversation turns in `input` (typed parts).

## Tests & Guards Added

- New tests:
  - `tests/test_adapter_fallback_minimal.py`: verifies SDK path, triggers fallback, and parses fallback output.
  - Modified tests to assert the `text` config (not `response_format`).
- Guards updated:
  - `guard_llm_call` allow‑list now includes `text`.
  - Self‑policing rejects Chat Completions params.

## Common Errors & Fixes

1) SDK signature/param errors
- `Responses.create() got an unexpected keyword argument 'response_format'`.
  - Resolution: moved to `text.format` path; retained minimal fallback.

2) httpx Timeout construction
- `httpx.Timeout must either include a default, or set all four parameters explicitly.`
  - Resolution: provided connect/read/write/pool fields.

3) Content type in `input.content` parts
- 400: `Invalid value: 'text'. Supported values are: 'input_text', ...`.
  - Resolution: switched to `{type: "input_text", text: "..."}`.

4) Reasoning models reject `top_p`
- Error: 400 `Unsupported parameter: 'top_p' ...`
  - Fix: the adapter omits `top_p` automatically for reasoning‑capable models (e.g., GPT‑5). Ensure you’re on the updated code.

## Current Status

- `.env` is now loaded automatically.
- Adapter and orchestration use typed messages and `text.format` for JSON.
- Raw POST fallback maps strict JSON requests to the new `text` configuration.
- Phase‑1 smoke is still blocked on server support for schema key naming under `text`. JSON object mode should work; schema enforcement will be in‑process for now.

## Handy Commands

Run semantic‑first and extract immediately:

```bash
export OPENAI_API_KEY=... \
export CHIRALITY_MODEL=gpt-5 \
export CHIRALITY_TEMPERATURE=1.0

python -m chirality.interfaces.cli phase1-dialogue-run \
  --lens-mode auto --relaxed-json --extract-structured --reasoning-effort low \
  --out runs/phase1_latest
```

Normalize a saved relaxed run later:

```bash
python -m chirality.interfaces.cli phase1-extract \
  --from runs/phase1_latest/phase1_relaxed_output.json \
  --out  runs/phase1_latest/phase1_structured.json \
  --matrices-only
```

## How to Run a Smoke

- Ensure `.env` has `OPENAI_API_KEY`.
- Command:
  - `python -m chirality.interfaces.cli phase1-dialogue-run --lens-mode auto --out runs/phase1_smoke_$(date +%Y%m%d_%H%M%S)`
- On failure, capture:
  - HTTP status, error.message, error.param, and the first ~2KB of the body (our adapter logs this in the `raw` field of the error raised by orchestrator).

## Triage Checklist

- Verify key loaded (print presence; never log secrets).
- Verify `input` shape uses typed parts with `{type:"input_text"}`.
- Verify `text.format` is set to `json_object`.
- If using schema, try both `text.schema` and `text.json_schema` (we saw both 400 here), and confirm your environment’s required key by referencing the docs version for your SDK.
- If 4xx persists, inspect the raw request sent in fallback (ensure only documented fields: model, instructions, input, text, seed/metadata/store if used).
- Try a minimal one‑shot cURL with only `text.format=json_object`.

## Open Questions

- What is the canonical schema parameter name under `text` for this server/SDK version?
- Is server‑side schema validation gated by model/endpoint version here?
- Should we pin a specific SDK version to align with the documented `text` shape for JSON Schema?

## Safe Toggles

- `expects_json=True`: forces `text.format=json_object` when no other `text` provided.
- In‑process strict validation: still applied after parsing to maintain correctness.
- Fallback: only on SDK parameter rejection; does not change semantics, just HTTP transport.

---

If you want, we can flip Phase‑1 to `json_object` for a successful smoke now, and keep strict post‑validation enabled, while we verify the schema parameter naming with your target environment.
