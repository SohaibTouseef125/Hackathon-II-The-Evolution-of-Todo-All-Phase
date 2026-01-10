#!/usr/bin/env python3
"""
React Helper Script
Utility functions for React development tasks
"""

import os
import json
import argparse
from pathlib import Path

def create_component(component_name, component_type="functional", with_style=True, with_test=True):
    """Create a new React component with optional style and test files."""

    # Determine the file extension based on component type
    ext = ".jsx" if component_type == "functional" else ".tsx"

    # Create component content
    if component_type == "functional":
        content = f'''import {{ useState, useEffect }} from 'react';

const {component_name} = ({{ children, ...props }}) => {{
  const [state, setState] = useState(null);

  useEffect(() => {{
    // Component did mount logic
  }}, []);

  return (
    <div className="{component_name.lower()}">
      <h2>{component_name}</h2>
      {{children}}
    </div>
  );
}};

export default {component_name};
'''
    else:
        content = f'''import {{ useState, useEffect }} from 'react';

interface {component_name}Props {{
  children?: React.ReactNode;
  [key: string]: any;
}}

const {component_name}: React.FC<{component_name}Props> = ({{ children, ...props }}) => {{
  const [state, setState] = useState<string | null>(null);

  useEffect(() => {{
    // Component did mount logic
  }}, []);

  return (
    <div className="{component_name.lower()}">
      <h2>{component_name}</h2>
      {{children}}
    </div>
  );
}};

export default {component_name};
'''

    # Write component file
    component_path = Path(f"src/components/{component_name}{ext}")
    component_path.parent.mkdir(parents=True, exist_ok=True)

    with open(component_path, 'w') as f:
        f.write(content)

    print(f"Created component: {component_path}")

    # Create style file if requested
    if with_style:
        style_path = component_path.with_suffix('.module.css')
        with open(style_path, 'w') as f:
            f.write(f'''.{component_name.lower()} {{
  /* Add your styles here */
}}
''')
        print(f"Created style file: {style_path}")

    # Create test file if requested
    if with_test:
        test_path = component_path.with_suffix(f'{ext.replace("x", ".test.jsx")}')
        test_content = f'''import {{ render, screen, fireEvent }} from '@testing-library/react';
import {component_name} from './{component_name}';

describe('{component_name}', () => {{
  test('renders without crashing', () => {{
    render(<<{component_name} />);
    expect(screen.getByText('{component_name}')).toBeInTheDocument();
  }});
}});
'''
        with open(test_path, 'w') as f:
            f.write(test_content)
        print(f"Created test file: {test_path}")

def create_hook(hook_name):
    """Create a custom React hook."""

    content = f'''import {{ useState, useEffect, useCallback }} from 'react';

export const {hook_name} = (initialValue) => {{
  const [value, setValue] = useState(initialValue);

  const reset = useCallback(() => {{
    setValue(initialValue);
  }}, [initialValue]);

  useEffect(() => {{
    // Add your effect logic here
  }}, []);

  return [value, setValue, reset];
}};
'''

    hook_path = Path(f"src/hooks/{hook_name}.js")
    hook_path.parent.mkdir(parents=True, exist_ok=True)

    with open(hook_path, 'w') as f:
        f.write(content)

    print(f"Created hook: {hook_path}")

def list_components():
    """List all React components in the project."""

    components_dir = Path("src/components")
    if components_dir.exists():
        components = list(components_dir.rglob("*.jsx")) + list(components_dir.rglob("*.tsx"))
        if components:
            print("Found React components:")
            for comp in components:
                print(f"  - {comp.name}")
        else:
            print("No React components found in src/components/")
    else:
        print("src/components/ directory does not exist")

def main():
    parser = argparse.ArgumentParser(description='React Development Helper')
    parser.add_argument('command', choices=['create-component', 'create-hook', 'list-components'],
                       help='Command to execute')
    parser.add_argument('--name', help='Name of the component or hook')
    parser.add_argument('--type', choices=['functional', 'typescript'], default='functional',
                       help='Type of component to create')
    parser.add_argument('--no-style', action='store_true', help='Skip creating style file')
    parser.add_argument('--no-test', action='store_true', help='Skip creating test file')

    args = parser.parse_args()

    if args.command == 'create-component':
        if not args.name:
            print("Error: --name is required for create-component")
            return

        create_component(
            args.name,
            args.type,
            not args.no_style,
            not args.no_test
        )

    elif args.command == 'create-hook':
        if not args.name:
            print("Error: --name is required for create-hook")
            return

        create_hook(args.name)

    elif args.command == 'list-components':
        list_components()

if __name__ == "__main__":
    main()