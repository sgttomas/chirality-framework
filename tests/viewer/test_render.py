"""
Tests for Matrix Snapshot Viewer Renderer

This module tests the HTML rendering functionality for matrix snapshots.
"""

import json
import tempfile
from pathlib import Path
import pytest

from chirality.viewer.render import (
    load_matrix_snapshot,
    render_matrix_table,
    render_page,
    render_elements_page,
    write_assets,
    get_latest_run_dir,
    load_snapshots_for_run,
    sanitize_value,
    CANONICAL_ORDER,
)


class TestGetLatestRunDir:
    """Test the get_latest_run_dir functionality."""

    def test_get_latest_run_dir_with_multiple_runs(self):
        """Test that the latest run directory is correctly identified."""
        with tempfile.TemporaryDirectory() as tmpdir:
            snapshots_dir = Path(tmpdir)

            # Create multiple run directories with different timestamps
            run1 = snapshots_dir / "pipeline-20250901-120000-abc123"
            run2 = snapshots_dir / "pipeline-20250903-140000-def456"
            run3 = snapshots_dir / "pipeline-20250902-100000-ghi789"

            run1.mkdir()
            run2.mkdir()
            run3.mkdir()

            # Should return the lexicographically last directory (which is chronologically latest)
            latest = get_latest_run_dir(snapshots_dir)
            assert latest == "pipeline-20250903-140000-def456"

    def test_get_latest_run_dir_empty_directory(self):
        """Test behavior when snapshots directory is empty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            snapshots_dir = Path(tmpdir)
            latest = get_latest_run_dir(snapshots_dir)
            assert latest is None

    def test_get_latest_run_dir_nonexistent_directory(self):
        """Test behavior when snapshots directory doesn't exist."""
        nonexistent_dir = Path("/nonexistent/path")
        latest = get_latest_run_dir(nonexistent_dir)
        assert latest is None

    def test_get_latest_run_dir_with_files(self):
        """Test that files in snapshots directory are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            snapshots_dir = Path(tmpdir)

            # Create both directories and files
            (snapshots_dir / "pipeline-20250901-120000-abc123").mkdir()
            (snapshots_dir / "some-file.txt").touch()

            latest = get_latest_run_dir(snapshots_dir)
            assert latest == "pipeline-20250901-120000-abc123"


class TestRenderMatrixTable:
    """Test the render_matrix_table functionality."""

    def test_render_matrix_table_with_valid_snapshot(self):
        """Test that HTML table is correctly generated with escaped content."""
        # Create mock snapshot data
        snapshot_data = {
            "matrix_name": "A",
            "station": "Problem Statement",
            "shape": [2, 2],
            "row_labels": ["Row1", "Row2"],
            "col_labels": ["Col1", "Col2"],
            "cells": [
                {
                    "row": 0,
                    "col": 0,
                    "value": "Test Value <script>",
                    "provenance": {"operation": "test_op", "timestamp": "2024-01-01T00:00:00Z"},
                },
                {
                    "row": 0,
                    "col": 1,
                    "value": "Another & Value",
                    "provenance": {"operation": "another_op", "timestamp": "2024-01-01T00:01:00Z"},
                },
                {
                    "row": 1,
                    "col": 0,
                    "value": "Third Value",
                    "provenance": {"operation": "third_op", "timestamp": "2024-01-01T00:02:00Z"},
                },
                {
                    "row": 1,
                    "col": 1,
                    "value": "Fourth Value",
                    "provenance": {"operation": "fourth_op", "timestamp": "2024-01-01T00:03:00Z"},
                },
            ],
        }

        html = render_matrix_table(snapshot_data, "A")

        # Verify basic table structure
        assert '<table class="matrix-table" id="a">' in html
        assert "<caption>Matrix A</caption>" in html
        assert "<thead>" in html
        assert "<tbody>" in html

        # Verify labels are escaped and present
        assert "Row1" in html
        assert "Col1" in html

        # Verify values are escaped properly
        assert "Test Value &lt;script&gt;" in html
        assert "Another &amp; Value" in html

        # Verify provenance information is included
        assert "test_op" in html
        assert "2024-01-01T00:00:00Z" in html

        # Verify coordinates are shown
        assert "(0,0)" in html
        assert "(1,1)" in html

        # Verify semantic structure
        assert 'scope="col"' in html
        assert 'scope="row"' in html

    def test_render_matrix_table_empty_cells(self):
        """Test handling of empty cells array."""
        snapshot_data = {"matrix_name": "EMPTY", "shape": [2, 2], "cells": []}

        html = render_matrix_table(snapshot_data, "EMPTY")
        assert "No cell data available" in html

    def test_render_matrix_table_invalid_shape(self):
        """Test handling of invalid shape."""
        snapshot_data = {"matrix_name": "INVALID", "shape": [0, 0], "cells": []}

        html = render_matrix_table(snapshot_data, "INVALID")
        assert "Invalid shape [0, 0]" in html

    def test_render_matrix_table_missing_cells(self):
        """Test handling of sparse matrix with missing cells."""
        snapshot_data = {
            "matrix_name": "SPARSE",
            "shape": [2, 2],
            "row_labels": ["Row1", "Row2"],
            "col_labels": ["Col1", "Col2"],
            "cells": [
                {
                    "row": 0,
                    "col": 0,
                    "value": "Only Value",
                    "provenance": {"operation": "test", "timestamp": "2024-01-01T00:00:00Z"},
                }
                # Missing cells for (0,1), (1,0), (1,1)
            ],
        }

        html = render_matrix_table(snapshot_data, "SPARSE")

        # Should contain the one valid cell
        assert "Only Value" in html
        # Should contain "No data" placeholders for missing cells
        assert "No data" in html


class TestWriteAssets:
    """Test the write_assets atomic write functionality."""

    def test_write_assets_creates_directory(self):
        """Test that output directory is created idempotently."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output" / "nested"
            html_content = "<html><body>Test</body></html>"

            # Directory should not exist initially
            assert not output_dir.exists()

            # Write assets should create it
            output_file = write_assets(html_content, output_dir)

            assert output_dir.exists()
            assert output_dir.is_dir()
            assert output_file == output_dir / "index.html"

    def test_write_assets_atomic_write(self):
        """Test that HTML content is written correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            html_content = "<html><body><h1>Test Content</h1></body></html>"

            output_file = write_assets(html_content, output_dir, "test.html")

            # Verify file exists and contains correct content
            assert output_file.exists()
            assert output_file.name == "test.html"

            with open(output_file, "r") as f:
                written_content = f.read()
                assert written_content == html_content


class TestLoadSnapshots:
    """Test snapshot loading functionality."""

    def test_load_snapshots_for_run(self):
        """Test loading multiple matrix snapshots from a run directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)

            # Create mock snapshot files
            snapshot_a = {
                "matrix_name": "A",
                "shape": [1, 1],
                "cells": [{"row": 0, "col": 0, "value": "test"}],
            }

            snapshot_c = {
                "matrix_name": "C",
                "shape": [1, 1],
                "cells": [{"row": 0, "col": 0, "value": "computed"}],
            }

            # Write snapshots
            with open(run_dir / "A-20250903-120000.jsonl", "w") as f:
                json.dump(snapshot_a, f)

            with open(run_dir / "C-20250903-120000.jsonl", "w") as f:
                json.dump(snapshot_c, f)

            # Load snapshots
            snapshots = load_snapshots_for_run(run_dir, ["A", "C"])

            assert len(snapshots) == 2
            assert "A" in snapshots
            assert "C" in snapshots
            assert snapshots["A"]["matrix_name"] == "A"
            assert snapshots["C"]["matrix_name"] == "C"

    def test_load_snapshots_with_newest_file(self):
        """Test that newest snapshot file is selected when multiple exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = Path(tmpdir)

            # Create multiple snapshots for same matrix (different timestamps)
            older_snapshot = {"matrix_name": "A", "cells": [{"value": "old"}]}
            newer_snapshot = {"matrix_name": "A", "cells": [{"value": "new"}]}

            with open(run_dir / "A-20250903-120000.jsonl", "w") as f:
                json.dump(older_snapshot, f)

            with open(run_dir / "A-20250903-140000.jsonl", "w") as f:
                json.dump(newer_snapshot, f)

            # Should load the newer snapshot
            snapshots = load_snapshots_for_run(run_dir, ["A"])

            assert len(snapshots) == 1
            assert snapshots["A"]["cells"][0]["value"] == "new"


class TestSanitizeValue:
    """Test the sanitize_value function."""

    def test_sanitize_validation_prefix(self):
        """Test removal of VALIDATION[...] prefix."""
        value = "VALIDATION[Stage 5] This is the actual content"
        result = sanitize_value(value)
        assert result == "This is the actual content"

    def test_sanitize_col_prefix(self):
        """Test removal of COL[...] prefix."""
        value = "COL[Guiding] Values and principles"
        result = sanitize_value(value)
        assert result == "Values and principles"

    def test_sanitize_row_prefix(self):
        """Test removal of ROW[...] prefix."""
        value = "ROW[Normative] Standards for evaluation"
        result = sanitize_value(value)
        assert result == "Standards for evaluation"

    def test_sanitize_multiple_prefixes(self):
        """Test that all defined prefixes are handled."""
        test_cases = [
            ("EVAL[Something] Test content", "Test content"),
            ("VERIFY[Check] Verification text", "Verification text"),
            ("SYNTH[Process] Synthesis result", "Synthesis result"),
            ("LENS[Column] Lensed perspective", "Lensed perspective"),
        ]

        for input_value, expected in test_cases:
            result = sanitize_value(input_value)
            assert result == expected

    def test_sanitize_no_prefix(self):
        """Test that values without prefixes are unchanged."""
        value = "Regular content without prefix"
        result = sanitize_value(value)
        assert result == value

    def test_sanitize_non_string(self):
        """Test handling of non-string values."""
        assert sanitize_value(123) == "123"
        assert sanitize_value(None) == "None"
        assert sanitize_value([1, 2, 3]) == "[1, 2, 3]"


class TestRenderElementsPage:
    """Test the Elements-style rendering functionality."""

    def test_render_elements_basic_structure(self):
        """Test that Elements page generates correct HTML structure."""
        snapshot_data = {
            "A": {
                "matrix_name": "A",
                "station": "Problem Statement",
                "shape": [2, 2],
                "resolver": "echo",
                "timestamp": "2024-01-01T00:00:00Z",
                "row_labels": ["Row1", "Row2"],
                "col_labels": ["Col1", "Col2"],
                "cells": [
                    {"row": 0, "col": 0, "value": "Value1"},
                    {"row": 0, "col": 1, "value": "Value2"},
                    {"row": 1, "col": 0, "value": "Value3"},
                    {"row": 1, "col": 1, "value": "Value4"},
                ],
            }
        }

        html = render_elements_page(snapshot_data, "test-run-123", "Test Title")

        # Check basic HTML structure
        assert "<!DOCTYPE html>" in html
        assert '<meta charset="UTF-8">' in html
        assert "<title>Test Title</title>" in html

        # Check header content
        assert "Run ID: test-run-123" in html
        assert "Resolver: echo" in html

        # Check Elements formatting
        assert "Elements[A] = [" in html
        assert "# Row1" in html
        assert "# Col1" in html
        assert '"Value1"' in html

        # Check CSS is included
        assert "Monaco" in html
        assert ".elements-grid" in html

    def test_render_elements_with_sanitization(self):
        """Test Elements rendering with value sanitization."""
        snapshot_data = {
            "C": {
                "matrix_name": "C",
                "shape": [1, 2],
                "row_labels": ["Test"],
                "col_labels": ["Col1", "Col2"],
                "cells": [
                    {"row": 0, "col": 0, "value": "VALIDATION[Stage5] Clean content"},
                    {"row": 0, "col": 1, "value": "COL[Guiding] More content"},
                ],
            }
        }

        # With sanitization (default behavior)
        html_clean = render_elements_page(snapshot_data, "test-run", sanitize=True)
        assert '"Clean content"' in html_clean
        assert '"More content"' in html_clean
        assert "VALIDATION[Stage5]" not in html_clean
        assert "COL[Guiding]" not in html_clean

        # Without sanitization (disabled)
        html_raw = render_elements_page(snapshot_data, "test-run", sanitize=False)
        assert "VALIDATION[Stage5] Clean content" in html_raw
        assert "COL[Guiding] More content" in html_raw

    def test_render_elements_canonical_order(self):
        """Test that matrices are rendered in canonical order."""
        # Create snapshots for matrices out of order
        snapshot_data = {
            "Z": {"matrix_name": "Z", "shape": [1, 1], "cells": []},
            "A": {"matrix_name": "A", "shape": [1, 1], "cells": []},
            "F": {"matrix_name": "F", "shape": [1, 1], "cells": []},
        }

        html = render_elements_page(snapshot_data, "test-run")

        # Find positions of each matrix header
        a_pos = html.find("Matrix A")
        f_pos = html.find("Matrix F")
        z_pos = html.find("Matrix Z")

        # Should be in canonical order: A, then F, then Z
        assert a_pos < f_pos < z_pos

    def test_render_elements_missing_matrix(self):
        """Test Elements rendering handles missing matrices gracefully."""
        snapshot_data = {"A": {"matrix_name": "A", "shape": [1, 1], "cells": []}}

        html = render_elements_page(snapshot_data, "test-run")

        # Should show A normally
        assert "Matrix A" in html

        # Should show "not found" for other matrices in canonical order
        assert "Snapshot not found" in html  # For missing matrices like B, J, etc.
