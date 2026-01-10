---
name: reusable-intelligence
description: Comprehensive reusable intelligence framework for Claude Code and Spec-Kit Plus. Use when Claude needs to work with reusable intelligence for creating and managing reusable skills and subagents, implementing agent skill development and deployment, building reusable components for AI-driven development, developing subagent architectures and communication patterns, or any other reusable intelligence tasks.
---

# Reusable Intelligence - Agent Skills and Subagents

## Overview

This skill provides comprehensive guidance for developing and managing reusable intelligence through agent skills and subagents using Claude Code and Spec-Kit Plus. It covers the creation of reusable components that can be leveraged across different projects and phases, enabling efficient AI-driven development with consistent patterns and best practices.

## Core Capabilities

### 1. Agent Skill Development
- Creating reusable skills with standardized interfaces
- Skill lifecycle management (development, testing, deployment)
- Skill composition and orchestration patterns
- Skill validation and quality assurance
- Skill documentation and maintenance

### 2. Subagent Architecture
- Subagent design patterns and communication protocols
- Hierarchical agent structures and delegation patterns
- Subagent state management and coordination
- Performance optimization for agent networks
- Error handling and recovery strategies

### 3. Reusable Component Patterns
- Template-based component generation
- Configuration-driven intelligence
- Modular architecture principles
- Cross-project component sharing
- Versioning and dependency management

### 4. Integration Framework
- Claude Code skill integration patterns
- Spec-Kit Plus specification management
- MCP (Model Context Protocol) server integration
- API and tool integration strategies
- Continuous improvement workflows

## Project Structure

### Recommended Reusable Intelligence Structure
```
reusable-intelligence/
├── skills/
│   ├── core/
│   │   ├── validation/
│   │   ├── templating/
│   │   └── deployment/
│   ├── domain-specific/
│   │   ├── development/
│   │   ├── ops/
│   │   └── research/
│   └── templates/
│       ├── skill-template/
│       ├── subagent-template/
│       └── component-template/
├── subagents/
│   ├── general-purpose/
│   │   ├── researcher/
│   │   ├── reviewer/
│   │   └── planner/
│   ├── specialized/
│   │   ├── code-analyzer/
│   │   ├── spec-validator/
│   │   └── architecture-reviewer/
│   └── utility/
│       ├── file-processor/
│       ├── data-transformer/
│       └── report-generator/
├── specs/
│   ├── skill-architecture.md
│   ├── subagent-patterns.md
│   ├── integration-protocols.md
│   └── quality-standards.md
├── configs/
│   ├── skill-registry.json
│   ├── subagent-config.yaml
│   └── integration-settings.json
├── scripts/
│   ├── create-skill.sh
│   ├── validate-skill.sh
│   ├── deploy-skill.sh
│   └── test-integration.sh
├── CLAUDE.md
└── README.md
```

## Agent Skill Development

### 1. Skill Creation Process
```bash
# scripts/create-skill.sh
#!/bin/bash

SKILL_NAME=$1
SKILL_PATH="./skills/$SKILL_NAME"

# Create skill directory structure
mkdir -p "$SKILL_PATH"
mkdir -p "$SKILL_PATH/references"
mkdir -p "$SKILL_PATH/scripts"
mkdir -p "$SKILL_PATH/assets"

# Create base skill file
cat > "$SKILL_PATH/SKILL.md" << EOF
---
name: $SKILL_NAME
description: Reusable skill for ...
---

# $SKILL_NAME

## Overview
...

## Core Capabilities
...

## Usage
...

## Resources
- references/
- assets/
EOF

echo "Skill $SKILL_NAME created successfully!"
```

### 2. Skill Template
```markdown
# Skill Template

## Standard Skill Structure
```markdown
---
name: skill-name
description: Clear, specific description of what the skill does and when to use it
---

# Skill Name

## Overview
Brief description of the skill's purpose and capabilities.

## Core Capabilities
### 1. Capability 1
- Description of first capability
- Key benefits and use cases

### 2. Capability 2
- Description of second capability
- Key benefits and use cases

## Usage Patterns
### Pattern 1: Common Usage
- When to use this pattern
- Example implementation

### Pattern 2: Advanced Usage
- When to use this pattern
- Example implementation

## Resources
### references/
- `guidelines.md` - Best practices and guidelines
- `examples.md` - Real-world examples and patterns
- `troubleshooting.md` - Common issues and solutions

### assets/
- `templates/` - Template files and boilerplates
- `configuration/` - Configuration examples
- `diagrams/` - Architecture diagrams and visuals
```

### 3. Skill Validation
```bash
# scripts/validate-skill.sh
#!/bin/bash

SKILL_PATH=$1

# Check if required files exist
if [ ! -f "$SKILL_PATH/SKILL.md" ]; then
    echo "ERROR: SKILL.md not found"
    exit 1
fi

# Validate YAML frontmatter
if ! head -20 "$SKILL_PATH/SKILL.md" | grep -q "name:"; then
    echo "ERROR: Invalid YAML frontmatter"
    exit 1
fi

# Check for essential sections
SECTIONS=("## Overview" "## Core Capabilities" "## Resources")
for section in "${SECTIONS[@]}"; do
    if ! grep -q "$section" "$SKILL_PATH/SKILL.md"; then
        echo "WARNING: Missing section: $section"
    fi
done

echo "Skill validation completed!"
```

## Subagent Architecture

### 1. Subagent Template
```python
# subagents/general-purpose/researcher/subagent.py
from typing import Dict, Any, List
import json

class ResearchSubagent:
    """Reusable research subagent for information gathering and analysis"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = "researcher"
        self.version = "1.0.0"

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research task with provided context"""
        try:
            # Perform research based on task
            research_results = await self._perform_research(task, context)

            # Validate and format results
            formatted_results = self._format_results(research_results)

            return {
                "status": "success",
                "results": formatted_results,
                "metadata": {
                    "subagent": self.name,
                    "version": self.version,
                    "task": task
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "metadata": {
                    "subagent": self.name,
                    "version": self.version,
                    "task": task
                }
            }

    async def _perform_research(self, task: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Internal method to perform actual research"""
        # Implementation would depend on specific research needs
        # Could include web search, documentation lookup, etc.
        pass

    def _format_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format research results for consumption"""
        return {
            "findings": results,
            "confidence_scores": [],
            "sources": [],
            "summary": ""
        }
```

### 2. Subagent Communication Protocol
```python
# subagents/core/communication.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import json

class SubagentProtocol(ABC):
    """Abstract base class for subagent communication"""

    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task with given context"""
        pass

    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data before processing"""
        pass

    @abstractmethod
    def format_output(self, raw_output: Any) -> Dict[str, Any]:
        """Format output for standardized response"""
        pass

class SubagentManager:
    """Manages subagent lifecycle and communication"""

    def __init__(self):
        self.subagents = {}
        self.active_sessions = {}

    def register_subagent(self, name: str, subagent: SubagentProtocol):
        """Register a subagent with the manager"""
        self.subagents[name] = subagent

    async def delegate_task(self, subagent_name: str, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate a task to a specific subagent"""
        if subagent_name not in self.subagents:
            return {
                "status": "error",
                "error": f"Subagent {subagent_name} not found"
            }

        subagent = self.subagents[subagent_name]
        return await subagent.execute(task, context)

    async def coordinate_multiple(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Coordinate multiple subagents for complex tasks"""
        results = []
        for task in tasks:
            result = await self.delegate_task(
                task['subagent'],
                task['task'],
                task.get('context', {})
            )
            results.append(result)

        return results
```

## Reusable Component Patterns

### 1. Template-Based Generation
```python
# skills/templates/component-generator.py
import os
import json
from string import Template
from pathlib import Path

class ComponentGenerator:
    """Generates reusable components from templates"""

    def __init__(self, template_dir: str = "./skills/templates"):
        self.template_dir = Path(template_dir)

    def generate_skill_from_template(self,
                                   template_name: str,
                                   output_path: str,
                                   **kwargs) -> bool:
        """Generate a skill from a template with provided parameters"""
        template_file = self.template_dir / f"{template_name}/SKILL.md"

        if not template_file.exists():
            print(f"Template {template_name} not found")
            return False

        # Read template
        with open(template_file, 'r') as f:
            template_content = f.read()

        # Substitute variables
        template = Template(template_content)
        rendered_content = template.safe_substitute(**kwargs)

        # Write to output
        output_file = Path(output_path) / "SKILL.md"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            f.write(rendered_content)

        print(f"Skill generated at {output_file}")
        return True

    def generate_subagent_from_template(self,
                                      template_name: str,
                                      output_path: str,
                                      **kwargs) -> bool:
        """Generate a subagent from a template with provided parameters"""
        # Similar implementation for subagents
        pass
```

### 2. Configuration-Driven Intelligence
```yaml
# configs/skill-registry.yaml
skills:
  validation:
    name: validation-skill
    description: Reusable validation components
    version: "1.0.0"
    endpoints:
      - name: validate-spec
        description: Validate specification files
        parameters: ["spec_file", "validation_rules"]
      - name: validate-code
        description: Validate code quality
        parameters: ["code_file", "style_guide"]

  templating:
    name: templating-skill
    description: Template-based generation
    version: "1.0.0"
    endpoints:
      - name: generate-from-template
        description: Generate content from template
        parameters: ["template", "variables"]

subagents:
  researcher:
    name: research-subagent
    description: Information gathering and analysis
    version: "1.0.0"
    capabilities: ["web-search", "documentation-lookup", "analysis"]
    config:
      timeout: 30
      max_retries: 3

  reviewer:
    name: code-reviewer-subagent
    description: Code review and quality assessment
    version: "1.0.0"
    capabilities: ["code-analysis", "style-check", "bug-detection"]
    config:
      severity_threshold: "medium"
      languages: ["python", "javascript", "typescript"]
```

## Integration Framework

### 1. Claude Code Integration
```markdown
# Claude Code Skill Integration

## Best Practices
### 1. Skill Discovery
- Use consistent naming conventions
- Maintain skill registry
- Document skill dependencies
- Version control for skills

### 2. Skill Activation
- Skills should be self-contained
- Clear activation triggers
- Proper error handling
- Graceful degradation

### 3. Skill Composition
- Chain skills for complex workflows
- Handle intermediate results
- Manage state between skills
- Coordinate parallel execution
```

### 2. Spec-Kit Plus Integration
```markdown
# Spec-Kit Plus Integration

## Specification Patterns
### 1. Skill Specifications
- Define skill capabilities
- Document usage patterns
- Specify input/output formats
- Outline error conditions

### 2. Integration Specifications
- MCP server protocols
- API endpoint definitions
- Data format standards
- Communication patterns
```

## Quality Assurance Framework

### 1. Skill Testing
```bash
# scripts/test-integration.sh
#!/bin/bash

SKILL_PATH=$1
TEST_TYPE=${2:-"all"}

echo "Running tests for skill: $SKILL_PATH"

case $TEST_TYPE in
    "unit")
        # Unit tests for skill components
        echo "Running unit tests..."
        ;;
    "integration")
        # Integration tests with Claude Code
        echo "Running integration tests..."
        ;;
    "e2e")
        # End-to-end tests
        echo "Running end-to-end tests..."
        ;;
    "all")
        # Run all tests
        echo "Running all tests..."
        ;;
    *)
        echo "Unknown test type: $TEST_TYPE"
        exit 1
        ;;
esac
```

### 2. Continuous Improvement
```markdown
# Continuous Improvement Process

## Feedback Collection
- User feedback on skill effectiveness
- Performance metrics and usage statistics
- Error logs and issue reports
- Peer reviews and suggestions

## Iteration Process
1. Collect feedback and metrics
2. Identify improvement opportunities
3. Design and implement changes
4. Test and validate improvements
5. Deploy updated skills
6. Monitor impact and results
```

## Development Workflow

### 1. Skill Creation Workflow
1. Identify reusable component opportunity
2. Design skill interface and capabilities
3. Implement skill with proper documentation
4. Test skill functionality and integration
5. Register skill in skill registry
6. Document usage patterns and examples

### 2. Subagent Development Workflow
1. Define subagent responsibilities and scope
2. Design communication protocols
3. Implement subagent with error handling
4. Test subagent in isolation and integration
5. Register subagent with manager
6. Document capabilities and usage

### 3. Quality Assurance Process
- Unit testing for individual components
- Integration testing for skill combinations
- End-to-end testing for complete workflows
- Performance testing for efficiency
- Security testing for vulnerabilities

## Resources

### references/
- `skill_development_patterns.md` - Best practices for skill creation
- `subagent_architecture_guide.md` - Subagent design and implementation
- `integration_protocols.md` - Communication and coordination patterns
- `quality_assurance_framework.md` - Testing and validation procedures
- `continuous_improvement_process.md` - Iteration and enhancement workflows

### assets/
- `skill_templates/` - Reusable skill templates and generators
- `subagent_templates/` - Subagent architecture templates
- `configuration_examples/` - Configuration files and settings
- `testing_frameworks/` - Test scripts and utilities
- `documentation_templates/` - Documentation templates and examples
