# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of custom extensions for Claude Code: Skills, Agents, and Plugins.

| Type | Context | Trigger | Location |
|------|---------|---------|----------|
| **Command** | Main context, invokes agent | `/command-name` | `commands/{name}.md` |
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

### Command vs Skill vs Agent Decision

- Use **Command** when: simple wrapper to invoke an agent via `/command`, single markdown file
- Use **Skill** when: complex workflow, needs multiple files, user interaction needed, intermediate steps visible
- Use **Agent** when: background processing, isolated context preferred, triggered by keywords or `Task` tool

### Installation Pattern

Extensions are installed via symlinks to `~/.claude/`:
```bash
# Command
ln -sf $(pwd)/commands/{name}.md ~/.claude/commands/{name}.md

# Skill
ln -sf $(pwd)/skills/{name} ~/.claude/skills/{name}

# Agent
ln -sf $(pwd)/agents/{name}/agent.md ~/.claude/agents/{name}.md
```

## Current Extensions

### Commands (agent invokers)
- `/plan` - Implementation planning, invokes planner agent
- `/architect` - System design and ADRs, invokes architect agent
- `/code-invs` - Codebase analysis, invokes codebase-investigator agent
- `/refactor-clean` - Dead code cleanup (Python/Go/JS/TS), invokes refactor-cleaner agent
- `/update-codemaps` - Generate architecture documentation, invokes codemap-updater agent
- `/e2e` - Browser E2E testing via Claude in Chrome, invokes e2e-browser agent

### Skills (cross-tool workflows)
- `cr` - Cross-model code review. Claude Code → Codex reviews, Codex CLI → Claude reviews.
- `peer-review` - Cross-model proposal/viewpoint review. Inbound (verify findings) + outbound (challenge plans).
- `eval` - Eval-Driven Development: define, check, report evals with pass@k metrics.
- `eval-harness` - EDD framework: capability/regression evals, code/model/human graders.
- `continuous-learning` - Active pattern extraction via `/learn`. Save to project/global storage.
- `tdd` - Test-driven development: Red-Green-Refactor, coverage targets.
- `skill-link` - Install skills/commands/agents via symlinks to Claude Code + Codex CLI.
- `drawio` - AI-powered draw.io diagram generation with MCP server.
- `research` - Web research via Tavily API with citations.

### Agents
- `code-reviewer` - Send diffs to OpenAI Codex, returns P1/P2/P3 feedback
- `codebase-investigator` - Read-only analysis, outputs to `notes/` directory
- `planner` - Implementation planning for complex features and refactoring
- `architect` - System design, scalability analysis, and architectural decisions
- `refactor-cleaner` - Dead code cleanup for Python, Go, JS/TS
- `codemap-updater` - Generate architecture documentation from codebase
- `e2e-browser` - Browser E2E testing using Claude in Chrome MCP

## Adding New Extensions

1. Create `commands/{name}.md`, `skills/{name}/SKILL.md`, or `agents/{name}/agent.md`
2. For commands: include YAML frontmatter with `description`
3. For agents: include YAML frontmatter with `name`, `description`, `model`
4. Keep descriptions concise with keyword triggers
5. Symlink to `~/.claude/` to install
6. Update README.md with documentation
