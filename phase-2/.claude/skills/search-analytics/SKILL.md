---
name: search-analytics
description: Advanced task searching, logical filtering, and daily diagnostic summaries. Use when a user asks for complex searches (e.g., "all high priority tasks missed this week") or needs a "daily debrief" of their productivity.
---

# Search & Analytics Skill

This skill provides advanced query capabilities and intelligence over the task database.

## Features
- **Semantic Search**: Find tasks related to broad concepts even if keywords don't match exactly.
- **Productivity Summary**: Generate a report of completed vs. pending tasks for a given period.
- **Priority Detection**: Automatically suggest priority levels based on task description keywords (e.g., "Urgent", "ASAP", "Final deadline").

## Analytic Reports
When user asks for a "Summary" or "Daily Debrief":
1. Fetch all tasks for `TODAY`.
2. Count `Status=Completed` and `Status=Pending`.
3. Identify oldest pending task (bottleneck).
4. Return a concise, motivational overview.

## Logic Mapping
- "Show me everything" -> `list_tasks(status=none)`
- "What did I do today?" -> `search_analytics(filter="completed_today")`
