---
description: Review pending skills extracted by continuous-learning. Keywords: learn, skills, patterns, extract
---

# /learn - Review Learned Skills

Review and confirm skills auto-captured by `continuous-learning` hook.

## Usage

```bash
/learn              # Review pending skills
/learn --dry-run    # Show pending without saving
```

## Workflow

1. **Check pending**: Read `~/.claude/pending-skills.md`
2. **Review each**: Ask user to confirm/skip/edit
3. **Save confirmed**: Write to `~/.claude/skills/learned/`
4. **Clear processed**: Remove from pending

## Review Process

For each pending skill:

```yaml
question: "Skill: {name}\n{summary}\n\n保存这个技能?"
options:
  - label: "存入项目 (推荐)"
    description: "保存到 .claude/skills/learned/ (仅当前项目)"
  - label: "存入全局"
    description: "保存到 ~/.claude/skills/learned/ (所有项目)"
  - label: "跳过"
    description: "不保存，从 pending 中移除"
  - label: "编辑后保存"
    description: "修改内容后保存"
```

## Pending Format

`~/.claude/pending-skills.md`:

```markdown
## prisma-connection-pool-fix
- extracted: 2024-01-15
- source: Session debugging Prisma timeout
- summary: Fix Prisma connection pool exhaustion by setting pool size

### Problem
Prisma throws "Timed out fetching a new connection from the pool"

### Solution
Set `connection_limit` in DATABASE_URL or use `@@map` for connection pooling

---

## next-cache-revalidation
...
```

## Output Format

Saved skills go to chosen location:
- **Project**: `.claude/skills/learned/{name}.md`
- **Global**: `~/.claude/skills/learned/{name}.md`

```markdown
---
name: prisma-connection-pool-fix
description: Fix Prisma connection pool exhaustion
extracted: 2024-01-15
---

# Prisma Connection Pool Fix

## Problem
...

## Solution
...

## Example
...

## When to Use
...
```

## No Pending?

If no pending skills, scan current session for extractable patterns:
- Error resolutions
- Debugging techniques
- Workarounds
- Project-specific patterns

## File Locations

```
.claude/                        # Project-level (higher priority)
└── skills/
    └── learned/                # Project skills

~/.claude/
├── pending-skills.md           # Pending (staging)
└── skills/
    └── learned/                # Global skills
```

**Priority**: Project skills override global skills with same name.

## Related

- `continuous-learning` skill - Auto-capture on session end
