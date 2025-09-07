#!/usr/bin/env python3
"""
Update SHA256 checksums and fix file paths for all prompt assets in metadata.yml.
Run this after modifying any prompt files to keep tests passing.
"""

import hashlib
import yaml
from pathlib import Path
from datetime import datetime, timezone
import sys


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def fix_metadata_and_update_checksums(verbose: bool = True):
    """Fix file paths and update all checksums in metadata.yml."""
    # Find the prompt_assets directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    assets_dir = project_root / "chirality" / "prompt_assets"
    metadata_path = assets_dir / "metadata.yml"
    
    if not metadata_path.exists():
        print(f"❌ Error: metadata.yml not found at {metadata_path}")
        sys.exit(1)
    
    # Define the correct file mappings based on actual files
    # Using a list format that prompt_registry.py expects
    assets_config = [
        {'id': 'system', 'path': 'system.md'},
        {'id': 'station_brief.requirements', 'path': 'station_briefs/requirements.md'},
        {'id': 'station_brief.objectives', 'path': 'station_briefs/objectives.md'},
        {'id': 'station_brief.verification', 'path': 'station_briefs/verification.md'},
        {'id': 'station_brief.validation', 'path': 'station_briefs/validation.md'},
        {'id': 'station_brief.evaluation', 'path': 'station_briefs/evaluation.md'},
        {'id': 'stage2_multiply', 'path': 'stage2_multiply.md'},  # Was: ops/operators/multiply.md
        {'id': 'stage2_elementwise', 'path': 'stage2_elementwise.md'},  # Was: ops/operators/elementwise.md
        {'id': 'combined_lens', 'path': 'combined_lens.md'},  # Was: ops/lensing/combined.md
        {'id': 'station_shift', 'path': 'station_shift.md'},  # Replaces lens_shift_z
    ]
    
    # Create new metadata structure with list format
    new_metadata = {
        'registry_version': '1.0',
        'assets': []
    }
    
    updated_count = 0
    missing_count = 0
    
    print("🔍 Fixing metadata.yml file paths and checksums...\n")
    
    # Process each expected asset
    for asset_config in assets_config:
        asset_id = asset_config['id']
        correct_path = asset_config['path']
        file_path = assets_dir / correct_path
        
        if not file_path.exists():
            print(f"⚠️  Warning: Expected file not found: {correct_path} (asset: {asset_id})")
            missing_count += 1
            continue
        
        # Calculate current file stats
        content = file_path.read_bytes()
        current_sha256 = calculate_sha256(file_path)
        current_size = len(content)
        
        # Create asset entry in list format
        asset_info = {
            'id': asset_id,
            'path': correct_path,
            'sha256': current_sha256,
            'version': '1.0.0',
            'size_bytes': current_size,
            'last_modified': datetime.now(timezone.utc).isoformat()
        }
        
        new_metadata['assets'].append(asset_info)
        
        if verbose:
            print(f"✅ Updated: {asset_id}")
            print(f"   Path: {correct_path}")
            print(f"   SHA256: {current_sha256[:32]}...")
            print(f"   Size: {current_size} bytes")
            print()
        
        updated_count += 1
    
    # Save updated metadata with correct list structure
    with open(metadata_path, 'w') as f:
        yaml.dump(new_metadata, f, default_flow_style=False, sort_keys=False, width=120)
    
    # Summary
    print("=" * 50)
    print(f"📊 Summary:")
    print(f"   Fixed paths and updated: {updated_count} assets")
    if missing_count > 0:
        print(f"   Missing files: {missing_count}")
    print(f"   Removed obsolete: lens_shift_z (replaced by station_shift)")
    print(f"\n✅ metadata.yml has been completely rebuilt with:")
    print(f"   - Correct file paths")
    print(f"   - Updated SHA256 checksums")
    print(f"   - Proper list structure for prompt_registry.py")
    print(f"   Path: {metadata_path}")
    
    # List all .md files to check we got everything
    print("\n📁 Verification - All .md files in prompt_assets:")
    tracked_paths = {asset['path'] for asset in new_metadata['assets']}
    for md_file in sorted(assets_dir.rglob("*.md")):
        relative_path = str(md_file.relative_to(assets_dir))
        tracked = relative_path in tracked_paths
        status = "✅" if tracked else "❌"
        print(f"   {status} {relative_path}")
    
    return updated_count


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix metadata paths and update SHA256 checksums")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show all files checked")
    
    args = parser.parse_args()
    
    # Fix metadata and update checksums
    updated = fix_metadata_and_update_checksums(verbose=True)  # Always verbose for this operation
    
    # Exit with status code
    sys.exit(0)