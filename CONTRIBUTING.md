# Contributing to the Chirality Framework

First, thank you for considering contributing! This project is a direct, canonical implementation of the Chirality Framework algorithm, and we welcome contributions that refine, test, and document this core implementation.

## Core Philosophy: The "Semantic Calculator"

Please understand that this project is not a general-purpose, extensible framework. It is a **"semantic calculator"** designed to execute a fixed algorithm. Contributions should focus on improving the correctness, clarity, and observability of this algorithm, not on adding new framework features, plugins, or abstractions.

## Getting Started

### Prerequisites
- Python 3.9+
- An OpenAI API key (set as the `OPENAI_API_KEY` environment variable for live tests)

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

## How to Contribute

The most valuable contributions will be those that improve the core algorithm, its tests, or its documentation. It is critical to understand the separation between the framework's mechanics (code) and its meaning (semantic assets).

### Semantic Contributions (The "Why")

The framework's reasoning, voice, and semantic interpretation are controlled exclusively by the maintainer through a series of version-controlled text files.

-   **Location**: `chirality/prompt_assets/`
-   **Content**: This directory contains the `system.md` prompt, the `station/*.md` briefs, and the `ops/**/*.md` operator and lensing templates.
-   **Contribution Process**: As these files define the canonical semantics of the framework, they are not open to direct modification via pull requests. Contributions to the semantics should be proposed in GitHub Issues for discussion with the maintainer.

### Code Contributions (The "How")

Contributions to the code that orchestrates the semantic pipeline are welcome. The new architecture is modular:

*   **`chirality/prompt_assets/metadata.yml`**: The manifest that registers all semantic assets and their checksums. The `PromptRegistry` uses this for validation.
*   **`chirality/lib/`**: The home of the new prompt assembly system.
    *   `prompt_registry.py`: Loads and validates the assets defined in the metadata file.
    *   `strategies.py`: Defines the canonical order of assets to be used for each stage of the pipeline.
    *   `prompt_builder.py`: Assembles the final prompt messages based on the strategy and substitutes the required placeholders.
*   **`chirality/core/llm_client.py`**: The exclusive wrapper for the OpenAI Responses API.
*   **`chirality/core/cell_resolver.py`**: The refactored resolver. Its role is to orchestrate the process, using the `PromptBuilder` to get messages and the `llm_client` to get a result. See its new, canonical API in `docs/API_REFERENCE.md`.
*   **`chirality/core/operations.py`**: The high-level orchestration layer. The `compute_cell_*` functions here define the steps of the canonical pipeline (e.g., Stage 2 multiplication followed by Stage 3 Combined Lensing).

### Testing Contributions

Our testing strategy is crucial for validating the calculator's correctness without making expensive LLM calls.

*   **Mocking**: All core logic is tested against mock objects and a deterministic `echo` resolver. No new tests should make live network calls.
*   **Adding Tests**: New tests for the core operations should be added to `tests/core/test_operations.py`. Tests for the prompt assembly system should go in `tests/lib/`.

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
