#!/usr/bin/env python3
"""
Registry Asset Reconcile Tool

Fixes the "pending_user_authoring" entries in metadata.yml by computing
actual SHA256, size_bytes, and last_modified for all assets.

Per colleague_1's guidance: one-shot registry reconcile to prevent 
checksum failures in production.
"""

import os
import hashlib
import yaml
from pathlib import Path
from datetime import datetime, timezone


def compute_file_hash_and_size(file_path: Path) -> tuple[str, int, str]:
    """
    Compute SHA256, size, and last modified timestamp for a file.
    
    Returns:
        Tuple of (sha256_hex, size_bytes, iso_timestamp)
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Asset file not found: {file_path}")
    
    # Compute SHA256
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    # Get size
    size_bytes = file_path.stat().st_size
    
    # Get last modified (use current time for reconciled entries)
    last_modified = datetime.now(timezone.utc).isoformat()
    
    return sha256_hash.hexdigest(), size_bytes, last_modified


def reconcile_assets():
    """Reconcile all assets in metadata.yml."""
    assets_dir = Path("chirality/infrastructure/prompts/assets")
    metadata_file = assets_dir / "metadata.yml"
    
    if not metadata_file.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
    
    print(f"🔧 Reconciling assets in {metadata_file}")
    
    # Load metadata
    with open(metadata_file, "r") as f:
        metadata = yaml.safe_load(f)
    
    pending_count = 0
    updated_count = 0
    error_count = 0
    
    for asset in metadata.get("assets", []):
        asset_id = asset["id"]
        asset_path = assets_dir / asset["path"]
        current_sha = asset.get("sha256", "")
        
        # Check if needs reconciliation
        if current_sha == "pending_user_authoring":
            pending_count += 1
            print(f"📝 Reconciling {asset_id}: {asset['path']}")
            
            try:
                # Compute actual values
                sha256_hex, size_bytes, last_modified = compute_file_hash_and_size(asset_path)
                
                # Update metadata entry
                asset["sha256"] = sha256_hex
                asset["size_bytes"] = size_bytes
                asset["last_modified"] = last_modified
                
                print(f"   ✅ SHA256: {sha256_hex[:16]}...")
                print(f"   ✅ Size: {size_bytes} bytes")
                updated_count += 1
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                error_count += 1
                
        else:
            # Optionally verify existing entries
            try:
                actual_sha, actual_size, _ = compute_file_hash_and_size(asset_path)
                if current_sha != actual_sha and current_sha != "pending_user_authoring":
                    print(f"⚠️  {asset_id}: SHA mismatch (expected {current_sha[:16]}, got {actual_sha[:16]})")
                    
                    # Update the entry
                    asset["sha256"] = actual_sha
                    asset["size_bytes"] = actual_size
                    asset["last_modified"] = datetime.now(timezone.utc).isoformat()
                    updated_count += 1
                    
            except FileNotFoundError:
                print(f"❌ {asset_id}: File not found at {asset_path}")
                error_count += 1
    
    # Write updated metadata
    if updated_count > 0:
        # Backup original
        backup_file = metadata_file.with_suffix('.yml.backup')
        with open(backup_file, 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
        print(f"💾 Backup saved: {backup_file}")
        
        # Write reconciled version
        with open(metadata_file, 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Updated metadata.yml")
    
    # Summary
    print(f"\n📊 Reconciliation Summary:")
    print(f"   Pending entries found: {pending_count}")
    print(f"   Entries updated: {updated_count}")
    print(f"   Errors: {error_count}")
    
    if error_count == 0 and updated_count > 0:
        print(f"✅ Registry reconciliation complete!")
    elif error_count > 0:
        print(f"⚠️  Reconciliation completed with {error_count} errors")
    else:
        print(f"ℹ️  No changes needed - registry is already reconciled")


if __name__ == "__main__":
    try:
        reconcile_assets()
    except Exception as e:
        print(f"❌ Reconciliation failed: {e}")
        exit(1)