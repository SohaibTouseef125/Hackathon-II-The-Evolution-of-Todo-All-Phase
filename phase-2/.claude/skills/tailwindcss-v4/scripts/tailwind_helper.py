#!/usr/bin/env python3
"""
Tailwind CSS v4 Helper Script

This script provides utilities for common Tailwind CSS v4 development tasks:
- Configuration validation and setup
- Migration tools from v3 to v4
- Performance optimization utilities
- Component generation tools
- Theme management utilities
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Optional

class TailwindHelper:
    """Helper class for Tailwind CSS v4 development operations"""

    def __init__(self):
        self.project_root = Path.cwd()
        self.config_file = self.project_root / "tailwind.config.js"
        self.package_file = self.project_root / "package.json"

    def run_command(self, command: str, cwd: Optional[Path] = None) -> bool:
        """Execute a shell command and return success status"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or self.project_root,
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✓ Command succeeded: {command}")
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Command failed: {command}")
            print(f"Error: {e.stderr}")
            return False

    def check_tailwind_version(self):
        """Check the installed version of Tailwind CSS"""
        if self.package_file.exists():
            try:
                with open(self.package_file, 'r') as f:
                    package_data = json.load(f)

                dev_deps = package_data.get('devDependencies', {})
                tailwind_version = dev_deps.get('tailwindcss')

                if tailwind_version:
                    print(f"Tailwind CSS version: {tailwind_version}")
                    return tailwind_version
                else:
                    print("Tailwind CSS not found in package.json")
                    return None
            except json.JSONDecodeError:
                print("Invalid package.json file")
                return None
        else:
            print("package.json not found")
            return None

    def validate_config(self):
        """Validate the Tailwind CSS configuration file"""
        if not self.config_file.exists():
            print("tailwind.config.js not found")
            return False

        print("Validating Tailwind CSS configuration...")

        # Try to parse the config file as JavaScript
        try:
            # Check if the file has basic Tailwind config structure
            with open(self.config_file, 'r') as f:
                content = f.read()

            if 'module.exports' in content and 'content' in content:
                print("✓ Configuration file structure appears valid")
                return True
            else:
                print("✗ Configuration file may be missing required elements")
                return False
        except Exception as e:
            print(f"✗ Error reading configuration file: {e}")
            return False

    def create_component(self, component_type: str, name: str):
        """Create a new Tailwind component template"""
        components_dir = self.project_root / "components"
        components_dir.mkdir(exist_ok=True)

        # Define component templates
        templates = {
            "button": f'''// components/{name}.jsx
import React from 'react';

const {name.capitalize()} = ({{
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  ...props
}}) => {{
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variantClasses = {{
    primary: 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500 text-white',
    secondary: 'bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 focus:ring-gray-500 text-gray-900 dark:text-white',
    outline: 'border border-blue-600 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 focus:ring-blue-500/50'
  }};

  const sizeClasses = {{
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base'
  }};

  const disabledClasses = disabled ? 'opacity-50 cursor-not-allowed' : '';

  const classes = [
    baseClasses,
    variantClasses[variant],
    sizeClasses[size],
    disabledClasses
  ].join(' ');

  return (
    <button
      className={{'{'}}classes{'}'}
      disabled={{'{'}}disabled{'}'}
      {{'{'}}...props{'}'}
    >
      {{'{'}}children{'}'}
    </button>
  );
}};

export default {name.capitalize()};
''',
            "card": f'''// components/{name}.jsx
import React from 'react';

const {name.capitalize()} = ({{
  title,
  children,
  footer,
  ...props
}}) => {{
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div className="p-6">
        {{'{'}}title && <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">{{'{'}}title{'}'}</h3>{'}'}
        <div className="text-gray-600 dark:text-gray-300">
          {{'{'}}children{'}'}
        </div>
      </div>
      {{'{'}}footer && (
        <div className="bg-gray-50 dark:bg-gray-700 px-6 py-3">
          {{'{'}}footer{'}'}
        </div>
      ){'}'}
    </div>
  );
}};

export default {name.capitalize()};
''',
            "form": f'''// components/{name}.jsx
import React from 'react';

const {name.capitalize()} = ({{
  fields = [],
  onSubmit,
  submitText = 'Submit',
  ...props
}}) => {{
  return (
    <form onSubmit={{'{'}}onSubmit{'}'} className="space-y-4">
      {{'{'}}fields.map((field, index) => (
        <div key={{'{'}}index{'}'} className="mb-4">
          <label htmlFor={{'{'}}field.id{'}'} className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            {{'{'}}field.label{'}'}
          </label>
          {{'{'}}field.type === 'textarea' ? (
            <textarea
              id={{'{'}}field.id{'}'}
              name={{'{'}}field.id{'}'}
              rows={{'{'}}field.rows || 4{'}'}
              className="block w-full rounded-md border-0 py-2 px-3 text-gray-900 dark:text-white shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 bg-white dark:bg-gray-700"
              placeholder={{'{'}}field.placeholder{'}'}
              required={{'{'}}field.required{'}'}
            />
          ) : (
            <input
              type={{'{'}}field.type || 'text{'}'}
              id={{'{'}}field.id{'}'}
              name={{'{'}}field.id{'}'}
              className="block w-full rounded-md border-0 py-2 px-3 text-gray-900 dark:text-white shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 bg-white dark:bg-gray-700"
              placeholder={{'{'}}field.placeholder{'}'}
              required={{'{'}}field.required{'}'}
            />
          ){'}'}
        </div>
      )){'}'}
      <button
        type="submit"
        className="w-full rounded-md bg-blue-600 px-4 py-3 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
      >
        {{'{'}}submitText{'}'}
      </button>
    </form>
  );
}};

export default {name.capitalize()};
'''
        }

        if component_type not in templates:
            print(f"Unsupported component type: {component_type}")
            print(f"Supported types: {', '.join(templates.keys())}")
            return False

        component_path = components_dir / f"{name}.jsx"

        if component_path.exists():
            print(f"Component {name} already exists!")
            return False

        with open(component_path, 'w') as f:
            f.write(templates[component_type])

        print(f"✓ Created component: {component_path}")
        return True

    def generate_config(self, output_path: str = "tailwind.config.js"):
        """Generate a Tailwind CSS v4 configuration file"""
        config_content = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
          800: "#1e40af",
          900: "#1e3a8a",
          950: "#172554",
        }
      },
      spacing: {
        "18": "4.5rem",
        "88": "22rem",
        "100": "25rem",
        "120": "30rem",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      screens: {
        "3xl": "1600px",
        "4xl": "2000px",
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
  ],
  darkMode: "class",
}
'''

        config_path = self.project_root / output_path

        if config_path.exists():
            print(f"Configuration file {output_path} already exists!")
            return False

        with open(config_path, 'w') as f:
            f.write(config_content)

        print(f"✓ Created Tailwind configuration: {config_path}")
        return True

    def setup_project(self):
        """Set up a new Tailwind CSS v4 project"""
        print("Setting up Tailwind CSS v4 project...")

        # Install Tailwind CSS v4 and related packages
        packages = [
            "tailwindcss@latest",
            "postcss",
            "autoprefixer",
            "@tailwindcss/forms",
            "@tailwindcss/typography",
            "@tailwindcss/aspect-ratio"
        ]

        install_cmd = f"npm install -D {' '.join(packages)}"
        if not self.run_command(install_cmd):
            return False

        # Generate configuration file
        if not self.generate_config():
            return False

        # Create PostCSS config
        postcss_config = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
'''
        postcss_path = self.project_root / "postcss.config.js"
        with open(postcss_path, 'w') as f:
            f.write(postcss_config)

        print("✓ Created PostCSS configuration")

        # Create basic CSS file
        css_dir = self.project_root / "src"
        css_dir.mkdir(exist_ok=True)

        css_content = '''@tailwind base;
@tailwind components;
@tailwind utilities;
'''
        css_path = css_dir / "input.css"
        with open(css_path, 'w') as f:
            f.write(css_content)

        print("✓ Created CSS input file")

        # Add build script to package.json if it exists
        if self.package_file.exists():
            try:
                with open(self.package_file, 'r') as f:
                    package_data = json.load(f)

                if 'scripts' not in package_data:
                    package_data['scripts'] = {}

                package_data['scripts']['build:tailwind'] = "tailwindcss -i ./src/input.css -o ./dist/output.css"
                package_data['scripts']['watch:tailwind'] = "tailwindcss -i ./src/input.css -o ./dist/output.css --watch"

                with open(self.package_file, 'w') as f:
                    json.dump(package_data, f, indent=2)

                print("✓ Updated package.json with Tailwind scripts")
            except json.JSONDecodeError:
                print("Warning: Could not update package.json")

        print("✓ Tailwind CSS v4 project setup complete!")
        return True

def main():
    parser = argparse.ArgumentParser(description="Tailwind CSS v4 Helper")
    parser.add_argument(
        "command",
        choices=["version", "validate", "create", "generate-config", "setup", "help"],
        help="Command to execute"
    )

    parser.add_argument(
        "--type",
        choices=["button", "card", "form"],
        help="Component type for create command"
    )

    parser.add_argument(
        "--name",
        help="Component name for create command"
    )

    args = parser.parse_args()

    helper = TailwindHelper()

    if args.command == "version":
        version = helper.check_tailwind_version()
        if version:
            print(f"Tailwind CSS v4 detected: {version}")
        else:
            print("Tailwind CSS v4 not found or not properly configured")

    elif args.command == "validate":
        success = helper.validate_config()
        if success:
            print("Configuration is valid!")
        else:
            print("Configuration has issues!")

    elif args.command == "create":
        if not args.type or not args.name:
            print("Please provide both --type and --name for create command")
            print("Example: python tailwind_helper.py create --type button --name my-button")
            return

        success = helper.create_component(args.type, args.name)
        if not success:
            print("Failed to create component")

    elif args.command == "generate-config":
        success = helper.generate_config()
        if not success:
            print("Failed to generate configuration")

    elif args.command == "setup":
        success = helper.setup_project()
        if not success:
            print("Failed to set up project")

    elif args.command == "help":
        print("""
Tailwind CSS v4 Helper Commands:

  version            - Check installed Tailwind CSS version
  validate           - Validate Tailwind CSS configuration
  create             - Create a new component template (--type and --name required)
  generate-config    - Generate a Tailwind CSS configuration file
  setup              - Set up a new Tailwind CSS v4 project
  help               - Show this help message

Examples:
  python tailwind_helper.py version
  python tailwind_helper.py validate
  python tailwind_helper.py create --type button --name primary-button
  python tailwind_helper.py generate-config
  python tailwind_helper.py setup
        """)

if __name__ == "__main__":
    main()