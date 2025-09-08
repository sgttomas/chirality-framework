# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Chirality Framework is a meta-ontological, system-agnostic methodology for mapping the solution space to a problem statement in the context of knowledge work. It creates structured semantic relationships that serve as "semantic anchors" to guide LLMs through problem-solving stages across a "semantic valley."

**Core Philosophy**: Fixed ontological structure + constrained stochastic processing = reproducible semantic computation.

**Current Status**: 
- **REFACTOR-3 BRANCH**: Complete legacy code obliteration completed
- Fully migrated to Domain-Driven Design (DDD) architecture
- Phase 1 complete: Matrices A through E implemented with conversational prompting
- Phase 2 ready for implementation: Tensors M, W, U, N with modular cell-by-cell construction
- **Version 19.2.0: Production-ready infrastructure** with budgets, caching, and resume capabilities
- Enterprise-grade reliability, cost control, and crash-safe operations
- **CI/CD Pipeline**: Guards-first approach with fail-fast architectural protection

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

# Type checking (non-strict mode during refactoring)
mypy chirality/

# Code formatting  
black chirality/ tests/ scripts/

# Linting
ruff check chirality/

# Fix linting issues automatically
ruff check chirality/ --fix
```

### CLI Development & Testing
```bash
# Production-ready Phase 2 computation with budgets and resume
python3 -m chirality.interfaces.cli phase2-run \
  --tensor-spec tensors.json \
  --snapshot phase1_snapshot.md \
  --out production-run \
  --token-budget 100000 \
  --cost-budget 25.0 \
  --time-budget 3600 \
  --resume \
  --cache \
  --parallel 4

# Phase 1 dialogue with budget tracking
python3 -m chirality.interfaces.cli phase1-dialogue-run \
  --out artifacts/ \
  --token-budget 50000 \
  --cost-budget 10.0 \
  --time-budget 1800

# Generate Phase 1 snapshot for Phase 2
python3 -m chirality.interfaces.cli phase1-snapshot \
  --from artifacts/phase1_dialogue.jsonl \
  --out artifacts/phase1_snapshot.md

# Build lens catalog for tensor computation
python3 -m chirality.interfaces.cli lenses-derive \
  --phase1 artifacts/phase1_output.json \
  --spec chirality/normative_spec.txt \
  --out artifacts/lenses_triples.json

python3 -m chirality.interfaces.cli lenses-build \
  --triples artifacts/lenses_triples.json \
  --out artifacts/lens_catalog.jsonl

# Export results to Neo4j
python3 -m chirality.interfaces.cli export-neo4j \
  --artifacts production-run \
  --uri bolt://localhost:7687 \
  --user neo4j \
  --pwd password

# Get current kernel hash for versioning
python3 -m chirality.interfaces.cli assets-hash

# Verify prompt assets integrity
python3 -m chirality.interfaces.cli assets-verify
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
├── interfaces/      # CLI and user interfaces (single entry point)
└── lib/             # RESTRICTED - Contains only logging.py for production infrastructure
```

## REFACTOR-3 OBLITERATION COMPLETE ✅

### Legacy Code Elimination
The refactor-3 branch has completed the **"obliteration"** phase, permanently removing all legacy code:

- **🗂️ Deleted**: `chirality/core/**` (entire legacy directory structure)
- **🗂️ Deleted**: All `*_shim.py` compatibility files 
- **🗂️ Deleted**: `chirality/application/services/pipeline_service.py`
- **🗂️ Deleted**: Secondary CLI entry point (`chirality/cli.py`)
- **🗂️ Cleaned**: `chirality/lib/` now contains ONLY `logging.py` for production infrastructure
- **🗂️ Removed**: All `__pycache__/` directories from version control

### Architectural Enforcement
- **Guard Scripts**: Prevent reintroduction of legacy patterns with fail-fast CI checks
- **Single CLI**: Only `chirality.interfaces.cli:main` entry point via `pyproject.toml`
- **No-Legacy Invariant**: Strict architectural rules enforced at commit time

### CI/CD Pipeline Enhancement
- **Guards-First Approach**: Architectural validation before any code quality checks
- **Asset Manifest Generation**: Automatic prompt asset verification in CI
- **Dependency Management**: Fixed missing dependencies (`pydantic>=2.0.0`, `ruff>=0.4.0`)
- **Output Channel Separation**: Logs → stderr, data → stdout for automation
- **Non-Strict Type Checking**: Relaxed mypy during refactoring phase

## Production Infrastructure (v19.2.0)

The framework now includes enterprise-grade production capabilities:

### Budget Management (`chirality/domain/budgets.py`)
- **Centralized Cost Control**: Single source of truth for pricing across all models
- **Multi-dimensional Budgets**: Token, cost, and time limits with real-time tracking
- **Budget Enforcement**: Automatic operation termination when limits exceeded
- **Detailed Reporting**: Comprehensive budget status with utilization metrics

### Caching System (`chirality/infrastructure/caching.py`)
- **Two-Layer Architecture**: In-memory + persistent disk caching
- **Deterministic Cache Keys**: Include all parameters affecting computation results
- **Automatic Invalidation**: Cache invalidates when dependencies change (operands, snapshot, kernel, lens catalog, model params)
- **Collision Resistance**: Robust SHA256-based key generation prevents false cache hits
- **Thread Safety**: Safe for concurrent tensor computation

### Resume Operations (`chirality/infrastructure/caching.py`)
- **Atomic File Writes**: Crash-safe operations using `tempfile + os.replace`
- **Corruption Recovery**: Automatic detection and cleanup of corrupted files
- **Centralized Path Management**: Canonical `compute_cell_path()` ensures consistency
- **Progress Tracking**: Detailed manifest with per-tensor completion status
- **Graceful Degradation**: Resume failures don't break computation

### CLI Output Management (`chirality/lib/logging.py`)
- **Channel Separation**: Logs → stderr, data → stdout for CI/CD integration
- **Consistent Formatting**: Emoji prefixes for different message types (🔄 ✅ ❌)
- **Clean Integration**: Suitable for automation and pipeline consumption
- **Structured Logging**: Statistics and progress tracking with proper formatting

### Normalized LLM Integration (`chirality/infrastructure/llm/openai_adapter.py`)
- **Robust Usage Fields**: Handles various OpenAI response structures with fallbacks
- **GPT-5 Support**: Full parameter support (verbosity, reasoning_effort, max_tokens)
- **Consistent Field Naming**: Always provides prompt_tokens, completion_tokens, cached_tokens, total_tokens
- **Error Handling**: Graceful degradation for malformed API responses

### Production Features
✅ **Crash-Safe Operations**: All file writes are atomic
✅ **Deterministic Caching**: Stable cache keys eliminate unnecessary computation
✅ **Accurate Cost Control**: Real-time budget tracking with centralized pricing
✅ **Clean CI/CD Integration**: Proper stdout/stderr separation
✅ **Comprehensive Error Recovery**: Graceful handling of corruption and failures
✅ **Thread-Safe Concurrency**: Support for parallel tensor computation

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

**Production Integration** (`chirality/infrastructure/llm/openai_adapter.py`):
- ✅ **Normalized Usage Fields**: Robust extraction with fallbacks for different response structures
- ✅ **GPT-5 Support**: Full parameter support (verbosity, reasoning_effort, max_tokens)
- ✅ **Budget Integration**: Provides consistent token counts for cost calculation
- ✅ **Error Handling**: Graceful degradation for malformed API responses
- ✅ **Cached Token Support**: Proper handling of cached input token pricing

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

### Interfaces Layer (`chirality/interfaces/`)
- **`cli.py`**: Single CLI entry point for all framework operations
- **IMPORTANT**: This is the ONLY CLI entry point - no secondary CLIs permitted

### Prompt Assets (`chirality/prompt_assets/`)
- Maintainer-authored markdown files
- NEVER modify these programmatically
- Only user should edit semantic content
- Phase 1: Conversational dialogue templates
- Phase 2: Normative implementation snapshots

### Normative Specifications (`chirality/`)
- **`normative_spec.txt`**: v19.2.0 canonical specification with Phase 2 instructions
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

### POST-OBLITERATION DEVELOPMENT GUIDELINES

**CRITICAL RULES FOR REFACTOR-3 BRANCH:**

#### 1. **No-Legacy Invariant (ABSOLUTE)**
- **NEVER** create code in `chirality/core/` - this directory must not exist
- **NEVER** create `*_shim.py` compatibility files
- **NEVER** import from `chirality.lib.*` except `chirality.lib.logging`
- **NEVER** create secondary CLI entry points beyond `chirality.interfaces.cli:main`

#### 2. **lib/ Directory Restrictions**
- **ONLY** `chirality/lib/logging.py` is permitted for production infrastructure
- **ALL** new utilities must go to appropriate DDD layers:
  - Domain utilities → `chirality/domain/`
  - Application utilities → `chirality/application/`
  - Infrastructure utilities → `chirality/infrastructure/`

#### 3. **CLI Development**
- **Single Entry Point**: Always use `chirality.interfaces.cli:main`
- **Commands**: Use `python3 -m chirality.interfaces.cli <command>`
- **Never** use `python3 -m chirality.cli` (deleted)
- **Output Channels**: Logs to stderr, data to stdout

#### 4. **Pre-Commit Guards (MANDATORY)**
Run these before EVERY commit:
```bash
python scripts/guard_no_legacy.py      # Architectural enforcement
python scripts/check_kernel_hash.py    # Asset integrity 
python scripts/codemod_legacy_imports.py  # Import validation
```

#### 5. **CI/CD Integration**
- Guards run FIRST in CI pipeline (fail-fast)
- Asset manifest generated automatically
- All dependencies properly declared in `pyproject.toml`
- Type checking in non-strict mode during refactoring

### General Guidelines
1. **Testing**:
   - Use echo resolver for mechanics testing
   - Use OpenAI resolver for semantic validation
   - Run `pytest` after all changes
   - **Production Test Coverage**: 51+ comprehensive tests covering cache invalidation, resume robustness, budget tracking, CLI output channels

2. **Production Testing Areas**:
   - **Cache Invalidation** (`tests/test_cache_invalidation.py`): Dependency change scenarios
   - **Resume Robustness** (`tests/test_resume_robustness.py`): Atomic writes, corruption recovery
   - **Budget Tracking** (`tests/test_budgets.py`): Cost calculation, limit enforcement
   - **Adapter Normalization** (`tests/test_adapter_usage_fields.py`): OpenAI response handling
   - **CLI Output Separation** (`tests/test_cli_output_channels.py`): stderr/stdout validation
   - **Pricing Accuracy** (`tests/test_pricing_table.py`): Model rates, cost calculations

3. **Debugging**:
   - Phase 1: Examine conversation flow
   - Phase 2: Check individual cell computations
   - Use `--trace` for detailed logs
   - **Production Debugging**: Check budget status, cache statistics, resume manifests

4. **Critical Notes**:
   - OpenAI resolver requires `OPENAI_API_KEY`
   - Prompt assets are maintainer-only
   - Canonical matrices never change
   - Phase separation is absolute
   - **Production Requirements**: All file operations are atomic, cache keys include all dependencies

## Phase 2 Implementation Roadmap

### ✅ **COMPLETED: Production Infrastructure (v19.2.0)**
- ✅ **System Prompt Infrastructure**: TensorEngine with Phase 1 snapshot loading
- ✅ **Cell Computation Engine**: Modular cell calculator with hierarchical tracking  
- ✅ **Budget & Cost Control**: Centralized pricing with multi-dimensional budgets
- ✅ **Caching System**: Two-layer caching with deterministic invalidation
- ✅ **Resume Operations**: Atomic file writes with corruption recovery
- ✅ **CLI Integration**: Production-ready CLI with proper output separation
- ✅ **Quality Assurance**: 51+ comprehensive tests with 100% pass rate

### **READY FOR IMPLEMENTATION: Semantic Tensor Operations**

### Step 1: Array R Implementation
- Define topics for valid knowledge generation in TensorEngine
- Create domain entity for Array R in `domain/matrices/`
- Update tensor specifications with R integration

### Step 2: Semantic Cross Product Operation
- Implement `semantic_cross_product` in `domain/semantics/`
- Support hierarchical tensor generation
- Maintain nested structure preservation in TensorEngine

### Step 3: Tensor M (Assessment) - [R] × [E] = [M]
- Implement 9×3×3 tensor structure
- Cell-by-cell construction using production infrastructure
- Topics → [Data/Information/Knowledge] → [Guiding/Applying/Judging]

### Step 4: Tensor W (Implementation) - [M] × [X] = [W] 
- Implement 9×3×3×4×4 tensor structure
- Extended hierarchical nesting
- Adds [Necessity/Sufficiency/Completeness/Consistency] → [Guiding/Applying/Judging/Reflecting]

### Step 5: Tensor U (Reflection) - [W] × [P] = [U]
- Implement 9×3×3×4×4×4 tensor structure
- Reflection through validity parameters
- Adds [Necessity/Sufficiency/Completeness/Consistency] from P

### Step 6: Tensor N (Resolution) - [U] × [H] = [N]
- Implement 9×3×3×4×4×4×1 tensor structure
- Final synthesis through Consistency/Reflecting lens

### Step 7: Semantic Pipeline Integration
- Integrate tensor operations with existing Phase 1 pipeline
- Update exporters for tensor visualization in Neo4j
- Extend CLI with tensor-specific operations

**Critical**: Maintain strict separation between Phase 1 (conversational) and Phase 2 (modular) approaches. Each phase has its own prompting strategy, context management, and computational architecture.