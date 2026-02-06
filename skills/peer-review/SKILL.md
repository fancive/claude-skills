---
name: peer-review
description: "Cross-model peer review for plans, architecture decisions, and viewpoints. Outbound only: send your proposal brief to the opposite model for challenge. For code diff review, use cr. Keywords: peer review, cross review, proposal review, architecture review, second opinion, 方案评审, 观点审查, 审查"
---

# Peer Review - Cross-Model Proposal Review

Review plans and viewpoints, not code diffs.

## Positioning

- `cr`: code-level review (diff, correctness, security, performance)
- `peer-review`: decision-level review (assumptions, tradeoffs, risks, alternatives)

If the request is code-diff focused, route to `cr`.

## Environment Detection

```bash
# Codex environment: CODEX_SANDBOX_ID or CODEX_THREAD_ID exists
# Claude environment: otherwise
```

## Input Contract

Prepare one proposal brief with:

1. Decision or claim to evaluate
2. Context and constraints
3. Options considered
4. Recommended option and rationale
5. Risks and unknowns
6. What feedback is requested

If user did not provide all fields, ask concise follow-up questions, then synthesize the brief.

Write brief to project-local temp file:

```bash
BRIEF_FILE=".git/peer-review-$(date +%s)-$$.md"
trap 'rm -f "$BRIEF_FILE"' EXIT
```

## Review Criteria

1. Problem framing: is the target problem stated correctly?
2. Assumptions: are they explicit, testable, and supported?
3. Tradeoffs: cost, complexity, latency, risk, maintainability
4. Alternatives: were viable options ignored?
5. Risk controls: rollback, blast radius, observability
6. Decision quality: is recommendation consistent with constraints?

## Workflow

### Claude Code Environment -> Codex Reviews

1. Verify backend availability:
   ```bash
   command -v codex || { echo "codex CLI not found"; exit 1; }
   ```
2. Run Codex challenge:
   ```bash
   codex exec "Read $BRIEF_FILE.
   Review this proposal using these criteria:
   1) Problem framing
   2) Assumptions
   3) Tradeoffs
   4) Alternatives
   5) Risk controls
   6) Decision quality
   Output:
   ## P1 - Must Reconsider
   ## P2 - Should Improve
   ## P3 - Nice to Strengthen
   ## Missing Alternatives
   ## Recommended Decision"
   ```

### Codex CLI Environment -> Claude Reviews

1. Verify backend availability:
   ```bash
   command -v claude || { echo "claude CLI not found"; exit 1; }
   ```
2. Run Claude challenge:
   ```bash
   claude -p "Read $BRIEF_FILE.
   Review this proposal using these criteria:
   1) Problem framing
   2) Assumptions
   3) Tradeoffs
   4) Alternatives
   5) Risk controls
   6) Decision quality
   Output:
   ## P1 - Must Reconsider
   ## P2 - Should Improve
   ## P3 - Nice to Strengthen
   ## Missing Alternatives
   ## Recommended Decision"
   ```

## Output Format

```markdown
## Peer Review Results

### P1 - Must Reconsider
- [decision/claim] why it is risky or invalid

### P2 - Should Improve
- [gap] concrete revision

### P3 - Nice to Strengthen
- [enhancement] optional but valuable

### Missing Alternatives
- [option] why it should be evaluated

### Recommended Decision
- Keep / Revise / Reject

### Next Actions
1. [ ] action item
2. [ ] action item
```

## Guardrails

- Focus on decision quality, not wording style.
- Prefer falsifiable arguments and measurable criteria.
- If evidence is insufficient, state `insufficient evidence` explicitly.
- Do not treat backend model output as truth; verify before adopting.
