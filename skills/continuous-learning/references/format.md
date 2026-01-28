# Output Format

## Pending Skills Format

`~/.claude/pending-skills.md`:

```markdown
## prisma-connection-pool-fix
- extracted: 2024-01-15
- source: Session debugging Prisma timeout
- summary: Fix Prisma connection pool exhaustion

### Problem
Prisma throws "Timed out fetching a new connection from the pool"

### Solution
Set `connection_limit` in DATABASE_URL or configure pooling

---

## next-cache-revalidation
- extracted: 2024-01-16
- source: Session fixing stale data
- summary: Force Next.js cache revalidation

### Problem
...
```

## Confirmed Skill Format

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

## Example
{Code example if applicable}

## When to Use
{Trigger conditions - what should activate this skill}
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
```javascript
// Bad
var name = "test";

// Good
const name = "test";
```

## When to Use
Any JavaScript/TypeScript code generation or review.
```
