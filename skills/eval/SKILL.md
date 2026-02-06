---
name: eval
description: "Eval-Driven Development: define capability/regression evals before coding, check during development, report after implementation. Use when: user says /eval, 'define eval', 'run eval', 'check eval', or wants to measure code quality with pass@k metrics. Keywords: eval, evaluate, test, metrics, pass@k, regression, capability, 评估"
---

# Eval — Eval-Driven Development

Define evals before coding, check during development, report after implementation.

## Usage

```
/eval define <name>   # Create eval definition before coding
/eval check <name>    # Run evals during development
/eval report <name>   # Generate full report after implementation
/eval list            # List all evals in project
```

## Subcommands

### define

Create eval definition at `.claude/evals/<name>.md`:

1. Ask user for feature description
2. Generate capability evals (what it should do)
3. Generate regression evals (what shouldn't break)
4. Define success metrics (pass@k targets)
5. Save to `.claude/evals/<name>.md`

### check

Run evals and show status:

1. Read eval definition from `.claude/evals/<name>.md`
2. Run code-based graders (grep, test, build)
3. Run model-based graders if needed
4. Flag items for human review
5. Show pass/fail status

### report

Generate comprehensive report:

1. Run all evals
2. Calculate pass@k metrics
3. Compare to baseline (if exists)
4. Generate markdown report
5. Append to `.claude/evals/<name>.log`

### list

Show all evals and their status.

## Output Format

```
EVAL REPORT: add-auth
=====================
Capability Evals:
  register:        PASS (pass@1)
  login:           PASS (pass@2)
  invalid-reject:  PASS (pass@1)
  Overall:         3/3

Regression Evals:
  public-routes:   PASS
  api-responses:   PASS
  Overall:         2/2

Metrics:
  pass@1: 67%
  pass@3: 100%

Status: READY FOR REVIEW
```

## File Structure

```
.claude/evals/
├── add-auth.md       # Definition
├── add-auth.log      # Run history
└── baseline.json     # Regression baselines
```
