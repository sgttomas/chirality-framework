#!/usr/bin/env python3
"""
Check for banned legacy imports in the codebase.
Exit with code 2 if any are found, 0 if clean.
"""

import sys
import subprocess
import re
import pathlib

BANNED = [
    r"^from\s+chirality\.core(\.| import )",
    r"^import\s+chirality\.core(\.|$)",
    r"^from\s+chirality\.lib\.(?!logging\b)(.*?)(\s+import|\.|$)",  # Allow ONLY lib.logging
    r"^import\s+chirality\.lib\.(?!logging\b)",  # Allow ONLY lib.logging
    r"^from\s+chirality\.lib\s+import\s+(?!logging\b)",  # Block "from chirality.lib import X" unless X is logging
    r"application\.services\.pipeline_service",
]


def grep(patterns):
    """Search for patterns in Python files."""
    pat = "|".join(f"({p})" for p in patterns)
    try:
        result = subprocess.run(
            ["rg", "-n", "--no-heading", "-g", "*.py", pat, "chirality"],
            capture_output=True,
            text=True,
        )
        return result.stdout
    except FileNotFoundError:
        print("Error: ripgrep (rg) is not installed. Please install it first.")
        sys.exit(1)


def main():
    hits = grep(BANNED)
    if hits.strip():
        print("Disallowed imports found:\n" + hits)
        print("\nRun your local fix to replace/remove these imports before committing.")
        sys.exit(2)

    print("OK: no legacy imports found.")
    sys.exit(0)


if __name__ == "__main__":
    main()
