"""
Phase-1 Verification Test

Tests the complete C→F→D→K→X→Z→E pipeline to ensure:
1. Matrix shapes and labels are correct
2. Representative cell contents contain expected semantic patterns
3. 3-stage provenance structure is maintained
4. No semantic drift in the pipeline

This is the "Phase-1 provenance test" that colleague_1 requested.
"""

import pytest
from chirality.domain.matrices.canonical import MATRIX_A, MATRIX_B, MATRIX_J
from chirality.application.services.pipeline_service import (
    compute_matrix_C,
    compute_matrix_F, 
    compute_matrix_D,
    compute_matrix_K,
    compute_matrix_X,
    compute_matrix_Z,
    compute_matrix_G,
    compute_array_P,
    compute_matrix_E,
)
from chirality.infrastructure.llm.mock_resolvers import EchoResolver


class TestPhase1Pipeline:
    """Test complete Phase-1 pipeline integrity."""
    
    @pytest.fixture
    def resolver(self):
        """Echo resolver for deterministic testing."""
        return EchoResolver()
    
    @pytest.fixture
    def problem_statement(self):
        """Standard problem statement for testing.""" 
        return "generating reliable knowledge"
    
    def test_matrix_c_computation(self, resolver, problem_statement):
        """Test Matrix C (A * B) computation and structure."""
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, problem_statement)
        
        # Check structure
        assert C.name == "C"
        assert C.shape == (3, 4)
        assert C.station == "Requirements"
        assert len(C.row_labels) == 3
        assert len(C.col_labels) == 4
        
        # Check representative cell content patterns
        c_00 = C.cells[0][0]
        assert "objectives" in c_00.value.lower()
        assert "necessary" in c_00.value.lower()
        
        # Check provenance structure
        assert "stage_1_construct" in c_00.provenance
        assert "stage_2_semantic" in c_00.provenance  
        assert "stage_3_combined_lensed" in c_00.provenance
        
        # Stage 1 should have texts (k-products)
        stage1 = c_00.provenance["stage_1_construct"]
        assert "texts" in stage1
        assert isinstance(stage1["texts"], list)
        
        # Stage 2 should have resolved text
        stage2 = c_00.provenance["stage_2_semantic"]
        assert "text" in stage2
        assert isinstance(stage2["text"], str)
        
        # Stage 3 should have combined lensed result
        stage3 = c_00.provenance["stage_3_combined_lensed"] 
        assert "text" in stage3
        assert isinstance(stage3["text"], str)
    
    def test_matrix_f_computation(self, resolver, problem_statement):
        """Test Matrix F (J ⊙ C) element-wise computation."""
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, problem_statement)
        F = compute_matrix_F(MATRIX_J, C, resolver, problem_statement)
        
        # Check structure
        assert F.name == "F"
        assert F.shape == (3, 4) 
        assert F.station == "Objectives"
        
        # Check representative cell
        f_00 = F.cells[0][0]
        
        # Should contain elements from both J and C
        assert any(j_word in f_00.value.lower() for j_word in ["necessary", "data"])
        
        # Check 3-stage provenance
        assert "stage_1_construct" in f_00.provenance
        assert "stage_2_semantic" in f_00.provenance
        assert "stage_3_combined_lensed" in f_00.provenance
    
    def test_matrix_d_computation(self, resolver, problem_statement):
        """Test Matrix D (A + F) synthesis computation.""" 
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, problem_statement)
        F = compute_matrix_F(MATRIX_J, C, resolver, problem_statement)
        D = compute_matrix_D(MATRIX_A, F, resolver, problem_statement)
        
        # Check structure
        assert D.name == "D"
        assert D.shape == (3, 4)
        assert D.station == "Objectives"
        
        # Check representative cell
        d_00 = D.cells[0][0]
        
        # Matrix D uses canonical synthesis formula
        assert "applied to frame the problem" in d_00.value
        assert "to resolve the problem" in d_00.value
        
        # Check provenance (D stage 2 is mechanical addition)
        assert "stage_1_construct" in d_00.provenance
        assert "stage_2_semantic" in d_00.provenance
        assert "stage_3_combined_lensed" in d_00.provenance
    
    def test_matrix_k_transpose(self, resolver, problem_statement):
        """Test Matrix K (transpose of D) computation."""
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, problem_statement)
        F = compute_matrix_F(MATRIX_J, C, resolver, problem_statement)
        D = compute_matrix_D(MATRIX_A, F, resolver, problem_statement)
        K = compute_matrix_K(D)
        
        # Check structure (K is transpose of D)
        assert K.name == "K"
        assert K.shape == (4, 3)  # Transposed dimensions
        assert K.station == D.station
        
        # Check transpose relationship
        assert K.cells[0][0].value == D.cells[0][0].value
        assert K.cells[1][0].value == D.cells[0][1].value
    
    def test_matrix_x_computation(self, resolver, problem_statement):
        """Test Matrix X (K * J) computation."""
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, problem_statement)
        F = compute_matrix_F(MATRIX_J, C, resolver, problem_statement)
        D = compute_matrix_D(MATRIX_A, F, resolver, problem_statement)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, problem_statement)
        
        # Check structure
        assert X.name == "X"
        assert X.shape == (4, 4)  # 4x3 * 3x4 = 4x4
        assert X.station == "Verification"
        
        # Check representative cell
        x_00 = X.cells[0][0]
        
        # Check 3-stage provenance
        assert "stage_1_construct" in x_00.provenance
        assert "stage_2_semantic" in x_00.provenance
        assert "stage_3_combined_lensed" in x_00.provenance
    
    def test_matrix_z_shift(self, resolver, problem_statement):
        """Test Matrix Z (station shift from Verification to Validation)."""
        # Build up to X matrix
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, problem_statement)
        F = compute_matrix_F(MATRIX_J, C, resolver, problem_statement)
        D = compute_matrix_D(MATRIX_A, F, resolver, problem_statement)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, problem_statement)
        Z = compute_matrix_Z(X, resolver, problem_statement)
        
        # Check structure
        assert Z.name == "Z"
        assert Z.shape == (4, 4)  # Same as X
        assert Z.station == "Validation"  # Shifted station
        
        # Check representative cell
        z_00 = Z.cells[0][0]
        
        # Z uses 2-stage pipeline (shift in stage 2, no stage 3)
        assert "stage_1_construct" in z_00.provenance
        assert "stage_2_semantic" in z_00.provenance
        assert z_00.provenance["stage_3_combined_lensed"] == {}  # Empty for Z
    
    def test_matrix_e_computation(self, resolver, problem_statement):
        """Test Matrix E (G * T) final evaluation computation."""
        # Build full pipeline up to Z
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, problem_statement)
        F = compute_matrix_F(MATRIX_J, C, resolver, problem_statement)
        D = compute_matrix_D(MATRIX_A, F, resolver, problem_statement)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, problem_statement)
        Z = compute_matrix_Z(X, resolver, problem_statement)
        
        # Compute supporting matrices
        G = compute_matrix_G(Z)  # First 3 rows of Z
        P = compute_array_P(Z)   # Fourth row of Z
        
        # Compute final evaluation matrix
        E = compute_matrix_E(G, MATRIX_B, resolver, problem_statement)
        
        # Check structure
        assert E.name == "E"
        assert E.shape == (3, 3)  # 3x4 * 4x3 = 3x3
        assert E.station == "Evaluation"
        
        # Check representative cell
        e_00 = E.cells[0][0]
        
        # Check 3-stage provenance  
        assert "stage_1_construct" in e_00.provenance
        assert "stage_2_semantic" in e_00.provenance
        assert "stage_3_combined_lensed" in e_00.provenance
    
    def test_full_phase1_pipeline(self, resolver, problem_statement):
        """Test complete Phase-1 pipeline end-to-end."""
        # Execute complete pipeline
        C = compute_matrix_C(MATRIX_A, MATRIX_B, resolver, problem_statement)
        F = compute_matrix_F(MATRIX_J, C, resolver, problem_statement)
        D = compute_matrix_D(MATRIX_A, F, resolver, problem_statement)
        K = compute_matrix_K(D)
        X = compute_matrix_X(K, MATRIX_J, resolver, problem_statement)
        Z = compute_matrix_Z(X, resolver, problem_statement)
        G = compute_matrix_G(Z)
        P = compute_array_P(Z)
        E = compute_matrix_E(G, MATRIX_B, resolver, problem_statement)
        
        # Verify pipeline structure
        matrices = [C, F, D, K, X, Z, G, E]
        
        for matrix in matrices:
            # Each matrix should have a name and station
            assert hasattr(matrix, 'name')
            assert hasattr(matrix, 'station')
            assert hasattr(matrix, 'shape')
            assert hasattr(matrix, 'cells')
            
            # Each should have valid dimensions
            rows, cols = matrix.shape
            assert rows > 0 and cols > 0
            assert len(matrix.cells) == rows
            assert all(len(row) == cols for row in matrix.cells)
        
        # Verify station progression
        assert C.station == "Requirements"
        assert F.station == "Objectives" 
        assert D.station == "Objectives"
        assert K.station == "Objectives"  # Same as D
        assert X.station == "Verification"
        assert Z.station == "Validation"
        assert G.station == "Validation"  # Same as Z
        assert E.station == "Evaluation"
        
        # Verify semantic journey completeness
        # Each step should build on the previous with clear provenance
        assert C.shape == (3, 4)  # A * B
        assert F.shape == (3, 4)  # J ⊙ C  
        assert D.shape == (3, 4)  # A + F
        assert K.shape == (4, 3)  # transpose(D)
        assert X.shape == (4, 4)  # K * J
        assert Z.shape == (4, 4)  # shift(X)
        assert G.shape == (3, 4)  # Z[0:3, :]
        assert E.shape == (3, 3)  # G * T
        
        # The array P should be a 1D array of length 4
        assert len(P) == 4
        assert all(hasattr(cell, 'value') for cell in P)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])