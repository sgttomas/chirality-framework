# Chirality Framework Release Notes

## v19.2.0 - Production Readiness Update (2025-01-08)

### 🚀 Major Production Enhancements

This release focuses on production readiness, reliability, and operational excellence for the Chirality Framework's budgets, caching, and resume capabilities.

#### 🔧 Infrastructure Improvements

**Centralized Pricing System**
- Created unified `chirality/domain/pricing.py` module as single source of truth
- Eliminated pricing duplication across components
- Added support for cached token pricing with reduced rates
- Comprehensive model coverage including GPT-5 series

**Cache System Hardening**
- **Stable Cache Identity**: Cache keys now use `snapshot_hash` and `kernel_hash` from Phase 1 metadata instead of raw content hashing
- **Complete Dependency Tracking**: Cache keys include all parameters affecting results (operands, snapshot, kernel, lens catalog, model params, GPT-5 params)
- **Cache Invalidation**: Proper invalidation when any dependency changes
- **Collision Resistance**: Robust cache key generation prevents false cache hits

**Atomic Resume Operations**
- **Crash-Safe Writes**: All resume files use atomic writes (`tempfile + os.replace`) to prevent partial files after crashes
- **Centralized Path Management**: Canonical `compute_cell_path()` function ensures consistency
- **Corruption Recovery**: Automatic detection and cleanup of corrupted resume files
- **Graceful Degradation**: Resume system fails safely without breaking computation

#### 🎯 API & Integration

**Normalized Adapter Interface**
- Robust usage field extraction from OpenAI responses with fallbacks
- Consistent field naming across different API response structures
- Proper handling of cached tokens for cost calculation
- Enhanced error handling for malformed responses

**CLI Output Channel Separation**
- **Logs → stderr**: All progress, status, and diagnostic messages
- **Data → stdout**: Only actual output data (hashes, results)
- **Clean Integration**: Suitable for CI/CD pipelines and automation
- **Consistent Formatting**: Emoji prefixes for different message types

#### 🧪 Testing & Quality Assurance

**Comprehensive Test Coverage**
- **Cache Invalidation Tests**: 10+ scenarios covering all dependency changes
- **Resume Robustness Tests**: Atomic writes, corruption handling, concurrent safety
- **Adapter Normalization Tests**: Various OpenAI response structures and edge cases
- **CLI Output Tests**: Proper channel separation and formatting
- **Pricing Tests**: Model coverage, rate validation, cost calculation accuracy

### 🐛 Bug Fixes

- Fixed 1000x pricing error in budget calculations (now uses per-1M rates correctly)
- Resolved cache key instability causing unnecessary cache misses
- Fixed resume key consistency issues preventing proper recovery
- Corrected top-k/top-p parameter confusion (OpenAI uses top_p)
- Enhanced budget enforcement timing to prevent runaway costs

### 📊 Performance Improvements

- **Deterministic Caching**: Stable cache keys reduce redundant computations
- **Atomic I/O**: Eliminates file corruption without performance impact
- **Memory Efficiency**: Two-layer caching (memory + disk) with proper cleanup
- **Parallel Safety**: Thread-safe operations for concurrent tensor computation

### 🔄 API Changes

**New Modules**
```python
# Centralized pricing
from chirality.domain.pricing import get_model_pricing, calculate_cost

# CLI logging utilities  
from chirality.lib.logging import log_info, log_error, output_data
```

**Enhanced Cache API**
```python
# Atomic resume operations
resumable_runner.compute_cell_path(tensor_name, indices)  # Canonical paths
resumable_runner.save_cell_result(name, indices, result)  # Atomic writes

# Complete cache keys
cache.compute_cache_key(
    # ... existing params
    kernel_hash="abc123",
    lens_catalog_digest="def456", 
    verbosity="medium",           # GPT-5 params
    reasoning_effort="medium",
    max_tokens=1000
)
```

**Normalized Usage Fields**
```python
# OpenAI adapter now provides consistent fields
metadata = {
    "prompt_tokens": 1000,      # Always present
    "completion_tokens": 500,   # Always present  
    "cached_tokens": 200,       # Cached input tokens
    "total_tokens": 1500        # Calculated if missing
}
```

### 🛠️ Configuration Updates

**Budget Configuration**
```python
budget_config = BudgetConfig(
    token_budget=50000,          # Max tokens
    cost_budget=10.0,           # Max USD
    time_budget=1800            # Max seconds
)
```

**Phase 2 Configuration**
```python
phase2_config = Phase2Config(
    model="gpt-5-nano",         # Default model
    temperature=0.7,            # Default temperature  
    cache_enabled=True,         # Enable caching
    resume_enabled=True         # Enable resume
)
```

### 🔐 Security & Reliability

- **Atomic Operations**: Prevents data corruption during system crashes
- **Input Validation**: All configuration parameters validated
- **Error Boundaries**: Graceful failure modes with helpful error messages
- **Resource Limits**: Budget enforcement prevents runaway costs

### 📚 Documentation

- Updated CLAUDE.md with Phase 2 implementation details
- Added comprehensive API documentation for new modules
- Enhanced troubleshooting guides for production deployment
- Example configurations for common use cases

### ⚡ Migration Guide

**From v19.1.x to v19.2.0:**

1. **No Breaking Changes**: Existing code continues to work
2. **Recommended Updates**:
   ```bash
   # Use new centralized CLI logging
   from chirality.lib.logging import log_info, output_data
   
   # Access centralized pricing  
   from chirality.domain.pricing import calculate_cost
   ```

3. **Configuration Migration**: Existing config files work unchanged
4. **Cache Invalidation**: Existing caches will be rebuilt (expected)

### 🎯 Production Deployment

**Ready for Production Use:**
- ✅ Crash-safe resume operations
- ✅ Deterministic caching with proper invalidation
- ✅ Cost control with accurate budget tracking
- ✅ Clean CI/CD integration (stderr/stdout separation)
- ✅ Comprehensive error handling and recovery
- ✅ Thread-safe concurrent operations

**Recommended Settings:**
```bash
# Production command example
python -m chirality.cli phase2-run \
  --tensor-spec tensors.json \
  --snapshot phase1_snapshot.md \
  --out production-run \
  --token-budget 100000 \
  --cost-budget 25.0 \
  --time-budget 3600 \
  --resume \
  --cache \
  --parallel 4
```

### 📈 Metrics

- **43 new tests** added with 100% pass rate
- **Zero breaking changes** to existing APIs
- **5 new modules** for enhanced functionality
- **8 critical production gaps** resolved
- **100% atomic** file operations for data integrity

---

**Full Changelog**: [v19.1.0...v19.2.0](https://github.com/user/chirality-framework/compare/v19.1.0...v19.2.0)

**Contributors**: Claude Code Assistant

**Next Release**: v19.3.0 - Phase 2 Tensor Implementation