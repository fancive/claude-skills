---
name: skill-link
description: "Install skills, commands, and agents via symlinks. Scans a source directory and creates symlinks to $CLAUDE_HOME and $CODEX_HOME. Use when: user says 'install skill', 'link skill', '安装', '同步', or wants to install/sync extensions across Claude Code and Codex CLI. Keywords: install, link, symlink, sync, skill, command, agent, 安装, 链接, 同步"
---

# skill-link — Install Extensions to Claude Code & Codex CLI

Create symlinks for skills, commands, and agents from a source directory.

Requires environment variables (set in shell profile):

```bash
export CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
```

## What Gets Installed

| Type | Source pattern | Claude Code target | Codex CLI target |
|------|---------------|-------------------|-----------------|
| Skills | `skills/{name}/` (has SKILL.md) | `$CLAUDE_HOME/skills/{name}` → dir symlink | `$CODEX_HOME/skills/{name}` → dir symlink |
| Commands | `commands/{name}.md` | `$CLAUDE_HOME/commands/{name}.md` → file symlink | N/A (Codex has no commands) |
| Agents | `agents/{name}/agent.md` | `$CLAUDE_HOME/agents/{name}.md` → file symlink to `agent.md` | N/A (Codex has no agents) |

## Workflow

1. Get source directory from user (default: current project root)
2. Scan for:
   - `skills/*/SKILL.md` → skill directories
   - `commands/*.md` → command files
   - `agents/*/agent.md` → agent files
3. Show discovered extensions with current status, AskUserQuestion to confirm
4. Create symlinks per the table above
5. Report results

## Linking Logic

```bash
src="$(realpath "/path/to/source")"
dst="$CLAUDE_HOME/skills/{name}"

# Check target type before linking
if [ -d "$dst" ] && [ ! -L "$dst" ]; then
    # Target is a real directory, not a symlink — warn user
    echo "WARNING: $dst is a real directory, skipping (use --force to replace)"
else
    ln -sfn "$src" "$dst"
fi
```

## Rules

- Always resolve source to **absolute path** with `realpath`
- **Quote all paths** to handle spaces
- Create target directories if missing
- **If target is a real directory** (not a symlink): skip and warn
- **If target is a symlink**: `ln -sfn` safely overwrites it
- Show status: `new` / `updated` / `already linked` / `skipped (real dir)`
- For agents: symlink points to the `agent.md` file, not the directory

## Example Session

```
User: /skill-link

Agent: Scanning /Users/me/claude-code-addons/ ...

Skills (3):
  ✓ continuous-learning  → not installed
  - skill-link           → already linked
  ✓ eval-harness         → not installed

Commands (4):
  ✓ peer-review.md       → not installed
  - learn.md             → already linked
  - cr.md                → already linked
  ✓ skill-link.md        → not installed

Agents (2):
  - code-reviewer.md     → already linked
  ✓ planner.md           → not installed

Install 5 extensions?

User: Yes

Agent:
  Skills:  2 installed to claude + codex
  Commands: 2 installed to claude
  Agents:  1 installed to claude

Done.
```
