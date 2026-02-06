---
name: cr
description: "Cross-model code review. In Claude Code, sends diff to Codex. In Codex CLI, sends diff to Claude. Auto-detects environment. Use when: user says /cr, 'code review', 'review my code', '代码审核', '代码审查', or wants a second opinion on code changes. Keywords: review, cr, code review, codex, 代码审核, 代码审查, second opinion"
---

# CR — Cross-Model Code Review

Get your code reviewed by a **different** model. Claude's code → Codex reviews. Codex's code → Claude reviews.

For proposal, architecture, or viewpoint review (non-code), use `peer-review`.

## Environment Detection

```bash
# Codex environment: CODEX_SANDBOX_ID or CODEX_THREAD_ID exists
# Claude environment: otherwise
```

## Workflow

### Claude Code Environment → Codex Reviews

Invoke the `code-reviewer` agent which handles:
- CHANGELOG auto-generation
- File staging
- Lint
- `codex review --uncommitted` with difficulty-based config
- Self-correction
- P1/P2/P3 report

See [references/codex-backend.md](references/codex-backend.md) for full agent protocol.

### Codex CLI Environment → Claude Reviews

**Prerequisite**: Verify `claude` CLI is available:
```bash
command -v claude || { echo "claude CLI not found"; exit 1; }
```

**Key constraint**: `claude -p` cannot read `/tmp` files but CAN read files in the current project directory.

1. Check workspace and assess difficulty:
   ```bash
   git diff --name-only && git status --short
   git diff --stat
   # Files ≥ 10 or changes ≥ 500 lines → Hard, otherwise Normal
   ```

2. Write diff to `.git/` temp files (hidden from working tree):
   ```bash
   DIFF_FILE=".git/cr-review-$(date +%s)-$$.diff"
   STAT_FILE=".git/cr-review-$(date +%s)-$$.stat"
   trap 'rm -f "$DIFF_FILE" "$STAT_FILE"' EXIT
   git diff > "$DIFF_FILE"
   git diff --stat > "$STAT_FILE"
   ```

3. Run Claude review:
   ```bash
   claude -p "Read $DIFF_FILE and $STAT_FILE. Review the code diff. Output ## P1 - Must Fix, ## P2 - Should Fix, ## P3 - Nice to Have. Focus: security, correctness, performance, maintainability."
   ```

4. Cleanup is automatic via `trap`.

## Output Format (unified)

```markdown
## Code Review Results

### P1 - Must Fix
- [file:line] Critical issue description

### P2 - Should Fix
- [file:line] Important improvement

### P3 - Nice to Have
- Optional optimization

### Suggested Actions
1. [ ] Action item 1
2. [ ] Action item 2
```

## Difficulty Assessment

| Condition | Level |
|-----------|-------|
| Files ≥ 10 or changes ≥ 500 lines | Hard |
| Otherwise | Normal |

For Codex backend: adjusts `model_reasoning_effort`. For Claude backend: included as context in the prompt.
