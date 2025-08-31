# Chirality Framework: A Semantic Calculator

**Version: See VERSION.md** | **Status: Refactored to Canonical Algorithm**

The Chirality Framework is a direct, simple, and observable implementation of a fixed, canonical algorithm for structured problem-solving. It is not a general-purpose framework but a "semantic calculator" designed to execute a specific sequence of semantic transformations.

The value of this project is in the unique, insightful **output** of the calculation, not in the flexibility of the code.

## Core Concept: The Three-Stage Interpretation Pipeline

The heart of the Chirality Framework is a three-stage process that generates deep meaning from fixed inputs:

1.  **Stage 1 (Combinatorial):** Mechanical combination of terms.
2.  **Stage 2 (Semantic Resolution):** An LLM resolves the raw terms into meaningful concepts.
3.  **Stage 3 (Ontological Lensing):** Universal three-step lensing applied to all matrices: Column → Row → Final Synthesis.

For a complete technical description of this process, see the **[Canonical Algorithm Documentation](docs/ALGORITHM.md)**.

## Quick Start: Using the CLI

The primary way to interact with the calculator is via the command-line interface. The most common command is `compute-cell`, which allows you to observe the 3-stage pipeline for any cell in a matrix.

### Prerequisites
- Python 3.8+
- An OpenAI API key set as the `OPENAI_API_KEY` environment variable.

### Examples: Computing cells through the 3-stage pipeline

```bash
# Navigate to the project root
cd /path/to/chirality-framework

# Compute cell C[0,0] with verbose output (shows all 3 stages)
python3 -m chirality.cli compute-cell C --i 0 --j 0 --verbose

# Compute with OpenAI resolver (requires API key)
python3 -m chirality.cli compute-cell C --i 0 --j 0 --resolver openai --verbose

# Compute different matrix types
python3 -m chirality.cli compute-cell F --i 1 --j 2 --verbose
python3 -m chirality.cli compute-cell D --i 2 --j 1 --verbose

# Enable tracing for full observability
python3 -m chirality.cli compute-cell C --i 0 --j 0 --trace --verbose

# Optional: export to Neo4j with a unique run/session id
python3 -m chirality.cli compute-cell C --i 0 --j 0 --neo4j-export --verbose

# Get help and information
python3 -m chirality.cli --help
python3 -m chirality.cli info
```

This will display the output of all three stages (including Column → Row → Final lensing) for the specified cell. When Neo4j export is enabled, the CLI prints a unique run_id and the exporter writes a full, metadata-rich graph for analysis.

## Development

To set up the development environment and run tests, please refer to the instructions in `CONTRIBUTING.md`.
