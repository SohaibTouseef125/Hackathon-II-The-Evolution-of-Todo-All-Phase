---
name: voice-command-processor
description: Processes transcriptions of voice commands into actionable task intents. Use when a user provides audio transcripts (STT output) and needs to map verbal fillers, pauses, and natural speech to specific Todo CRUD operations.
---

# Voice Command Processor Skill

This skill handles the nuances of spoken language for the Todo Chatbot. It is designed to clean up "messy" transcripts and extract the core intent.

## Handling Spoken Language
- **Fillers**: Strip "um", "uh", "you know", "like".
- **Confirmation**: Handle trailing confirmations like "...actually never mind" or "...yeah that's it".
- **Implicit Subjects**: Resolve "it" or "that" to the last mentioned task.

## Processing Logic
1. **Clean**: Remove disfluencies.
2. **Segment**: Identify if one audio clip contains multiple commands (e.g., "Add milk and also remind me to call mom").
3. **Map**: Use keyword weighting to trigger MCP tools.

## Example
Input: "Uh hey okay so I need to um add a task for tomorrow morning call it buy eggs... yeah"
Output: `add_task(title="buy eggs", due_date="tomorrow 09:00:00")`
