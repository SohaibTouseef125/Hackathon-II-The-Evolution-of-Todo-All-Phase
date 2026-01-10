#!/usr/bin/env python3
"""
Validation script for react.js-latest skill

This script validates that all required components of the React.js latest skill
are present and properly configured.
"""

import os
import sys
from pathlib import Path

def validate_skill_structure():
    """Validate the overall skill structure."""
    skill_path = Path("/mnt/d/skills/.claude/skills/react.js-latest")

    # Check if main skill file exists
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        print(f"❌ Missing SKILL.md file")
        return False
    else:
        print(f"✅ Found SKILL.md file")

    # Check if required directories exist
    required_dirs = ["assets", "references", "scripts"]
    all_dirs_exist = True
    for dir_name in required_dirs:
        dir_path = skill_path / dir_name
        if not dir_path.exists():
            print(f"❌ Missing directory: {dir_name}")
            all_dirs_exist = False
        else:
            print(f"✅ Found directory: {dir_name}")

    if not all_dirs_exist:
        return False

    return True

def validate_references():
    """Validate that reference files exist and have content."""
    references_path = Path("/mnt/d/skills/.claude/skills/react.js-latest/references")

    # Check for API reference
    api_ref = references_path / "api_reference.md"
    if not api_ref.exists():
        print(f"❌ Missing API reference file")
        return False

    content = api_ref.read_text()
    if len(content) < 100:  # Basic check for content
        print(f"❌ API reference file appears to have insufficient content")
        return False

    print(f"✅ API reference file exists with sufficient content")
    return True

def validate_assets():
    """Validate that asset templates exist."""
    assets_path = Path("/mnt/d/skills/.claude/skills/react.js-latest/assets")

    # Check for key asset templates
    required_assets = [
        "functional-component.jsx",
        "custom-hook.js",
        "error-boundary.jsx",
        "lazy-component.jsx",
        "context-provider.jsx",
        "example_asset.txt"
    ]

    all_assets_exist = True
    for asset in required_assets:
        asset_path = assets_path / asset
        if not asset_path.exists():
            print(f"❌ Missing asset: {asset}")
            all_assets_exist = False
        else:
            print(f"✅ Found asset: {asset}")

    # Check for project templates
    project_templates = ["vite-react-app", "nextjs-app", "react-router-setup", "redux-toolkit-setup", "testing-setup"]
    for template in project_templates:
        template_path = assets_path / template
        if not template_path.exists():
            print(f"❌ Missing project template: {template}")
            all_assets_exist = False
        else:
            print(f"✅ Found project template: {template}")

    # Check for configuration files
    config_files = ["tsconfig.json", "eslint.config.js", "jest.config.js"]
    for config in config_files:
        config_path = assets_path / config
        if not config_path.exists():
            print(f"❌ Missing config file: {config}")
            all_assets_exist = False
        else:
            print(f"✅ Found config file: {config}")

    return all_assets_exist

def validate_content_quality():
    """Basic validation of content quality."""
    skill_file = Path("/mnt/d/skills/.claude/skills/react.js-latest/SKILL.md")
    content = skill_file.read_text()

    # Check for key sections
    required_sections = [
        "React 18+",
        "Hooks",
        "Server Components",
        "State Management",
        "Performance Optimization",
        "Testing"
    ]

    all_sections_present = True
    for section in required_sections:
        if section not in content:
            print(f"⚠️  Section '{section}' might be missing from SKILL.md")
            all_sections_present = False
        else:
            print(f"✅ Found content related to: {section}")

    return True  # Don't fail validation just for missing sections

def main():
    print("🔍 Validating React.js Latest Skill...")
    print("="*50)

    # Validate overall structure
    structure_ok = validate_skill_structure()
    if not structure_ok:
        print("\n❌ Skill structure validation failed")
        return False

    print()

    # Validate references
    refs_ok = validate_references()
    if not refs_ok:
        print("\n❌ Reference validation failed")
        return False

    print()

    # Validate assets
    assets_ok = validate_assets()
    if not assets_ok:
        print("\n❌ Asset validation failed")
        return False

    print()

    # Validate content quality
    content_ok = validate_content_quality()

    print()
    print("="*50)

    if structure_ok and refs_ok and assets_ok:
        print("🎉 React.js Latest Skill validation PASSED!")
        print("✅ Skill is complete and ready for use")
        return True
    else:
        print("❌ React.js Latest Skill validation FAILED!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)