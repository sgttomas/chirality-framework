# Support Matrices Integration Guide

## Overview
This document outlines the integration of support matrix prompts (J, K, G, P, T) into the Phase 1 dialogue pipeline.

## Files Created

### 1. Prompt Asset Files
Created placeholder .md files for you to write the actual prompts:

- `chirality/infrastructure/prompts/assets/phase1/J/extract.md` - Extract J from B
- `chirality/infrastructure/prompts/assets/phase1/K/transform.md` - Transform D to K (transpose)
- `chirality/infrastructure/prompts/assets/phase1/G/extract.md` - Extract G from Z (rows 1-3)
- `chirality/infrastructure/prompts/assets/phase1/P/extract.md` - Extract P from Z (row 4)
- `chirality/infrastructure/prompts/assets/phase1/T/transform.md` - Transform J to T (transpose)

### 2. Template Variables
Each prompt file includes template variables that will be replaced at runtime:

#### Matrix J
- `{{matrix_id}}`: J
- `{{source_matrix}}`: B
- `{{rows}}`: 3
- `{{cols}}`: 4
- `{{row_labels}}`: ["data", "information", "knowledge"]
- `{{col_labels}}`: ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"]

#### Matrix K
- `{{matrix_id}}`: K
- `{{source_matrix}}`: D
- `{{operation}}`: transpose
- `{{k_rows}}`: 4
- `{{k_cols}}`: 3
- `{{k_row_labels}}`: ["guiding", "applying", "judging", "reflecting"]
- `{{k_col_labels}}`: ["normative", "operative", "iterative"]

#### Matrix G
- `{{matrix_id}}`: G
- `{{source_matrix}}`: Z
- `{{station}}`: evaluation
- `{{rows}}`: 3
- `{{cols}}`: 4
- `{{row_labels}}`: ["guiding", "applying", "judging"]
- `{{col_labels}}`: ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"]

#### Matrix P
- `{{matrix_id}}`: P
- `{{source_matrix}}`: Z
- `{{station}}`: evaluation
- `{{rows}}`: 1
- `{{cols}}`: 4
- `{{row_label}}`: "reflecting"
- `{{col_labels}}`: ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"]

#### Matrix T
- `{{matrix_id}}`: T
- `{{source_matrix}}`: J
- `{{operation}}`: transpose
- `{{t_rows}}`: 4
- `{{t_cols}}`: 3
- `{{t_row_labels}}`: ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"]
- `{{t_col_labels}}`: ["data", "information", "knowledge"]

## Integration Sequence

The support matrices should be integrated in this order within `dialogue_run.py`:

1. **After Matrix C completion** → Add Matrix J extraction
2. **Before Matrix F** → J must be available for F = C ⊙ J
3. **After Matrix D completion** → K transform (currently data-drop only)
4. **Before Matrix X** → K and J must be available for X = K · J
5. **After Matrix Z completion** → Extract G and P
6. **Before Matrix E** → Transform J to T, then E = G · T

## Required Code Changes

### 1. dialogue_run.py
See `chirality/application/phase1/dialogue_run_updates.py` for the specific locations where to add:

```python
# After C, before F:
j_extract_result, j_extract_trace = self._execute_stage(
    "phase1_j_extract", "J", "extract"
)

# After Z, before E:
g_extract_result, g_extract_trace = self._execute_stage(
    "phase1_g_extract", "G", "extract"
)

p_extract_result, p_extract_trace = self._execute_stage(
    "phase1_p_extract", "P", "extract"
)

t_transform_result, t_transform_trace = self._execute_stage(
    "phase1_t_transform", "T", "transform"
)
```

### 2. metadata.yml
Add the entries from `chirality/infrastructure/prompts/assets/phase1/metadata_additions.yml` to the main metadata.yml file.

## Next Steps

1. **Write the actual prompt content** in each .md file
2. **Update dialogue_run.py** to call these prompts at the right sequence points
3. **Update metadata.yml** with the new asset entries
4. **Test the pipeline** to ensure proper sequencing

## Notes

- Some matrices (K, G, T) are currently handled as data-drops. The prompt files allow you to optionally introduce them with LLM calls first before the data-drop.
- The template variables should match what's being passed from dialogue_run.py
- Consider whether some operations should remain code-only (data-drops) vs. having LLM involvement