# Command vs Skill Overlap Analysis

## Summary

Analyzed all 12 commands and 13 skills to determine overlap, redundancy, and whether commands can be replaced by skills.

## Inventory

### Commands (12)
| File | Name |
|------|------|
| `commands/plan.md` | `/plan` |
| `commands/architect.md` | `/architect` |
| `commands/tdd.md` | `/tdd` |
| `commands/refactor-clean.md` | `/refactor-clean` |
| `commands/update-codemaps.md` | `/update-codemaps` |
| `commands/code-invs.md` | `/code-invs` |
| `commands/e2e.md` | `/e2e` |
| `commands/eval.md` | `/eval` |
| `commands/cr.md` | `/cr` |
| `commands/learn.md` | `/learn` |
| `commands/peer-review.md` | `/peer-review` |
| `commands/skill-link.md` | `/skill-link` |

### Skills (13)
| File | Name |
|------|------|
| `skills/spec-interview/SKILL.md` | spec-interview |
| `skills/tech-design/SKILL.md` | tech-design |
| `skills/cli-style/SKILL.md` | cli-style |
| `skills/research/SKILL.md` | research |
| `skills/daily/SKILL.md` | daily |
| `skills/pyenv/SKILL.md` | pyenv |
| `skills/implement/SKILL.md` | implement |
| `skills/agent-browser/SKILL.md` | agent-browser |
| `skills/tdd/SKILL.md` | tdd |
| `skills/draw-io/SKILL.md` | draw-io |
| `skills/drawio/SKILL.md` | drawio |
| `skills/continuous-learning/SKILL.md` | continuous-learning |
| `skills/skill-link/SKILL.md` | skill-link |

### Agents (8)
| File | Name |
|------|------|
| `agents/planner/agent.md` | planner |
| `agents/architect/agent.md` | architect |
| `agents/tdd-guide/agent.md` | tdd-guide |
| `agents/refactor-cleaner/agent.md` | refactor-cleaner |
| `agents/codemap-updater/agent.md` | codemap-updater |
| `agents/codebase-investigator/agent.md` | codebase-investigator |
| `agents/e2e-browser/agent.md` | e2e-browser |
| `agents/code-reviewer/agent.md` | code-reviewer |

## Analysis Table

| Command | What it does (brief) | Has matching skill? | Has matching agent? | Verdict |
|---------|---------------------|--------------------|--------------------|---------|
| `/plan` | Thin wrapper: invokes `planner` agent for implementation planning. Only has usage docs and example. | No | Yes (`planner`) | **Keep as command** -- clean thin wrapper for agent invocation, no skill equivalent |
| `/architect` | Thin wrapper: invokes `architect` agent for system design and ADRs. Only has usage docs. | Partial (`tech-design` skill overlaps in scope) | Yes (`architect`) | **Keep as command** -- thin wrapper for agent. `tech-design` skill is complementary (interview-based), not identical |
| `/tdd` | Thin wrapper: invokes `tdd-guide` agent for TDD workflow. Only usage docs. | **Yes** (`skills/tdd/SKILL.md`) | Yes (`tdd-guide`) | **Redundant** -- both command and skill exist for TDD. Command invokes agent; skill provides inline TDD workflow. The `implement` skill also subsumes TDD+review. Consider merging or removing one. |
| `/refactor-clean` | Thin wrapper: invokes `refactor-cleaner` agent. Documents supported languages, safety measures. | No | Yes (`refactor-cleaner`) | **Keep as command** -- no skill equivalent, clean agent wrapper |
| `/update-codemaps` | Thin wrapper: invokes `codemap-updater` agent. Documents output structure and supported languages. | No | Yes (`codemap-updater`) | **Keep as command** -- no skill equivalent, clean agent wrapper |
| `/code-invs` | Thin wrapper: invokes `codebase-investigator` agent. Documents read-only analysis, outputs to `notes/`. | No | Yes (`codebase-investigator`) | **Keep as command** -- no skill equivalent, clean agent wrapper |
| `/e2e` | Thin wrapper: invokes `e2e-browser` agent. Documents browser E2E testing with screenshots/GIFs. | Partial (`agent-browser` skill covers browser automation broadly) | Yes (`e2e-browser`) | **Keep as command** -- `agent-browser` skill is a general browser automation toolkit, not E2E-test-specific. Different purpose. |
| `/eval` | Substantial content: defines subcommands (define/check/report/list), eval file structure, output format. Self-contained workflow. | No (CLAUDE.md mentions `eval-harness` skill but it does not exist on disk) | No | **Merge into skill** -- has substantial standalone logic, no backing agent. Better suited as a skill with its own directory for eval templates/scripts. |
| `/cr` | Invokes `code-reviewer` agent. Adds unique features: CHANGELOG auto-gen, lint integration, smart difficulty assessment, auto-staging, self-correction. Substantial content beyond thin wrapper. | No | Yes (`code-reviewer`) | **Keep as command** -- substantial value-add on top of agent invocation. Could be promoted to skill for more structure, but works well as-is. |
| `/learn` | Thin wrapper: delegates entirely to `skills/continuous-learning/SKILL.md`. Line 30 says "see `skills/continuous-learning/SKILL.md`" for details. | **Yes** (`continuous-learning`) | No | **Keep as command (entry point)** -- serves as a convenient trigger for the skill. The skill has all the logic. This is the intended pattern: command triggers skill. |
| `/peer-review` | Self-contained: cross-model review workflow. Verify each claim, structured output, no agent/skill backing. | No | No | **Keep as command OR merge into skill** -- has substantial standalone logic. If it grows, could become a skill. Currently compact enough as a command. |
| `/skill-link` | Thin wrapper: delegates to `skills/skill-link/SKILL.md` for full workflow. | **Yes** (`skill-link`) | No | **Keep as command (entry point)** -- serves as convenient trigger for the skill. Same pattern as `/learn`. |

## Key Findings

### Direct Overlaps (command + skill with same functionality)

1. **`/tdd` command + `skills/tdd/` skill + `tdd-guide` agent**: Triple overlap. The command invokes the agent, the skill provides an inline workflow, and the `implement` skill also incorporates TDD. The `skills/tdd/SKILL.md` is a lightweight 44-line version while the command invokes a full agent. Consider whether both are needed.

2. **`/learn` command + `skills/continuous-learning/` skill**: Intentional design. Command is a thin entry point; skill has all logic. This is the correct pattern per CLAUDE.md conventions.

3. **`/skill-link` command + `skills/skill-link/` skill**: Same intentional design as above. Command is entry point; skill has logic.

### Commands Without Backing Agent or Skill

1. **`/eval`**: Substantial standalone logic defining an eval-driven development workflow. CLAUDE.md references an `eval-harness` skill that does not exist. This command should either become a skill or the missing `eval-harness` skill should be created.

2. **`/peer-review`**: Self-contained cross-model review workflow with no backing agent or skill. Compact but could grow.

### Skills Without Matching Commands

These skills have no corresponding command entry point:
- `spec-interview` -- interview-based spec generation
- `tech-design` -- interview-based technical design
- `cli-style` -- CLI output styling reference
- `research` -- web research via Tavily
- `daily` -- Obsidian daily journaling
- `pyenv` -- Python environment setup
- `implement` -- TDD implementation with Codex review (overlaps with `/tdd` + `/cr`)
- `agent-browser` -- browser automation toolkit
- `draw-io` -- draw.io diagram editing (XML-based)
- `drawio` -- AI-powered draw.io with MCP (different from `draw-io`)

### Duplicate Skills

- **`draw-io`** and **`drawio`** are two separate skills for draw.io diagrams. `draw-io` is XML-editing focused; `drawio` is an AI-powered MCP-based approach (v2.0.0 by DayuanJiang). These appear to be two different approaches to the same domain rather than duplicates, but the naming is confusing.

### The `implement` Skill Subsumes Multiple Commands

The `skills/implement/SKILL.md` skill combines:
- TDD workflow (overlaps `/tdd` command)
- Codex code review per feature (overlaps `/cr` command)
- Task breakdown from tech-plan (overlaps `/plan` command partially)

This is the most comprehensive implementation skill but has no corresponding command.
