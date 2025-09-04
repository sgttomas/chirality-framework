import json
from pathlib import Path

from chirality.core.types import Cell, Matrix
from chirality.exporters.snapshot_exporter import MatrixSnapshotWriter


def _matrix_2x2(name: str, station: str) -> Matrix:
    rows = ["R1", "R2"]
    cols = ["C1", "C2"]
    cells = [
        [Cell(0, 0, "v00", {}), Cell(0, 1, "v01", {})],
        [Cell(1, 0, "v10", {}), Cell(1, 1, "v11", {})],
    ]
    return Matrix(name=name, station=station, row_labels=rows, col_labels=cols, cells=cells)


def test_write_matrix_cells_jsonl(tmp_path: Path):
    m = _matrix_2x2("C", "Problem Requirements")
    writer = MatrixSnapshotWriter("t123")
    out = tmp_path / "out"
    path = writer.write_matrix_cells_jsonl(m, out, "C.jsonl")
    assert path.exists()

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    # Expect 4 lines (2x2)
    assert len(lines) == 4
    first = json.loads(lines[0])
    assert first["id"] == "C:r0:c0"
    assert first["matrix"] == "C"
    assert first["row"] == 0 and first["col"] == 0
    assert first["row_label"] == "R1"
    assert first["col_label"] == "C1"
    assert first["station"] == "Problem Requirements"
    assert first["text"] == "v00"
    assert first["citations"] == [] and first["refs"] == []
    assert isinstance(first["meta"].get("order"), int)

