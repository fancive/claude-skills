---
description: System design and architecture decisions. Evaluates trade-offs, recommends patterns, creates ADRs. Use for technical decision-making.
---

# /architect

Invoke the **architect** agent for system design and technical decisions.

## When to Use

- Choosing between technologies
- Designing new system components
- Evaluating scalability approaches
- Making architectural trade-offs
- Creating Architecture Decision Records (ADRs)

## What It Does

1. Analyze current architecture
2. Gather requirements (functional + non-functional)
3. Propose design with trade-off analysis
4. Document decision as ADR

## Example

```
/architect should we use Redis or PostgreSQL for caching?

Agent will output:
- Context analysis
- Trade-off comparison (Pros/Cons)
- Alternatives considered
- Recommendation with rationale
- ADR format documentation
```

## Output: ADR Format

```markdown
# ADR-001: [Decision Title]

## Context
[Why this decision is needed]

## Decision
[What we decided]

## Consequences
- Positive: ...
- Negative: ...
- Alternatives considered: ...
```

## Integration

- For implementation planning → `/plan`
- For code review → `/cr`
