"""
Tests for Station 5: Validation (Z matrix)

This module tests:
1. Station shift operation (X → Z)
2. Z matrix computation with lean 2-stage provenance
3. Validation enforcement and compatibility
"""

from chirality.core.matrices import MATRIX_A, MATRIX_B, MATRIX_J
from chirality.core.operations import (
    compute_matrix_C,
    compute_matrix_F,
    compute_matrix_D,
    compute_matrix_K,
    compute_matrix_X,
    compute_cell_Z,
    compute_matrix_Z,
)
from chirality.core.validate import validate_provenance
from tests.mocks import MockCellResolver


class TestMatrixZComputation:
    """Test the computation of Matrix Z through station shift."""

    def test_compute_cell_Z(self):
        """Test individual cell computation for Z matrix."""
        resolver = MockCellResolver()
        valley_summary = "Validation stage"

        # Compute prerequisite matrices
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)

        # Test a single cell computation
        cell = compute_cell_Z(0, 0, X, resolver, valley_summary)

        # Verify cell structure
        assert cell.row == 0
        assert cell.col == 0
        assert cell.value is not None
        assert "stage_1_construct" in cell.provenance
        assert "stage_2_semantic" in cell.provenance

        # Verify lean 2-stage structure (stage 3 should be empty for Z)
        assert "stage_3_combined_lensed" in cell.provenance
        assert cell.provenance["stage_3_combined_lensed"] == {}

        # Verify Stage 1 has direct extraction
        stage1_text = cell.provenance["stage_1_construct"]["text"]
        assert stage1_text is not None

        # Verify Stage 2 has station shift result
        stage2_text = cell.provenance["stage_2_semantic"]["text"]
        assert "VALIDATION_SHIFT" in stage2_text  # Should have validation context from mock

        # Verify sources
        assert "sources" in cell.provenance
        assert cell.provenance["sources"] == ["X"]

    def test_compute_matrix_Z(self):
        """Test full matrix Z computation."""
        resolver = MockCellResolver()
        valley_summary = "Validation stage"

        # Compute prerequisite matrices
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)

        # Compute Z
        Z = compute_matrix_Z(X, resolver, valley_summary)

        # Verify matrix properties
        assert Z.name == "Z"
        assert Z.station == "Validation"
        assert Z.shape == (4, 4), f"Expected (4, 4) but got {Z.shape}"

        # Verify row and column labels match X
        assert Z.row_labels == X.row_labels
        assert Z.col_labels == X.col_labels

        # Verify all cells are computed
        for i in range(4):
            for j in range(4):
                cell = Z.get_cell(i, j)
                assert cell is not None, f"Cell Z[{i},{j}] should exist"
                assert cell.value is not None
                assert "sources" in cell.provenance
                assert cell.provenance["sources"] == ["X"]

    def test_Z_provenance_validation(self):
        """
        CRUCIAL TEST: Verify that validate_provenance accepts Z's 2-stage structure.

        This test confirms that the changes in Task 3 work correctly.
        """
        resolver = MockCellResolver()
        valley_summary = "Validation test"

        # Compute matrices up to Z
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)

        # Compute a Z cell
        z_cell = compute_cell_Z(0, 0, X, resolver, valley_summary)

        # The crucial test: validate_provenance should return no errors
        validation_errors = validate_provenance(z_cell)
        assert (
            validation_errors == []
        ), f"Z cell should pass validation, but got errors: {validation_errors}"

    def test_Z_dimensions_and_station_shift(self):
        """Test that Z preserves X dimensions and applies station shift correctly."""
        resolver = MockCellResolver()
        valley_summary = "Test"

        # Compute matrices
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)

        # X should be 4x4
        assert X.shape == (4, 4)

        Z = compute_matrix_Z(X, resolver, valley_summary)

        # Z should also be 4x4 (station shift preserves dimensions)
        assert Z.shape == (4, 4)

        # Verify that station shift was applied
        # Check a few cells to ensure they have validation context
        for i in range(2):  # Check first 2 rows
            for j in range(2):  # Check first 2 columns
                z_cell = Z.get_cell(i, j)
                x_cell = X.get_cell(i, j)

                # Z cell value should be different from X cell (transformed by station shift)
                assert (
                    z_cell.value != x_cell.value
                ), f"Z[{i},{j}] should be different from X[{i},{j}] due to station shift"

                # Z cell should contain validation context from mock resolver
                assert "VALIDATION" in z_cell.value, f"Z[{i},{j}] should contain VALIDATION prefix"

    def test_resolver_call_count(self):
        """Test that MockCellResolver tracks station shift calls."""
        resolver = MockCellResolver()
        valley_summary = "Call count test"

        # Compute matrices up to X
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)

        # Reset call count before Z computation
        resolver.reset_call_counts()

        # Compute a single Z cell
        compute_cell_Z(0, 0, X, resolver, valley_summary)

        # Verify that shift_station_context was called
        call_counts = resolver.get_call_counts()
        assert call_counts["run_shift"] == 1, "Should call run_shift once per Z cell"

        # Other methods should not be called for Z (lean 2-stage)
        assert call_counts["run_combined_lens"] == 0, "Z should not use combined lens"
