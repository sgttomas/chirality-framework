# Contributing to the Chirality Framework

First, thank you for considering contributing! This project is a direct, canonical implementation of the Chirality Framework algorithm, and we welcome contributions that refine, test, and document this core implementation.

## Core Philosophy: Meta-Ontological Semantic Computation

The Chirality Framework is a meta-ontological, system-agnostic methodology that employs two distinct phases:
- **Phase 1**: Uses conversational prompting to build semantic understanding through dialogue
- **Phase 2**: Uses Phase 1 implementation as system prompt for modular tensor construction

Contributions should respect this two-phase architecture and focus on improving the correctness, clarity, and observability of the semantic computations, not on adding new framework features or abstractions.

## Getting Started

### Prerequisites
- Python 3.9+
- An OpenAI API key (set as the `OPENAI_API_KEY` environment variable for live tests)
- **Note**: The framework uses OpenAI's Responses API exclusively and requires OpenAI SDK >=1.50.0
- **Version**: Currently at v19.2.0 with production-ready infrastructure

### Development Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd chirality-framework

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies, including development tools
pip install -e ".[dev]"

# 4. Run the offline test suite to verify setup
pytest
```

## Architecture Guidelines

### Domain-Driven Design Structure

The codebase follows Domain-Driven Design (DDD) with clear separation of concerns:

- **`chirality/domain/`**: Core business logic and entities
- **`chirality/application/`**: Application services and use cases  
- **`chirality/infrastructure/`**: External integrations (LLM, export, monitoring)
- **`chirality/interfaces/`**: User interfaces (single CLI entry point)
- **`chirality/lib/`**: **RESTRICTED** - Contains `logging.py` only for production infrastructure

### Critical Architectural Rules

1. **No Legacy Code**: The framework maintains a strict no-legacy invariant
   - `chirality/core/` and legacy shims have been permanently deleted
   - Guard scripts prevent reintroduction of legacy patterns

2. **lib/ Directory Restriction**: 
   - **ONLY** `chirality/lib/logging.py` is permitted for CLI output channel separation
   - Any new utilities must go to the appropriate DDD layer (domain/application/infrastructure)
   - This carve-out exists solely for production logging infrastructure

3. **Single CLI Entry Point**: 
   - Only `chirality.interfaces.cli:main` via `pyproject.toml [project.scripts]`
   - No secondary CLI entry points or `--legacy` flags permitted

4. **Guard Scripts**: Run these locally before commits:
   ```bash
   python scripts/guard_no_legacy.py      # Prevents legacy code drift
   python scripts/check_kernel_hash.py    # Validates prompt asset integrity  
   python scripts/codemod_legacy_imports.py  # Checks for banned imports
   ```

5. **Semantic‑first pipeline**:
   - Phase‑1 Stage‑A prompts should emit markdown tables that match canonical labels/dimensions. Avoid heading lines that become stray keys. If row labels are present, they must be the canonical labels in a leftmost column; otherwise omit them.
   - Do not include JSON directives in Stage‑A prompts; the transcript must remain clean. The orchestrator strips “Output format → only JSON” sections when running with `--relaxed-json`.
   - Stage‑B normalization (strict JSON) happens out‑of‑band via the extractor. Don’t embed JSON tails in assets.

### Logging & Output Channels

- **Logs → stderr**: All progress, status, and diagnostic messages  
- **Data → stdout**: Only actual output data (for CI/CD pipeline consumption)
- Use `chirality.lib.logging` functions: `log_info()`, `log_error()`, `log_success()`, `output_data()`

## How to Contribute

The most valuable contributions will be those that improve the core algorithm, its tests, or its documentation. It is critical to understand the separation between the framework's mechanics (code) and its meaning (semantic assets).

### Semantic Contributions (The "Why")

The framework's semantic interpretation differs by phase:

**Phase 1**: Uses conversational dialogue history as system prompt
-   **Location**: `chirality/prompt_assets/` (conversation templates)
-   **Content**: Dialogue that builds semantic multiplication concepts through examples
-   **Critical**: The conversation IS the instruction - it creates semantic state

**Phase 2**: Uses complete Phase 1 implementation as system prompt
-   **Location**: `chirality/normative_implementation_*.txt`
-   **Content**: Full Phase 1 results become semantic foundation for tensor operations
-   **Critical**: Cell-by-cell computation without rolling context

**Contribution Process**: As these define canonical semantics, they are not open to direct modification via pull requests. Propose changes in GitHub Issues for maintainer discussion.

### Code Contributions (The "How")

Contributions to the code must respect the two-phase architecture:

**Domain-Driven Design Structure**:
*   **`chirality/domain/`**: Core business logic and entities
    *   `matrices/`: Matrix entities and canonical values
    *   `pipeline/`: Pipeline orchestration logic
    *   `semantics/`: Semantic resolution strategies
*   **`chirality/application/`**: Application services and use cases
*   **`chirality/infrastructure/`**: External integrations
    *   `llm/`: LLM client implementations (OpenAI Responses API)
    *   `prompts/`: Phase-specific prompt management
    *   `exporters/`: Neo4j, JSONL exporters

**Phase-Specific Components**:
*   **Phase 1**: Conversational prompt management with rolling context
*   **Phase 2**: Modular cell computation engine for tensors
*   **Semantic Cross Product**: New operation for hierarchical tensor generation

### Testing Contributions

Our testing strategy is crucial for validating the framework's correctness and architectural integrity.

#### Architectural Guardrails

This project uses a series of "guardrail" tests to programmatically enforce its core architectural principles. Before submitting any changes, you **must** run these tests to ensure your changes are compliant. These are more important than standard unit tests.

Key guardrail tests include:
- `tests/test_architecture_guards.py`: Checks for forbidden legacy code patterns and ensures the system prompt has not been altered.
- `tests/test_clean_transcript.py`: Scans dialogue transcripts to ensure no framework metadata (e.g., SHAs, sources, modes) is ever exposed to the LLM.

To run all critical guards:
```bash
pytest -v tests/test_architecture_guards.py tests/test_clean_transcript.py
```

#### Full Test Suite

*   **Mocking**: All core logic is tested against mock objects and a deterministic `echo` resolver. No new tests should make live network calls unless they are specifically designed for integration testing and use a dedicated, low-cost model.
*   **Adding Tests**: New tests for core domain logic should be added to the `tests/` directory with a clear and descriptive filename.

### Prompt Assets & Manifest

- Prompt files live under `chirality/infrastructure/prompts/assets/phase1/...`.
- Asset integrity is tracked by `infrastructure/prompts/assets/metadata.yml`.
- During active editing you may set `sha256: pending_user_authoring` and `size_bytes: null` for assets you’re changing to avoid hash churn; restore real hashes before releases.

### Running the Semantic‑first Flow

```bash
export OPENAI_API_KEY=...
export CHIRALITY_MODEL=gpt-5
export CHIRALITY_TEMPERATURE=1.0

python -m chirality.interfaces.cli phase1-dialogue-run \
  --lens-mode auto --relaxed-json --extract-structured --reasoning-effort low \
  --out runs/dev

# Stage‑A only through C (quick iteration)
python -m chirality.interfaces.cli phase1-dialogue-run \
  --lens-mode auto --relaxed-json --stop-at C_interpreted --extract-structured \
  --out runs/c_stageA

# Normalize saved relaxed output later
python -m chirality.interfaces.cli phase1-extract \
  --from runs/dev/phase1_relaxed_output.json \
  --out  runs/dev/phase1_structured.json
```

### Responses API Notes

- Use typed input parts (`type: "input_text"`).
- The adapter omits unsupported sampling params (like `top_p`) for reasoning‑capable models.

### Documentation Contributions

Clarity is essential. The two primary documents are:

*   **`README.md`**: The high-level project overview.
*   **`docs/ALGORITHM.md`**: The definitive technical description of the canonical algorithm and the 3-stage pipeline.

Improvements to these documents are highly welcome.

## Development Workflow

We follow a standard GitHub flow:

1.  Create a feature branch from `main` (e.g., `feature/refine-lensing-prompt`).
2.  Make your changes, including adding or updating tests.
3.  Ensure all tests pass (`pytest`).
4.  Update documentation if applicable.
5.  Submit a Pull Request to `main` with a clear description of your changes.

## Commit Message Convention

To maintain a clear and readable git history, this project follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. Each commit message should be prefixed with a type that describes the change.

**Common Types:**
*   **feat:** A new feature or enhancement to the calculator's capabilities.
*   **fix:** A bug fix in the algorithm or its implementation.
*   **docs:** Changes to documentation (`.md` files, docstrings).
*   **test:** Adding new tests or correcting existing ones.
*   **refactor:** A code change that neither fixes a bug nor adds a feature.
*   **style:** Changes that do not affect the meaning of the code (white-space, formatting, etc).
*   **chore:** Changes to the build process or auxiliary tools.

**Example:**
```
feat(operations): Add compute_matrix_X function

This commit implements the next stage of the semantic valley, computing
the verification matrix [X] from [K] and [J].
```
