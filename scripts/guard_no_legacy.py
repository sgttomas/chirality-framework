#!/usr/bin/env python3
"""
Guard against legacy code paths, imports, and multiple CLI entrypoints.
Exit with code 1 if any violations are found, 0 if clean.
"""

import os
import sys
import subprocess
import tomllib
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
fails = []

# 1) Disallowed directories
# Note: chirality/lib is allowed but only for logging.py (production infrastructure)
for d in ["chirality/core"]:
    if (ROOT / d).exists():
        fails.append(f"Disallowed directory present: {d}")

# Check that lib only contains allowed files
lib_path = ROOT / "chirality/lib"
if lib_path.exists():
    allowed_lib_files = {"__init__.py", "logging.py", "__pycache__"}
    actual_files = {f.name for f in lib_path.iterdir()}
    unauthorized = actual_files - allowed_lib_files
    if unauthorized:
        fails.append(f"Unauthorized files in chirality/lib: {unauthorized}")

# 2) Disallowed imports
# Note: ONLY lib.logging imports are allowed (production infrastructure)
patterns = [
    r"chirality\.core\.",
    r"chirality\.lib\.(?!logging\b)",  # Allow lib.logging but nothing else (strict word boundary)
    r"from\s+chirality\.lib\s+import\s+(?!logging\b)",  # Block "from chirality.lib import X" unless X is logging
    r"application\.services\.pipeline_service"
]
try:
    rg = subprocess.run(
        ["rg", "-n", "--no-heading", "-g", "*.py", "|".join(patterns), "chirality"],
        capture_output=True,
        text=True,
        cwd=ROOT
    )
    if rg.stdout.strip():
        fails.append("Disallowed imports found:\n" + rg.stdout)
except FileNotFoundError:
    fails.append("Error: ripgrep (rg) is not installed. Please install it first.")

# 3) Single CLI entrypoint
try:
    ppt_path = ROOT / "pyproject.toml"
    if ppt_path.exists():
        ppt = tomllib.loads(ppt_path.read_text())
        scripts = ppt.get("project", {}).get("scripts", {})
        if scripts != {"chirality": "chirality.interfaces.cli:main"}:
            fails.append(
                "Project scripts must define exactly one entrypoint: "
                "chirality=chirality.interfaces.cli:main\n"
                f"Current scripts: {scripts}"
            )
except Exception as e:
    fails.append(f"Error reading pyproject.toml: {e}")

if fails:
    print("\n".join(fails))
    sys.exit(1)

print("No-legacy guard passed.")
sys.exit(0)