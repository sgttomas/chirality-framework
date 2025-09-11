# Phase 1 Sequence Analysis: Normative vs. Implementation

## Expected Sequence (from normative_system_prompt_Phase2.txt)

### Matrix C Pipeline
1. **Matrix C Construction** - A · B = C (mechanical)
2. **Matrix C Interpretation** - Resolve semantic operators  
3. **Matrix C Lens Generation** - Generate interpretive lenses
4. **Matrix C Lens Application** - Apply lenses to get final C

### Matrix J Introduction
5. **Matrix J Extraction** - Extract J from B (remove wisdom row)

### Matrix F Pipeline  
6. **Matrix F Construction** - C ⊙ J = F (mechanical, element-wise)
7. **Matrix F Interpretation** - Resolve semantic operators
8. **Matrix F Lens Generation** - Generate interpretive lenses  
9. **Matrix F Lens Application** - Apply lenses to get final F

### Matrix D Pipeline
10. **Matrix D Construction** - A + F = D (semantic addition with template)
11. **Matrix D Lens Generation** - Generate interpretive lenses
12. **Matrix D Lens Application** - Apply lenses to get final D

### Matrix K Introduction
13. **Matrix K Transformation** - Transpose of final D

### Matrix X Pipeline
14. **Matrix X Construction** - K · J = X (mechanical dot product)
15. **Matrix X Interpretation** - Resolve semantic operators
16. **Matrix X Lens Generation** - Generate interpretive lenses
17. **Matrix X Lens Application** - Apply lenses to get final X

### Matrix Z Pipeline
18. **Matrix Z Lens Generation** - Generate validation lenses
19. **Matrix Z Transformation** - Apply validation shift X -> Z
20. **Matrix Z Principles** - Distill into principles

### Matrix G & P Extraction
21. **Matrix G Extraction** - Extract first 3 rows from Z
22. **Matrix P Extraction** - Extract 4th row from Z

### Matrix T Introduction
23. **Matrix T Transformation** - Transpose of J

### Matrix E Pipeline
24. **Matrix E Construction** - G · T = E (mechanical dot product)
25. **Matrix E Interpretation** - Resolve semantic operators
26. **Matrix E Lens Generation** - Generate interpretive lenses
27. **Matrix E Lens Application** - Apply lenses to get final E

## Current Implementation Issues

### ❌ MISSING: Matrix J Introduction
- **Problem**: J is used in F = C ⊙ J but never explicitly introduced
- **Location**: Should be between C completion and F start
- **Fix**: Add `phase1_j_extract` stage

### ❌ MISSING: Explicit Matrix K Introduction
- **Problem**: K appears as data-drop without explanation
- **Location**: Before X pipeline starts
- **Fix**: Add `phase1_k_transform` stage before data-drop

### ❌ MISSING: Matrix G & P Introduction
- **Problem**: G and T appear as data-drops without explanation
- **Location**: After Z completion, before E pipeline
- **Fix**: Add `phase1_g_extract` and `phase1_p_extract` stages

### ❌ MISSING: Matrix T Introduction
- **Problem**: T appears as data-drop without explanation  
- **Location**: After G/P extraction, before E pipeline
- **Fix**: Add `phase1_t_transform` stage before data-drop

### ⚠️ SEQUENCE ISSUE: Z Principles
- **Problem**: Z principles stage exists but may be out of order
- **Current**: After Z lensed
- **Expected**: After Z lensed (correct)

## Critical Sequence Gaps

The normative prompt shows that each matrix should be:
1. **Introduced/Explained** via prompt (what it is, how it's derived)
2. **Constructed** mechanically (if applicable)
3. **Interpreted** semantically (if applicable)
4. **Lensed** with station-appropriate lenses

Currently the implementation jumps directly to data-drops for J, K, G, P, T without explanation.

## Required Fixes

### 1. Add Missing Introduction Stages
```python
# After C lensed, before F mechanical:
j_extract_result, j_extract_trace = self._execute_stage(
    "phase1_j_extract", "J", "extract"
)

# After D lensed, before K data-drop:
k_transform_result, k_transform_trace = self._execute_stage(
    "phase1_k_transform", "K", "transform"
)

# After Z principles, before G data-drop:
g_extract_result, g_extract_trace = self._execute_stage(
    "phase1_g_extract", "G", "extract"
)

p_extract_result, p_extract_trace = self._execute_stage(
    "phase1_p_extract", "P", "extract"  
)

# After P extraction, before T data-drop:
t_transform_result, t_transform_trace = self._execute_stage(
    "phase1_t_transform", "T", "transform"
)
```

### 2. Update Prompt Asset Registry
Add entries in metadata.yml for the 5 new prompt assets.

### 3. Write Actual Prompt Content
The placeholder .md files need actual content explaining:
- What each matrix is
- How it's derived from source matrices
- Its role in the semantic valley progression

## Quality Check Summary

**Missing Prompts**: 5 critical introduction stages
**Sequence Issues**: Support matrices appear without explanation
**Impact**: LLM confusion about matrix origins, leading to requests for missing data

The current implementation treats J, K, G, P, T as "magic" data-drops when they should be properly introduced and explained in the conversational flow.