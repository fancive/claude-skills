---
name: reflect
description: "Extract reusable engineering rules from conversation corrections/feedback. Use when user says 'reflect', 'remember this', 'learn from this', or after receiving corrections. Two-phase workflow: auto-capture to pending → user review to commit."
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
argument-hint: "[--dry-run] [--review]"
---

# Reflect Skill

Extract corrections and preferences into reusable rules. **Correct once, never again.**

## Two-Phase Workflow

### Phase 1: Auto-Capture (Passive)

During normal conversation, detect correction signals and log to pending:

```
User: "不要用 var，用 const"
Claude: [fixes code]
        📝 规则信号: prefer-const (已暂存)
```

**Trigger keywords**: 不要、别、必须、always、never、don't、用X不用Y

**Pending file**: `.claude/pending-rules.md`

### Phase 2: Review (`/reflect`)

1. Read pending rules from `.claude/pending-rules.md`
2. For each rule, use AskUserQuestion:
   ```yaml
   question: "规则: {id}\n{constraint}\n\n来源: \"{signal}\""
   options:
     - label: "存入项目 (推荐)"
     - label: "存入全局"
     - label: "跳过"
   ```
3. Write confirmed rules, clear pending
4. Log to `reflect-log.md`

**Important**: Ask first, then write. Never show diff before confirmation.

## File Locations

```
~/.claude/
├── learned-rules.md      # Global rules
└── reflect-log.md

./.claude/
├── learned-rules.md      # Project rules (higher priority)
├── pending-rules.md      # Pending (Phase 1 output)
└── reflect-log.md
```

## Rule Format

```markdown
### {rule-id}
- scope: {frontend|backend|api|security|general}
- confidence: {high|medium|low}
- constraint: {imperative instruction for Claude}
- rationale: {why this rule exists}
- added: {date}
```

## Quality Filter

Only capture rules that are:
- **Non-trivial**: Not obvious (✗ "变量要命名")
- **Actionable**: Specific instruction (✓ "用 dayjs 不用 moment")
- **Reusable**: Not one-time decisions

Skip: typos, formatting, temporary decisions.

## Arguments

- `--dry-run`: Show detected signals without writing
- `--review`: Review pending rules (same as no args if pending exists)

## Safety

- Auto-capture only stages, never writes directly
- All rules require user confirmation
- Never auto-delete rules
- Always show source signal
