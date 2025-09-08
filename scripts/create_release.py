#!/usr/bin/env python3
"""
Helper script to create GitHub releases for PyPI deployment.

This script reads the current version from VERSION.md and provides
the appropriate GitHub release URL for easy deployment.
"""

import sys
from pathlib import Path


def get_current_version():
    """Read current version from VERSION.md."""
    version_path = Path(__file__).parent.parent / "VERSION.md"
    try:
        with open(version_path, "r") as f:
            # First line should be like "16.2.0 — See full history in CHANGELOG.md"
            return f.readline().split("—")[0].strip()
    except Exception as e:
        print(f"Error reading VERSION.md: {e}")
        return None


def main():
    """Generate release creation URL and instructions."""
    version = get_current_version()
    if not version:
        sys.exit(1)

    tag = f"v{version}"
    repo_url = "https://github.com/sgttomas/chirality-framework"
    release_url = f"{repo_url}/releases/new?tag={tag}&title=Chirality%20Framework%20{tag}"

    print(f"📦 Current version: {version}")
    print(f"🏷️  Release tag: {tag}")
    print()
    print("To deploy to PyPI:")
    print(f"1. Click: {release_url}")
    print("2. Add release notes (copy from CHANGELOG.md)")
    print("3. Click 'Publish release'")
    print("4. Monitor deployment: https://github.com/sgttomas/chirality-framework/actions")
    print()
    print("The PyPI deployment will start automatically when you publish the release!")


if __name__ == "__main__":
    main()
