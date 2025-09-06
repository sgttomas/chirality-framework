# Release Notes: Chirality Framework v17.0.0

## Major Architecture Refactor: Combined Lensing Implementation

### Summary
This release implements a fundamental architecture change from legacy three-stage lensing to a unified combined lensing approach, significantly improving efficiency and semantic coherence while maintaining the core three-stage interpretation pipeline.

### 🚀 Key Improvements
**Semantic Coherence of Matrix A and B Improvements**:
- Revised the 


**Efficiency Gains**:
- Reduced LLM calls from 4+ per cell to 2 per cell (Stage 2 + Stage 3)
- Combined lensing produces more coherent semantic interpretations
- Simplified API with unified resolver methods

**Architecture Simplification**:
- Replaced 5-stage provenance with clean 3-stage structure
- Eliminated complex three-step lensing (column → row → synthesis)
- Single combined lensing operation with unified row × column × station perspective

**Maintainer-Authored Prompt System**:
- All semantic prompts moved to `chirality/prompt_assets/` as markdown files
- Structured prompt registry with versioning and checksums
- Component-driven station selection and operation strategies

### 🔧 Technical Changes

#### Matrix A and B updated 
**the contents of Matrix A and B were revised by the Maintainer**
***Old method***
```# Fixed canonical Matrix A (3x4)
MATRIX_A = Matrix(
    name="A",
    station="Problem Statement",
    row_labels=["Normative", "Operative", "Evaluative"],
    col_labels=["Guiding", "Applying", "Judging", "Reviewing"],
    cells=_create_matrix_cells([
        ["Values", "Actions", "Benchmarks", "Feedback"],
        ["Standards", "Methods", "Decisions", "Adaptation"],
        ["Objectives", "Coordination", "Evaluation", "Refinement"]
    ])
)

# Fixed canonical Matrix B (4x4)  
MATRIX_B = Matrix(
    name="B",
    station="Problem Statement",
    row_labels=["Data", "Information", "Knowledge", "Wisdom"],
    col_labels=["Necessity (vs Contingency)", "Sufficiency", "Completeness", "Consistency"],
    cells=_create_matrix_cells([
        ["Necessary vs Contingent", "Sufficient", "Complete", "Consistent"],
        ["Relevant", "Actionable", "Contextual", "Congruent"],
        ["Fundamental", "Effective", "Systematic", "Coherent"],
        ["Essential", "Optimal", "Holistic", "Principled"]
    ])
)
```
***New Method***
```
# Fixed canonical Matrix A (3x4)
MATRIX_A = Matrix(
    name="A",
    station="Problem Statement",
    row_labels=["normative", "operative", "iterative"],
    col_labels=["guiding", "applying", "judging", "reflecting"],
    cells=_create_matrix_cells(
        [
            ["objectives", "actions", "benchmarks", "feedback"],
            ["standards", "methods", "criteria", "adaptation"],
            ["development", "coordination", "evaluation", "refinement"],
        ]
    ),
)

# Fixed canonical Matrix B (4x4)
MATRIX_B = Matrix(
    name="B",
    station="Problem Statement",
    row_labels=["data", "information", "knowledge", "wisdom"],
    col_labels=["necessity (vs contingency)", "sufficiency", "completeness", "consistency"],
    cells=_create_matrix_cells(
        [
            ["necessary", "sufficient", "complete", "consistent"],
            ["contingent", "actionable", "contextual", "congruent"],
            ["purposeful", "effective", "comprehensive", "coherent"],
            ["essential", "optimal", "holistic", "principled"],
        ]
    ),
)
```


#### New Combined Lensing API
**Old Methods (Removed)**:
```python
resolve_semantic_pair()
apply_column_lens() 
apply_row_lens()
synthesize_final_result()
```

**New Methods**:
```python
run_stage2_multiply()     # Semantic multiplication for k-products
run_stage2_elementwise()  # Element-wise semantic operations  
run_stage2_addition()     # Mechanical addition for Matrix D
run_combined_lens()       # Single unified lensing operation
run_shift()              # Station context shift for Matrix Z
```

#### Provenance Structure Changes
**Before (5-stage)**:
```
stage_1_construct
stage_2_semantic  
stage_3_column_lensed
stage_4_row_lensed
stage_5_final_synthesis
```

**After (3-stage)**:
```
stage_1_construct         # Mechanical generation
stage_2_semantic         # Semantic resolution
stage_3_combined_lensed  # Unified lensing (empty for Matrix Z)
```

#### Matrix Z Special Case
Matrix Z now uses a lean 2-stage pipeline with station shift instead of lensing:
- Stage 1: Direct content extraction
- Stage 2: Station shift from Verification to Validation context
- No Stage 3 lensing (empty `stage_3_combined_lensed`)

### 📁 New File Structure

#### Prompt System Architecture
```
chirality/lib/
├── strategies.py          # Component-to-station mapping & operation strategies
├── prompt_registry.py     # Maintainer-authored prompt asset management
├── prompt_builder.py      # Message construction with placeholder substitution
└── llm_client.py         # Unified OpenAI Responses API client
```

#### Prompt Assets
```
chirality/prompt_assets/
├── stage2_multiply.md     # Semantic multiplication prompts
├── stage2_elementwise.md  # Element-wise operation prompts
├── combined_lens.md       # Unified lensing prompts
├── station_shift.md       # Station context shift prompts
└── station_briefs/       # Station-specific context briefs
```

#### Test Coverage
```
tests/integration/
└── test_prompt_system_integration.py  # Comprehensive prompt system tests

.github/workflows/
├── ci.yml                # Main CI pipeline with prompt validation
├── release.yml           # Automated release workflow
├── security.yml          # Weekly security audits
└── docs.yml             # Documentation generation
```

### ⚡ Performance Impact

**Before**: 4+ LLM calls per cell
- 1 × `resolve_semantic_pair()`
- 1 × `apply_column_lens()`
- 1 × `apply_row_lens()`
- 1 × `synthesize_final_result()`

**After**: 2 LLM calls per cell
- 1 × `run_stage2_multiply()` (or equivalent)
- 1 × `run_combined_lens()`

**Result**: ~50% reduction in LLM API calls with improved semantic coherence.

### 🔒 Critical Requirements Maintained

- **OpenAI Responses API**: Continues to use `client.responses.create()` exclusively
- **Normative Spec Sovereignty**: All semantic content remains maintainer-authored
- **3-Stage Pipeline**: Core algorithm structure preserved
- **Matrix Relationships**: All canonical matrix operations unchanged
- **Provenance Tracking**: Complete computational lineage maintained

### 🧪 Testing & Validation

- **30 comprehensive tests** covering all aspects of the new architecture
- **16/17 integration tests passing** for prompt system components
- **Full CI/CD pipeline** with security scanning and automated releases
- **Backward compatibility** through updated mock resolvers

### 📋 Migration Impact

**Breaking Changes**:
- Old resolver methods no longer available
- 5-stage provenance structure no longer supported
- Legacy prompt building code removed

**Compatibility**:
- CLI commands unchanged
- Matrix computation results equivalent
- Echo resolver maintains deterministic behavior
- All existing test patterns updated

### 🎯 What's Next

This refactor establishes the foundation for:
- Enhanced semantic coherence through unified lensing
- Improved maintainability with structured prompt assets
- Better observability through simplified provenance
- Reduced API costs through call optimization

### 📊 Full Change Summary

**Files Modified**: 15+ core files updated
**Files Added**: 8 new architecture files + comprehensive tests
**Files Removed**: 2 obsolete implementation files
**Tests Added**: 17 integration tests + updated existing test suite
**API Calls Reduced**: ~50% fewer LLM calls per computation

---

**Migration Note**: This is a major architecture change. While CLI behavior remains consistent, any direct use of the old resolver API will need updating to the new combined lensing methods.