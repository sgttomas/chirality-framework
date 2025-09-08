# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Chirality Framework is a meta-ontological, system-agnostic methodology for mapping the solution space to a problem statement in the context of knowledge work. It creates structured semantic relationships that serve as "semantic anchors" to guide LLMs through problem-solving stages across a "semantic valley."

**Core Philosophy**: Fixed ontological structure + constrained stochastic processing = reproducible semantic computation.

**Current Status**: 
- Recently migrated to Domain-Driven Design (DDD) architecture
- Phase 1 complete: Matrices A through E implemented with conversational prompting
- Phase 2 ready for implementation: Tensors M, W, U, N with modular cell-by-cell construction
- Version 19.1.0 per normative specification

## Critical Architectural Insight: Two-Phase Prompting Strategy

The framework uses fundamentally different prompting strategies for Phase 1 and Phase 2:

### Phase 1: Conversational System Prompt
- **Strategy**: Uses a dialogue history as the system prompt to create semantic understanding
- **Key Elements**:
  - Builds semantic multiplication concept through examples ("sufficient" * "reason" = "justification")
  - Develops "developments" concept organically through multiple contexts
  - Establishes modal ontologies through iterative refinement
  - Creates a "semantic state" in the LLM that enables proper interpretation
- **Context Management**: Maintains rolling context through the entire matrix computation
- **Purpose**: Primes the LLM to understand semantic operations intuitively before formal application

### Phase 2: Normative Implementation as System Prompt
- **Strategy**: Uses the complete Phase 1 implementation (through Matrix E) as the system prompt
- **Key Elements**:
  - Provides full semantic context through completed Phase 1 matrices
  - Includes all semantic operation definitions and examples
  - Contains complete station progression and transformations
- **Context Management**: Cell-by-cell construction WITHOUT rolling context window
- **Purpose**: Enables modular tensor construction with each cell computed independently

This two-phase approach is essential because:
1. Phase 1 requires building semantic understanding from first principles
2. Phase 2 can leverage the completed Phase 1 as semantic foundation
3. Tensor hierarchies in Phase 2 are naturally modular, supporting isolated cell computation

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

# Linting
ruff check chirality/
```

### CLI Development & Testing
```bash
# Basic cell computation (echo resolver - deterministic, no API calls)
python3 -m chirality.cli compute-cell C --i 0 --j 0 --verbose

# Live OpenAI testing (requires OPENAI_API_KEY env var + SDK >=1.50.0)
python3 -m chirality.cli compute-cell C --i 0 --j 0 --resolver openai --verbose

# Full pipeline execution
python3 -m chirality.cli compute-pipeline --resolver openai --snapshot-jsonl --include-base

# Full observability (tracing + Neo4j export)
python3 -m chirality.cli compute-cell C --i 0 --j 0 --trace --neo4j-export --verbose

# App integration mode (manifest + cells-jsonl-v1 snapshots + final stdout JSON)
python3 -m chirality.cli compute-pipeline \
  --resolver echo \
  --out runs/dev-run-1 \
  --problem-file problem.json \
  --max-seconds 900

# Render viewer for results
python3 -m chirality.cli render-viewer --latest --open
```

### Installation
```bash
# Development setup
pip install -e ".[dev]"

# Optional dependencies
pip install -e ".[openai]"    # For OpenAI LLM resolver
pip install -e ".[neo4j]"     # For graph export
pip install -e ".[all]"       # All optional dependencies
```

## Architecture Overview

### DDD Structure (Post-Migration)
The codebase follows Domain-Driven Design with clear separation of concerns:

```
chirality/
├── domain/           # Core business logic and entities
│   ├── matrices/     # Matrix entities and operations
│   ├── pipeline/     # Pipeline orchestration
│   ├── semantics/    # Semantic resolution logic
│   └── types.py      # Core domain types
├── application/      # Application services
│   └── services/     # Use case implementations
├── infrastructure/   # External integrations
│   ├── llm/         # LLM provider implementations
│   ├── prompts/     # Prompt management
│   ├── exporters/   # Neo4j, JSONL exporters
│   └── monitoring/  # Tracing and observability
├── core/            # Legacy core (being refactored)
└── lib/             # Shared libraries
```

## Semantic Operations

### Core Operations (Phase 1)
1. **Semantic Multiplication (*)**: Combines word meanings into coherent intersection
   - Example: "sufficient" * "reason" = "justification"
2. **Semantic Addition (+)**: Concatenates words/fragments into statements
   - Example: "faisal" + "has" + "seven" + "balloons" = "faisal has seven balloons"
3. **Semantic Dot Product (·)**: Matrix multiplication using semantic operations
4. **Element-wise Product (⊙)**: Pairwise semantic multiplication
5. **Semantic Shift (→)**: Station context transformation

### New Operations (Phase 2)
1. **Semantic Cross Product (×)**: Creates hierarchical semantic tensors
   - Generates nested hierarchies rather than combining perspectives
   - Used for tensors M, W, U, N
   - Enables modular cell-by-cell computation

### Order of Operations
1. Apply semantic multiplication first
2. Then semantic addition

## The Semantic Valley

The framework follows a logical progression of 10 stations:

### Phase 1 (Implemented with Conversational Prompting)
1. **Problem Statement**: [A] · [B] = [C]
2. **Requirements**: [C] ⊙ [J] = [F]
3. **Objectives**: [A] + [F] = [D]
4. **Verification**: [K] · [J] = [X]
5. **Validation**: [X] → [Z]
6. **Evaluation**: [G] · [T] = [E]

### Phase 2 (To Implement with Modular Construction)
7. **Assessment**: [R] × [E] = [M]
8. **Implementation**: [M] × [X] = [W]
9. **Reflection**: [W] × [P] = [U]
10. **Resolution**: [U] × [H] = [N]

## Matrix/Tensor Specifications

### Phase 1 Matrices (Conversational Context)

#### Canonical Matrices (Axiomatic)
- **[A]** (3×4): Problem space modalities (normative/operative/iterative × guiding/applying/judging/reflecting)
- **[B]** (4×4): Epistemic levels (data/information/knowledge/wisdom × necessity/sufficiency/completeness/consistency)
- **[J]** (3×4): Truncated [B] without wisdom row

#### Derived Matrices
- **[C]** (3×4): [A] · [B] - Problem statement synthesis
- **[F]** (3×4): [C] ⊙ [J] - Requirements specification
- **[D]** (3×4): [A] + [F] - Objectives formulation
- **[K]** (4×3): transpose([D]) - Reoriented objectives
- **[X]** (4×4): [K] · [J] - Verification matrix
- **[Z]** (4×4): [X] → shift - Validation transformation
- **[G]** (3×4): [Z][0:3, :] - First 3 rows of Z
- **[P]** (1×4): [Z][3, :] - Fourth row of Z (Reflecting)
- **[T]** (4×3): transpose([J]) - Reoriented epistemic levels
- **[E]** (3×3): [G] · [T] - Evaluation matrix
- **[H]** (1×1): [P][0, 3] - Consistency/Reflecting element

### Phase 2 Tensors (Modular Cell Construction)

#### New Axiomatic Component
- **[R]** (1×9): Topics for generating valid knowledge
  - Elements: Problem Statement, Requirements, Objectives, Methodology, Analysis, Evaluation, Assessment, Implementation, Integration

#### Semantic Tensors (Hierarchical)
- **[M]** (9×3×3): [R] × [E] - Assessment tensor
  - Hierarchy: Topics → [Data/Information/Knowledge] → [Guiding/Applying/Judging]
- **[W]** (9×3×3×4×4): [M] × [X] - Implementation tensor
  - Adds: [Necessity/Sufficiency/Completeness/Consistency] → [Guiding/Applying/Judging/Reflecting]
- **[U]** (9×3×3×4×4×4): [W] × [P] - Reflection tensor
  - Adds: [Necessity/Sufficiency/Completeness/Consistency] from P
- **[N]** (9×3×3×4×4×4×1): [U] × [H] - Resolution tensor
  - Final synthesis through Consistency/Reflecting lens

## Implementation Pipeline Architecture

### Phase 1: Three-Stage Pipeline with Rolling Context
All matrix operations follow this universal pipeline:

1. **Stage 1 (Combinatorial)**: Mechanical generation of k-products or direct pairs
2. **Stage 2 (Semantic Resolution)**: LLM resolves concepts via operation-specific strategies
3. **Stage 3 (Combined Lensing)**: Unified semantic operation combining row × column × station perspectives

**Context Management**: Maintains full conversation history through all stages

**Special Cases**:
- **Matrix Z**: Uses lean 2-stage pipeline with station shift instead of lensing
- **Matrix D**: Stage 2 uses mechanical addition (no LLM call)

### Phase 2: Modular Cell-by-Cell Construction
Tensor operations use a different approach:

1. **System Prompt Setup**: Load complete Phase 1 implementation as context
2. **Hierarchical Decomposition**: Break tensor into individual cells
3. **Independent Cell Computation**: Each cell computed without rolling context
4. **Tensor Assembly**: Combine cells into complete tensor structure

**Context Management**: Each cell computation is stateless beyond system prompt

## CRITICAL SEMANTIC RULES

1. **The normative spec (`chirality/normative_spec.txt`) is canonical and immutable**. AI must NEVER modify it, only notify the user of suggested changes.
2. **All prompts are part of the normative spec** - NEVER write or generate semantic prompts. Only the user writes semantic content.
3. **Station briefs provide station-specific context** - these must be user-authored, not AI-generated.
4. **Semantic meaning belongs to the human operator** - AI can only assist with code structure, not semantic decisions.
5. **Phase 1 and Phase 2 are clearly delineated** - different prompting strategies, different context management.
6. **Conversational prompts (Phase 1) build semantic state** - the dialogue IS the instruction.
7. **Normative implementation (Phase 2) provides semantic foundation** - completed Phase 1 becomes the context.

## CRITICAL OpenAI API Requirements

**MANDATORY**: The framework uses OpenAI's **Responses API** exclusively.
- **NEVER USE**: `client.chat.completions.create(messages=[...])` - FORBIDDEN
- **ALWAYS USE**: `client.responses.create(input=..., ...)` - REQUIRED
- **CRITICAL**: Use `input` parameter, NOT `prompt` parameter
- **SDK VERSION**: Requires OpenAI SDK >=1.50.0
- The framework requires direct prompt control without message role abstractions
- ANY use of Chat Completions API must be immediately fixed

## Key Files & Locations

### Domain Layer (`chirality/domain/`)
- **`matrices/`**: Matrix entities and canonical values (A, B, J)
- **`pipeline/`**: Pipeline orchestration logic
- **`semantics/`**: Semantic resolution strategies
- **`types.py`**: Core domain types (Cell, Matrix, RichResult)
- **`validation.py`**: Framework structural integrity checks
- **`stations.py`**: Station definitions and contexts

### Infrastructure Layer (`chirality/infrastructure/`)
- **`llm/`**: LLM client implementations (OpenAI Responses API)
- **`prompts/`**: Prompt registry and builder
  - Phase 1: Conversational prompt management
  - Phase 2: Normative implementation loader
- **`exporters/`**: Neo4j graph export, JSONL tracing
- **`monitoring/`**: Observability and tracing

### Application Layer (`chirality/application/`)
- **`services/`**: Application service implementations

### Legacy Core (`chirality/core/`)
- Being refactored as part of DDD migration
- **`operations.py`**: Current 3-stage pipeline implementation
- **`cell_resolver.py`**: LLM interface with combined operations

### Prompt Assets (`chirality/prompt_assets/`)
- Maintainer-authored markdown files
- NEVER modify these programmatically
- Only user should edit semantic content
- Phase 1: Conversational dialogue templates
- Phase 2: Normative implementation snapshots

### Normative Specifications (`chirality/`)
- **`normative_spec.txt`**: v19.1.0 canonical specification with Phase 2 instructions
- **`normative_system_prompt.txt`**: System prompt for LLM operations
- **`normative_implementation_chirality-framework_v*.txt`**: Implementation snapshots
  - These become system prompts for Phase 2

## Provenance Schema

### Phase 1 (3-stage provenance with context)
All cells maintain conversation history:
- `stage_1_construct`: Mechanical construction
- `stage_2_semantic`: Semantic resolution result
- `stage_3_combined_lensed`: Combined lensing interpretation
- `conversation_context`: Full dialogue history

### Phase 2 (Hierarchical provenance without context)
Tensors use modular provenance:
- `hierarchical_path`: Location in tensor structure
- `semantic_operation`: Cross-product transformation applied
- `source_elements`: Input matrix/tensor elements
- `resolved_value`: Final semantic result
- No conversation context (stateless beyond system prompt)

## Development Guidelines

### Phase 1 Implementation
1. **Conversational Prompt Design**:
   - Start with semantic examples to build understanding
   - Develop key concepts through dialogue
   - Ground matrices in established semantic context
   
2. **Context Management**:
   - Maintain full conversation history
   - Each operation builds on previous understanding
   - Rolling context window through entire pipeline

3. **Testing Strategy**:
   - Verify semantic coherence across conversation
   - Test with different conversational variations
   - Ensure consistent semantic resolution

### Phase 2 Implementation
1. **System Prompt Preparation**:
   - Load complete Phase 1 implementation
   - Include all matrix definitions and transformations
   - Provide full semantic operation examples

2. **Modular Construction**:
   - Decompose tensors into individual cells
   - Compute each cell independently
   - No inter-cell context dependencies

3. **Testing Strategy**:
   - Verify cell-level semantic accuracy
   - Test tensor assembly procedures
   - Ensure hierarchical structure preservation

### General Guidelines
1. **Testing**:
   - Use echo resolver for mechanics testing
   - Use OpenAI resolver for semantic validation
   - Run `pytest` after all changes

2. **Debugging**:
   - Phase 1: Examine conversation flow
   - Phase 2: Check individual cell computations
   - Use `--trace` for detailed logs

3. **Critical Notes**:
   - OpenAI resolver requires `OPENAI_API_KEY`
   - Prompt assets are maintainer-only
   - Canonical matrices never change
   - Phase separation is absolute

## Phase 2 Implementation Roadmap

### Step 1: System Prompt Infrastructure
- Create loader for Phase 1 implementation as system prompt
- Implement prompt template for Phase 2 operations
- Ensure proper semantic context transfer

### Step 2: Cell Computation Engine
- Build modular cell calculator
- Implement hierarchical path tracking
- Create cell-level semantic resolver

### Step 3: Array R Implementation
- Define topics for valid knowledge generation
- Create domain entity for Array R

### Step 4: Semantic Cross Product
- Implement operation in `domain/semantics/`
- Support hierarchical tensor generation
- Maintain nested structure preservation

### Step 5: Tensor M (Assessment)
- Implement [R] × [E] = [M]
- 9×3×3 tensor structure
- Cell-by-cell construction

### Step 6: Tensor W (Implementation)
- Implement [M] × [X] = [W]
- 9×3×3×4×4 tensor structure
- Extended hierarchical nesting

### Step 7: Tensor U (Reflection)
- Implement [W] × [P] = [U]
- 9×3×3×4×4×4 tensor structure
- Reflection through validity parameters

### Step 8: Tensor N (Resolution)
- Implement [U] × [H] = [N]
- 9×3×3×4×4×4×1 tensor structure
- Final synthesis

### Step 9: Integration
- Unify Phase 1 and Phase 2 pipelines
- Extend CLI for tensor operations
- Update exporters for tensor visualization

**Critical**: Maintain strict separation between Phase 1 (conversational) and Phase 2 (modular) approaches. Each phase has its own prompting strategy, context management, and computational architecture.