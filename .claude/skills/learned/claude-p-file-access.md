---
name: claude-p-file-access
description: "claude -p cannot read /tmp files. Use .git/ for temp files with trap cleanup."
tags: [blocker, claude-cli, codex-cli]
---

# claude -p File Access Constraints

## Blocker

`claude -p` (piped/prompt mode) **cannot** read files in `/tmp/` or other system temp directories.

## What Works

- Project-local files (relative or absolute paths within the repo)
- `.git/` subdirectory files (hidden from working tree but readable)

## Pattern

```bash
TEMP_FILE=".git/my-temp-$(date +%s)-$$.md"
trap 'rm -f "$TEMP_FILE"' EXIT

# Write content
echo "..." > "$TEMP_FILE"

# claude -p can read it
claude -p "Read $TEMP_FILE and analyze it."
```

## Avoid

```bash
# BROKEN: claude -p cannot read this
TEMP_FILE="/tmp/review-$$.md"
claude -p "Read $TEMP_FILE"  # Will fail silently or error
```

## Context

Discovered while building the `cr` skill's Codex CLI -> Claude review path.
