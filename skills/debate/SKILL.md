---
name: debate
description: "Interactive cross-model debate orchestrator. Auto-detects latest artifact (code/proposal/doc), routes review to opposite model, runs multi-round critique-response loop, and presents decision options (A/B/C/D/E). Use when: user says /debate, wants model-vs-model discussion, second opinion with iterative refinement, or structured convergence. Keywords: debate, discuss, challenge, second opinion, 辩论, 讨论, 交叉评审, 多轮"
---

# Debate - Cross-Model Discussion Loop

Orchestrate multi-round discussion between two models.

- `cr` handles code-focused critique.
- `peer-review` handles proposal/viewpoint critique.
- `debate` is the routing + loop + decision layer.

**Load references when needed:**

- **Phase 3 (Routing)**: Read `references/protocols.md` for I/O contracts, backend call formats, and mixed artifact splitting rules
- **Phase 4 (Judge Analysis)**: Read `references/judge-analysis.md` for critique validation rubric and A/B/C/D/E recommendation logic
- **Code Snippets (non-git)**: Read `references/code-snippet-handling.md` when reviewing code without git context

## Usage

```bash
/debate
/debate "explicit content to debate"
/debate --target auto --max-rounds 3 --mode auto
/debate --target code --scope commit:abc1234
/debate --target proposal --max-rounds 2
```

Script-first execution (recommended for repeatability):

```bash
python3 skills/debate/scripts/debate.py
python3 skills/debate/scripts/debate.py --target code --scope uncommitted --max-rounds 3 --mode manual
python3 skills/debate/scripts/debate.py --target proposal --artifact-file /tmp/proposal.md --mode auto
python3 skills/debate/scripts/debate.py --target proposal --state-dir /tmp/debate-state --mode auto
python3 skills/debate/scripts/debate.py --target proposal --mode auto --skip-materialize-opposite
```

## Parameters

- `--target`: `auto|code|proposal|mixed` (default `auto`)
- `--scope` (code only):
  - git workspace: `uncommitted|commit:<sha>|base:<branch>|range:<a>..<b>|file:<path>`
  - non-git workspace: `file:<path>` or explicit snippet content
- `--max-rounds`: `1..5` (default `3`)
- `--mode`: `auto|manual` (default `auto`)
- `--budget-minutes`: default `20`
- `--backend-timeout-seconds`: timeout per backend model call (default `600`, recommend `>=120` for proposal/mixed)
- `--skip-materialize-opposite`: skip the second model call when choosing `B` (faster, but final artifact is not auto-rewritten)
- `--state-dir`: override session storage root

## Phase 1 - Resolve Artifact (auto by default)

If user provides explicit content, use it directly.

Else detect from latest context in this order:

1. If working tree has changes and user intent is code review, candidate is code (`git diff`).
2. Else inspect last assistant message:
   - has fenced code blocks -> candidate code
   - has proposal sections (`Design`, `Proposal`, `Approach`, `Decision`) -> candidate proposal
   - short generic text (<2000 chars) -> candidate full message
3. If confidence is low, ask one confirmation question:
   - "I detected X as debate target. Continue?"

Confidence guideline:

- high: explicit scope or obvious code/proposal markers
- medium: partial markers
- low: ambiguous or multiple candidates

For `target=mixed`, use deterministic splitting rules from `references/protocols.md`.

## Phase 2 - Package Context

Create session folder:

```bash
SESSION_ID="debate-$(date +%Y%m%d-%H%M%S)-$$"
if in_git_repo; then
  SESSION_BASE="<git_root>/.git/review-loop"
else
  SESSION_BASE="${XDG_STATE_HOME:-$HOME/.local/state}/debate/<workspace-key>/review-loop"
fi
SESSION_DIR="$SESSION_BASE/$SESSION_ID"
mkdir -p "$SESSION_DIR"
```

Persist:

- `artifact.md` - debated content
- `metadata.json` - target type, scope, rounds, timestamp
- `round-<n>-input.md` / `round-<n>-critique.md`
- `summary.md`

Do not stage these files.

## Phase 3 - Route to Opposite Model

Use explicit call contracts in `references/protocols.md`.

### Target `code`

- Run `cr` protocol with resolved `scope`.
- Request structured output:
  - `P1/P2/P3`
  - concrete evidence (`file:line` when possible)
  - suggested actions

### Target `proposal` or `doc`

- Run `peer-review` protocol.
- Request structured output:
  - `P1/P2/P3`
  - missing alternatives
  - recommended decision

### Target `mixed`

- Split artifact into code and proposal segments per protocol rules.
- Run both paths and merge critiques into one round result.

For code snippets (no git diff), follow `references/code-snippet-handling.md`.

## Phase 4 - Multi-Round Loop

For each round `n` up to `max-rounds`:

1. Send current artifact to opposite model.
2. Receive critique and summarize:
   - agreements
   - concerns
   - suggestions
3. Judge analyzes critique (current model):
   - classify findings: `Valid / Invalid / Missing`
   - score severity concentration (`P1/P2/P3`)
   - generate recommendation: `A|B|C|D|E` + rationale
   - use rubric in `references/judge-analysis.md`
4. Present choices with judge recommendation:
   - `A` Keep original
   - `B` Accept opposite model recommendation
   - `C` Generate compromise version
   - `D` Continue with rebuttal (next round)
   - `E` Stop without final decision
5. Handle choice:
   - `A/B` -> finalize and exit
   - `C` -> generate v-next and continue
   - `D` -> attach rebuttal and continue
   - `E` -> stop and save session
6. Save round artifacts in `SESSION_DIR`.

## Phase 5 - Convergence and Budget Guards

Stop when any condition is met:

1. `max-rounds` reached
2. budget exceeded (`--budget-minutes`)
3. two consecutive rounds have no new `P1/P2`
4. critique indicates agreement (`no concerns`, `LGTM`, equivalent)
5. user chooses `A`, `B`, or `E`

Never run unbounded loops.

## Final Output Contract

```markdown
## Debate Summary

Session: <id>
Target: <code|proposal|mixed>
Rounds: <n>
Converged: <yes|no>

### Final Decision
- Keep Original | Accept Opposite | Compromise | Stopped

### Final Artifact
<content or reference>

### Key Findings
- P1:
- P2:
- P3:

### Judge Recommendation History
- Round 1: <A|B|C|D|E + reason>
- Round 2: <...>

### Unresolved
- ...

### Next Actions
1. [ ] ...
2. [ ] ...
```

## Automation Rules

- Prefer `target=auto` and low-friction defaults.
- Ask at most one clarifying question per round unless blocked.
- If tool/backend unavailable, provide fallback:
  - continue with local model critique
  - keep session state for audit/history
