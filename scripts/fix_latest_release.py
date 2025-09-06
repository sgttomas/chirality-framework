#!/usr/bin/env python3
"""
Fix the latest release flag issue for the Chirality Framework.

This script addresses the issue where v17.1.0 was created successfully
but GitHub's "latest release" endpoint still returns v17.0.0.
"""

import subprocess
import sys
from pathlib import Path


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


def get_current_version():
    """Read current version from VERSION.md."""
    version_path = Path(__file__).parent.parent / "VERSION.md"
    try:
        with open(version_path, "r") as f:
            return f.readline().split("—")[0].strip()
    except Exception as e:
        print(f"❌ Error reading VERSION.md: {e}")
        return None


def check_releases():
    """Check current release status."""
    print("🔍 Checking current release status...")
    
    try:
        # Get latest release
        result = subprocess.run(
            ["gh", "release", "view", "--json", "tagName,publishedAt"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            import json
            latest_data = json.loads(result.stdout)
            print(f"📋 Current 'latest' release: {latest_data['tagName']}")
            print(f"   Published: {latest_data['publishedAt']}")
        else:
            print(f"⚠️  Could not get latest release: {result.stderr}")
            
        # List recent releases
        result = subprocess.run(
            ["gh", "release", "list", "--limit", "3"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print("\n📋 Recent releases:")
            print(result.stdout)
        else:
            print(f"⚠️  Could not list releases: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error checking releases: {e}")


def mark_release_as_latest(tag):
    """Mark a specific release as latest."""
    print(f"🚀 Marking {tag} as latest release...")
    
    try:
        # Use gh release edit to mark as latest
        cmd = ["gh", "release", "edit", tag, "--latest"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully marked {tag} as latest release!")
            return True
        else:
            print(f"❌ Failed to update release:")
            print(f"   stdout: {result.stdout}")
            print(f"   stderr: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating release: {e}")
        return False


def create_missing_release():
    """Create the missing v17.1.1 release to match VERSION.md."""
    current_version = get_current_version()
    if not current_version:
        return False
        
    tag = f"v{current_version}"
    print(f"🚀 Creating missing release {tag}...")
    
    # Extract changelog for this version
    changelog_path = Path(__file__).parent.parent / "CHANGELOG.md"
    release_notes = f"Release version {current_version}\n\nSee CHANGELOG.md for details."
    
    if changelog_path.exists():
        try:
            with open(changelog_path, "r") as f:
                content = f.read()
            
            version_header = f"## [{current_version}]"
            if version_header in content:
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
                    
                    version_content = '\n'.join(lines[start_idx+1:end_idx]).strip()
                    release_notes = f"# Chirality Framework v{current_version}\n\n{version_content}"
                    
        except Exception as e:
            print(f"⚠️  Could not extract changelog: {e}")
    
    try:
        cmd = [
            "gh", "release", "create", tag,
            "--title", f"Chirality Framework v{current_version}",
            "--notes", release_notes,
            "--latest"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Release {tag} created successfully!")
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
    print("🔧 Chirality Framework Release Fix Tool")
    print("=" * 50)
    
    if not check_gh_cli():
        return 1
    
    # Check current status
    check_releases()
    
    current_version = get_current_version()
    if not current_version:
        return 1
        
    print(f"\n📄 VERSION.md shows: {current_version}")
    
    # Check if we need to create v17.1.1 or fix v17.1.0
    if current_version == "17.1.1":
        print("\n🎯 Issue: VERSION.md shows 17.1.1 but no release exists")
        print("💡 Solution: Create v17.1.1 release")
        
        if input("\nCreate v17.1.1 release? (y/N): ").lower() == 'y':
            if create_missing_release():
                print("\n✅ Fixed! v17.1.1 is now the latest release.")
            else:
                print("\n❌ Failed to create v17.1.1 release.")
                return 1
    
    elif current_version == "17.1.0":
        print("\n🎯 Issue: v17.1.0 exists but not marked as latest")
        print("💡 Solution: Mark v17.1.0 as latest")
        
        if input("\nMark v17.1.0 as latest? (y/N): ").lower() == 'y':
            if mark_release_as_latest("v17.1.0"):
                print("\n✅ Fixed! v17.1.0 is now the latest release.")
            else:
                print("\n❌ Failed to mark v17.1.0 as latest.")
                return 1
    
    else:
        print(f"\n🤔 Unexpected version: {current_version}")
        print("Manual intervention may be required.")
        return 1
    
    # Verify the fix
    print("\n🔍 Verifying fix...")
    check_releases()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())