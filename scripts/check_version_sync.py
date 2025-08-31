#!/usr/bin/env python3
"""
Version synchronization checker for Chirality Framework.

Ensures that the version in VERSION.md matches the version in pyproject.toml
to prevent deployment issues where the wrong version gets packaged.
"""

import sys
import tomllib
from pathlib import Path


def get_version_from_version_md() -> str:
    """Read version from VERSION.md file."""
    version_path = Path(__file__).parent.parent / "VERSION.md"
    try:
        with open(version_path, "r") as f:
            # First line should be like "16.0.0 — See full history in CHANGELOG.md"
            return f.readline().split("—")[0].strip()
    except Exception as e:
        print(f"Error reading VERSION.md: {e}")
        return ""


def get_version_from_pyproject() -> str:
    """Read version from pyproject.toml file."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            return data.get("project", {}).get("version", "")
    except Exception as e:
        print(f"Error reading pyproject.toml: {e}")
        return ""


def main():
    """Check if versions are synchronized."""
    version_md = get_version_from_version_md()
    version_pyproject = get_version_from_pyproject()
    
    print(f"VERSION.md: {version_md}")
    print(f"pyproject.toml: {version_pyproject}")
    
    if version_md != version_pyproject:
        print(f"\nERROR: Version mismatch!")
        print(f"VERSION.md has '{version_md}' but pyproject.toml has '{version_pyproject}'")
        print(f"Please update pyproject.toml version to match VERSION.md")
        sys.exit(1)
    
    print(f"\n✅ Versions are synchronized: {version_md}")
    return 0


if __name__ == "__main__":
    main()