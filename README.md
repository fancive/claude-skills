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

## Commands

Slash entry points in this repo include both command files and skills.

| Command | Agent | Purpose |
|---------|-------|---------|
| `/plan` | planner | Implementation planning |
| `/architect` | architect | System design, ADRs |
| `/tdd` | - | Test-driven development (tdd skill) |
| `/cr` | - | Cross-model code review (cr skill) |
| `/code-invs` | codebase-investigator | Codebase analysis |
| `/refactor-clean` | refactor-cleaner | Dead code cleanup (Python/Go/JS/TS) |
| `/update-codemaps` | codemap-updater | Generate architecture documentation |
| `/e2e` | e2e-browser | Browser E2E testing via Claude in Chrome |
| `/eval` | - | Eval-Driven Development: define, check, report |
| `/learn` | - | Extract patterns from current session (continuous-learning skill) |

### Installation

```bash
ln -sf $(pwd)/commands/plan.md ~/.claude/commands/plan.md
ln -sf $(pwd)/commands/architect.md ~/.claude/commands/architect.md
ln -sf $(pwd)/commands/code-invs.md ~/.claude/commands/code-invs.md
ln -sf $(pwd)/commands/refactor-clean.md ~/.claude/commands/refactor-clean.md
ln -sf $(pwd)/commands/update-codemaps.md ~/.claude/commands/update-codemaps.md
ln -sf $(pwd)/commands/e2e.md ~/.claude/commands/e2e.md
```

### Skill Installation (examples)

```bash
ln -sf $(pwd)/skills/cr ~/.claude/skills/cr
ln -sf $(pwd)/skills/peer-review ~/.claude/skills/peer-review
ln -sf $(pwd)/skills/continuous-learning ~/.claude/skills/continuous-learning
ln -sf $(pwd)/skills/tdd ~/.claude/skills/tdd
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

### continuous-learning

Extract reusable technical patterns from the current session with interactive confirmation.

**Usage (`/learn`)**:
```bash
/learn              # Scan current session and review extracted patterns
/learn --dry-run    # Preview without saving
```

**Output**: Skills saved to `~/.claude/skills/learned/`

See [skills/continuous-learning/SKILL.md](skills/continuous-learning/SKILL.md)

## Agents

### code-reviewer

Send code changes to OpenAI Codex for review, returns P1/P2/P3 prioritized feedback.

**Triggers**:
- Keywords: `review my code`, `codex review`, `code review`
- Direct call: `Task(subagent_type: "code-reviewer")`

**Workflow** (runs in isolated subprocess):
1. Inspect workspace + CHANGELOG status (no auto-edit by default)
2. Check untracked files and ask before staging
3. Run non-mutating lint checks
4. Call `codex review` with difficulty-based config
5. Return P1/P2/P3 structured feedback

**Advantage**: Doesn't consume main window context, intermediate steps run in background.

See [agents/code-reviewer/agent.md](agents/code-reviewer/agent.md)

### codebase-investigator

Read-only codebase analysis: search files, trace dependencies, understand architecture, document findings.

**Triggers**:
- Keywords: `investigate`, `analyze`, `trace`, `how does`, `where is`, `find code`
- Direct call: `Task(subagent_type: "codebase-investigator")`

**Output**: Structured analysis report (Markdown) in `notes/` directory.

See [agents/codebase-investigator/agent.md](agents/codebase-investigator/agent.md)

### planner

Implementation planning specialist for complex features and refactoring.

**Triggers**:
- Keywords: `plan`, `implementation`, `feature planning`, `refactor planning`
- Direct call: `Task(subagent_type: "planner")`

**Output**: Structured implementation plan with phases, steps, risks, and success criteria.

See [agents/planner/agent.md](agents/planner/agent.md)

### architect

Software architecture specialist for system design and technical decision-making.

**Triggers**:
- Keywords: `architecture`, `system design`, `scalability`, `technical decision`
- Direct call: `Task(subagent_type: "architect")`

**Output**: Architecture Decision Records (ADRs), design proposals, trade-off analysis.

See [agents/architect/agent.md](agents/architect/agent.md)

### refactor-cleaner

Multi-language dead code detection and cleanup.

**Supported Languages**:
- Python: vulture, dead, autoflake
- Go: deadcode, staticcheck, go mod tidy
- JS/TS: knip, depcheck, ts-prune

**Triggers**:
- Keywords: `refactor`, `clean`, `dead code`, `unused`
- Direct call: `Task(subagent_type: "refactor-cleaner")`

**Safety**: Tests before/after each removal, auto-rollback on failure.

See [agents/refactor-cleaner/agent.md](agents/refactor-cleaner/agent.md)

### codemap-updater

Generate token-efficient architecture documentation from codebase analysis.

**Output**:
```
codemaps/
├── architecture.md   # Overall structure
├── backend.md        # API routes, services
├── frontend.md       # Pages, components
└── data.md           # Models, schemas
```

**Triggers**:
- Keywords: `codemap`, `architecture`, `documentation`
- Direct call: `Task(subagent_type: "codemap-updater")`

**Features**: Multi-language support (Go, Python, JS/TS, Rust), diff detection, freshness timestamps.

See [agents/codemap-updater/agent.md](agents/codemap-updater/agent.md)

### e2e-browser

Run E2E tests using Claude in Chrome for real browser automation.

**Prerequisites**:
- Claude in Chrome MCP extension installed and connected

**Triggers**:
- Keywords: `e2e`, `test`, `browser`, `chrome`, `visual`
- Direct call: `Task(subagent_type: "e2e-browser")`

**Capabilities**:
- Navigate to URLs, click elements, fill forms
- Take screenshots at each step
- Record test flow as GIF
- Verify page content and element states
- Generate test reports

**Usage**:
```bash
/e2e test login flow on https://example.com
/e2e verify search works on current page
/e2e record checkout flow with GIF
```

See [agents/e2e-browser/agent.md](agents/e2e-browser/agent.md)

## Plugins

*Coming soon*

## Directory Structure

```
claude-skills/
├── commands/
│   ├── plan.md
│   ├── architect.md
│   ├── code-invs.md
│   ├── refactor-clean.md
│   ├── update-codemaps.md
│   └── e2e.md
├── skills/
│   ├── continuous-learning/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── cr/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── peer-review/
│   │   └── SKILL.md
│   └── tdd/
│       └── SKILL.md
├── agents/
│   ├── architect/
│   │   └── agent.md
│   ├── code-reviewer/
│   │   └── agent.md
│   ├── codebase-investigator/
│   │   └── agent.md
│   ├── planner/
│   │   └── agent.md
│   ├── refactor-cleaner/
│   │   └── agent.md
│   ├── codemap-updater/
│   │   └── agent.md
│   └── e2e-browser/
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
