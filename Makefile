# Chirality Framework - Development Makefile
# Domain-driven architecture utilities

.PHONY: help checksums lint-boundaries import-rewrite smoke test

help:
	@echo "Chirality Framework Development Commands"
	@echo "========================================"
	@echo ""
	@echo "checksums        - Update prompt asset checksums"
	@echo "lint-boundaries  - Check architectural boundary violations" 
	@echo "import-rewrite   - Fix imports after refactoring"
	@echo "smoke            - Basic smoke test (import + simple computation)"
	@echo "test             - Run full test suite"
	@echo ""

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
	@python -c "from chirality import MATRIX_A, MATRIX_B, EchoResolver, compute_cell_C; resolver = EchoResolver(); cell = compute_cell_C(0, 0, MATRIX_A, MATRIX_B, resolver); print('✅ Pipeline works:', cell.value[:50] + '...')"
	@echo "🎉 Smoke test passed!"

test:
	@echo "🧪 Running test suite..."
	pytest -v