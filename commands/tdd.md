---
description: Test-Driven Development workflow. Write tests FIRST, then implement. Enforces Red-Green-Refactor cycle with 80%+ coverage.
---

# /tdd

Invoke the **tdd-guide** agent to implement with test-driven development.

## When to Use

- Implementing new features
- Fixing bugs (write failing test first)
- Refactoring existing code
- Building critical business logic

## TDD Cycle

```
RED    → Write failing test
GREEN  → Minimal code to pass
REFACTOR → Improve while green
```

## What It Does

1. Define interfaces/types
2. Write failing tests (RED)
3. Implement minimal code (GREEN)
4. Refactor with tests passing
5. Verify 80%+ coverage

## Example

```
/tdd implement a function to validate email addresses

Agent will:
1. Create interface: validateEmail(email: string): boolean
2. Write tests: valid emails, invalid emails, edge cases
3. Run tests → verify FAIL
4. Implement validation logic
5. Run tests → verify PASS
6. Refactor and check coverage
```

## Coverage Requirements

- **80% minimum** for all code
- **100%** for financial/auth/security logic

## Integration

- Use `/plan` first to understand scope
- Use `/cr` after implementation
