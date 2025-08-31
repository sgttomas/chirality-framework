# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Chirality Framework is a "semantic calculator" that implements a fixed, canonical algorithm for structured problem-solving. It's NOT a general-purpose framework but a specific implementation of a three-stage interpretation pipeline that transforms mechanical combinations into meaningful semantic insights.

**Core Philosophy**: Fixed ontological structure + constrained stochastic processing = reproducible semantic computation.

## Development Commands

### Testing
```bash
# Run all tests (uses mock resolvers - fast, no API calls)
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/core/test_operations.py -v

# Run with coverage
pytest --cov=chirality

# Type checking (strict mode enabled)
mypy chirality/

# Code formatting
black chirality/ tests/
```

### CLI Development & Testing
```bash
# Basic cell computation (echo resolver - deterministic, no API calls)
python3 -m chirality.cli compute-cell C --i 0 --j 0 --verbose

# Live OpenAI testing (requires OPENAI_API_KEY env var)
python3 -m chirality.cli compute-cell C --i 0 --j 0 --resolver openai --verbose

# Different matrix types
python3 -m chirality.cli compute-cell F --i 1 --j 2 --verbose
python3 -m chirality.cli compute-cell D --i 2 --j 1 --verbose

# Full observability (tracing + Neo4j export)
python3 -m chirality.cli compute-cell C --i 0 --j 0 --trace --neo4j-export --verbose

# Framework info
python3 -m chirality.cli info
```

### Installation & Setup
```bash
# Development setup
pip install -e ".[dev]"

# Optional dependencies
pip install -e ".[openai]"    # For CellResolver
pip install -e ".[neo4j]"     # For working memory export
pip install -e ".[all]"       # All optional dependencies
```

## Architecture Overview

### Core Algorithm: Three-Stage Interpretation Pipeline
All matrix operations (C, F, D) follow the same universal pipeline:

1. **Stage 1 (Combinatorial)**: Mechanical generation of k-products or direct pairs
2. **Stage 2 (Semantic Resolution)**: LLM resolves word pairs into coherent concepts  
3. **Stage 3 (Universal Ontological Lensing)**: Column → Row → Final synthesis for ALL matrices

### Key Files & Their Roles

#### Core Implementation (`chirality/core/`)
- **`operations.py`**: The "secret sauce" - implements the 3-stage pipeline for all matrix types
  - `compute_cell_C()`: Matrix multiplication with k-products
  - `compute_cell_F()`: Element-wise multiplication  
  - `compute_cell_D()`: Synthesis using canonical formula
  - `_perform_three_step_lensing()`: Universal lensing for all matrices
- **`cell_resolver.py`**: Single LLM interface with 4 key methods returning `RichResult`
  - `resolve_semantic_pair()`: Stage 2 semantic multiplication
  - `apply_column_lens()`, `apply_row_lens()`, `synthesize_lensed_perspectives()`: Stage 3 lensing
- **`prompts.py`**: Single source of truth for all prompt construction
  - `build_stage2_prompt()`, `build_column_lensing_prompt()`, etc.
  - Centralized prompt fragments and canonical `SYSTEM_PROMPT`
- **`matrices.py`**: Fixed canonical matrices (A, B, J) - these are constants, not configurable
- **`types.py`**: Core data structures (`Cell`, `Matrix`, `RichResult`, `SemanticContext`)

#### Supporting Systems
- **`exporters/working_memory_exporter.py`**: Neo4j export with universal 5-stage schema
- **`tracer.py`**: JSONL tracing for complete observability
- **`validate.py`**: Validation for framework structural integrity

### Matrix Relationships
```
C = A * B    (3×4 = 3×4 dot 4×4, via k-products)
F = J ⊙ C    (3×4 = 3×4 element-wise)  
D = synthesis(A, F)  (3×4, canonical formula)
```

### Universal Provenance Schema
All cells use the same 5-stage provenance structure:
- `stage_1_construct`: Construction content (`texts` for lists, `text` for singles)
- `stage_2_semantic`: Resolved concepts (`texts` for C Stage 2, `text` for F/D)
- `stage_3_column_lensed`: Column lens interpretation (`text`)
- `stage_4_row_lensed`: Row lens interpretation (`text`)  
- `stage_5_final_synthesis`: Final integrated interpretation (`text`)

### Testing Strategy
- **`tests/mocks.py`**: `MockCellResolver` provides deterministic outputs without LLM calls
- **`tests/core/test_operations.py`**: Tests each stage independently + complete pipeline
- Use echo resolver for pipeline mechanics testing, OpenAI resolver for semantic validation

### Key Design Principles
1. **RichResult Objects**: All resolver methods return structured objects with `text`, `terms_used`, `warnings`, `metadata`
2. **Universal Lensing**: Same 3-step process (Column → Row → Final) for ALL matrices
3. **Canonical Problem**: Fixed to "generating reliable knowledge" for D matrix
4. **Single Atomic Transactions**: Neo4j export uses UNWIND for efficiency
5. **Deterministic Stage IDs**: Generated with timestamp hashing for instance distinction

### Critical Development Notes
- Always run tests after changes: `pytest`
- Use echo resolver for development/testing (fast, deterministic)
- OpenAI resolver requires `OPENAI_API_KEY` environment variable
- Prompt engineering happens in `prompts.py` using builder functions
- Neo4j export preserves both type distinctions (labels) and instance distinctions (unique IDs)
- Never modify canonical matrices (A, B, J) unless updating the fundamental specification

### Common Debugging Workflow
1. Test with echo resolver first to verify pipeline mechanics
2. Test with OpenAI resolver to verify semantic resolution
3. Use `--verbose` flag to see all stage outputs
4. Use `--trace` flag for detailed JSONL logs
5. Use `--neo4j-export` for graph analysis of semantic journeys