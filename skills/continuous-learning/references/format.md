# Skill Output Format

Saved to `.claude/skills/learned/{name}.md` or `~/.claude/skills/learned/{name}.md`:

```markdown
---
name: {pattern-name}
description: {one-line description}
extracted: {date}
---

# {Descriptive Pattern Name}

## Problem
{What problem this solves - be specific}

## Solution
{The pattern/technique/workaround}
{For negative patterns, use "What Failed" + "Avoid" + "Instead" sections below}

## Example
{Code example if applicable}

## When to Use
{Trigger conditions - what should activate this skill}

## What Failed (negative patterns only)
{The approach that was tried and why it doesn't work}

## Avoid (negative patterns only)
{What NOT to do}

## Instead (negative patterns only)
{What to do instead}
```

## Example: Dead End / Blocker Skill

```markdown
---
name: no-stdin-in-stop-hook
description: Claude Code Stop hook does not pipe session transcript to stdin
extracted: 2026-02-06
---

# Stop Hook Has No stdin Access

## Problem
Attempted to read session transcript via `TRANSCRIPT=$(cat)` in a Stop hook script.

## What Failed
The script hangs or gets empty input — Claude Code's Stop hook triggers the command but does not pipe any data to stdin.

## Avoid
Don't design pipelines that rely on reading transcript from Stop hook stdin.

## Instead
Do extraction inside the active session (e.g., `/learn` command) where the model has full conversation context.
```

## Example: Agent Introspection Skill

```markdown
---
name: dont-assert-stdin-in-hooks
description: Agent assumed Stop hook receives stdin without testing — design flaw went undetected through 3 review rounds
extracted: 2026-02-06
---

# Verify Assumptions Before Building On Them

## What Went Wrong
Agent designed a two-phase system where Stop hook reads transcript from stdin. Multiple review rounds accepted this assumption without anyone testing it.

## Why
Knowledge gap: agent didn't know Claude Code's hook execution model. Combined with confirmation bias — the design "made sense" so nobody questioned the premise.

## What to Update
When a design depends on an unverified platform behavior, add a "verify first" step before building the rest of the pipeline. Mark assumptions explicitly as UNTESTED.
```

## Example: User Preference Skill

```markdown
---
name: prefer-const-over-var
description: Always use const/let instead of var in JavaScript
extracted: 2024-01-15
---

# Prefer const Over var

## Problem
User corrected: "不要用 var，用 const"

## Solution
Always use `const` for immutable bindings, `let` for mutable. Never use `var`.

## Example
// Bad
var name = "test";

// Good
const name = "test";

## When to Use
Any JavaScript/TypeScript code generation or review.
```
