"""
Tests for Station 6: Evaluation (G, T, P, E matrices)

This module tests:
1. Prerequisite matrix construction (G, T, P from Z and B)
2. E matrix computation with full 3-stage pipeline
3. Evaluation matrix dimensions and structural integrity
"""

from chirality.core.types import Matrix, Cell
from chirality.core.matrices import MATRIX_A, MATRIX_B, MATRIX_J
from chirality.core.operations import (
    compute_matrix_C,
    compute_matrix_F,
    compute_matrix_D,
    compute_matrix_K,
    compute_matrix_X,
    compute_matrix_Z,
    compute_matrix_T_from_B,
    compute_matrix_G,
    compute_array_P,
    compute_cell_E,
    compute_matrix_E
)
from chirality.core.validate import validate_provenance, validate_matrix
from tests.mocks import MockCellResolver


class TestPrerequisiteMatrices:
    """Test the construction of G, T, and P matrices."""
    
    def test_compute_matrix_T_from_B(self):
        """Test that T is correctly derived from B slice and transpose."""
        T = compute_matrix_T_from_B(MATRIX_B)
        
        # Verify matrix properties
        assert T.name == "T"
        assert T.station == "Evaluation Criteria"
        assert T.shape == (4, 3), f"Expected (4, 3) but got {T.shape}"
        
        # Verify that T is transpose of first 3 rows of B
        for i in range(4):
            for j in range(3):
                t_cell = T.get_cell(i, j)
                b_cell = MATRIX_B.get_cell(j, i)  # Transposed indices
                assert t_cell.value == b_cell.value, f"T[{i},{j}] should match B[{j},{i}]"
        
        # Verify labels are correctly transposed
        assert T.row_labels == MATRIX_B.col_labels  # B columns → T rows
        assert T.col_labels == MATRIX_B.row_labels[:3]  # First 3 B rows → T columns
    
    def test_compute_matrix_G(self):
        """Test that G is correctly sliced from Z."""
        resolver = MockCellResolver()
        valley_summary = "Evaluation stage"
        
        # Compute prerequisite matrices up to Z
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)
        Z = compute_matrix_Z(X, resolver, valley_summary)
        
        G = compute_matrix_G(Z)
        
        # Verify matrix properties
        assert G.name == "G"
        assert G.station == "Evaluation Input"
        assert G.shape == (3, 4), f"Expected (3, 4) but got {G.shape}"
        
        # Verify G contains first 3 rows of Z
        for i in range(3):
            for j in range(4):
                g_cell = G.get_cell(i, j)
                z_cell = Z.get_cell(i, j)
                assert g_cell.value == z_cell.value, f"G[{i},{j}] should match Z[{i},{j}]"
        
        # Verify labels match first 3 rows of Z
        assert G.row_labels == Z.row_labels[:3]
        assert G.col_labels == Z.col_labels
    
    def test_compute_array_P(self):
        """Test that P is correctly extracted from Z fourth row."""
        resolver = MockCellResolver()
        valley_summary = "Evaluation stage"
        
        # Compute prerequisite matrices up to Z
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)
        Z = compute_matrix_Z(X, resolver, valley_summary)
        
        P = compute_array_P(Z)
        
        # Verify matrix properties
        assert P.name == "P"
        assert P.station == "Evaluation Context"
        assert P.shape == (1, 4), f"Expected (1, 4) but got {P.shape}"
        
        # Verify P contains fourth row of Z with reset row indices
        for j in range(4):
            p_cell = P.get_cell(0, j)  # P uses row 0
            z_cell = Z.get_cell(3, j)  # Z fourth row (index 3)
            assert p_cell.value == z_cell.value, f"P[0,{j}] should match Z[3,{j}]"
            assert p_cell.row == 0, f"P cell should have row=0, got {p_cell.row}"
            assert p_cell.col == j, f"P cell should have col={j}, got {p_cell.col}"
        
        # Verify labels
        assert P.row_labels == [Z.row_labels[3]]  # Fourth row label from Z
        assert P.col_labels == Z.col_labels
        
        # Validate matrix structure
        validation_errors = validate_matrix(P)
        assert validation_errors == [], f"P should pass validation, but got errors: {validation_errors}"


class TestMatrixEComputation:
    """Test the computation of Matrix E through G * T."""
    
    def test_compute_cell_E(self):
        """Test individual cell computation for E matrix."""
        resolver = MockCellResolver()
        valley_summary = "Evaluation stage"
        
        # Compute prerequisite matrices
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)
        Z = compute_matrix_Z(X, resolver, valley_summary)
        G = compute_matrix_G(Z)
        T = compute_matrix_T_from_B(MATRIX_B)
        
        # Test a single cell computation
        cell = compute_cell_E(0, 0, G, T, resolver, valley_summary)
        
        # Verify cell structure
        assert cell.row == 0
        assert cell.col == 0
        assert cell.value is not None
        assert "stage_1_construct" in cell.provenance
        assert "stage_2_semantic" in cell.provenance
        assert "stage_3_column_lensed" in cell.provenance
        assert "stage_4_row_lensed" in cell.provenance
        assert "stage_5_final_synthesis" in cell.provenance
        
        # Verify Stage 1 has k-products (like C and X)
        stage1_texts = cell.provenance["stage_1_construct"]["texts"]
        assert isinstance(stage1_texts, list)
        assert len(stage1_texts) == 4  # G is 3x4, T is 4x3, so 4 k-products
        
        # Verify Stage 2 has resolved concepts
        stage2_texts = cell.provenance["stage_2_semantic"]["texts"]
        assert isinstance(stage2_texts, list)
        assert len(stage2_texts) == 4  # One resolved concept per k-product
        
        # Verify sources
        assert "sources" in cell.provenance
        assert cell.provenance["sources"] == ["G", "T"]
    
    def test_compute_matrix_E(self):
        """Test full matrix E computation."""
        resolver = MockCellResolver()
        valley_summary = "Evaluation stage"
        
        # Compute prerequisite matrices
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)
        Z = compute_matrix_Z(X, resolver, valley_summary)
        G = compute_matrix_G(Z)
        T = compute_matrix_T_from_B(MATRIX_B)
        
        # Compute E
        E = compute_matrix_E(G, T, resolver, valley_summary)
        
        # Verify matrix properties
        assert E.name == "E"
        assert E.station == "Evaluation"
        assert E.shape == (3, 3), f"Expected (3, 3) but got {E.shape}"
        
        # Verify row and column labels
        assert E.row_labels == G.row_labels
        assert E.col_labels == T.col_labels
        
        # Verify all cells are computed
        for i in range(3):
            for j in range(3):
                cell = E.get_cell(i, j)
                assert cell is not None, f"Cell E[{i},{j}] should exist"
                assert cell.value is not None
                assert "sources" in cell.provenance
                assert cell.provenance["sources"] == ["G", "T"]
    
    def test_E_provenance_validation(self):
        """
        CRUCIAL TEST: Verify that validate_provenance accepts E's 5-stage structure.
        """
        resolver = MockCellResolver()
        valley_summary = "Evaluation test"
        
        # Compute matrices up to E
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)
        Z = compute_matrix_Z(X, resolver, valley_summary)
        G = compute_matrix_G(Z)
        T = compute_matrix_T_from_B(MATRIX_B)
        
        # Compute an E cell
        e_cell = compute_cell_E(0, 0, G, T, resolver, valley_summary)
        
        # The crucial test: validate_provenance should return no errors
        validation_errors = validate_provenance(e_cell)
        assert validation_errors == [], f"E cell should pass validation, but got errors: {validation_errors}"
    
    def test_E_dimensions_and_computation(self):
        """Test that E preserves G×T dimensions and computes correctly."""
        resolver = MockCellResolver()
        valley_summary = "Test"
        
        # Compute matrices
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)
        Z = compute_matrix_Z(X, resolver, valley_summary)
        G = compute_matrix_G(Z)
        T = compute_matrix_T_from_B(MATRIX_B)
        
        # G should be 3x4, T should be 4x3
        assert G.shape == (3, 4)
        assert T.shape == (4, 3)
        
        E = compute_matrix_E(G, T, resolver, valley_summary)
        
        # E should be 3x3 (G rows × T columns)
        assert E.shape == (3, 3)
        
        # Verify that evaluation was applied
        # Check a few cells to ensure they have evaluation content
        for i in range(2):  # Check first 2 rows
            for j in range(2):  # Check first 2 columns
                e_cell = E.get_cell(i, j)
                
                # E cell should have evaluation-specific content
                assert e_cell.value is not None
                assert len(e_cell.value) > 0


class TestResolverCallCounts:
    """Test that MockCellResolver tracks calls correctly for Station 6."""
    
    def test_E_resolver_call_count(self):
        """Test that MockCellResolver tracks E matrix calls."""
        resolver = MockCellResolver()
        valley_summary = "Call count test"
        
        # Compute prerequisite matrices
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, valley_summary)
        F = compute_matrix_F(MATRIX_J, C, resolver, valley_summary)
        D = compute_matrix_D(MATRIX_A, F, resolver, valley_summary)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, valley_summary)
        Z = compute_matrix_Z(X, resolver, valley_summary)
        G = compute_matrix_G(Z)
        T = compute_matrix_T_from_B(MATRIX_B)
        
        # Reset call count before E computation
        resolver.reset_call_counts()
        
        # Compute a single E cell
        compute_cell_E(0, 0, G, T, resolver, valley_summary)
        
        # Verify call counts for full 3-stage pipeline
        call_counts = resolver.get_call_counts()
        
        # E uses full 3-stage pipeline like C and X
        assert call_counts["resolve_semantic_pair"] == 4, "Should call resolve_semantic_pair 4 times (one per k-product)"
        assert call_counts["apply_column_lens"] == 1, "Should call column lens once"
        assert call_counts["apply_row_lens"] == 1, "Should call row lens once"
        assert call_counts["synthesize_lensed_perspectives"] == 1, "Should call synthesis once"
        
        # Station shift should not be called for E
        assert call_counts["shift_station_context"] == 0, "E should not use station shift"