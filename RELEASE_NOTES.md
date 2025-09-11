# Release Notes: Version 19.4.0

**Release Date:** 2025-09-10
**Codename:** Support Matrix Integration

## Overview

Version 19.4.0 addresses critical gaps in the Phase 1 dialogue pipeline by integrating missing support matrix explanations and fixing model selection consistency issues. This release resolves the "empty_normalizer_output" problems that were causing Phase 1 runs to fail with GPT-5, ensuring the LLM properly understands where support matrices (J, K, G, P, T) come from in the conversation flow.

## Major Changes

### ✅ **Support Matrix Integration**

- **Missing Matrix Explanations Added:** Five critical prompt stages have been integrated into the Phase 1 dialogue pipeline:
  - **Matrix J Extraction** (`phase1/J/extract.md`) - Explains J is extracted from B (removing wisdom row)
  - **Matrix K Transformation** (`phase1/K/transform.md`) - Explains K is the transpose of D  
  - **Matrix G Extraction** (`phase1/G/extract.md`) - Explains G is extracted from first 3 rows of Z
  - **Matrix P Extraction** (`phase1/P/extract.md`) - Explains P is extracted from 4th row of Z
  - **Matrix T Transformation** (`phase1/T/transform.md`) - Explains T is the transpose of J

- **Correct Sequencing:** All support matrices are now introduced via LLM prompts before being used in subsequent operations, following the normative specification sequence exactly.

- **Dialogue Flow Fixes:** Eliminates the "magic data-drop" problem where matrices appeared without explanation, causing LLM confusion and extraction failures.

### ✅ **Model Selection SSOT Compliance**

- **Eliminated Hardcoded Models:** Fixed multiple Single Source of Truth violations where different components ignored the global `CHIRALITY_MODEL` configuration:
  - **CLI lens-derive:** No longer hardcoded to `gpt-4o-mini`
  - **LensBuilder class:** Now respects global config instead of defaulting to `gpt-5`
  - **build_lens_catalog function:** No longer defaults to `gpt-4o-mini`
  - **Phase 2 CLI:** No longer defaults to `gpt-5-nano`

- **Consistent Model Hierarchy:** All components now properly follow the hierarchy:
  1. CLI argument `--model` (highest priority)
  2. Environment variable `CHIRALITY_MODEL` (middle priority)  
  3. Global config default (lowest priority)

### ✅ **Infrastructure Updates**

- **Prompt Asset Registry:** Added metadata entries for all new support matrix prompts
- **Pipeline Integration:** Updated `dialogue_run.py` to call support matrix prompts at correct sequence points
- **Metadata Validation:** Fixed normative_spec.txt hash and size validation after recent updates
- **Test Organization:** Moved all test_*.py files from project root to `tests/` directory for better organization

## Technical Details

### Prompt Asset Structure
Each support matrix prompt follows the established pattern:
- Clear explanation of what the matrix is and how it's derived
- Template variables for runtime replacement
- Consistent output format requirements
- No framework metadata in the semantic content

### Sequence Integration Points
- **J extraction:** After C completion, before F (needed for F = C ⊙ J)
- **K transformation:** After D completion, before X (needed for X = K · J)  
- **G & P extraction:** After Z completion, before E (needed for E = G · T)
- **T transformation:** After J extraction, before E (needed for E = G · T)

## Impact & Benefits

### For GPT-5 Users
- **Resolves Empty Output Issues:** The missing matrix explanations were causing GPT-5 to produce "empty_normalizer_output" errors
- **Consistent Model Usage:** GPT-5 selection via `CHIRALITY_MODEL=gpt-5` now works throughout the entire pipeline
- **Improved Semantic Understanding:** LLM no longer confused about matrix origins in the conversation

### For Framework Reliability  
- **Architectural Purity:** Maintains the "Conversation as Program" model with proper semantic flow
- **Auditable Dialogue:** Every matrix operation is now explained and visible in the conversation transcript
- **Deterministic Execution:** Eliminates non-deterministic failures due to missing context

## Breaking Changes

**None** - This release is fully backward compatible. All changes are additive improvements to the existing pipeline.

## Migration Guide

**No migration required** - Existing scripts and configurations will work unchanged. The new support matrix prompts are automatically integrated into the dialogue flow.

To take advantage of consistent model selection:
```bash
# Set your preferred model globally
export CHIRALITY_MODEL=gpt-5

# All components will now use GPT-5 consistently
python -m chirality.interfaces.cli phase1-dialogue-run --lens-mode auto --out runs/latest
```

## Files Added/Modified

### Added
- `chirality/infrastructure/prompts/assets/phase1/J/extract.md`
- `chirality/infrastructure/prompts/assets/phase1/K/transform.md` 
- `chirality/infrastructure/prompts/assets/phase1/G/extract.md`
- `chirality/infrastructure/prompts/assets/phase1/P/extract.md`
- `chirality/infrastructure/prompts/assets/phase1/T/transform.md`

### Modified
- `chirality/application/phase1/dialogue_run.py` - Integrated new prompt stages
- `chirality/infrastructure/prompts/assets/metadata.yml` - Added new asset entries
- `chirality/interfaces/cli.py` - Fixed hardcoded model references
- `chirality/infrastructure/lenses/build.py` - Respects global model config
- `chirality/infrastructure/lenses/derive.py` - Uses global config for lens generation

### Moved
- All `test_*.py` files from project root → `tests/` directory for proper organization

## Known Issues

- **Pipeline Timeouts:** Some full runs may still experience timeouts, investigation ongoing
- **Content Filtering:** LLM-generated "Note:" text may trigger transcript validation errors in some cases

## Next Steps

Future releases will focus on:
- Performance optimization for full pipeline runs
- Enhanced content filtering rules
- End-to-end validation of the complete support matrix integration

---

This release represents a significant step toward robust, reliable Phase 1 execution with proper semantic flow and consistent model usage throughout the framework.