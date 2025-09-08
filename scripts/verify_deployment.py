#!/usr/bin/env python3
"""
PyPI deployment verification script.

This script checks that all components needed for PyPI deployment are properly configured.
"""

import json
import sys
import tomllib
import yaml
from pathlib import Path


def check_version_sync():
    """Check if VERSION.md and pyproject.toml are synchronized."""
    print("🔍 Checking version synchronization...")

    # Read VERSION.md
    version_path = Path("VERSION.md")
    if not version_path.exists():
        print("❌ VERSION.md not found")
        return False

    with open(version_path, "r") as f:
        version_md = f.readline().split("—")[0].strip()

    # Read pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        return False

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
        version_toml = data.get("project", {}).get("version", "")

    if version_md == version_toml:
        print(f"✅ Versions synchronized: {version_md}")
        return version_md
    else:
        print(f"❌ Version mismatch: VERSION.md={version_md}, pyproject.toml={version_toml}")
        return False


def check_workflow():
    """Check if the workflow file is valid."""
    print("🔍 Checking GitHub Actions workflow...")

    workflow_path = Path(".github/workflows/python-publish.yml")
    if not workflow_path.exists():
        print("❌ Workflow file not found")
        return False

    try:
        with open(workflow_path, "r") as f:
            workflow = yaml.safe_load(f)

        # Check if it has both release and workflow_dispatch triggers
        # Note: 'on' becomes True in YAML parsing, so we check for both keys
        on_events = workflow.get("on", workflow.get(True, {}))
        has_release = "release" in on_events
        has_dispatch = "workflow_dispatch" in on_events

        if has_release and has_dispatch:
            print("✅ Workflow configured for both releases and manual deployment")
            return True
        else:
            print(f"❌ Workflow missing triggers: release={has_release}, dispatch={has_dispatch}")
            return False

    except Exception as e:
        print(f"❌ Workflow YAML error: {e}")
        return False


def check_pypi_status(version):
    """Check current PyPI status."""
    print("🔍 Checking PyPI status...")
    try:
        import urllib.request

        url = "https://pypi.org/pypi/chirality-framework/json"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            pypi_version = data["info"]["version"]

        if pypi_version == version:
            print(f"✅ PyPI is up to date: {pypi_version}")
            return True
        else:
            print(f"📦 PyPI has {pypi_version}, local is {version} - deployment needed")
            return False
    except Exception as e:
        print(f"⚠️  Could not check PyPI status: {e}")
        return None


def main():
    """Run all checks."""
    print("🚀 PyPI Deployment Verification\n")

    version = check_version_sync()
    if not version:
        sys.exit(1)

    workflow_ok = check_workflow()
    if not workflow_ok:
        sys.exit(1)

    pypi_status = check_pypi_status(version)

    print("\n📋 Summary:")
    print(f"   Version: {version}")
    print(f"   Workflow: {'✅ Ready' if workflow_ok else '❌ Issues'}")
    print(
        f"   PyPI: {'✅ Current' if pypi_status else '📦 Needs deployment' if pypi_status is False else '❓ Unknown'}"
    )

    if not pypi_status:
        print(f"\n🎯 To deploy version {version}:")
        print("   python scripts/create_release.py")

    return 0 if workflow_ok else 1


if __name__ == "__main__":
    sys.exit(main())
