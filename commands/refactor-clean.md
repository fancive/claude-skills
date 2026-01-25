---
description: Dead code cleanup for Python, Go, JS/TS. Detects language, finds unused code, safely removes with test verification.
---

# /refactor-clean

Invoke the **refactor-cleaner** agent to find and remove dead code.

## Supported Languages

| Language | Detection | Tools Used |
|----------|-----------|------------|
| Python | `pyproject.toml`, `requirements.txt` | vulture, dead, autoflake |
| Go | `go.mod` | deadcode, staticcheck, go mod tidy |
| JS/TS | `package.json` | knip, depcheck, ts-prune |

## Usage

```bash
/refactor-clean              # Auto-detect language, full cleanup
/refactor-clean --check      # Analysis only, no changes
/refactor-clean --python     # Force Python mode
/refactor-clean --go         # Force Go mode
/refactor-clean --js         # Force JS/TS mode
```

## What It Finds

- Unused imports
- Unused functions/methods
- Unused variables
- Unused files
- Unused dependencies

## Safety

1. **Tests run before AND after each removal**
2. **Auto-rollback if tests fail**
3. **Never removes entry points or configs**
4. **Creates backup branch first**

## Example

```
/refactor-clean

Agent will:
1. Detect: Python project (found pyproject.toml)
2. Run: vulture, dead, autoflake --check
3. Find: 12 unused imports, 3 unused functions, 1 unused dependency
4. Remove safely (with test verification)
5. Output: .reports/dead-code-cleanup.md
```

## Output

```
CLEANUP COMPLETE

Removed:
- 12 unused imports
- 3 unused functions (_old_helper, _deprecated, _unused)
- 1 dependency (unused-package)

Skipped (manual review):
- 2 exported functions (may be used dynamically)

Tests: 45/45 passed
Coverage: 82% → 84% (+2%)
```

## Integration

- Use `/verify` after cleanup to confirm project health
- Use `/cr` to review the cleanup changes
