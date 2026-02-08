---
name: cli-style
description: "CLI output styling for modern terminal apps. Use when: (1) optimizing CLI app output, (2) adding colors/icons to terminal, (3) improving terminal UX, (4) designing CLI interfaces. Keywords: cli style, terminal output, 命令行美化, cli ui, spinner, progress bar"
---

# CLI Style

Style CLI output following modern CLI Agent UI patterns (based on Claude Code design).

## Quick Reference

### Semantic Colors

```
green   success/create     ✓ Success, file created
red     error/delete       ✗ Error, file deleted
yellow  warning/confirm    ⚠ Warning, needs confirmation
blue    info/in-progress   ℹ Info, analyzing
cyan    review/secondary   Code review, hints
magenta AI-generated       Generated content
grey    disabled/history   Old items, disabled
```

### Status Symbols

```
✓ success (green)     ○ pending (grey)
✗ error (red)         ● active (cyan)
⚠ warning (yellow)    → selected
ℹ info (blue)
```

### Components

**Spinner** (Braille, 80ms/frame):
```
⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏
⠋ Thinking... (234 tokens)
```

**Progress**:
```
[████████░░░░] 67% (4/6)
```

**Selection**:
```
  ○ option-a
→ ● option-b (recommended)
  ○ option-c
```

**Dialog**:
```
┌─ Title ─────────────────────┐
│  Content here               │
│  [Cancel]  [OK]             │
└─────────────────────────────┘
```

**Diff**:
```
- old line  (red)
+ new line  (green)
```

### Box Drawing

```
Single: ┌──┐ │ └──┘
Double: ╔══╗ ║ ╚══╝
ASCII:  +--+ | +--+  (fallback)
Tree:   ├── │ └──
```

## Libraries

| Lang   | Color        | Spinner     | Progress     | Interactive |
|--------|--------------|-------------|--------------|-------------|
| Node   | chalk        | ora         | cli-progress | inquirer    |
| Go     | fatih/color  | spinner     | progressbar  | survey      |
| Python | rich         | rich        | rich         | rich        |
| Rust   | colored      | indicatif   | indicatif    | dialoguer   |

## Degradation

```bash
# Respect NO_COLOR
if [ -n "$NO_COLOR" ] || ! [ -t 1 ]; then
  # disable colors and animations
fi
```

Unicode fallback:
```
✓ → [OK]   ✗ → [FAIL]   ⚠ → [WARN]   → → ->
```

## Workflow

When optimizing CLI output:

1. **Audit current output**
   - Identify status messages, errors, progress indicators
   - Find places lacking visual feedback

2. **Apply semantic colors**
   - Map message types to colors (see Quick Reference)
   - Add status symbols where appropriate

3. **Add dynamic feedback**
   - Spinner for operations >500ms
   - Progress bar for multi-step tasks
   - Status line for persistent state

4. **Handle degradation**
   - Check `NO_COLOR` env var
   - Check `!isTTY` for piped output
   - Provide ASCII fallbacks

5. **Test accessibility**
   - Don't rely on color alone (use symbols too)
   - Ensure 4.5:1 contrast ratio

## Checklist

```
[ ] Semantic colors applied (green=success, red=error, etc.)
[ ] Status symbols present (✓ ✗ ⚠ ℹ)
[ ] Spinner for long operations (>500ms)
[ ] Progress bar for multi-step tasks
[ ] NO_COLOR env var respected
[ ] Non-TTY fallback works
[ ] Error messages are actionable
[ ] Dangerous actions require confirmation
```

## Full Spec

For complete documentation including ANSI codes, keyboard shortcuts, and detailed component specs, see [cli-agent-ui-spec.md](references/cli-agent-ui-spec.md).
