# Agent Instructions for Codex CLI

This file provides guidance to Codex CLI agents when working with extensions in this repository.

## Debate Skill

### Purpose
Cross-model discussion loop for code/proposal/mixed artifacts. Routes to opposite model (Claude ↔ Codex) with multi-round critique-response flow.

### When to Use
- User says `/debate`, "second opinion", "challenge this", "辩论"
- After completing a complex feature/refactor
- Before finalizing architectural decisions
- When code review reveals contentious issues

### Execution

**Primary method** (script-first, recommended):
```bash
python3 skills/debate/scripts/debate.py --target auto --intensity standard
python3 skills/debate/scripts/debate.py --target code --scope uncommitted
python3 skills/debate/scripts/debate.py --target proposal --artifact-file ./proposal.md --state-dir ./.debate-state
```

**Parameters**:
- `--target`: `auto|code|proposal|mixed` (default `auto`)
- `--intensity`: `quick|standard|extensive` (default `standard`)
  - `quick`: 1 round, 10min budget, 180s timeout
  - `standard`: 3 rounds, 20min budget, 600s timeout
  - `extensive`: 5 rounds, 40min budget, 900s timeout
- `--scope` (code only): `uncommitted|commit:<sha>|base:<branch>|file:<path>`
- `--mode`: `auto|manual` (default `auto`)
- `--state-dir`: override session storage (default: `.git/review-loop/` or `~/.local/state/debate/`)

### Output Contract

Session artifacts are saved to:
- Git repos: `<git_root>/.git/review-loop/<session-id>/`
- Non-git: `${XDG_STATE_HOME:-~/.local/state}/debate/<workspace-key>/review-loop/<session-id>/`

Key files:
- `metadata.json`: full session state with rounds history
- `decision.json`: machine-readable final decision and judge recommendations
- `summary.md`: human-readable summary
- `final-artifact.md`: converged or selected artifact content
- `round-<n>-input.md`: input for each round
- `round-<n>-critique.md`: critique from opposite model

### Decision Flow

After each round, the script outputs a judge recommendation:
- **A**: Keep original (no material concerns)
- **B**: Accept opposite model recommendation (P1 issues detected)
- **C**: Generate compromise (multiple P2 issues)
- **D**: Continue with rebuttal (unresolved concerns)
- **E**: Stop (backend error or user choice)

In `--mode auto`, the script automatically selects the recommended choice. In `--mode manual`, it prompts for user input.

### Backend Failure Handling

**IMPORTANT**: When the script outputs:
```
Final Decision: Stopped (backend error - no review performed)
```

**DO NOT** add your own extra critique or manual "local fallback analysis".

If the script already produced structured fallback content in `round-<n>-critique.md`,
you may summarize that script-generated content only.

**INSTEAD**, report the failure and suggest fixes:
1. Check opposite backend CLI authentication
2. Increase `--backend-timeout-seconds` (default 600)
3. Use `--intensity quick` for faster iteration
4. Run `debate.py` directly to debug backend calls
5. Check session logs in `<session-dir>/round-*-critique.md`

### Backend Call Contract

From Codex CLI environment:
- Opposite backend: `claude` CLI
- Code review: `claude -p "Read <diff_file>. Review with P1/P2/P3 and evidence."`
- Proposal review: `claude -p "Read <artifact_file>. Review proposal with: 1) problem framing..."`

Expected output sections:
```markdown
## P1 - Must Fix
- [concrete evidence with file:line if possible]

## P2 - Should Fix
- [concrete evidence]

## P3 - Nice to Have
- [concrete evidence]

## Missing Alternatives
- [alternative approaches not considered]

## Recommended Decision
- [A|B|C|D|E with rationale]
```

### Troubleshooting

**Claude CLI timeout in Codex environment**:
- Symptom: `Command '['claude', '-p', '...']' timed out after N seconds`
- Common causes:
  - CLI auth/session issues
  - backend file path not readable by `claude -p` (often `/tmp` paths)
  - accidental repeated re-runs instead of waiting one process
- Fix:
  - use project-local state path: `--state-dir ./.debate-state`
  - increase `--backend-timeout-seconds`
  - verify `claude -p "Reply with exactly: OK"` works

**Fallback backend also fails**:
- Symptom: Both primary and fallback backends report errors
- Cause: Environment/permission issues
- Fix: Run `codex exec "echo test"` and `claude -p "echo test"` to verify both CLIs work

**Session state permission errors**:
- Symptom: `Permission denied` when writing to `~/.local/state/`
- Fix: Use project-local path `--state-dir ./.debate-state` or ensure write permission
- Avoid `/tmp` when backend is `claude`; file-read restrictions may cause backend failures.

### Progressive Disclosure

The debate skill uses lazy-loading reference files:
- **Phase 3 (Routing)**: `references/protocols.md` - backend call formats
- **Phase 4 (Judge Analysis)**: `references/judge-analysis.md` - A/B/C/D/E logic
- **Code Snippets**: `references/code-snippet-handling.md` - non-git code review

Only read these files when you need to understand the internals.

## Other Skills

(Add documentation for other skills as they're created)
