#!/usr/bin/env python3
"""
Verification script for Chirality Framework package structure.
This helps debug CI import issues.
"""

import sys
import importlib.util

def test_import(module_name):
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            print(f"❌ Module '{module_name}' not found in sys.path")
            return False
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✅ Module '{module_name}' imported successfully from {spec.origin}")
        return True
    except Exception as e:
        print(f"❌ Error importing '{module_name}': {e}")
        return False

def main():
    print("🔍 Chirality Framework Package Verification")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.path}")
    print()
    
    # Test imports in order of dependency
    modules_to_test = [
        "chirality",
        "chirality.lib",
        "chirality.lib.prompt_registry", 
        "chirality.lib.prompt_builder",
        "chirality.lib.strategies",
        "chirality.core",
        "chirality.core.cell_resolver",
        "chirality.exporters",
    ]
    
    success_count = 0
    for module in modules_to_test:
        if test_import(module):
            success_count += 1
        print()
    
    print(f"📊 Results: {success_count}/{len(modules_to_test)} modules imported successfully")
    
    if success_count == len(modules_to_test):
        print("🎉 All package imports working!")
        return 0
    else:
        print("💥 Some imports failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())