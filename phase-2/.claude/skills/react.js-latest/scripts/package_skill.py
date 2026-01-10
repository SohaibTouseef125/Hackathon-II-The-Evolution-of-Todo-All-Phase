#!/usr/bin/env python3
"""
Packaging script for react.js-latest skill

This script packages the React.js latest skill for distribution or use.
"""

import os
import sys
import json
from pathlib import Path
import zipfile
from datetime import datetime

def create_skill_manifest():
    """Create a manifest file for the skill."""
    manifest = {
        "name": "react.js-latest",
        "version": "1.0.0",
        "description": "Expert guidance for React.js development covering latest features, hooks, state management, component patterns, performance optimization, testing, and best practices for modern React applications.",
        "author": "Claude Code Skill Creator",
        "created": datetime.now().isoformat(),
        "files": [],
        "dependencies": [],
        "capabilities": [
            "React 18+ features",
            "Hooks patterns",
            "Component architecture",
            "State management",
            "Performance optimization",
            "Testing strategies",
            "TypeScript integration",
            "Server Components",
            "React Router patterns"
        ]
    }

    # Add all skill files to manifest
    skill_path = Path("/mnt/d/skills/.claude/skills/react.js-latest")
    for root, dirs, files in os.walk(skill_path):
        for file in files:
            file_path = Path(root) / file
            relative_path = file_path.relative_to(skill_path)
            manifest["files"].append(str(relative_path))

    manifest_path = skill_path / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Created skill manifest: {manifest_path}")
    return manifest_path

def create_zip_package():
    """Create a zip package of the skill."""
    skill_path = Path("/mnt/d/skills/.claude/skills/react.js-latest")
    zip_path = skill_path.parent / f"react.js-latest-{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arc_path)

    print(f"✅ Created skill package: {zip_path}")
    return zip_path

def verify_skill():
    """Verify that the skill is properly configured."""
    skill_path = Path("/mnt/d/skills/.claude/skills/react.js-latest")

    # Verify main skill file
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        print("❌ SKILL.md file is missing")
        return False

    # Verify it has substantial content
    content = skill_file.read_text()
    if len(content) < 1000:
        print("❌ SKILL.md file appears to have insufficient content")
        return False

    # Verify references exist
    refs_path = skill_path / "references"
    if not refs_path.exists():
        print("❌ References directory is missing")
        return False

    api_ref = refs_path / "api_reference.md"
    if not api_ref.exists():
        print("❌ API reference file is missing")
        return False

    # Verify assets exist
    assets_path = skill_path / "assets"
    if not assets_path.exists():
        print("❌ Assets directory is missing")
        return False

    print("✅ Skill verification passed")
    return True

def main():
    print("📦 Packaging React.js Latest Skill...")
    print("="*50)

    # Verify the skill first
    if not verify_skill():
        print("\n❌ Skill verification failed")
        return False

    print()

    # Create manifest
    manifest_path = create_skill_manifest()
    print()

    # Create zip package
    zip_path = create_zip_package()
    print()

    print("="*50)
    print("🎉 React.js Latest Skill packaged successfully!")
    print(f"📄 Manifest: {manifest_path}")
    print(f"📦 Package: {zip_path}")
    print()
    print("✅ Skill is ready for use with Claude Code")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)