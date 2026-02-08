# Judge Analysis Rubric

Use this rubric in each debate round after receiving opposite-model critique.

## Goal

Convert raw critique into actionable decision guidance:

- validate claims against current artifact/context
- classify findings
- recommend next action (`A/B/C/D/E`)

## 1) Classification

Classify each critique item:

- `Valid`: supported by evidence and relevant constraints.
- `Invalid`: incorrect assumption, wrong context, or non-issue.
- `Missing`: important issue not raised by opposite model.

For valid items, assign severity:

- `P1`: correctness/security/reliability risk
- `P2`: significant maintainability/performance/compatibility issue
- `P3`: optional improvement

## 2) Evidence Rules

Require concrete evidence:

- code: `file:line` or reproducible behavior
- proposal: explicit constraint/tradeoff/risk linkage

If evidence is weak, mark item as `needs_evidence` and avoid `P1`.

## 3) Recommendation Mapping (A/B/C/D/E)

Recommend one option per round:

- `A Keep original`
  - use when most critique is invalid, no new P1/P2
- `B Accept opposite`
  - use when opposite has dominant valid P1/P2 and clear replacement
- `C Generate compromise`
  - use when both sides have partially valid points
- `D Continue debate`
  - use when key disagreements remain unresolved
- `E Stop`
  - use when budget exhausted or low-value churn

## 4) Decision Heuristics

Suggested thresholds:

- Recommend `B` if `valid(P1)>=1` and replacement is concrete.
- Recommend `C` if both sides have valid non-overlapping strengths.
- Recommend `D` if unresolved P1 exists and evidence is incomplete.
- Recommend `A` if `invalid` dominates and no `valid P1/P2`.

## 5) Judge Output Template

```markdown
## Judge Analysis

### Valid
- [P1|P2|P3] ...

### Invalid
- ...

### Missing
- ...

### Recommendation
- Suggested option: A|B|C|D|E
- Why: ...
```

## 6) Guardrails

- Do not auto-accept opposite critique.
- Do not over-index on style-only comments.
- Prefer conservative recommendations under uncertainty.
