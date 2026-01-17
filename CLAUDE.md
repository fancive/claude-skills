# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of custom extensions for Claude Code: Skills, Agents, and Plugins.

| Type | Context | Trigger | Location |
|------|---------|---------|----------|
| **Skill** | Uses main window context | `/skill-name` | `skills/{name}/SKILL.md` |
| **Agent** | Isolated subprocess context | `Task(subagent_type)` or keywords | `agents/{name}/agent.md` |
| **Plugin** | Varies | Auto-loaded | `plugins/` |

## Key Conventions

### Agent Files Must Have YAML Frontmatter

```yaml
---
name: my-agent
description: "Short description. Keywords: trigger1, trigger2"
model: inherit
---
```

Without this frontmatter, agents won't be recognized by the `Task` tool.

### Skill vs Agent Decision

- Use **Skill** when: user interaction needed, intermediate steps should be visible, triggered via `/command`
- Use **Agent** when: background processing, isolated context preferred, triggered by keywords or `Task` tool

### Installation Pattern

Extensions are installed via symlinks to `~/.claude/`:
```bash
# Skill
ln -sf $(pwd)/skills/{name} ~/.claude/skills/{name}

# Agent
ln -sf $(pwd)/agents/{name}/agent.md ~/.claude/agents/{name}.md
```

## Current Extensions

### Skills
- `reflect` - Extract engineering rules from conversation corrections/preferences. Two-phase workflow: auto-capture to pending → user review to commit.

### Agents
- `code-reviewer` - Send diffs to OpenAI Codex, returns P1/P2/P3 feedback
- `codebase-investigator` - Read-only analysis, outputs to `notes/` directory
- `paper-summarizer` - Summarize papers or generate draw.io architecture diagrams

## Adding New Extensions

1. Create `skills/{name}/SKILL.md` or `agents/{name}/agent.md`
2. For agents: include required YAML frontmatter with `name`, `description`, `model`
3. Keep descriptions concise with keyword triggers
4. Update README.md with documentation
