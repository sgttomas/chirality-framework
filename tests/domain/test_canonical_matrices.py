"""
Golden test for canonical matrices - ensures exact normative compliance

These tests verify that Matrix A, B, and J match the exact specification
provided by the user. Any deviation will cause these tests to fail,
preventing semantic drift in the framework's core ontology.
"""

import pytest
from chirality.domain.matrices.canonical import MATRIX_A, MATRIX_B, MATRIX_J


class TestMatrixA:
    """Test Matrix A against exact specification."""
    
    def test_matrix_a_structure(self):
        """Test Matrix A basic structure."""
        assert MATRIX_A.name == "A"
        assert MATRIX_A.station == "Problem Statement"
        assert MATRIX_A.shape == (3, 4)
    
    def test_matrix_a_labels(self):
        """Test Matrix A labels exactly."""
        assert MATRIX_A.row_labels == ["normative", "operative", "iterative"]
        assert MATRIX_A.col_labels == ["guiding", "applying", "judging", "reflecting"]
    
    def test_matrix_a_cells_row_0(self):
        """Test Matrix A row 0 cells exactly."""
        row_0 = [cell.value for cell in MATRIX_A.cells[0]]
        assert row_0 == ["objectives", "actions", "benchmarks", "feedback"]
    
    def test_matrix_a_cells_row_1(self):
        """Test Matrix A row 1 cells exactly."""
        row_1 = [cell.value for cell in MATRIX_A.cells[1]]
        assert row_1 == ["standards", "methods", "criteria", "adaptation"]
    
    def test_matrix_a_cells_row_2(self):
        """Test Matrix A row 2 cells exactly."""
        row_2 = [cell.value for cell in MATRIX_A.cells[2]]
        assert row_2 == ["development", "coordination", "evaluation", "refinement"]
    
    def test_matrix_a_specific_cells(self):
        """Test specific Matrix A cells for spot checks."""
        assert MATRIX_A.cells[0][0].value == "objectives"
        assert MATRIX_A.cells[0][3].value == "feedback"
        assert MATRIX_A.cells[1][1].value == "methods"
        assert MATRIX_A.cells[2][3].value == "refinement"


class TestMatrixB:
    """Test Matrix B against exact specification."""
    
    def test_matrix_b_structure(self):
        """Test Matrix B basic structure."""
        assert MATRIX_B.name == "B"
        assert MATRIX_B.station == "Problem Statement"
        assert MATRIX_B.shape == (4, 4)
    
    def test_matrix_b_labels(self):
        """Test Matrix B labels exactly."""
        assert MATRIX_B.row_labels == ["data", "information", "knowledge", "wisdom"]
        assert MATRIX_B.col_labels == ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"]
    
    def test_matrix_b_cells_row_0(self):
        """Test Matrix B row 0 cells exactly."""
        row_0 = [cell.value for cell in MATRIX_B.cells[0]]
        assert row_0 == ["necessary", "sufficient", "complete", "consistent"]
    
    def test_matrix_b_cells_row_1(self):
        """Test Matrix B row 1 cells exactly."""
        row_1 = [cell.value for cell in MATRIX_B.cells[1]]
        assert row_1 == ["contingent", "insufficient", "incomplete", "inconsistent"]
    
    def test_matrix_b_cells_row_2(self):
        """Test Matrix B row 2 cells exactly."""
        row_2 = [cell.value for cell in MATRIX_B.cells[2]]
        assert row_2 == ["purposeful", "effective", "comprehensive", "coherent"]
    
    def test_matrix_b_cells_row_3(self):
        """Test Matrix B row 3 cells exactly."""
        row_3 = [cell.value for cell in MATRIX_B.cells[3]]
        assert row_3 == ["constitutive", "optimal", "holistic", "principled"]
    
    def test_matrix_b_specific_cells(self):
        """Test specific Matrix B cells for spot checks."""
        assert MATRIX_B.cells[0][0].value == "necessary"
        assert MATRIX_B.cells[0][3].value == "consistent"
        assert MATRIX_B.cells[3][0].value == "constitutive"
        assert MATRIX_B.cells[3][3].value == "principled"


class TestMatrixJ:
    """Test Matrix J (truncated B) against exact specification."""
    
    def test_matrix_j_structure(self):
        """Test Matrix J basic structure."""
        assert MATRIX_J.name == "J"
        assert MATRIX_J.station == "Objectives"
        assert MATRIX_J.shape == (3, 4)
    
    def test_matrix_j_labels(self):
        """Test Matrix J labels exactly."""
        assert MATRIX_J.row_labels == ["data", "information", "knowledge"]  # No "wisdom"
        assert MATRIX_J.col_labels == ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"]
    
    def test_matrix_j_is_truncated_b(self):
        """Test that Matrix J is exactly the first 3 rows of Matrix B."""
        for i in range(3):  # First 3 rows only
            for j in range(4):
                assert MATRIX_J.cells[i][j].value == MATRIX_B.cells[i][j].value, \
                    f"Matrix J cell [{i}][{j}] should match Matrix B cell [{i}][{j}]"
    
    def test_matrix_j_cells_row_0(self):
        """Test Matrix J row 0 cells exactly."""
        row_0 = [cell.value for cell in MATRIX_J.cells[0]]
        assert row_0 == ["necessary", "sufficient", "complete", "consistent"]
    
    def test_matrix_j_cells_row_1(self):
        """Test Matrix J row 1 cells exactly."""
        row_1 = [cell.value for cell in MATRIX_J.cells[1]]
        assert row_1 == ["contingent", "insufficient", "incomplete", "inconsistent"]
    
    def test_matrix_j_cells_row_2(self):
        """Test Matrix J row 2 cells exactly."""
        row_2 = [cell.value for cell in MATRIX_J.cells[2]]
        assert row_2 == ["purposeful", "effective", "comprehensive", "coherent"]


class TestMatrixRelationships:
    """Test relationships between canonical matrices."""
    
    def test_matrices_have_different_column_ontologies(self):
        """Test that Matrix A and B have different column semantics."""
        assert MATRIX_A.col_labels != MATRIX_B.col_labels, \
            "Matrix A and B should have different column ontologies"
    
    def test_matrix_j_column_ontology_matches_b(self):
        """Test that Matrix J uses Matrix B's column ontology."""
        assert MATRIX_J.col_labels == MATRIX_B.col_labels, \
            "Matrix J should use Matrix B's column ontology"
    
    def test_all_matrices_same_station(self):
        """Test that Matrix A and B are at same station."""
        assert MATRIX_A.station == MATRIX_B.station == "Problem Statement"
        assert MATRIX_J.station == "Objectives"  # Different station


if __name__ == "__main__":
    pytest.main([__file__, "-v"])