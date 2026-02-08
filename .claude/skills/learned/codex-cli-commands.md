---
name: codex-cli-commands
description: "Codex CLI only has: codex (interactive), codex review, codex completion. No exec subcommand."
tags: [blocker, codex-cli, api-limitation]
---

# Codex CLI Available Commands

## Blocker

Codex CLI does **not** have a general-purpose `exec` or prompt subcommand.

## Available Commands

| Command | Purpose |
|---------|---------|
| `codex` | Interactive mode (like claude interactive) |
| `codex review` | Review code diffs (uncommitted or specific commit) |
| `codex completion` | Shell completion setup |

## Avoid

```bash
# BROKEN: 'exec' is not a codex subcommand
codex exec "Read file.md and analyze it"
```

## For Arbitrary Prompts

There is no direct equivalent of `claude -p "prompt"` for Codex CLI. To send arbitrary content to Codex for review, use `codex review` with the content staged as uncommitted changes.

## Context

Discovered while building `peer-review` skill's outbound challenge mode. The proposed `codex exec` command doesn't exist.
