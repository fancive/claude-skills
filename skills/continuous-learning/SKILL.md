---
name: continuous-learning
description: "Auto-extract reusable patterns and preferences from Claude Code sessions. Two-phase: auto-capture to pending, /learn to review. Use when: (1) session ends via Stop hook, (2) user says 'learn this', 'remember', '记住', '学习这个'. Keywords: learn, patterns, skills, preferences, 记住, 学习"
---

# Continuous Learning

Auto-extract reusable patterns from sessions. **Learn once, reuse forever.**

## Two-Phase Workflow

### Phase 1: Auto-Capture (Stop Hook)

Session ends → evaluate → stage to pending:

```text
[Session ends, 15+ messages]
[ContinuousLearning] Detected: prisma-connection-pool-fix
[ContinuousLearning] Staged to pending (run /learn to review)
```

### Phase 2: Review (`/learn`)

1. Read `~/.claude/pending-skills.md`
2. For each skill, AskUserQuestion:
   - "存入项目 (推荐)" → `.claude/skills/learned/`
   - "存入全局" → `~/.claude/skills/learned/`
   - "跳过" / "编辑后保存"
3. Write confirmed, clear pending

## Pattern Detection

**Detect**:
- `error_resolution` - Error + root cause + fix
- `debugging_techniques` - Non-obvious debug steps
- `workarounds` - Library quirks, API limitations
- `project_specific` - Codebase conventions
- `user_preference` - Corrections (不要、别、必须、always、never、don't)

**Ignore**: Simple typos, one-time fixes, trivial patterns.

## Quality Filter

Only extract patterns that are:
- **Non-trivial**: Not obvious
- **Reusable**: Helps future sessions
- **Specific**: Clear problem + solution
- **Actionable**: Can apply directly

## File Locations

```text
.claude/skills/learned/     # Project (higher priority)
~/.claude/skills/learned/   # Global
~/.claude/pending-skills.md # Staging
```

## References

- [Setup Guide](references/setup.md) - Hook configuration
- [Output Format](references/format.md) - Skill file format

## Related

- `/learn` command - Review pending skills
