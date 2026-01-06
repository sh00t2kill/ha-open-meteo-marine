#!/usr/bin/env python3
"""
Simple validation test for the Home Assistant Open Meteo Marine component.
Tests the component files for syntax errors and basic structure.
"""

import os
import ast
import json
import sys
from pathlib import Path


def test_python_syntax(file_path: Path) -> bool:
    """Test if a Python file has valid syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the AST
        ast.parse(content)
        print(f"✅ {file_path.name}: Syntax OK")
        return True
        
    except SyntaxError as e:
        print(f"❌ {file_path.name}: Syntax Error - {e}")
        return False
    except Exception as e:
        print(f"❌ {file_path.name}: Error reading file - {e}")
        return False


def test_json_syntax(file_path: Path) -> bool:
    """Test if a JSON file has valid syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✅ {file_path.name}: JSON OK")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ {file_path.name}: JSON Error - {e}")
        return False
    except Exception as e:
        print(f"❌ {file_path.name}: Error reading file - {e}")
        return False


def test_manifest_structure(manifest_path: Path) -> bool:
    """Test if manifest.json has required fields."""
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        required_fields = ["domain", "name", "version", "requirements", "iot_class"]
        missing_fields = [field for field in required_fields if field not in manifest]
        
        if missing_fields:
            print(f"❌ manifest.json: Missing required fields: {missing_fields}")
            return False
        
        # Check domain matches directory name
        if manifest.get("domain") != "openmeteo_marine":
            print(f"❌ manifest.json: Domain '{manifest.get('domain')}' should be 'openmeteo_marine'")
            return False
            
        print(f"✅ manifest.json: Structure OK")
        return True
        
    except Exception as e:
        print(f"❌ manifest.json: Error validating structure - {e}")
        return False


def test_component_structure() -> bool:
    """Test if the component directory structure is correct."""
    component_dir = Path("custom_components/openmeteo_marine")
    
    if not component_dir.exists():
        print(f"❌ Component directory not found: {component_dir}")
        return False
    
    required_files = [
        "__init__.py",
        "manifest.json", 
        "const.py",
        "config_flow.py",
        "coordinator.py",
        "sensor.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not (component_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print(f"✅ Component structure: All required files present")
    return True


def main():
    """Main validation function."""
    print("🔍 Home Assistant Component Validation")
    print("=" * 50)
    
    all_passed = True
    
    # Test component structure
    if not test_component_structure():
        all_passed = False
    
    # Test Python files
    component_dir = Path("custom_components/openmeteo_marine")
    python_files = [
        "__init__.py",
        "const.py", 
        "config_flow.py",
        "coordinator.py",
        "sensor.py"
    ]
    
    for file in python_files:
        file_path = component_dir / file
        if file_path.exists():
            if not test_python_syntax(file_path):
                all_passed = False
    
    # Test JSON files
    json_files = [
        ("manifest.json", component_dir / "manifest.json"),
        ("strings.json", component_dir / "strings.json")
    ]
    
    for name, file_path in json_files:
        if file_path.exists():
            if not test_json_syntax(file_path):
                all_passed = False
    
    # Test manifest structure
    manifest_path = component_dir / "manifest.json"
    if manifest_path.exists():
        if not test_manifest_structure(manifest_path):
            all_passed = False
    
    # Test additional files
    other_files = ["README.md", "requirements.txt"]
    for file in other_files:
        if Path(file).exists():
            print(f"✅ {file}: File present")
        else:
            print(f"⚠️ {file}: File missing (optional)")
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 All tests passed! Component structure looks good.")
        print("\n📋 Next steps:")
        print("1. Run: python test_marine_api.py")
        print("2. Copy to Home Assistant custom_components/")
        print("3. Restart Home Assistant")
        print("4. Add integration via UI")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())