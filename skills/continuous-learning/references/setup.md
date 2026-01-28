# Setup Guide

## Hook Configuration

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning/scripts/evaluate-session.sh"
      }]
    }]
  }
}
```

## Configuration

Create `~/.claude/skills/continuous-learning/config.json`:

```json
{
  "min_session_length": 10,
  "patterns_to_detect": [
    "error_resolution",
    "debugging_techniques",
    "workarounds",
    "project_specific",
    "user_preference"
  ],
  "ignore_patterns": [
    "simple_typos",
    "one_time_fixes",
    "trivial"
  ]
}
```

## Installation

```bash
# Symlink skill to ~/.claude/skills/
ln -sf /path/to/continuous-learning ~/.claude/skills/continuous-learning

# Verify hook setup
cat ~/.claude/settings.json | grep -A5 "Stop"
```

## Verify Installation

After setup, end a session with 10+ messages. Check:

```bash
cat ~/.claude/pending-skills.md
```

Should show detected patterns if any were found.
