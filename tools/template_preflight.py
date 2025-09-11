# tools/template_preflight.py
# Usage:
#   python tools/template_preflight.py
# (Optionally) limit to phase1 only by default.

import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except Exception:
    print("PyYAML not installed. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

RE_PLACEHOLDER = re.compile(r"{{\s*([a-zA-Z0-9_]+)\s*}}")

ROOT = Path(__file__).resolve().parents[1]
ASSETS_META = ROOT / "chirality" / "infrastructure" / "prompts" / "assets" / "metadata.yml"
ASSETS_DIR  = ROOT / "chirality" / "infrastructure" / "prompts" / "assets"

# Baseline variables commonly provided in Phase 1 steps.
COMMON_VARS = {
    "station", "matrix_id", "n_rows", "n_cols", "rows_json", "cols_json"
}

# Additional variables required by asset families (keep this HONEST—don't mask gaps).
# Adjust as your templates evolve.
REQUIRED_BY_DIR = {
    # C/D/E/F/X families: mechanical / interpreted / lensed all require a json_tail
    "phase1/C/": {"json_tail"},
    "phase1/D/": {"json_tail"},
    "phase1/E/": {"json_tail"},
    "phase1/F/": {"json_tail"},
    "phase1/X/": {"json_tail"},
    # Z family uses json_tail for principles/lensed
    "phase1/Z/": {"json_tail"},
    # Lens catalog generation additionally requires high-level context
    "phase1/lens_catalog_generation.md": {"context", "json_tail"},
}

def load_metadata():
    if not ASSETS_META.exists():
        print(f"Metadata not found: {ASSETS_META}", file=sys.stderr)
        sys.exit(2)
    with ASSETS_META.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def extract_placeholders(text: str):
    return set(RE_PLACEHOLDER.findall(text or ""))

def main():
    meta = load_metadata()
    items = meta if isinstance(meta, list) else meta.get("assets") or meta  # support both shapes

    failures = []
    total = 0
    scanned = 0

    for item in items:
        asset_id = item.get("id")
        rel_path = item.get("path")
        if not rel_path or not rel_path.startswith("phase1/"):
            continue  # only lint phase1 for now

        total += 1
        asset_file = ASSETS_DIR / rel_path
        if not asset_file.exists():
            failures.append((asset_id, rel_path, {"<missing file>"}))
            continue

        text = asset_file.read_text(encoding="utf-8")
        placeholders = extract_placeholders(text)
        # Build “expected available vars” set
        expected = set(COMMON_VARS)
        # Apply directory/file-specific requirements (explicit over heuristic).
        for prefix, req in REQUIRED_BY_DIR.items():
            if rel_path.startswith(prefix) or rel_path == prefix:
                expected |= req

        missing = placeholders - expected
        scanned += 1

        if missing:
            failures.append((asset_id, rel_path, missing))

    # Report
    print(f"\nTemplate Preflight — Phase 1")
    print(f"Scanned: {scanned} assets (of {total} phase1 entries in metadata)\n")

    if not failures:
        print("✅ All scanned templates only reference known variables.")
        sys.exit(0)

    print("❌ Missing variables detected (template references not covered by stage template_vars):\n")
    for asset_id, rel_path, missing in failures:
        miss_list = ", ".join(sorted(missing))
        print(f"  - {asset_id or '<no-id>'} :: {rel_path} -> missing: {miss_list}")
    print("\nTip: Add the missing variables to the stage’s template_vars in dialogue_run.py,")
    print("     or remove/rename the placeholders in the template.")
    sys.exit(1)

if __name__ == "__main__":
    main()
