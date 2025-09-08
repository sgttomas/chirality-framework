# Makefile for Chirality Framework development

.PHONY: fmt lint type guard test all clean install help checksums lint-boundaries import-rewrite smoke

# Default target
help:
	@echo "Chirality Framework Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Core Development:"
	@echo "  fmt              - Format code with black"
	@echo "  lint             - Run ruff linter"
	@echo "  type             - Run mypy type checker"
	@echo "  guard            - Run legacy guard and kernel hash checks"
	@echo "  test             - Run pytest"
	@echo "  all              - Run guard, fmt, lint, type, and test"
	@echo ""
	@echo "Utilities:"
	@echo "  checksums        - Update prompt asset checksums"
	@echo "  lint-boundaries  - Check architectural boundary violations"
	@echo "  import-rewrite   - Fix imports after refactoring"
	@echo "  smoke            - Basic smoke test"
	@echo "  clean            - Remove generated files and caches"
	@echo "  install          - Install development dependencies"
	@echo ""

# Format code
fmt:
	black chirality/ tests/ scripts/

# Lint code
lint:
	ruff check chirality/

# Type check
type:
	mypy chirality/

# Guard against legacy code
guard:
	python scripts/guard_no_legacy.py
	python scripts/check_kernel_hash.py

# Run tests
test:
	pytest -q

# Run all checks
all: guard fmt lint type test

# Legacy utilities (kept for compatibility)
checksums:
	@echo "🔧 Updating prompt asset checksums..."
	python scripts/update_checksums.py

lint-boundaries:
	@echo "🔍 Checking architectural boundaries..."
	python scripts/lint_boundaries.py

import-rewrite:
	@echo "🔄 Fixing imports after refactoring..."
	python scripts/simple_import_fix.py

smoke:
	@echo "🚀 Running smoke test..."
	@python -c "import chirality; print('✅ Import works')"
	@echo "🎉 Smoke test passed!"

# Clean generated files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	rm -rf build/ dist/ 2>/dev/null || true

# Install development dependencies
install:
	pip install -e ".[dev]"