# Release Issue Analysis and Solution

## Problem Statement
The commit `ef9c42b` that was approved 1 hour ago is not showing as the "Current Release" on the project front page.

## Root Cause Analysis

### What I Found:
1. **Commit `ef9c42b`** corresponds to the **v17.1.0 release** (not v17.1.1)
2. **v17.1.0 release EXISTS** and was created successfully:
   - Release ID: 245294420
   - Created: 2025-09-06T18:41:47Z
   - Published: 2025-09-06T18:43:09Z
   - Status: `"draft":false, "prerelease":false`
   - PyPI deployment: Completed successfully

3. **GitHub API Inconsistency**:
   - `list_releases` API: Returns v17.1.0 as the FIRST (most recent) release ✅
   - `get_latest_release` API: Returns v17.0.0 as the "latest" release ❌

### The Core Issue:
**GitHub's "latest release" endpoint is not recognizing v17.1.0 as the latest release despite being created with the `--latest` flag.**

This is a GitHub API caching/synchronization issue where:
- The release was created correctly with `gh release create v17.1.0 --latest`
- The workflow completed successfully
- But GitHub's latest release endpoint hasn't updated

## Secondary Issues Found:
1. **VERSION.md** shows `17.1.1` but no `v17.1.1` release exists
2. There's a version sync issue between VERSION.md and actual releases

## Solutions

### Immediate Fix (Primary Issue):
```bash
# Mark v17.1.0 as latest (requires GitHub CLI authentication)
gh release edit v17.1.0 --latest
```

### Complete Fix (Both Issues):
```bash
# Option 1: Create v17.1.1 to match VERSION.md
gh release create v17.1.1 --title "Chirality Framework v17.1.1" --notes "Release version 17.1.1" --latest

# Option 2: Update VERSION.md to match current release
echo "17.1.0 — See full history in CHANGELOG.md" > VERSION.md
```

### Verification:
```bash
# Check that the fix worked
gh release view --json tagName,publishedAt
gh release list --limit 3
```

## Files Created:
- `scripts/fix_latest_release.py` - Automated diagnostic and fix tool

## Workflow Status:
- ✅ v17.1.0 release creation: SUCCESS
- ✅ PyPI deployment: SUCCESS  
- ❌ GitHub latest release flag: FAILED (API inconsistency)

## Recommended Action:
Run the automated fix script with GitHub authentication:
```bash
python3 scripts/fix_latest_release.py
```

This will either:
1. Create the missing v17.1.1 release (if VERSION.md = 17.1.1)
2. Mark v17.1.0 as latest (if VERSION.md = 17.1.0)