#!/usr/bin/env python3
"""
Reconcile prompt assets metadata (sha256, size_bytes, last_modified).

Usage:
  - Dry run (check only):  python scripts/reconcile_assets.py --check
  - Write updates:         python scripts/reconcile_assets.py --write

Updates chirality/infrastructure/prompts/assets/metadata.yml deterministically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any

import yaml


ASSETS_DIR = Path(__file__).resolve().parents[1] / "chirality" / "infrastructure" / "prompts" / "assets"
METADATA_FILE = ASSETS_DIR / "metadata.yml"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def isoformat_file_mtime(path: Path) -> str:
    ts = path.stat().st_mtime
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile prompt assets metadata")
    parser.add_argument("--check", action="store_true", help="Check for drift; non-zero exit on mismatch")
    parser.add_argument("--write", action="store_true", help="Write updates to metadata.yml")
    args = parser.parse_args()

    if not METADATA_FILE.exists():
        print(f"metadata.yml not found at {METADATA_FILE}")
        return 2

    meta = yaml.safe_load(METADATA_FILE.read_text()) or {}
    assets = meta.get("assets", [])
    changed = False

    for entry in assets:
        asset_path = ASSETS_DIR / entry["path"]
        if not asset_path.exists():
            print(f"WARN: missing asset file {asset_path} for id={entry.get('id')}")
            continue

        new_sha = sha256_file(asset_path)
        new_size = asset_path.stat().st_size
        new_mtime = isoformat_file_mtime(asset_path)

        if entry.get("sha256") != new_sha or entry.get("size_bytes") != new_size:
            changed = True
            print(f"update: {entry['id']}: sha256/size drift detected")
            entry["sha256"] = new_sha
            entry["size_bytes"] = new_size
            entry["last_modified"] = new_mtime

    if args.check:
        if changed:
            print("DRIFT: metadata.yml is out of sync with assets")
            return 1
        print("OK: metadata.yml matches assets")
        return 0

    if args.write and changed:
        # Write with stable ordering
        METADATA_FILE.write_text(yaml.dump(meta, sort_keys=True))
        print(f"Wrote updates to {METADATA_FILE}")
        return 0

    print("No changes needed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

