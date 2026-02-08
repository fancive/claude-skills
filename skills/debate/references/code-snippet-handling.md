# Code Snippet Handling (No Git Pollution)

Use this protocol when debate target is code snippet, not a git diff.

## Rule

- Never `git add` snippet files by default.
- Keep snippet files in session directory only.
- Remove temp files via `trap` when round ends, while preserving session artifacts.

## Session Paths

```bash
SESSION_DIR="<SESSION_BASE>/<session-id>"
SNIPPET_FILE="$SESSION_DIR/snippet-r<round>.code"
```

## Claude Code -> Codex

Preferred (no staging):

```bash
codex exec "Read $SNIPPET_FILE. Review this code snippet.
Output:
## P1 - Must Fix
## P2 - Should Fix
## P3 - Nice to Have
Include concrete evidence."
```

Fallback (only if explicitly requested by user):

1. stage isolated snippet
2. run `codex review --uncommitted`
3. unstage immediately

## Codex CLI -> Claude

```bash
claude -p "Read $SNIPPET_FILE. Review this code snippet.
Output:
## P1 - Must Fix
## P2 - Should Fix
## P3 - Nice to Have
Include concrete evidence."
```

## Large Snippet Guard

If snippet is too large:

1. split into logical chunks
2. review high-risk functions first
3. aggregate findings into one round summary

## File Type Hint

If possible, include language hint in filename:

- `snippet-r1.py`
- `snippet-r1.ts`
- `snippet-r1.go`

This improves linting and model interpretation.
