# Repository Guidelines

## Project Structure & Module Organization
- Source: `chirality/` using DDD layers — `domain/`, `application/`, `infrastructure/`, `interfaces/`.
- CLI: `chirality/interfaces/cli.py` (entry `chirality` or `python -m chirality.interfaces.cli`).
- Tests: `tests/` (pytest discovers `test_*.py`).
- Scripts: `scripts/` for guard and maintenance utilities.
- Assets: `chirality/infrastructure/prompts/assets/` (managed; do not hand-edit manifest).
- Outputs: `artifacts/`, `runs/`, `snapshots/`, `traces/`.

## Build, Test, and Development Commands
- `make install`: Install dev deps (`.[dev]`).
- `make fmt`: Format with Black.
- `make lint`: Lint with Ruff.
- `make type`: Type check with mypy.
- `make guard`: Architectural + kernel hash checks.
- `make test`: Run pytest quickly (`-q`).
- `make all`: Run guard, fmt, lint, type, test.
- Example CLI: `chirality assets-verify` to build prompt asset manifest.

## Coding Style & Naming Conventions
- Python ≥3.9, 4‑space indentation, 100‑char line length (Black).
- Naming: `snake_case` functions/vars, `PascalCase` classes, `UPPER_SNAKE` constants.
- Imports respect DDD boundaries; place helpers in the correct layer (avoid new code in `lib/`).
- Tools: Black, Ruff, mypy (type hints preferred on public interfaces).

## Testing Guidelines
- Framework: pytest; tests live in `tests/` and are named `test_*.py`.
- Markers: use `@pytest.mark.slow`, `integration`, `neo4j` as appropriate.
- Quick run: `pytest -q -m "not slow"`.
- Aim for focused unit tests in `domain/` and `application/`; avoid network calls unless explicitly marked.

## Commit & Pull Request Guidelines
- Commit style: Conventional Commits (`feat:`, `fix:`, `refactor:`, `ci:`, `docs:`). Keep messages imperative and scoped.
- Before PR: run `make all` and ensure guard checks pass; include a clear description, linked issues, and sample CLI output or screenshots when relevant.
- PR scope: respect DDD boundaries; update docs/tests alongside code.

## Security & Configuration Tips
- Secrets via `.env` (see `.env.example`); never commit credentials.
- Optional extras: `pip install .[openai]` or `.[neo4j]` as needed.
- Asset integrity: use `chirality assets-verify` or `make checksums`; do not edit generated manifests by hand.
