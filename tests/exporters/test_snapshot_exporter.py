"""
Tests for Matrix Snapshot Exporter

This module tests the MatrixSnapshotWriter functionality including:
1. Directory creation and atomic writes
2. JSON format and content validation
3. Run ID correlation
"""

import json
import tempfile
from pathlib import Path

from chirality.exporters.snapshot_exporter import MatrixSnapshotWriter
from chirality.core.types import Matrix, Cell
from chirality.core.matrices import MATRIX_A


class TestMatrixSnapshotWriter:
    """Test the MatrixSnapshotWriter functionality."""

    def test_directory_creation(self):
        """Test that snapshot directories are created properly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            run_id = "test-run-123"
            writer = MatrixSnapshotWriter(run_id, base_path=tmpdir)

            # Directory should not exist yet
            assert not writer.run_directory.exists()

            # Write a matrix
            snapshot_path = writer.write_matrix(MATRIX_A, "echo")

            # Directory should now exist
            assert writer.run_directory.exists()
            assert writer.run_directory.is_dir()
            assert snapshot_path.parent == writer.run_directory

    def test_snapshot_content(self):
        """Test that snapshot files contain correct JSON structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            run_id = "test-run-456"
            writer = MatrixSnapshotWriter(run_id, base_path=tmpdir)

            # Write a matrix snapshot
            snapshot_path = writer.write_matrix(MATRIX_A, "echo")

            # Read and parse the snapshot
            with open(snapshot_path, "r") as f:
                snapshot = json.load(f)

            # Verify basic structure
            assert snapshot["matrix_name"] == "A"
            assert snapshot["station"] == "Problem Statement"
            assert snapshot["shape"] == [3, 4]
            assert snapshot["row_labels"] == ["normative", "operative", "iterative"]
            assert snapshot["col_labels"] == ["guiding", "applying", "judging", "reflecting"]
            assert snapshot["run_id"] == run_id
            assert snapshot["resolver"] == "echo"
            assert "timestamp" in snapshot
            assert "cells" in snapshot

            # Verify cells
            assert len(snapshot["cells"]) == 12  # 3×4 matrix

            # Check first cell
            first_cell = snapshot["cells"][0]
            assert first_cell["row"] == 0
            assert first_cell["col"] == 0
            assert first_cell["value"] == "objectives"
            assert first_cell["row_label"] == "normative"
            assert first_cell["col_label"] == "guiding"
            assert "provenance" in first_cell

    def test_filename_format(self):
        """Test that filenames follow the expected format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            run_id = "test-run-789"
            writer = MatrixSnapshotWriter(run_id, base_path=tmpdir)

            # Write a matrix
            snapshot_path = writer.write_matrix(MATRIX_A, "openai")

            # Check filename format: <matrix>-<timestamp>.jsonl
            filename = snapshot_path.name
            assert filename.startswith("A-")
            assert filename.endswith(".jsonl")

            # Verify timestamp format in filename
            parts = filename[:-6].split("-")  # Remove .jsonl
            assert len(parts) >= 2  # A-YYYYMMDD-HHMMSS

    def test_atomic_write_safety(self):
        """Test that atomic writes prevent partial file corruption."""
        with tempfile.TemporaryDirectory() as tmpdir:
            run_id = "test-run-atomic"
            writer = MatrixSnapshotWriter(run_id, base_path=tmpdir)

            # Write multiple matrices to ensure atomicity
            paths = []
            for i in range(3):
                path = writer.write_matrix(MATRIX_A, f"resolver-{i}")
                paths.append(path)

                # Each file should be complete and valid JSON
                with open(path, "r") as f:
                    data = json.load(f)
                    assert data["matrix_name"] == "A"
                    assert data["resolver"] == f"resolver-{i}"

            # All files should exist
            for path in paths:
                assert path.exists()

    def test_custom_matrix_snapshot(self):
        """Test snapshot of a custom matrix with specific provenance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            run_id = "test-custom"
            writer = MatrixSnapshotWriter(run_id, base_path=tmpdir)

            # Create a simple custom matrix
            cells = [
                [
                    Cell(
                        0,
                        0,
                        "test_value",
                        provenance={
                            "operation": "test_op",
                            "sources": ["X", "Y"],
                            "timestamp": "2024-01-01T00:00:00Z",
                            "coordinates": "(0, 0)",
                            "stage_1_construct": {"text": "construct"},
                            "stage_2_semantic": {"text": "semantic"},
                            "stage_3_column_lensed": {},  # Empty stage (like Z matrix)
                            "stage_4_row_lensed": {},
                            "stage_5_final_synthesis": {},
                        },
                    )
                ]
            ]

            custom_matrix = Matrix(
                name="TEST",
                station="Test Station",
                row_labels=["Row1"],
                col_labels=["Col1"],
                cells=cells,
            )

            # Write snapshot
            snapshot_path = writer.write_matrix(custom_matrix, "test_resolver")

            # Verify content
            with open(snapshot_path, "r") as f:
                snapshot = json.load(f)

            assert snapshot["matrix_name"] == "TEST"
            assert snapshot["station"] == "Test Station"
            assert len(snapshot["cells"]) == 1

            cell_data = snapshot["cells"][0]
            assert cell_data["value"] == "test_value"
            assert cell_data["provenance"]["operation"] == "test_op"
            assert cell_data["provenance"]["sources"] == ["X", "Y"]
            assert cell_data["provenance"]["stage_1_construct"] == "construct"
            assert cell_data["provenance"]["stage_2_semantic"] == "semantic"
            # Empty stages should be preserved as empty dicts
            assert cell_data["provenance"]["stage_3_column_lensed"] == {}

    def test_get_snapshot_directory(self):
        """Test the get_snapshot_directory method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            run_id = "test-dir"
            writer = MatrixSnapshotWriter(run_id, base_path=tmpdir)

            expected_dir = Path(tmpdir) / run_id
            assert writer.get_snapshot_directory() == expected_dir

            # Write a matrix to create the directory
            writer.write_matrix(MATRIX_A, "echo")
            assert writer.get_snapshot_directory().exists()
