# Codex Backend Protocol

Full protocol when using Codex as the review backend (Claude Code environment).

This is handled by the `code-reviewer` agent. The skill invokes the agent; this reference documents what the agent does.

## Protocol

```
1. [CHECK]     git status → decide review mode
2. [CHANGELOG] Check & auto-generate if not updated
3. [STAGE]     Stage new files (codex requires tracked files)
4. [LINT]      Run project-specific linter
5. [ASSESS]    Parse git diff --stat → determine difficulty
6. [REVIEW]    codex review with appropriate config
7. [FIX]       Self-correct if intent ≠ implementation
8. [REPORT]    Return P1/P2/P3 structured results
```

## CHANGELOG Auto-Generation

If CHANGELOG.md not updated in the diff:
1. Analyze changes via `git diff --stat` and `git diff`
2. Generate entry under `[Unreleased]` section
3. Format: Added / Changed / Fixed with brief descriptions

## Staging

```bash
git ls-files --others --exclude-standard -z | while IFS= read -r -d '' f; do git add -- "$f"; done
```

## Lint (Auto-detect)

```bash
# Go: go fmt ./... && go vet ./...
# Node: npm run lint:fix || npm run lint || true
# Python: black . || true && ruff check --fix . || true
```

## Difficulty → Codex Config

| Condition | Config |
|-----------|--------|
| Files ≥ 10 or changes ≥ 500 lines | `model_reasoning_effort=xhigh` |
| Otherwise | `model_reasoning_effort=high` |

## Codex Commands

```bash
codex review --uncommitted --config model_reasoning_effort=high
codex review --uncommitted --config model_reasoning_effort=xhigh
codex review --commit HEAD --config model_reasoning_effort=high
```

## Self-Correction

If Codex finds CHANGELOG inconsistent with code:
- Code error → fix the code
- Description inaccurate → update CHANGELOG
