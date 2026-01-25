---
description: Generate architecture documentation from codebase. Creates token-efficient codemaps for quick context understanding.
---

# /update-codemaps

Invoke the **codemap-updater** agent to generate architecture documentation.

## What It Does

1. Scan project structure
2. Extract routes, components, models
3. Generate structured codemaps
4. Compare with previous version
5. Update if changed (ask if >30% diff)

## Output

```
codemaps/
├── architecture.md   # Overall structure
├── backend.md        # API routes, services
├── frontend.md       # Pages, components
├── data.md           # Models, schemas
└── index.md          # Quick reference
```

## Supported Languages

- Go
- Python
- TypeScript/JavaScript
- Rust

## Usage

```bash
/update-codemaps              # Full update
/update-codemaps --check      # Show diff only, no update
/update-codemaps --force      # Update without confirmation
```

## Example Output (backend.md)

```markdown
# Backend Architecture

**Last Updated**: 2025-01-25

## API Routes

| Route | Method | Handler | Purpose |
|-------|--------|---------|---------|
| /api/users | GET | ListUsers | List users |
| /api/auth/login | POST | Login | User login |

## Services

| Service | Location | Dependencies |
|---------|----------|--------------|
| UserService | internal/user | DB, Cache |
```

## Why Use Codemaps

1. **Save tokens** - Claude reads codemaps instead of all source files
2. **Faster context** - Structured overview vs. raw code
3. **Stay fresh** - Timestamps show when last updated

## Integration

- Run after major code changes
- Commit codemaps to git
- Use `/verify` after updating
