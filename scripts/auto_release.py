#!/usr/bin/env python3
"""
Auto-create GitHub release for the current version.

This script will:
1. Read the current version from VERSION.md
2. Extract relevant changelog entries  
3. Create a GitHub release using the gh CLI tool
4. Trigger automatic PyPI deployment

Requires: gh CLI tool installed and authenticated
Install: https://cli.github.com/
"""

import subprocess
import sys
from pathlib import Path


def get_current_version():
    """Read current version from VERSION.md."""
    version_path = Path(__file__).parent.parent / "VERSION.md"
    try:
        with open(version_path, "r") as f:
            return f.readline().split("—")[0].strip()
    except Exception as e:
        print(f"❌ Error reading VERSION.md: {e}")
        return None


def extract_changelog_for_version(version):
    """Extract changelog entries for the current version."""
    changelog_path = Path(__file__).parent.parent / "CHANGELOG.md"
    if not changelog_path.exists():
        return f"Release version {version}"
    
    try:
        with open(changelog_path, "r") as f:
            content = f.read()
        
        # Find the section for this version
        version_header = f"## [{version}]"
        if version_header not in content:
            return f"Release version {version}\n\nSee CHANGELOG.md for details."
        
        # Extract content between this version and the next
        lines = content.split('\n')
        start_idx = None
        end_idx = None
        
        for i, line in enumerate(lines):
            if version_header in line:
                start_idx = i
            elif start_idx is not None and line.startswith("## [") and version_header not in line:
                end_idx = i
                break
        
        if start_idx is not None:
            if end_idx is None:
                end_idx = len(lines)
            
            # Get the content, skip the version header
            version_content = '\n'.join(lines[start_idx+1:end_idx]).strip()
            return f"# Chirality Framework v{version}\n\n{version_content}"
        
        return f"Release version {version}\n\nSee CHANGELOG.md for details."
        
    except Exception as e:
        print(f"⚠️  Could not extract changelog: {e}")
        return f"Release version {version}"


def check_gh_cli():
    """Check if gh CLI is installed and authenticated."""
    try:
        result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GitHub CLI authenticated")
            return True
        else:
            print("❌ GitHub CLI not authenticated. Run: gh auth login")
            return False
    except FileNotFoundError:
        print("❌ GitHub CLI not installed. Install from: https://cli.github.com/")
        return False
    except Exception as e:
        print(f"❌ Error checking GitHub CLI: {e}")
        return False


def create_release(version, release_notes):
    """Create GitHub release using gh CLI."""
    tag = f"v{version}"
    title = f"Chirality Framework v{version}"
    
    print(f"🚀 Creating release {tag}...")
    
    try:
        # Create the release
        cmd = [
            "gh", "release", "create", tag,
            "--title", title,
            "--notes", release_notes,
            "--latest"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Release created successfully!")
            print(f"   URL: https://github.com/sgttomas/chirality-framework/releases/tag/{tag}")
            print(f"   PyPI deployment will start automatically.")
            print(f"   Monitor: https://github.com/sgttomas/chirality-framework/actions")
            return True
        else:
            print(f"❌ Failed to create release:")
            print(f"   stdout: {result.stdout}")
            print(f"   stderr: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating release: {e}")
        return False


def main():
    """Main function."""
    print("🎯 Auto-Release for PyPI Deployment\n")
    
    # Check prerequisites
    version = get_current_version()
    if not version:
        sys.exit(1)
    
    if not check_gh_cli():
        print("\n💡 Alternative: Use manual approach:")
        print("   python scripts/create_release.py")
        sys.exit(1)
    
    # Get release notes
    release_notes = extract_changelog_for_version(version)
    
    print(f"📋 Release Details:")
    print(f"   Version: {version}")
    print(f"   Tag: v{version}")
    print(f"   Notes: {release_notes[:100]}{'...' if len(release_notes) > 100 else ''}")
    
    # Confirm
    confirm = input(f"\n❓ Create release v{version} and deploy to PyPI? [y/N]: ")
    if confirm.lower() not in ['y', 'yes']:
        print("❌ Cancelled by user")
        sys.exit(0)
    
    # Create release
    success = create_release(version, release_notes)
    
    if success:
        print(f"\n🎉 Success! Version {version} is being deployed to PyPI.")
        return 0
    else:
        print(f"\n💥 Failed to create release. Try manual approach:")
        print("   python scripts/create_release.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())