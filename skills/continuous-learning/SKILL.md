---
name: continuous-learning
description: "Extract reusable patterns and preferences from current session and save as skill files. Use when: (1) user runs /learn, (2) user says 'learn this', 'remember', '记住这个', '学习这个', '记住', '学习'. Keywords: learn, patterns, skills, preferences, extract, 记住, 学习"
---

# Learn — Extract & Save Reusable Patterns

Scan current session for reusable knowledge, review with user, save as skill files.

## Workflow

1. Scan current conversation for extractable patterns
2. Present each candidate via AskUserQuestion
3. Save confirmed patterns as skill files
4. Report summary

## What to Extract

| Type | Signal |
|------|--------|
| Error resolution | Error + root cause + fix |
| Debugging technique | Non-obvious debug steps |
| Workaround | Library quirks, API limitations |
| Project convention | Codebase-specific patterns |
| User preference | Corrections: 不要/别/必须/always/never/don't |
| Dead end | Approach tried → failed → why it doesn't work |
| Blocker | Limitation discovered: API/tool/library can't do X |
| Anti-pattern | Method that seems right but causes subtle issues |
| Agent introspection | Agent failed → why? Prompt gap / tool limitation / knowledge blind spot |

**Skip**: Simple typos, one-time fixes, obvious patterns, anything non-reusable.

### Agent Introspection

When the agent makes a mistake or fails at a task, go deeper than "what failed":

- **What went wrong?** — The observable failure
- **Why?** — Root cause: was it a prompt issue, tool limitation, missing context, or knowledge gap?
- **What to update?** — CLAUDE.md rule, skill instruction, or tool configuration to prevent recurrence

## Quality Gate

Extract only if **all four** hold: non-trivial, reusable across sessions, specific (clear problem + solution), actionable.

## Review UX

For each extracted pattern:

```yaml
question: "Pattern: {name}\n{summary}\n\nSave?"
options:
  - label: "Save to project (Recommended)"
    description: "Write to .claude/skills/learned/ (current project only)"
  - label: "Save globally"
    description: "Write to ~/.claude/skills/learned/ (all projects)"
  - label: "Skip"
    description: "Discard"
  - label: "Edit then save"
    description: "Modify before saving"
```

## Save Locations

```
{project}/.claude/skills/learned/   # Project-level (higher priority)
~/.claude/skills/learned/           # Global
```

Project skills override global skills with the same name.

## Output Format

See [references/format.md](references/format.md) for the saved skill file structure.

## Agent-Agnostic Usage

This skill works with any AI coding agent:

- **Claude Code**: `/learn`
- **Codex CLI / others**: Point the agent to this file and say "follow the workflow above"
