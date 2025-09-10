#!/usr/bin/env python3
"""
P1-8: Asset Linting - Ban ChatML markers & framework metadata tokens.

Per colleague_1's specification: "Add a quick lint to fail if any prompt asset 
contains ChatML remnants (e.g., <|system|>, System: headers) or framework 
metadata tokens (e.g., system_sha, source:)."

This script scans all prompt assets for forbidden patterns and fails if any are found.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple


# ChatML patterns - various formats that should not appear in prompt assets
CHATML_PATTERNS = [
    # Standard ChatML format
    r'<\|system\|>',
    r'<\|user\|>',
    r'<\|assistant\|>',
    r'<\|end\|>',
    
    # Alternative ChatML formats
    r'<\|im_start\|>',
    r'<\|im_end\|>',
    
    # Role-based headers that suggest ChatML structure
    r'^System:',
    r'^User:',
    r'^Assistant:',
    r'^Human:',
    r'^AI:',
    
    # OpenAI-style message format indicators
    r'"role":\s*"system"',
    r'"role":\s*"user"',
    r'"role":\s*"assistant"',
    r'"content":\s*"',
    
    # Function calling format
    r'"function_call"',
    r'"functions"',
    r'"name":\s*"[^"]+"\s*,\s*"description"',
]

# Framework metadata tokens that pollute LLM transcripts
METADATA_TOKENS = [
    # System identification and versioning
    r'system_sha',
    r'kernel_hash',
    r'framework_version',
    r'chirality_version',
    
    # Source tracking
    r'source:',
    r'generated_at',
    r'generated_by',
    r'timestamp:',
    
    # Framework delimiters
    r'<<<BEGIN',
    r'>>>END',
    r'===START',
    r'===END',
    
    # Provenance metadata
    r'provenance:',
    r'trace_id',
    r'session_id',
    r'run_id',
    
    # Debug/development markers
    r'DEBUG:',
    r'TODO:',  # Should use proper TODO tracking, not in prompts
    r'FIXME:',
    r'HACK:',
    
    # Template engine artifacts
    r'\{\{[^}]*_metadata[^}]*\}\}',
    r'\{\{[^}]*_system[^}]*\}\}',
    r'\{\{[^}]*_framework[^}]*\}\}',
]


def find_assets_directory() -> Path:
    """Find the prompt assets directory."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    assets_dir = project_root / "chirality" / "infrastructure" / "prompts" / "assets"
    
    if not assets_dir.exists():
        raise FileNotFoundError(f"Prompt assets directory not found: {assets_dir}")
    
    return assets_dir


def scan_file_for_violations(file_path: Path, patterns: List[str]) -> List[Tuple[int, str, str]]:
    """
    Scan a file for pattern violations.
    
    Args:
        file_path: Path to the file to scan
        patterns: List of regex patterns to check
        
    Returns:
        List of (line_number, matched_text, pattern) tuples for violations
    """
    violations = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        violations.append((line_num, match.group(), pattern))
    
    except UnicodeDecodeError:
        # Skip binary files
        pass
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}", file=sys.stderr)
    
    return violations


def lint_prompt_assets() -> bool:
    """
    Lint all prompt assets for ChatML markers and framework metadata tokens.
    
    Returns:
        True if no violations found, False if violations detected
    """
    assets_dir = find_assets_directory()
    
    print("🔍 Scanning prompt assets for ChatML markers and framework metadata tokens...")
    print(f"   Assets directory: {assets_dir}")
    
    # Find all asset files (markdown, yaml, txt)
    asset_extensions = {'.md', '.yml', '.yaml', '.txt'}
    asset_files = []
    
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            if Path(file).suffix.lower() in asset_extensions:
                asset_files.append(Path(root) / file)
    
    print(f"   Found {len(asset_files)} asset files to scan")
    
    # Track violations
    chatml_violations = {}
    metadata_violations = {}
    
    # Scan each file
    for file_path in asset_files:
        # Check for ChatML violations
        chatml_issues = scan_file_for_violations(file_path, CHATML_PATTERNS)
        if chatml_issues:
            chatml_violations[file_path] = chatml_issues
        
        # Check for metadata violations
        metadata_issues = scan_file_for_violations(file_path, METADATA_TOKENS)
        if metadata_issues:
            metadata_violations[file_path] = metadata_issues
    
    # Report violations
    has_violations = False
    
    if chatml_violations:
        has_violations = True
        print("\n❌ ChatML VIOLATIONS DETECTED:")
        print("   Prompt assets must not contain ChatML markers or role headers.")
        print("   Use conversational format with <User> and <llm> tags instead.")
        
        for file_path, violations in chatml_violations.items():
            rel_path = file_path.relative_to(assets_dir.parent.parent.parent)
            print(f"\n   📄 {rel_path}:")
            for line_num, matched_text, pattern in violations:
                print(f"     Line {line_num}: '{matched_text}' (matches: {pattern})")
    
    if metadata_violations:
        has_violations = True
        print("\n❌ FRAMEWORK METADATA VIOLATIONS DETECTED:")
        print("   Prompt assets must not contain framework metadata tokens.")
        print("   Keep prompts semantically pure without system identification.")
        
        for file_path, violations in metadata_violations.items():
            rel_path = file_path.relative_to(assets_dir.parent.parent.parent)
            print(f"\n   📄 {rel_path}:")
            for line_num, matched_text, pattern in violations:
                print(f"     Line {line_num}: '{matched_text}' (matches: {pattern})")
    
    # Summary
    if has_violations:
        print(f"\n❌ ASSET LINTING FAILED")
        print(f"   ChatML violations in {len(chatml_violations)} files")
        print(f"   Metadata violations in {len(metadata_violations)} files")
        print("\n   REMEDIATION:")
        print("   1. Remove all ChatML markers (<|system|>, <|user|>, etc.)")
        print("   2. Remove role headers (System:, User:, Assistant:)")
        print("   3. Remove framework metadata tokens (system_sha, source:, etc.)")
        print("   4. Use only conversational format: <User> and <llm> tags")
        print("   5. Keep prompts semantically pure without system identification")
        return False
    
    else:
        print(f"\n✅ ASSET LINTING PASSED")
        print(f"   Scanned {len(asset_files)} files")
        print("   No ChatML markers found")
        print("   No framework metadata tokens found")
        print("   All prompt assets are semantically clean")
        return True


def main():
    """Main entry point for asset linting."""
    try:
        success = lint_prompt_assets()
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ ASSET LINTING ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()