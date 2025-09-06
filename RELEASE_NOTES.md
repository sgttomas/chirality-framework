# Chirality Framework v17.1.0 - Release Notes

**Release Date**: September 6, 2025  
**Status**: Production Ready  
**Breaking Changes**: None

## 🎉 Major Milestone: Full Semantic Resolution Operational

Version 17.1.0 marks a critical milestone in the Chirality Framework's development - **the semantic calculator is now fully operational** with authentic LLM-driven semantic resolution across the entire pipeline from Requirements (Matrix C) through Evaluation (Matrix E).

## 🚀 What's New

### Complete Semantic Content Implementation
All maintainer-authored prompt assets have been populated with canonical semantic content:
- **System Prompt**: Complete framework context with semantic operations and JSON output contract
- **Station Briefs**: Dedicated context for Requirements, Objectives, Verification, Validation, and Evaluation stations
- **Stage 2 Operators**: Multiplication and element-wise semantic operations with examples
- **Stage 3 Lensing**: Combined lensing and Z-specific shift operations for context transformation

### OpenAI Responses API Integration ✅
The framework now successfully integrates with OpenAI's Responses API:
- **Fixed API Compatibility**: Updated to use `input` parameter instead of `prompt`
- **Robust Response Parsing**: Implements fallback logic for `output_text` and `output[].content[].text`
- **Enhanced Error Handling**: Added JSON error diagnostics with truncated response previews
- **SDK Upgrade**: Minimum requirement upgraded to OpenAI SDK >=1.50.0
- **JSON Output Enforcement**: Relies on system prompt contract for consistent JSON formatting

### Semantic Tracing System Restored 🔧
Critical diagnostic capabilities have been fully restored:
- **Fixed Tracer Architecture**: Updated to work without deprecated SemanticContext class
- **Semantic Journey Tracking**: Captures complete provenance for coherence diagnostics
- **Error-Free Operation**: Eliminated all attribute access errors that were breaking diagnostics

## 🔬 Technical Improvements

### Architecture Enhancements
- **Enhanced Placeholder Support**: Added `{{station_id}}` for dynamic station identification
- **Path B D-Matrix Implementation**: Hard-coded canonical D formula as mechanical operation
- **Z Matrix Handling**: Dedicated shift lensing template for Validation context transformation
- **Strategies Module**: Added station metadata support and updated asset routing

### Quality Assurance
- **Full Test Suite**: All 81 tests passing with new architecture
- **Echo Resolver Validation**: Successful validation for all matrices (C, D, F, X, Z, E)
- **OpenAI Resolver Validation**: Complete semantic pipeline validated with live API
- **Asset Integrity**: SHA256 validation functional for all prompt assets
- **Package Build**: Production-ready package with all prompt assets included

## 🛠️ Developer Experience

### Configuration Improvements
- **Centralized LLM Config**: `llm_config.py` is now single source of truth for LLM parameters
- **Environment Cleanup**: Removed model and temperature from environment variables
- **Asset Registry**: Updated metadata.yml with correct checksums and versions

### Documentation Updates
- **API Reference**: Updated with OpenAI requirements and compatibility notes
- **Algorithm Documentation**: Added Responses API implementation details
- **Contributing Guide**: Enhanced with SDK requirements and API notes

## 🌟 Demonstration: Complete Semantic Resolution

This release enables the framework to perform authentic semantic transformations. For example:

**Input (Stage 1 - Mechanical)**: `"objectives * necessary"`  
**Stage 2 (Semantic Resolution)**: *"The Chirality Framework systematically constrains large-language-model outputs through typed semantic operators..."*  
**Stage 3 (Combined Lensing)**: *"...systematically guides the derivation of comprehensive requirements by exhaustively spanning the problem space..."*

The framework now successfully transforms mechanical k-products into coherent, contextually-appropriate knowledge artifacts that progress logically through the semantic valley.

## 📋 Compatibility & Requirements

### System Requirements
- Python 3.9+
- OpenAI SDK >=1.50.0 (for semantic resolution)
- OpenAI API key set as `OPENAI_API_KEY` environment variable

### Installation
```bash
# Install with OpenAI support
pip install 'chirality-framework[openai]'

# Set your API key
export OPENAI_API_KEY="sk-..."

# Run complete semantic pipeline
python3 -m chirality.cli compute-pipeline --resolver openai --snapshot-jsonl -v
```

### Backward Compatibility
- All existing CLI commands and options remain unchanged
- Echo resolver continues to work for development/testing
- Existing snapshot and trace formats preserved
- No breaking changes to public API

## 🎯 Use Cases Now Enabled

### Research & Development
- **Semantic Analysis**: Complete pipeline from problem requirements to evaluation
- **Coherence Diagnostics**: Full tracing for semantic drift detection
- **Knowledge Generation**: Authentic semantic transformations with provenance

### Integration & Automation
- **App Mode**: Producer contract for chirality-app integration
- **Batch Processing**: Complete pipeline automation with manifest generation
- **Observability**: HTML viewer for semantic journey visualization

## 🔍 Quality Validation

This release has been thoroughly validated:
- ✅ Complete pipeline execution (C through E matrices) with OpenAI resolver
- ✅ All mechanical operations (A, B, J matrices) functioning correctly  
- ✅ Semantic tracing system operational for coherence diagnostics
- ✅ HTML viewer rendering complete semantic results
- ✅ App mode producing valid manifests and snapshots
- ✅ All unit and integration tests passing (81 tests)

## 🚀 Getting Started

### Quick Start
```bash
# Complete semantic pipeline
python3 -m chirality.cli compute-pipeline --resolver openai --snapshot-jsonl --include-base

# View results in browser
python3 -m chirality.cli render-viewer --latest --open

# Inspect single cell with full tracing
python3 -m chirality.cli compute-cell C --i 0 --j 0 --resolver openai --verbose --trace
```

## 🎉 Conclusion

Version 17.1.0 represents the successful realization of the Chirality Framework as a production-ready "semantic calculator." The framework now performs authentic semantic resolution, transforming mechanical combinations into meaningful knowledge artifacts through a structured, observable, and reproducible process.

The semantic valley is fully operational - from problem requirements through final evaluation - with complete observability and diagnostic capabilities intact.

---

**For Technical Details**: See [CHANGELOG.md](CHANGELOG.md)  
**For Integration**: See [docs/API_REFERENCE.md](docs/API_REFERENCE.md)  
**For Development**: See [CONTRIBUTING.md](CONTRIBUTING.md)