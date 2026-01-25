---
description: Read-only codebase analysis. Search files, trace dependencies, understand architecture. Outputs findings to notes/ directory.
---

# /code-invs

Invoke the **codebase-investigator** agent for code analysis.

## When to Use

- Understanding unfamiliar codebase
- Tracing how a feature works
- Finding where something is defined
- Analyzing dependencies
- Documenting architecture

## What It Does

1. Search files and code patterns
2. Trace dependencies and data flow
3. Analyze architecture
4. Output structured report to `notes/`

## Example

```
/code-invs how does the authentication flow work?

Agent will:
1. Search for auth-related files
2. Trace login → session → middleware
3. Map dependencies
4. Output: notes/auth-flow-analysis.md
```

## Output Location

All findings are saved to `notes/` directory as Markdown.

## Read-Only

This agent only reads code, never modifies. Safe for exploration.

## Integration

- After investigation → `/plan` to implement changes
- For architecture decisions → `/architect`
