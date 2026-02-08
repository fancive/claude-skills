#!/usr/bin/env python3
"""Debate orchestrator MVP.

Cross-model, multi-round discussion loop for code/proposal artifacts.
Stores session state under:
- <git_root>/.git/review-loop/<session-id>/ when in a git repo
- ${XDG_STATE_HOME:-~/.local/state}/debate/<workspace-key>/review-loop/<session-id>/ otherwise
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DEFAULT_MAX_ROUNDS = 3
DEFAULT_BUDGET_MINUTES = 20
PROPOSAL_SECTION_PATTERN = (
    r"(?im)^\s{0,3}(#+\s*(design|proposal|approach|decision|tradeoff|rebuttal|response)\b)"
)


@dataclasses.dataclass
class CmdResult:
    code: int
    stdout: str
    stderr: str


@dataclasses.dataclass
class ParsedCritique:
    p1: List[str]
    p2: List[str]
    p3: List[str]
    missing: List[str]
    recommendation: Optional[str]
    backend_error: bool


def run_cmd(
    cmd: List[str],
    *,
    cwd: Optional[Path] = None,
    timeout: int = 600,
) -> CmdResult:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    return CmdResult(proc.returncode, proc.stdout.strip(), proc.stderr.strip())


def log_event(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def require_tool(name: str) -> bool:
    return run_cmd(["/usr/bin/env", "bash", "-lc", f"command -v {shlex.quote(name)}"]).code == 0


def get_git_root() -> Optional[Path]:
    res = run_cmd(["git", "rev-parse", "--show-toplevel"])
    if res.code != 0:
        return None
    return Path(res.stdout)


def detect_env() -> str:
    if os.getenv("CODEX_THREAD_ID") or os.getenv("CODEX_SANDBOX_ID"):
        return "codex"
    return "claude"


def opposite_backend(env_name: str) -> str:
    return "claude" if env_name == "codex" else "codex"


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def default_state_root() -> Path:
    raw = os.getenv("XDG_STATE_HOME")
    if raw:
        return Path(os.path.expanduser(raw)).resolve()
    return (Path.home() / ".local" / "state").resolve()


def workspace_key(workspace_root: Path) -> str:
    normalized = str(workspace_root.resolve())
    digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:12]
    name = re.sub(r"[^A-Za-z0-9_.-]+", "-", workspace_root.name.strip()) or "workspace"
    return f"{name}-{digest}"


def resolve_session_base_dir(
    *,
    git_root: Optional[Path],
    workspace_root: Path,
    explicit_state_dir: Optional[str],
) -> Path:
    if explicit_state_dir:
        return Path(explicit_state_dir).expanduser().resolve()
    if git_root:
        return git_root / ".git" / "review-loop"
    return default_state_root() / "debate" / workspace_key(workspace_root) / "review-loop"


def make_session_dir(session_base_dir: Path) -> Tuple[str, Path]:
    session_id = f"debate-{now_stamp()}-{os.getpid()}"
    session_dir = session_base_dir / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_id, session_dir


def classify_text_target(text: str) -> str:
    has_code = "```" in text
    proposal_markers = re.search(PROPOSAL_SECTION_PATTERN, text)
    if has_code and proposal_markers:
        return "mixed"
    if has_code:
        return "code"
    if proposal_markers:
        return "proposal"
    return "proposal"


def parse_scope(scope: str) -> Tuple[str, Optional[str]]:
    if ":" not in scope:
        return scope, None
    k, v = scope.split(":", 1)
    return k, v


def collect_code_artifact(
    git_root: Path,
    scope: str,
    session_dir: Path,
) -> Tuple[str, str, str]:
    kind, value = parse_scope(scope)
    artifact_kind = "diff"
    if kind == "uncommitted":
        diff_res = run_cmd(["git", "diff"], cwd=git_root)
        stat_res = run_cmd(["git", "diff", "--stat"], cwd=git_root)
        if diff_res.code != 0:
            raise RuntimeError(f"git diff failed: {diff_res.stderr or diff_res.stdout}")
        diff = diff_res.stdout
        stat = stat_res.stdout
    elif kind == "commit" and value:
        diff_res = run_cmd(["git", "show", "--patch", value], cwd=git_root)
        stat_res = run_cmd(["git", "show", "--stat", "--oneline", value], cwd=git_root)
        if diff_res.code != 0:
            raise RuntimeError(f"git show commit {value} failed: {diff_res.stderr or diff_res.stdout}")
        diff = diff_res.stdout
        stat = stat_res.stdout
    elif kind == "base" and value:
        expr = f"{value}...HEAD"
        diff_res = run_cmd(["git", "diff", expr], cwd=git_root)
        stat_res = run_cmd(["git", "diff", "--stat", expr], cwd=git_root)
        if diff_res.code != 0:
            raise RuntimeError(f"git diff base {value} failed: {diff_res.stderr or diff_res.stdout}")
        diff = diff_res.stdout
        stat = stat_res.stdout
    elif kind == "range" and value:
        diff_res = run_cmd(["git", "diff", value], cwd=git_root)
        stat_res = run_cmd(["git", "diff", "--stat", value], cwd=git_root)
        if diff_res.code != 0:
            raise RuntimeError(f"git diff range {value} failed: {diff_res.stderr or diff_res.stdout}")
        diff = diff_res.stdout
        stat = stat_res.stdout
    elif kind == "file" and value:
        diff_res = run_cmd(["git", "diff", "--", value], cwd=git_root)
        stat_res = run_cmd(["git", "diff", "--stat", "--", value], cwd=git_root)
        if diff_res.code != 0:
            raise RuntimeError(f"git diff file {value} failed: {diff_res.stderr or diff_res.stdout}")
        diff = diff_res.stdout
        stat = stat_res.stdout
        if not diff.strip():
            p = (git_root / value).resolve()
            if p.exists():
                artifact_kind = "snippet"
                diff = p.read_text(encoding="utf-8", errors="replace")
                stat = f"file:{value} bytes={p.stat().st_size}"
    else:
        raise ValueError(f"Unsupported scope: {scope}")

    diff_file = session_dir / "artifact.diff"
    stat_file = session_dir / "artifact.stat"
    diff_file.write_text(diff, encoding="utf-8")
    stat_file.write_text(stat, encoding="utf-8")
    return diff, stat, artifact_kind


def collect_non_git_code_artifact(
    workspace_root: Path,
    scope: str,
    session_dir: Path,
) -> Tuple[str, str, str]:
    kind, value = parse_scope(scope)
    if kind != "file" or not value:
        raise RuntimeError(
            "Non-git code review requires explicit content/artifact file, "
            "or scope=file:<path> (scope=snippet is allowed only with explicit content)."
        )

    file_path = Path(value).expanduser()
    if not file_path.is_absolute():
        file_path = workspace_root / file_path
    file_path = file_path.resolve()
    if not file_path.exists() or not file_path.is_file():
        raise RuntimeError(f"File scope path does not exist or is not a file: {file_path}")

    text = file_path.read_text(encoding="utf-8", errors="replace")
    stat = f"file:{file_path} bytes={file_path.stat().st_size}"
    diff_file = session_dir / "artifact.diff"
    stat_file = session_dir / "artifact.stat"
    diff_file.write_text(text, encoding="utf-8")
    stat_file.write_text(stat, encoding="utf-8")
    return text, stat, "snippet"


def resolve_artifact(
    args: argparse.Namespace,
    git_root: Optional[Path],
    workspace_root: Path,
    session_dir: Path,
) -> Tuple[str, str, str]:
    """Return (target, artifact_text, artifact_kind)."""
    if args.content:
        text = args.content
        target = args.target if args.target != "auto" else classify_text_target(text)
        return target, text, "text"

    if args.artifact_file:
        text = Path(args.artifact_file).read_text(encoding="utf-8", errors="replace")
        target = args.target if args.target != "auto" else classify_text_target(text)
        return target, text, "text"

    if git_root and (args.target in ("auto", "code", "mixed")):
        scope = args.scope or "uncommitted"
        diff = run_cmd(["git", "diff"], cwd=git_root).stdout
        if args.target == "code" or diff.strip():
            text, _stat, artifact_kind = collect_code_artifact(git_root, scope, session_dir)
            target = "code" if args.target == "auto" else args.target
            return target, text, artifact_kind
    elif not git_root and args.target == "code":
        scope = args.scope or "snippet"
        kind, _value = parse_scope(scope)
        if kind == "file":
            text, _stat, artifact_kind = collect_non_git_code_artifact(workspace_root, scope, session_dir)
            return "code", text, artifact_kind
        if kind not in ("snippet",):
            raise RuntimeError(
                f"Unsupported code scope in non-git workspace: {scope}. "
                "Use file:<path> or provide explicit snippet content."
            )

    print("No auto-detected artifact. Paste content, then Ctrl-D:", file=sys.stderr)
    pasted = sys.stdin.read()
    if not pasted.strip():
        raise RuntimeError("No artifact content provided.")
    if not git_root and args.target == "code":
        return "code", pasted, "snippet"
    target = args.target if args.target != "auto" else classify_text_target(pasted)
    return target, pasted, "text"


def split_mixed(text: str) -> Tuple[str, str]:
    code_blocks = re.findall(r"```[\s\S]*?```", text)
    code_part = "\n\n".join(code_blocks).strip()
    without_code = re.sub(r"```[\s\S]*?```", "", text).strip()

    proposal_sections: List[str] = []
    current: List[str] = []
    keep = False
    for line in without_code.splitlines():
        if re.match(r"(?i)^\s{0,3}#{1,6}\s*(design|proposal|approach|decision|tradeoff|rebuttal|response)\b", line):
            if current and keep:
                proposal_sections.append("\n".join(current).strip())
            current = [line]
            keep = True
            continue
        if re.match(r"^\s{0,3}#{1,6}\s+", line):
            if current and keep:
                proposal_sections.append("\n".join(current).strip())
            current = [line]
            keep = False
            continue
        current.append(line)

    if current and keep:
        proposal_sections.append("\n".join(current).strip())

    proposal_part = "\n\n".join(s for s in proposal_sections if s).strip()
    if not proposal_part:
        proposal_part = without_code
    return code_part, proposal_part


def call_backend_review(
    backend: str,
    *,
    target: str,
    artifact_file: Path,
    scope: str,
    git_root: Optional[Path],
    timeout: int = 600,
) -> str:
    if backend == "codex":
        if target == "code" and git_root:
            kind, value = parse_scope(scope)
            cmd = None
            if kind == "uncommitted":
                cmd = ["codex", "review", "--uncommitted", "--config", "model_reasoning_effort=high"]
            elif kind == "commit" and value:
                cmd = ["codex", "review", "--commit", value, "--config", "model_reasoning_effort=high"]
            elif kind == "base" and value:
                cmd = ["codex", "review", "--base", value, "--config", "model_reasoning_effort=high"]
            if cmd:
                res = run_cmd(cmd, cwd=git_root, timeout=timeout)
                if res.code == 0:
                    return res.stdout or res.stderr
        prompt = (
            f"Read {artifact_file}. Review this {target} artifact.\n"
            "Output sections:\n"
            "## P1 - Must Fix\n## P2 - Should Fix\n## P3 - Nice to Have\n"
            "## Missing Alternatives\n## Recommended Decision\n"
            "Include concrete evidence."
        )
        cmd = ["codex", "exec"]
        if git_root is None:
            cmd.append("--skip-git-repo-check")
        cmd.append(prompt)
        res = run_cmd(cmd, cwd=git_root, timeout=timeout)
        if res.code != 0:
            raise RuntimeError(f"codex failed: {res.stderr or res.stdout}")
        return res.stdout

    if backend == "claude":
        prompt = (
            f"Read {artifact_file}. Review this {target} artifact.\n"
            "Output sections:\n"
            "## P1 - Must Fix\n## P2 - Should Fix\n## P3 - Nice to Have\n"
            "## Missing Alternatives\n## Recommended Decision\n"
            "Include concrete evidence."
        )
        res = run_cmd(["claude", "-p", prompt], cwd=git_root, timeout=timeout)
        if res.code != 0:
            raise RuntimeError(f"claude failed: {res.stderr or res.stdout}")
        return res.stdout

    raise RuntimeError(f"Unknown backend: {backend}")


def parse_critique(text: str) -> ParsedCritique:
    section = None
    p1: List[str] = []
    p2: List[str] = []
    p3: List[str] = []
    missing: List[str] = []
    recommendation = None
    backend_error = bool(re.search(r"(?im)^#{1,6}\s*Backend Error\b", text))

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.match(r"(?i)^#{1,6}\s*P1\b|^#{1,6}\s*.*Must Fix|^#{1,6}\s*.*Must Reconsider", line):
            section = "p1"
            continue
        if re.match(r"(?i)^#{1,6}\s*P2\b|^#{1,6}\s*.*Should Fix|^#{1,6}\s*.*Should Improve", line):
            section = "p2"
            continue
        if re.match(r"(?i)^#{1,6}\s*P3\b|^#{1,6}\s*.*Nice to Have|^#{1,6}\s*.*Nice to Strengthen", line):
            section = "p3"
            continue
        if re.match(r"(?i)^#{1,6}\s*Missing\b", line):
            section = "missing"
            continue
        if re.match(r"(?i)^#{1,6}\s*Recommended Decision\b", line):
            section = "recommendation"
            continue

        if line.startswith(("-", "*")):
            item = line[1:].strip()
            if section == "p1":
                p1.append(item)
            elif section == "p2":
                p2.append(item)
            elif section == "p3":
                p3.append(item)
            elif section == "missing":
                missing.append(item)
            elif section == "recommendation" and not recommendation:
                recommendation = item
        elif section == "recommendation" and not recommendation:
            recommendation = line

    return ParsedCritique(
        p1=p1,
        p2=p2,
        p3=p3,
        missing=missing,
        recommendation=recommendation,
        backend_error=backend_error,
    )


def judge_recommendation(parsed: ParsedCritique) -> Tuple[str, str]:
    if parsed.backend_error and not (parsed.p1 or parsed.p2 or parsed.p3 or parsed.missing):
        return "E", "Backend review failed; no structured critique was produced."
    p1c, p2c, p3c = len(parsed.p1), len(parsed.p2), len(parsed.p3)
    if p1c > 0:
        return "B", f"Detected {p1c} P1 issue(s); accepting opposite recommendation is safer."
    if p2c >= 2:
        return "C", f"Detected {p2c} P2 issue(s); compromise likely balances tradeoffs."
    if p1c == 0 and p2c == 0 and p3c == 0:
        return "A", "No material concerns detected."
    return "D", "There are unresolved concerns; continue one more round."


def detect_agreement_signal(text: str) -> bool:
    lower = text.lower()
    markers = [
        "lgtm",
        "looks good",
        "no concerns",
        "no critical issues",
        "approved",
    ]
    return any(m in lower for m in markers)


def choose_interactive(default_choice: str) -> str:
    options = {"A", "B", "C", "D", "E"}
    prompt = f"Choose [A/B/C/D/E] (default {default_choice}): "
    try:
        val = input(prompt).strip().upper()
    except EOFError:
        print("Input stream closed. Using default.", file=sys.stderr)
        return default_choice
    if not val:
        return default_choice
    if val not in options:
        print("Invalid choice. Using default.", file=sys.stderr)
        return default_choice
    return val


def generate_compromise(
    local_backend: str,
    current: str,
    critique: str,
    cwd: Optional[Path],
    timeout_seconds: int,
    *,
    allow_stdin_fallback: bool,
) -> str:
    prompt = (
        "Generate a compromise revision that addresses the critique while preserving valid parts "
        "of the original. Output only revised artifact content.\n\n"
        f"Original:\n{current}\n\nCritique:\n{critique}\n"
    )
    try:
        if local_backend == "codex":
            cmd = ["codex", "exec"]
            if cwd is None:
                cmd.append("--skip-git-repo-check")
            cmd.append(prompt)
            res = run_cmd(cmd, cwd=cwd, timeout=timeout_seconds)
        else:
            res = run_cmd(["claude", "-p", prompt], cwd=cwd, timeout=timeout_seconds)
        if res.code == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass

    if not allow_stdin_fallback:
        return current
    print("Compromise generation failed; paste compromise content, then Ctrl-D:", file=sys.stderr)
    user_text = sys.stdin.read().strip()
    if not user_text:
        return current
    return user_text


def accept_opposite_revision(
    local_backend: str,
    current: str,
    critique: str,
    cwd: Optional[Path],
    timeout_seconds: int,
) -> str:
    prompt = (
        "Apply the opposite model's review feedback to the artifact.\n"
        "Output only the revised artifact content.\n\n"
        f"Current Artifact:\n{current}\n\nCritique:\n{critique}\n"
    )
    try:
        if local_backend == "codex":
            cmd = ["codex", "exec"]
            if cwd is None:
                cmd.append("--skip-git-repo-check")
            cmd.append(prompt)
            res = run_cmd(cmd, cwd=cwd, timeout=timeout_seconds)
        else:
            res = run_cmd(["claude", "-p", prompt], cwd=cwd, timeout=timeout_seconds)
        if res.code == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return current


def write_json(path: Path, data: Dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Cross-model debate orchestrator MVP")
    parser.add_argument("content", nargs="?", help="Explicit artifact content")
    parser.add_argument("--artifact-file", help="Read artifact content from file")
    parser.add_argument("--target", choices=["auto", "code", "proposal", "mixed"], default="auto")
    parser.add_argument("--scope", default="uncommitted")
    parser.add_argument("--max-rounds", type=int, default=DEFAULT_MAX_ROUNDS)
    parser.add_argument("--mode", choices=["auto", "manual"], default="auto")
    parser.add_argument("--budget-minutes", type=int, default=DEFAULT_BUDGET_MINUTES)
    parser.add_argument(
        "--backend-timeout-seconds",
        type=int,
        default=600,
        help="Timeout per backend model call in seconds.",
    )
    parser.add_argument(
        "--skip-materialize-opposite",
        action="store_true",
        help=(
            "When choice=B in auto/manual mode, skip the second model call that materializes "
            "the opposite recommendation into revised artifact content."
        ),
    )
    parser.add_argument(
        "--state-dir",
        help=(
            "Override session state directory. "
            "Default: <git_root>/.git/review-loop in git repos, "
            "${XDG_STATE_HOME:-~/.local/state}/debate/<workspace-key>/review-loop otherwise."
        ),
    )
    args = parser.parse_args()

    git_root = get_git_root()
    workspace_root = (git_root if git_root else Path.cwd()).resolve()
    session_base_dir = resolve_session_base_dir(
        git_root=git_root,
        workspace_root=workspace_root,
        explicit_state_dir=args.state_dir,
    )

    env_name = detect_env()
    backend = opposite_backend(env_name)
    fallback_local_backend = False
    if not require_tool(backend):
        print(
            f"warning: opposite backend '{backend}' unavailable; fallback to local '{env_name}' critique.",
            file=sys.stderr,
        )
        backend = env_name
        fallback_local_backend = True
        if not require_tool(backend):
            print(f"error: local backend '{backend}' is unavailable", file=sys.stderr)
            return 2

    session_id, session_dir = make_session_dir(session_base_dir)
    started_at = time.time()
    log_event(
        "debate: start "
        f"env={env_name} opposite_backend={backend} target={args.target} session_dir={session_dir}"
    )

    try:
        target, artifact_text, artifact_kind = resolve_artifact(args, git_root, workspace_root, session_dir)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if target in ("proposal", "mixed") and args.backend_timeout_seconds < 120:
        log_event(
            "debate: warning backend-timeout-seconds is low for proposal/mixed reviews; "
            "recommend >=120 (default 600)."
        )

    artifact_file = session_dir / "artifact.md"
    artifact_file.write_text(artifact_text, encoding="utf-8")

    session_state: Dict = {
        "session_id": session_id,
        "started_at": dt.datetime.now().isoformat(),
        "target": target,
        "scope": args.scope,
        "max_rounds": args.max_rounds,
        "budget_minutes": args.budget_minutes,
        "workspace_root": str(workspace_root),
        "session_dir": str(session_dir),
        "backend": backend,
        "fallback_local_backend": fallback_local_backend,
        "rounds": [],
        "status": "in_progress",
    }
    write_json(session_dir / "metadata.json", session_state)

    current_artifact = artifact_text
    final_decision = "Stopped"
    final_artifact = current_artifact
    previous_has_material = False

    for round_no in range(1, args.max_rounds + 1):
        elapsed_min = (time.time() - started_at) / 60.0
        if elapsed_min >= args.budget_minutes:
            final_decision = "Stopped (budget exceeded)"
            break

        round_input = session_dir / f"round-{round_no}-input.md"
        round_input.write_text(current_artifact, encoding="utf-8")
        log_event(f"debate: round={round_no} route_start target={target}")

        backend_unavailable = fallback_local_backend
        backend_used = backend
        effective_target = target
        try:
            if target == "mixed":
                mixed_code_part, mixed_proposal_part = split_mixed(current_artifact)
                if not mixed_code_part.strip() and mixed_proposal_part.strip():
                    effective_target = "proposal"
                elif mixed_code_part.strip() and not mixed_proposal_part.strip():
                    effective_target = "code"
                else:
                    effective_target = "mixed"

                code_file = session_dir / f"round-{round_no}-mixed-code.md"
                proposal_file = session_dir / f"round-{round_no}-mixed-proposal.md"
                code_file.write_text(mixed_code_part, encoding="utf-8")
                proposal_file.write_text(mixed_proposal_part, encoding="utf-8")

                if effective_target == "code":
                    log_event(f"debate: round={round_no} call_backend backend={backend} target=code")
                    scope_for_code = args.scope
                    if artifact_kind in ("text", "snippet"):
                        scope_for_code = "snippet"
                    critique = call_backend_review(
                        backend,
                        target="code",
                        artifact_file=code_file,
                        scope=scope_for_code,
                        git_root=git_root,
                        timeout=args.backend_timeout_seconds,
                    )
                elif effective_target == "proposal":
                    log_event(f"debate: round={round_no} call_backend backend={backend} target=proposal")
                    critique = call_backend_review(
                        backend,
                        target="proposal",
                        artifact_file=proposal_file,
                        scope=args.scope,
                        git_root=git_root,
                        timeout=args.backend_timeout_seconds,
                    )
                else:
                    scope_for_code = args.scope
                    if artifact_kind in ("text", "snippet"):
                        scope_for_code = "snippet"
                    critique_code = call_backend_review(
                        backend,
                        target="code",
                        artifact_file=code_file,
                        scope=scope_for_code,
                        git_root=git_root,
                        timeout=args.backend_timeout_seconds,
                    )
                    log_event(f"debate: round={round_no} call_backend backend={backend} target=proposal")
                    critique_proposal = call_backend_review(
                        backend,
                        target="proposal",
                        artifact_file=proposal_file,
                        scope=args.scope,
                        git_root=git_root,
                        timeout=args.backend_timeout_seconds,
                    )
                    critique = (
                        "## Code Critique\n\n"
                        + critique_code
                        + "\n\n## Proposal Critique\n\n"
                        + critique_proposal
                    )
            else:
                log_event(f"debate: round={round_no} call_backend backend={backend} target={target}")
                # When artifact is explicit text/snippet, use scope="snippet" for code reviews
                scope_to_use = args.scope
                if target == "code" and artifact_kind in ("text", "snippet"):
                    scope_to_use = "snippet"
                critique = call_backend_review(
                    backend,
                    target=target,
                    artifact_file=round_input,
                    scope=scope_to_use,
                    git_root=git_root,
                    timeout=args.backend_timeout_seconds,
                )
        except Exception as exc:
            primary_error = str(exc)
            local_backend = env_name
            if backend != local_backend and require_tool(local_backend):
                backend_unavailable = True
                backend_used = local_backend
                log_event(
                    f"debate: round={round_no} backend_failed primary={backend} "
                    f"fallback={local_backend} error={primary_error}"
                )
                try:
                    if effective_target == "mixed":
                        # Best-effort fallback: run single proposal review when mixed fallback fails.
                        fallback_file = session_dir / f"round-{round_no}-fallback-proposal.md"
                        fallback_file.write_text(current_artifact, encoding="utf-8")
                        local_critique = call_backend_review(
                            local_backend,
                            target="proposal",
                            artifact_file=fallback_file,
                            scope=args.scope,
                            git_root=git_root,
                            timeout=args.backend_timeout_seconds,
                        )
                    else:
                        local_critique = call_backend_review(
                            local_backend,
                            target=effective_target,
                            artifact_file=round_input,
                            scope=args.scope,
                            git_root=git_root,
                            timeout=args.backend_timeout_seconds,
                        )
                    critique = (
                        "## Backend Fallback\n"
                        f"- primary_backend: {backend}\n"
                        f"- error: {primary_error}\n\n"
                        + local_critique
                    )
                except Exception as fallback_exc:
                    critique = (
                        "## Backend Error\n"
                        f"- primary_backend: {backend}\n"
                        f"- primary_error: {primary_error}\n"
                        f"- fallback_backend: {local_backend}\n"
                        f"- fallback_error: {fallback_exc}\n"
                    )
            else:
                log_event(f"debate: round={round_no} backend_error backend={backend} error={exc}")
                critique = f"## Backend Error\n- {exc}\n"

        round_crit = session_dir / f"round-{round_no}-critique.md"
        round_crit.write_text(critique, encoding="utf-8")

        parsed = parse_critique(critique)
        rec_choice, rec_reason = judge_recommendation(parsed)
        has_material = (len(parsed.p1) + len(parsed.p2)) > 0
        has_agreement_signal = detect_agreement_signal(critique)

        print(f"\n=== Round {round_no} ===")
        print(f"Judge recommendation: {rec_choice} ({rec_reason})")
        print(f"P1={len(parsed.p1)} P2={len(parsed.p2)} P3={len(parsed.p3)} Missing={len(parsed.missing)}")

        auto_stop_reason: Optional[str] = None
        if (
            round_no > 1
            and not parsed.backend_error
            and not has_material
            and not previous_has_material
        ):
            auto_stop_reason = "Converged (two consecutive rounds with no new P1/P2)"
        elif has_agreement_signal and not has_material and not parsed.backend_error:
            auto_stop_reason = "Converged (agreement signal from opposite model)"

        if auto_stop_reason:
            round_entry = {
                "round": round_no,
                "choice": "AUTO_STOP",
                "judge_recommendation": rec_choice,
                "judge_reason": rec_reason,
                "backend_error": parsed.backend_error,
                "p1": parsed.p1,
                "p2": parsed.p2,
                "p3": parsed.p3,
                "missing": parsed.missing,
            }
            session_state["rounds"].append(round_entry)
            write_json(session_dir / "metadata.json", session_state)
            final_decision = auto_stop_reason
            final_artifact = current_artifact
            break

        if args.mode == "auto":
            choice = rec_choice
            print(f"Auto mode choice: {choice}")
        else:
            choice = choose_interactive(rec_choice)

        round_entry = {
            "round": round_no,
            "choice": choice,
            "judge_recommendation": rec_choice,
            "judge_reason": rec_reason,
            "target": effective_target,
            "backend_used": backend_used,
            "backend_unavailable": backend_unavailable,
            "backend_error": parsed.backend_error,
            "p1": parsed.p1,
            "p2": parsed.p2,
            "p3": parsed.p3,
            "missing": parsed.missing,
        }
        session_state["rounds"].append(round_entry)
        write_json(session_dir / "metadata.json", session_state)

        if choice == "A":
            final_decision = "Keep Original"
            final_artifact = current_artifact
            break
        if choice == "B":
            if args.skip_materialize_opposite:
                log_event("debate: skip materialize_opposite due to --skip-materialize-opposite")
                final_decision = "Accept Opposite (materialization skipped)"
                final_artifact = current_artifact
            else:
                final_decision = "Accept Opposite"
                local_backend = "codex" if env_name == "codex" else "claude"
                log_event(f"debate: round={round_no} materialize_opposite backend={local_backend}")
                final_artifact = accept_opposite_revision(
                    local_backend,
                    current_artifact,
                    critique,
                    git_root,
                    timeout_seconds=args.backend_timeout_seconds,
                )
            break
        if choice == "C":
            previous_has_material = has_material
            local_backend = "codex" if env_name == "codex" else "claude"
            log_event(f"debate: round={round_no} generate_compromise backend={local_backend}")
            current_artifact = generate_compromise(
                local_backend,
                current_artifact,
                critique,
                git_root,
                timeout_seconds=args.backend_timeout_seconds,
                allow_stdin_fallback=(args.mode == "manual"),
            )
            continue
        if choice == "D":
            previous_has_material = has_material
            rebuttal = ""
            if args.mode == "manual":
                rebuttal = input("Optional rebuttal (empty to auto-generate): ").strip()
            if not rebuttal:
                rebuttal = "Please address remaining concerns with concrete evidence and tradeoffs."
            current_artifact = f"{current_artifact}\n\n## Rebuttal\n{rebuttal}\n"
            continue
        if choice == "E":
            if parsed.backend_error and args.mode == "auto":
                final_decision = "Stopped (backend error - no review performed)"
            else:
                final_decision = "Stopped by user"
            final_artifact = current_artifact
            break

    session_state["status"] = "closed"
    session_state["final_decision"] = final_decision
    write_json(session_dir / "metadata.json", session_state)

    summary = [
        "## Debate Summary",
        "",
        f"Session: {session_id}",
        f"Target: {target}",
        f"Rounds: {len(session_state['rounds'])}",
        f"Final Decision: {final_decision}",
        "",
        "### Next Actions",
        "1. Apply selected artifact content",
        "2. Run validation/tests",
    ]
    (session_dir / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    (session_dir / "final-artifact.md").write_text(final_artifact, encoding="utf-8")

    print("\n" + "\n".join(summary))
    print(f"Saved: {session_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
