import json
import hashlib
from pathlib import Path

from chirality.exporters.manifest_exporter import ManifestExporter


def _write_lines(p: Path, lines: list[str]):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)
            if not line.endswith("\n"):
                f.write("\n")


def _sha256_text(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def test_manifest_exporter_writes_expected_index(tmp_path: Path):
    run_dir = tmp_path / "runs" / "sample_run_001"
    snaps = run_dir / "snapshots"
    c = snaps / "C.jsonl"
    d = snaps / "D.jsonl"
    x = snaps / "X.jsonl"
    e = snaps / "E.jsonl"

    _write_lines(c, ['{"v":1}', '{"v":2}'])
    _write_lines(d, ['{"v":3}'])
    _write_lines(x, ['{"v":4}', '{"v":5}', '{"v":6}'])
    _write_lines(e, ['{"v":7}'])

    files = {
        "C": (c, "cells-jsonl-v1"),
        "D": (d, "cells-jsonl-v1"),
        "X": (x, "cells-jsonl-v1"),
        "E": (e, "cells-jsonl-v1"),
    }

    exporter = ManifestExporter(
        run_dir, "chirality-framework", "0.0-test", framework_schema_version="1.0.0"
    )
    manifest_path = exporter.write_manifest(
        run_id="sample_run_001",
        problem={"title": "T", "statement": "S"},
        durations={"total_ms": 123},
        matrices=files,
    )

    assert manifest_path.exists()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert data["run_id"] == "sample_run_001"
    assert data["tool"]["name"] == "chirality-framework"
    assert data["framework_schema_version"] == "1.0.0"
    mats = data["matrices"]
    assert set(mats.keys()) == {"C", "D", "X", "E"}
    # Check one entry thoroughly
    cmeta = mats["C"]
    assert cmeta["format"] == "cells-jsonl-v1"
    assert cmeta["path"] == "snapshots/C.jsonl"
    assert cmeta["records"] == 2
    assert cmeta["bytes"] == c.stat().st_size
    assert cmeta["sha256"] == _sha256_text(c)
