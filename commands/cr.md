---
description: Code review via OpenAI Codex. Sends git diff for external review, returns P1/P2/P3 prioritized feedback.
---

# /cr

Invoke the **code-reviewer** agent to review code changes via Codex.

## When to Use

- Before committing changes
- Want a second opinion on implementation
- Checking for security/performance issues

## What It Does

1. Gather git diff (uncommitted or last commit)
2. Format review request
3. Send to OpenAI Codex
4. Return structured P1/P2/P3 feedback

## Example

```
/cr review my uncommitted changes

Agent will:
1. Run git diff --stat
2. Format code review request
3. Call codex exec
4. Return:
   - P1 (Must fix): Critical issues
   - P2 (Should fix): Important improvements
   - P3 (Nice to have): Optional optimizations
```

## Review Focus

- **Security**: credentials, injection, auth bypass
- **Correctness**: logic errors, edge cases
- **Performance**: inefficient patterns
- **Maintainability**: complexity, readability

## Integration

- For design review → `/architect`
- For implementation → `/tdd`
