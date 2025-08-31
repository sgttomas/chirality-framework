# The Three-Stage Interpretation Pipeline: The "Secret Sauce"

**Version: See VERSION.md** | **Updated: August 2025**

This document provides the definitive explanation of the Three-Stage Interpretation Pipeline—the core algorithm that transforms mechanical combinations into meaningful semantic insights. This pipeline is the "secret sauce" that makes the Chirality Framework a powerful semantic calculator rather than just a matrix manipulation tool.

## Overview: Why Three Stages?

The three-stage pipeline is necessary for **semantic integrity**. Each stage builds meaning progressively:

1. **Stage 1 (Combinatorial)**: Creates structural combinations without interpretation
2. **Stage 2 (Semantic Resolution)**: Transforms raw pairs into coherent concepts  
3. **Stage 3 (Ontological Lensing)**: Applies deep contextual interpretation

This progression ensures that meaning emerges naturally from structure while preserving the ontological coherence that makes the results actionable and insightful.

## Detailed Stage Breakdown

### Stage 1: Combinatorial (Mechanical)

**Purpose**: Generate k-products mechanically without semantic interpretation.

**Process**: For matrix multiplication C = A * B, generate all word pairs A[i,k] * B[k,j] for each k.

**Example Input** (Computing C[0,0]):
- Matrix A[0,:]: ["Values", "Actions", "Benchmarks", "Feedback"]  
- Matrix B[:,0]: ["Necessary", "Contingent", "Fundamental", "Best Practices"]

**Example Output**:
```
k=0: Values * Necessary
k=1: Actions * Contingent  
k=2: Benchmarks * Fundamental
k=3: Feedback * Best Practices
```

**Key Point**: No LLM involvement. Pure mechanical string concatenation.

### Stage 2: Semantic Resolution (First Meaning Layer)

**Purpose**: Transform each raw word pair into a coherent concept.

**Process**: LLM resolves semantic intersection of two terms.

**Example Transformations**:
```
Input  → Output
Values * Necessary         → Essential Values
Actions * Contingent       → Conditional Actions  
Benchmarks * Fundamental   → Foundational Benchmarks
Feedback * Best Practices → Optimal Reference Points
```

**Semantic Rules**:
- Find the **intersection** of meanings, not just concatenation
- Create **coherent concepts** that preserve both original meanings
- Aim for **concise expressions** (1-3 words preferred)

### Stage 3: Ontological Lensing (Deep Interpretation)

**Purpose**: Interpret the resolved concepts through the ontological context of the cell's coordinates.

**Process**: Apply row and column ontological lenses to create deep, context-specific insights.

**Example Input**:
- **Combined concepts**: "Essential Values, Conditional Actions, Foundational Benchmarks, Optimal Reference Points"
- **Row lens**: "Normative" (establishing standards)
- **Column lens**: "Necessity" (identifying requirements)
- **Station context**: "Problem Requirements"

**Example Output**:
```
"To establish normative standards for generating reliable knowledge, we must identify the essential values that define quality requirements, implement conditional actions that respond to contextual necessities, establish foundational benchmarks that set measurable standards, and create optimal reference points that guide decision-making toward required outcomes."
```

**Lensing Rules**:
- **Row lens** provides the **perspective** (how to approach)
- **Column lens** provides the **focus** (what to emphasize)  
- **Station context** provides the **purpose** (why this matters)
- Result should be **actionable insight**, not just description

## Complete Example: Computing C[0,0]

### Input Context
- **Cell coordinates**: C[0,0] 
- **Row ontology**: "Normative" (establishing standards)
- **Column ontology**: "Necessity" (vs Contingency)
- **Station**: "Problem Requirements"
- **Valley position**: "Problem Statement → [Problem Requirements] → Solution Objectives"

### Stage-by-Stage Transformation

**Stage 1 (Combinatorial)**:
```
k=0: Values * Necessary
k=1: Actions * Contingent
k=2: Benchmarks * Fundamental  
k=3: Feedback * Best Practices
```

**Stage 2 (Semantic Resolution)**:
```
Values * Necessary         → Essential Values
Actions * Contingent       → Conditional Actions
Benchmarks * Fundamental   → Foundational Benchmarks
Feedback * Best Practices → Optimal Reference Points
```

**Stage 3 (Ontological Lensing)**:
```
Input: "Essential Values, Conditional Actions, Foundational Benchmarks, Optimal Reference Points"

Applied through Normative/Necessity lens:

Output: "By establishing normative standards and focusing on necessity requirements, we interpret: Essential Values define what must be preserved, Conditional Actions specify required responses to circumstances, Foundational Benchmarks establish measurement standards, and Optimal Reference Points guide decision-making toward necessary outcomes."
```

## Why This is the "Secret Sauce"

### 1. **Progressive Meaning Generation**
- Each stage adds a layer of semantic depth
- Mechanical → Conceptual → Contextual  
- Preserves both structure and meaning

### 2. **Ontological Coherence**
- Row/column coordinates provide consistent interpretive framework
- Every result anchored in the framework's meta-ontology
- Prevents semantic drift across operations

### 3. **Full Observability**
- Every transformation step is captured
- Complete provenance from raw inputs to final insights
- Enables debugging and refinement

### 4. **Scalable Intelligence**
- Same algorithm works for all matrix operations
- Consistent interpretation patterns across the semantic valley
- Reliable, predictable meaning generation

## Implementation Details

### Cell-Level Functions
- `compute_cell_C(i, j, A, B, resolver, valley_summary, tracer)` - Matrix multiplication
- `compute_cell_F(i, j, J, C, resolver, valley_summary, tracer)` - Element-wise multiplication  
- `compute_cell_D(i, j, A, F, resolver, valley_summary, tracer)` - D cell (mechanical + universal lensing)

### Matrix-Level Functions  
- `compute_matrix_C(A, B, resolver, valley_summary, tracer)` - Full C matrix
- `compute_matrix_F(J, C, resolver, valley_summary, tracer)` - Full F matrix
- `compute_matrix_D(A, F, resolver, valley_summary, tracer)` - Full D matrix

### Testing the Pipeline

```python
# Test with MockCellResolver (fast, offline)
from tests.mocks import MockCellResolver, create_test_matrices
from chirality.core.operations import compute_cell_C

A, B = create_test_matrices()
resolver = MockCellResolver()
cell = compute_cell_C(0, 0, A, B, resolver, "Test valley")

# Examine provenance (universal 5-stage schema)
s1 = cell.provenance['stage_1_construct']
s2 = cell.provenance['stage_2_semantic']
s5 = cell.provenance['stage_5_final_synthesis']
print(s1.get('texts') or s1.get('text'))   # Mechanical k-products (list) or element_pair
print(s2.get('texts') or s2.get('text'))   # Semantic resolutions (list) or text
print(s5.get('text'))                      # Final integrated interpretation
```

### CLI Debugging

```bash
# See all stages for any cell
python3 -m chirality.cli compute-cell C --i 0 --j 0 --verbose

# Test with different resolvers
python3 -m chirality.cli compute-cell C --i 1 --j 2 --resolver echo --verbose
python3 -m chirality.cli compute-cell C --i 1 --j 2 --resolver openai --verbose

# Enable full tracing
python3 -m chirality.cli compute-cell C --i 0 --j 0 --trace --verbose
```

## Semantic Valley Context

The three-stage pipeline operates within the broader context of the "semantic valley"—the conceptual space that provides coherent meaning across the entire problem-solving process.

### Valley Stations
- **Problem Statement**: Initial framing and axioms (Matrix A)
- **Problem Requirements**: Structured analysis (Matrix C = A * B)
- **Solution Objectives**: Interpreted goals (Matrix F = J ⊙ C) and synthesized outcomes (Matrix D = synthesis(A, F))

### Valley Navigation
Each computation carries forward the "valley summary" that tracks the current position in the problem-solving journey, ensuring that every semantic operation understands its place in the larger transformative process.

This context-awareness is what elevates the calculator from a simple matrix manipulation tool to a sophisticated semantic intelligence system that generates meaningful, actionable insights for complex problem-solving scenarios.
