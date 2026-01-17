# Claude Extensions

[中文文档](README.zh-CN.md)

Custom extensions for Claude Code: Skills, Agents, and Plugins.

## Concepts

| Type | Purpose | Context | Trigger |
|------|---------|---------|---------|
| **Skill** | Task workflow in main window | Uses main window context | `/skill-name` |
| **Agent** | Background subprocess, isolated context | Doesn't use main window | `Task(subagent_type)` or keywords |
| **Plugin** | Provides MCP servers, hooks, etc. | Depends on implementation | Auto-loaded |

### When to Use Skill vs Agent

- **Skill**: Requires user interaction, view intermediate steps, triggered via `/skill-name`
- **Agent**: Runs in background subprocess with isolated context, invoked via `Task` tool

### Agent YAML Frontmatter (Required)

Agent files must include YAML frontmatter to be recognized by the `Task` tool:

```yaml
---
name: my-agent          # Task(subagent_type: "my-agent")
description: "Description and keywords..."
model: inherit          # or specify sonnet/opus/haiku
---
```

## Installation

```bash
# Clone the repository
git clone https://github.com/fancive/claude-skills.git
cd claude-skills

# Install skill (symlink)
ln -sf $(pwd)/skills/reflect ~/.claude/skills/reflect

# Install agent (symlink)
ln -sf $(pwd)/agents/code-reviewer/agent.md ~/.claude/agents/code-reviewer.md

# Install plugin (follow plugin instructions)
```

## Skills

### reflect

Extract reusable engineering rules from conversations. "Correct once, never again."

```bash
/reflect                # Analyze conversation, extract rules
/reflect --dry-run      # Preview without modifying
/reflect --global       # Save to global rules
/reflect --project      # Save to project rules
```

See [skills/reflect/SKILL.md](skills/reflect/SKILL.md)

## Agents

### code-reviewer

Send code changes to OpenAI Codex for review, returns P1/P2/P3 prioritized feedback.

**Triggers**:
- Keywords: `review my code`, `codex review`, `code review`
- Direct call: `Task(subagent_type: "code-reviewer")`

**Workflow** (runs in isolated subprocess):
1. Collect git diff
2. Format review request to temp file
3. Call `codex exec` to send to Codex
4. Return P1/P2/P3 structured feedback

**Advantage**: Doesn't consume main window context, intermediate steps run in background.

See [agents/code-reviewer/agent.md](agents/code-reviewer/agent.md)

### codebase-investigator

Read-only codebase analysis: search files, trace dependencies, understand architecture, document findings.

**Triggers**:
- Keywords: `investigate`, `analyze`, `trace`, `how does`, `where is`, `find code`
- Direct call: `Task(subagent_type: "codebase-investigator")`

**Output**: Structured analysis report (Markdown) in `notes/` directory.

See [agents/codebase-investigator/agent.md](agents/codebase-investigator/agent.md)

### paper-summarizer

Summarize academic papers/PDFs or generate draw.io architecture diagrams for codebases.

**Triggers**:
- Keywords: `paper`, `PDF`, `arXiv`, `research`, `architecture diagram`, `draw.io`
- Direct call: `Task(subagent_type: "paper-summarizer")`

**Output**: Paper summary (in Chinese) or `.drawio` architecture diagram file.

See [agents/paper-summarizer/agent.md](agents/paper-summarizer/agent.md)

## Plugins

*Coming soon*

## Directory Structure

```
claude-skills/
├── skills/
│   └── reflect/
│       └── SKILL.md
├── agents/
│   ├── code-reviewer/
│   │   └── agent.md
│   ├── codebase-investigator/
│   │   └── agent.md
│   └── paper-summarizer/
│       └── agent.md
├── plugins/
│   └── (future)
├── templates/
│   ├── learned-rules.md
│   └── reflect-log.md
└── README.md
```

## Adding New Extensions

### Adding a Skill

1. Create directory `skills/{name}/`
2. Add `SKILL.md` (refer to reflect for format)
3. Create symlink: `ln -sf $(pwd)/skills/{name} ~/.claude/skills/{name}`
4. Update this README

### Adding an Agent

1. Create directory `agents/{name}/`
2. Add `agent.md`, **must include YAML frontmatter**:
   ```yaml
   ---
   name: {name}
   description: "Description... Keywords: keyword1, keyword2"
   model: inherit
   ---
   ```
3. Create symlink: `ln -sf $(pwd)/agents/{name}/agent.md ~/.claude/agents/{name}.md`
4. Update this README

### Adding a Plugin

*Documentation coming soon*

## License

MIT
