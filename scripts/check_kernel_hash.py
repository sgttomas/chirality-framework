#!/usr/bin/env python3
"""
Check that the kernel hash in the manifest matches the computed hash.
Exit with code 2 if mismatch, 1 if missing, 0 if matching.
"""

import sys
import pathlib
import yaml

# Add parent directory to path to import chirality modules
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from chirality.infrastructure.prompts.registry import get_registry

ROOT = pathlib.Path(__file__).resolve().parents[1]
manifest_path = ROOT / "artifacts/prompts_assets.manifest.yaml"

if not manifest_path.exists():
    print(f"Missing {manifest_path}")
    sys.exit(1)

try:
    reg = get_registry()
    computed = reg.compute_kernel_hash()
except Exception as e:
    print(f"Error computing kernel hash: {e}")
    sys.exit(1)

try:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    recorded = manifest.get("kernel_hash")
except Exception as e:
    print(f"Error reading manifest: {e}")
    sys.exit(1)

if not recorded:
    print("Manifest missing kernel_hash")
    sys.exit(1)

if computed != recorded:
    print("Kernel hash mismatch:")
    print(f"  computed: {computed}")
    print(f"  recorded: {recorded}")
    print("Run: chirality assets verify (or regenerate manifest) and commit.")
    sys.exit(2)

print("Kernel hash check passed.")
sys.exit(0)
