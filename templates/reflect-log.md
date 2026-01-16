# Reflect Change Log

> Append-only log of all rule changes. Do not manually edit.

## Log Format

```
[{timestamp}] {action} | {rule-id} | {details}
```

### Action Types
- `PROPOSED` - New rule extracted from conversation
- `APPROVED` - High-confidence rule approved by user
- `DEMOTED` - Rule confidence level decreased
- `PROMOTED` - Rule confidence level increased
- `REJECTED` - Proposed rule rejected
- `DEPRECATED` - Existing rule marked deprecated
- `CONFIRMED` - Existing rule reinforced (increment counter)

---

## Change History

<!--
Example entries:
[2024-01-15 14:30:00] PROPOSED | frontend-no-inline-styles | confidence=high, scope=frontend
[2024-01-15 14:35:00] APPROVED | frontend-no-inline-styles | approved by user
[2024-01-14 10:00:00] PROMOTED | api-error-codes | low → medium (3 confirmations)
[2024-01-13 16:45:00] CONFIRMED | security-sql-parameterized | confirmations=5
-->

