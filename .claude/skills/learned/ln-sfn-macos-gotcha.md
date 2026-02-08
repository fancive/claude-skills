---
name: ln-sfn-macos-gotcha
description: "ln -sfn creates symlink INSIDE real directories on macOS. Must detect and rm -rf first."
tags: [blocker, macos, symlink]
---

# ln -sfn on macOS: Real Directory Gotcha

## Blocker

On macOS, `ln -sfn source target` behaves differently depending on whether `target` is:
- **A symlink** -> replaces it (correct)
- **A real directory** -> creates symlink INSIDE the directory (wrong)

## Safe Pattern

```bash
dst="$HOME/.claude/skills/my-skill"
src="/path/to/skills/my-skill"

if [ -d "$dst" ] && [ ! -L "$dst" ]; then
  echo "Warning: $dst is a real directory, replacing with symlink"
  rm -rf "$dst"
fi
ln -sfn "$src" "$dst"
```

## Avoid

```bash
# DANGEROUS: if ~/.claude/skills/my-skill/ is a real dir,
# this creates ~/.claude/skills/my-skill/my-skill -> source
ln -sfn /path/to/skills/my-skill ~/.claude/skills/my-skill
```

## Context

Discovered while building `skill-link`. Codex CLI's `~/.codex/skills/` had real directories from manual copies. `ln -sfn` silently created nested symlinks instead of replacing them.
