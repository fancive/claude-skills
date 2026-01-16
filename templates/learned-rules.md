# Learned Rules

> 由 `/reflect` 自动管理。可手动编辑，变更会被追踪。

---

## High Confidence

严格执行。Claude 不会违反这些规则。

### security-no-secrets-in-code
- scope: general
- confidence: high
- constraint: Never hardcode secrets, API keys, passwords, or tokens. Always use environment variables or secret management.
- rationale: 安全基线，防止凭证泄露
- added: baseline
- confirmations: 0

---

## Medium Confidence

推荐模式。Claude 会遵循，除非有充分理由。

<!-- 示例:
### frontend-component-naming
- scope: frontend
- confidence: medium
- constraint: Use PascalCase for React component names.
- rationale: 团队代码风格约定
- added: 2024-01-15
- confirmations: 2
-->

---

## Low Confidence

观察到的模式。Claude 会考虑但不强制。

<!-- 示例:
### observability-tracing
- scope: backend
- confidence: low
- constraint: Consider adding tracing spans to new service methods.
- rationale: 连续 3 次 review 中被要求
- added: 2024-01-10
- confirmations: 3
-->

---

## Deprecated

已弃用的规则，保留用于审计。

<!-- 格式: {rule-id}: deprecated on {date}, reason: {reason} -->
