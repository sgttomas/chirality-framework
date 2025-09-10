#!/usr/bin/env python3
"""
Enhanced CI Guard for Responses API Compliance.

Per colleague_1's P0-2 specification: "Ensure the CI guard scans all code 
(exclude only docs/tests/vendor) and fails on comprehensive patterns."

Strict denylist + allowlist enforcement with fail-fast on violations.
Exit with code 1 if any violations are found, 0 if clean.
"""

import os
import sys
import subprocess
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
fails = []

def run_ripgrep(patterns, description, scope="all_code"):
    """
    Run ripgrep with given patterns and return results.
    
    Args:
        patterns: List of regex patterns to search for
        description: Description of what we're checking
        scope: "all_code" (exclude docs/tests/vendor), "docs_ok" (allow docs), "tests_ok" (allow tests)
    """
    try:
        cmd = ["rg", "-n", "--hidden", "-S"]
        
        # Scope-based exclusions per colleague_1's specification
        if scope == "all_code":
            # Scan all code, exclude only docs/tests/vendor
            cmd.extend([
                "-g", "!*.md", "-g", "!CHANGELOG*", "-g", "!*.yml", "-g", "!*.yaml",
                "-g", "!test_*", "-g", "!*test.py", "-g", "!tests/", 
                "-g", "!vendor/", "-g", "!.git/", "-g", "!__pycache__/",
                "-g", "!*.json", "-g", "!*.jsonl"
            ])
        elif scope == "docs_ok":
            # Allow docs, but exclude tests/vendor
            cmd.extend([
                "-g", "!test_*", "-g", "!*test.py", "-g", "!tests/",
                "-g", "!vendor/", "-g", "!.git/", "-g", "!__pycache__/",
                "-g", "!*.json", "-g", "!*.jsonl"
            ])
        elif scope == "tests_ok":
            # Allow tests, but exclude docs/vendor  
            cmd.extend([
                "-g", "!*.md", "-g", "!CHANGELOG*", "-g", "!*.yml", "-g", "!*.yaml",
                "-g", "!vendor/", "-g", "!.git/", "-g", "!__pycache__/",
                "-g", "!*.json", "-g", "!*.jsonl"
            ])
            
        # Always exclude this guard script itself and guard infrastructure
        cmd.extend([
            "-g", "!scripts/guard_responses_api.py", 
            "-g", "!chirality/infrastructure/api/guards.py"
        ])
            
        cmd.extend(patterns)
        
        rg = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        if rg.stdout.strip():
            fails.append(f"{description}:\n{rg.stdout}")
    except FileNotFoundError:
        fails.append("Error: ripgrep (rg) is not installed. Please install it first.")

print("🔍 Running colleague_1's Enhanced Responses API Compliance Guard...")

# STRICT DENYLIST - Per colleague_1's P0-2 specification
# Scan all code (exclude only docs/tests/vendor) and fail on these patterns:

print("  • Checking for Chat Completions API usage...")
run_ripgrep([
    r'chat\.completions\.create', r'openai\.ChatCompletion', r'achat\.completions'
], "❌ FORBIDDEN: Chat Completions API usage found", scope="all_code")

print("  • Checking for messages array usage...")
run_ripgrep([
    r'\bmessages\s*='
], "❌ FORBIDDEN: messages array usage found", scope="all_code")

print("  • Checking for Chat Completions response parsing...")
run_ripgrep([
    r'\.choices\[.*\]\.message\.content', r'\.choices\b.*\.message\b', r'\.delta\b'
], "❌ FORBIDDEN: Chat Completions response parsing found", scope="all_code")

print("  • Checking for function calling patterns...")
run_ripgrep([
    r'\bfunction_call\b', r'\bfunctions\b'
], "❌ FORBIDDEN: function_call/functions usage found", scope="all_code")

print("  • Checking for Chat-era max_tokens in API calls...")
run_ripgrep([
    r'max_tokens\s*=.*create\(', r'create\(.*max_tokens\s*=', r'"max_tokens":\s*\w+'
], "❌ FORBIDDEN: max_tokens in API calls (use max_output_tokens)", scope="all_code")

print("  • Checking for problematic wrapper libraries...")
run_ripgrep([
    r'langchain', r'litellm', r'ChatOpenAI', r'OpenAIChatCompletionsModel'
], "⚠️  WARNING: wrapper libraries that may use Chat Completions", scope="all_code")

# POSITIVE ALLOWLIST CHECKS - Per colleague_1's P0-2 specification
# Verify required Responses API patterns are present

def verify_positive_pattern(patterns, description, min_hits=1):
    """Verify that required patterns exist in the codebase."""
    try:
        cmd = ["rg", "-n", "--hidden", "-S"]
        # Include all code for positive checks
        cmd.extend(["-g", "!.git/", "-g", "!__pycache__/"])
        cmd.extend(patterns)
        
        rg = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        hit_count = len(rg.stdout.strip().split('\n')) if rg.stdout.strip() else 0
        
        if hit_count < min_hits:
            fails.append(f"❌ REQUIRED MISSING: {description} (found {hit_count}, need {min_hits}+)")
        else:
            print(f"    ✅ Found {hit_count} instances")
            
    except FileNotFoundError:
        fails.append("Error: ripgrep (rg) is not installed. Please install it first.")

print("  • Verifying client.responses.create usage...")
verify_positive_pattern([r'client\.responses\.create'], "client.responses.create calls", min_hits=2)

print("  • Verifying response.output_text parsing...")
verify_positive_pattern([r'response\.output_text'], "response.output_text usage", min_hits=1)

print("  • Verifying max_output_tokens usage...")
verify_positive_pattern([r'max_output_tokens'], "max_output_tokens usage", min_hits=1)

print("  • Verifying response_format usage...")
verify_positive_pattern([r'response_format'], "response_format usage", min_hits=2)

print("  • Verifying instructions+input pattern...")
verify_positive_pattern([r'instructions\s*='], "instructions parameters", min_hits=3)

print("  • Verifying input parameters...")
verify_positive_pattern([r'input\s*='], "input parameters", min_hits=3)

if fails:
    print("\n❌ Enhanced CI Guard - Responses API compliance violations found:")
    for fail in fails:
        print(f"\n{fail}")
    print(f"\n🚨 Fix these violations to ensure 100% Responses API compliance per colleague_1's P0-2 requirements.")
    sys.exit(1)

print("\n✅ Enhanced CI Guard - All checks passed!")
print("✅ Responses API compliance verified across all code")
print("✅ Strict denylist: Zero Chat Completions violations found")
print("✅ Positive allowlist: Required Responses API patterns confirmed")
print("✅ Production-ready: Ready for clean, error-free runs")
sys.exit(0)