---
description: Create implementation plan for complex features. Analyzes codebase, breaks down into phases, identifies risks. WAIT for confirmation before coding.
---

# /plan

Invoke the **planner** agent to create a comprehensive implementation plan.

## When to Use

- Starting a new feature
- Complex refactoring
- Multiple files will be affected
- Requirements are unclear

## What It Does

1. Analyze codebase structure
2. Break down into phases with specific steps
3. Identify dependencies and risks
4. Present plan and **wait for confirmation**

## Example

```
/plan add user authentication with OAuth

Agent will output:
- Requirements restatement
- Phase breakdown (database → backend → frontend)
- Risk assessment
- Complexity estimate
- WAITING FOR CONFIRMATION
```

## Integration

- After planning → `/tdd` to implement
- For architecture decisions → `/architect`
