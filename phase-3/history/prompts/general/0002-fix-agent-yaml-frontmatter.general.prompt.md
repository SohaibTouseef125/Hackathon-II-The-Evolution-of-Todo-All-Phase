---
id: 0002
title: Fix agent YAML frontmatter
stage: general
date: 2026-01-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: unknown
user: unknown
command: /sp.phr
labels: ["agents", "yaml", "frontmatter", "claude-code"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - /home/sohaib/.claude/agents/css-expert.md
  - /home/sohaib/.claude/agents/tailwind-expert.md
  - /home/sohaib/.claude/agents/mern-specialist.md
  - /home/sohaib/.claude/agents/typescript-expert.md
  - /home/sohaib/.claude/agents/react-expert.md
  - /home/sohaib/.claude/agents/nextjs-expert.md
  - /home/sohaib/.claude/agents/openai-agents-expert.md
  - /home/sohaib/.claude/agents/javascript-expert.md
  - /home/sohaib/.claude/agents/uiux-expert.md
  - /home/sohaib/.claude/agents/fullstack-integrator.md
  - /home/sohaib/.claude/agents/api-endpoint-generator.md
  - /mnt/d/phase-3/.claude/agents/api-endpoint-generator.md
  - /mnt/d/phase-3/.claude/agents/lead-phase3-architect.md
  - /home/sohaib/.claude/agents/uiux-expert.md
  - /home/sohaib/.claude/agents/react-expert.md
tests:
  - python -c "import yaml" (PyYAML used)
  - python frontmatter parse/validate script (see response)
---

## Prompt

Fix the 10 failing agent YAMLs

## Response snapshot

Converted invalid single-line `description:` values (with literal \\n and <example> blocks) to valid YAML block scalars (`description: |`) and normalized `skills:` to proper YAML lists where needed. Re-validated all agent frontmatter by parsing the YAML between the `---` delimiters with `yaml.safe_load`.

## Outcome

- ✅ Impact: All agent frontmatter in both directories parses successfully as YAML (0 failures).
- 🧪 Tests: Python YAML frontmatter parse validation ran clean.
- 📁 Files: Updated 10 personal-level agent files to fix description and skills YAML; updated api-endpoint-generator skill key; ensured project-level agents already parse.
- 🔁 Next prompts: none
- 🧠 Reflection: YAML failures were caused by unescaped multiline content in plain scalars; using `description: |` is the most robust normalization.

## Evaluation notes (flywheel)

- Failure modes observed: Initial edits used exact-string replacements that failed because the on-disk description strings differed in punctuation/quotes; fixed by reading files and replacing the actual current scalars.
- Graders run and results (PASS/FAIL): PASS (python yaml.safe_load over frontmatter)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add an automated script to normalize agent frontmatter (description + skills) and run it as a pre-commit/hook.
