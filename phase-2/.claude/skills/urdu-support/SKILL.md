---
name: urdu-support
description: Multilingual capability for handling tasks and conversations in Urdu (Native script) and Roman Urdu. Use when the user interacts in Urdu, needs translation of tasks, or requires natural language understanding for Urdu-specific intents.
---

# Urdu Support Skill

This skill enables Claude to handle tasks and provide responses in Urdu and Roman Urdu, specifically tailored for the Phase 3 Todo Chatbot.

## Capabilities
- Understand user intents in Urdu (e.g., "نئی ٹاسک شامل کریں") and Roman Urdu (e.g., "Nayi task add karo").
- Translate tasks between English and Urdu.
- Provide culturally relevant responses and respectful terminology.

## Workflow

### 1. Intent Detection
When a user provides input in Urdu/Roman Urdu:
- Map common Urdu verbs (karo, hatao, dikhao) to MCP tools:
  - "Shamil/Add karo" -> `add_task`
  - "Dikhayen/List" -> `list_tasks`
  - "Khatam/Urhao" -> `delete_task`
  - "Done/Mukammal" -> `complete_task`

### 2. Normalization
- For Roman Urdu, handle variations in spelling (e.g., "karo", "kerdo", "kardu").
- Extract dates/times from Urdu phrases (e.g., "kal subah" -> Tomorrow 9:00 AM).

## Reference Material
See [urdu_dictionary.md](references/urdu_dictionary.md) for a map of common verbs and terms.
