# Debate Protocols

This file defines executable contracts for `debate` routing.

## Contents

1. [Input Envelope](#1-input-envelope)
2. [Output Envelope](#2-output-envelope)
3. [Code Route Protocol](#3-code-route-protocol)
4. [Proposal Route Protocol](#4-proposal-route-protocol)
5. [Mixed Splitting Rules](#5-mixed-splitting-rules)
6. [Failure and Fallback](#6-failure-and-fallback)

---

## 1) Input Envelope

Every round builds one envelope:

```json
{
  "session_id": "debate-YYYYmmdd-HHMMSS-pid",
  "round": 1,
  "target": "code|proposal|mixed",
  "scope": "uncommitted|commit:<sha>|base:<branch>|range:<a>..<b>|file:<path>|snippet",
  "artifact_file": "<SESSION_DIR>/artifact.md",
  "budget_minutes": 20
}
```

## 2) Output Envelope

All backends should produce:

```json
{
  "summary": "short summary",
  "p1": ["..."],
  "p2": ["..."],
  "p3": ["..."],
  "missing": ["..."],
  "recommendation": "keep|revise|reject|continue",
  "evidence": ["file:line or textual evidence"]
}
```

If strict JSON is not possible, parse structured markdown sections with equivalent fields.

## 3) Code Route Protocol

### From Claude Code

When routing to Codex for code review:

```bash
codex review --uncommitted --config model_reasoning_effort=high
codex review --commit <sha> --config model_reasoning_effort=high
codex review --base <branch> --config model_reasoning_effort=high
```

For `scope=file:<path>` or `scope=snippet`, use snippet protocol in `code-snippet-handling.md`.

### From Codex CLI

When routing to Claude for code review, build diff artifacts under `<SESSION_DIR>/` and call:

```bash
claude -p "Read <diff_file> and <stat_file>. Review with P1/P2/P3 and evidence."
```

## 4) Proposal Route Protocol

### From Claude Code

When routing to Codex for proposal review:

```bash
codex exec "Read <artifact_file>. Review proposal with:
1) problem framing
2) assumptions
3) tradeoffs
4) alternatives
5) risk controls
6) decision quality
Output P1/P2/P3 + Missing + Recommended Decision."
```

### From Codex CLI

When routing to Claude for proposal review:

```bash
claude -p "Read <artifact_file>. Review proposal using the same six criteria. Output P1/P2/P3 + Missing + Recommended Decision."
```

## 5) Mixed Splitting Rules

When `target=mixed`, split deterministically:

1. Extract all fenced code blocks -> code segments.
2. Extract heading sections with signals (`Design`, `Proposal`, `Approach`, `Decision`, `Tradeoff`) -> proposal segments.
3. If one segment is empty, downgrade to single target.
4. If overlap/ambiguity remains, ask one question:
   - "Treat as `mixed` or `proposal-only`?"

Merge strategy:

1. Keep separate findings for code and proposal.
2. De-duplicate semantically equivalent items.
3. Preserve highest severity when merging.

## 6) Failure and Fallback

If opposite backend is unavailable:

1. Emit `backend_unavailable` in round metadata.
2. Continue with local critique using the same output envelope.
3. Keep round history for audit and post-analysis.
