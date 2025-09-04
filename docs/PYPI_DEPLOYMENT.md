# PyPI Deployment Guide

This document describes how to deploy the Chirality Framework to PyPI.

## Important: Deployment Triggers

**The PyPI deployment does NOT happen automatically on pushes to main.** Instead, it uses release-based deployment for better control and security:

- ✅ **Automatic**: Triggered when you [create a GitHub release](https://github.com/sgttomas/chirality-framework/releases/new)
- ⚡ **Manual**: Available via [workflow dispatch](https://github.com/sgttomas/chirality-framework/actions/workflows/python-publish.yml) for emergency deployments

## Automated Deployment (Recommended)

The repository is configured with automated PyPI deployment via GitHub Actions. When a GitHub release is published, the package is automatically built and uploaded to PyPI using trusted publishing.

### Prerequisites

1. **GitHub Environment**: The repository must have a `pypi` environment configured with trusted publishing enabled
2. **Version Sync**: Ensure `VERSION.md` and `pyproject.toml` have the same version number

### Steps

1. **Verify Version Sync**:
   ```bash
   python scripts/check_version_sync.py
   ```

2. **Run Tests** (optional but recommended):
   ```bash
   pytest -q
   ```

3. **Create GitHub Release**:
   ```bash
   # Use helper script for easy release creation
   python scripts/create_release.py
   ```
   
   Or manually:
   - Go to the [GitHub repository releases page](https://github.com/sgttomas/chirality-framework/releases/new)
   - Click "Create a new release"
   - Create a tag with format `vX.Y.Z` (e.g., `v16.2.0`) - **must match VERSION.md**
   - Fill in release title and description
   - **Publish the release** - this automatically triggers PyPI deployment

4. **Monitor Deployment**:
   - Check the [GitHub Actions tab](https://github.com/sgttomas/chirality-framework/actions/workflows/python-publish.yml) for the "Upload Python Package" workflow
   - The workflow should build and upload the package automatically
   - Check PyPI for the new version at https://pypi.org/project/chirality-framework/

## Manual Deployment (Emergency Only)

If you need to deploy immediately without creating a release:

1. **Go to Actions**: Navigate to [Upload Python Package workflow](https://github.com/sgttomas/chirality-framework/actions/workflows/python-publish.yml)
2. **Click "Run workflow"**: You'll see a "Run workflow" button on the right
3. **Enter confirmation**: Type exactly `deploy-to-pypi` in the confirmation field
4. **Run workflow**: Click the green "Run workflow" button

⚠️ **Warning**: Manual deployments bypass release notes and changelog updates. Use only for critical fixes.

## Manual Deployment (Fallback)

If the automated deployment fails or for testing purposes:

### Prerequisites

1. Install build dependencies:
   ```bash
   pip install build twine
   ```

2. Ensure you have PyPI credentials or API token configured

### Steps

1. **Clean Previous Builds**:
   ```bash
   rm -rf dist/ build/ *.egg-info/
   ```

2. **Build Package**:
   ```bash
   python -m build --no-isolation
   ```

3. **Verify Package**:
   ```bash
   python -m twine check dist/*
   ```

4. **Upload to PyPI**:
   ```bash
   # Test PyPI first (recommended)
   python -m twine upload --repository testpypi dist/*
   
   # Production PyPI
   python -m twine upload dist/*
   ```

## Troubleshooting

### "Why didn't PyPI deploy automatically after my push to main?"

PyPI deployment is **release-based**, not push-based. You need to:
1. Verify versions are synced: `python scripts/check_version_sync.py`
2. [Create a GitHub release](https://github.com/sgttomas/chirality-framework/releases/new) with tag matching your VERSION.md
3. The release publication will trigger the deployment

### Version Mismatch Error
If you get "File already exists" errors on PyPI, check:
- `VERSION.md` and `pyproject.toml` have the same version
- The version hasn't been published to PyPI already
- Run `python scripts/check_version_sync.py` to verify

### Build Failures
If builds fail:
- Ensure all dependencies are properly specified in `pyproject.toml`
- Check for syntax errors in the code
- Run tests locally first: `pytest -q`

### Network Timeouts
If experiencing network timeouts during build:
- Use `python -m build --no-isolation` instead of the default isolated build
- This uses the current environment's packages instead of downloading fresh ones

## Version Management

The project uses a centralized versioning system:
- **Source of Truth**: `VERSION.md` contains the current version
- **CLI Version**: Read dynamically from `VERSION.md`
- **Package Version**: Must be manually synchronized in `pyproject.toml`

When updating versions:
1. Update `VERSION.md` with new version
2. Update `pyproject.toml` with same version
3. Run `python scripts/check_version_sync.py` to verify
4. Update `CHANGELOG.md` with release notes
5. Create GitHub release to trigger deployment