#!/usr/bin/env python3
"""Run a system-under-test against benchmark testcases.

Speaks the contest stdin/stdout protocol:
  - feed prompts one per line via stdin
  - read system stdout, find #END <id> per prompt as "ready for next" signal
  - capture system-written <case_name>.log from system cwd
  - enforce per-prompt timeout (60s basic / 300s other) per contest §3.1

Selectors:
  --source {official|community|personal|all}   default: all
  --cases test01,test10,...                    explicit case names
  --tag tag1,tag2                              filter by meta.yaml tags (future)

Each case runs in its own temp workdir. Netlist gets symlinked at the path
the prompts reference; cwd is set so the system's relative paths resolve.

Output: results/<run_id>/per-case JSON + final result_book.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("error: PyYAML is required. Install via:",
          file=sys.stderr)
    print("  python3 -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
# Default points at a sibling repo named `system/` for new contestants to
# clone next to this benchmark. Override with --system-cmd or set the
# BENCH_SYSTEM_CMD environment variable to point at your own binary.
DEFAULT_SYSTEM_CMD = os.environ.get(
    "BENCH_SYSTEM_CMD",
    "./your_team_alpha -config llm_config.yaml",
)

BASIC_TIMEOUT_S = 60
OTHER_TIMEOUT_S = 300
# Hard ceiling per testcase. Upper-bound from contest spec: 20 prompts × 300s
# = 6000s. Set just above that so genuinely slow large-netlist cases (test12,
# test39 on 100k+ line designs) don't get auto-truncated by the runner before
# the per-prompt timeout has a chance to fire.
CASE_HARD_CEILING_S = 6300


@dataclass
class PromptResult:
    id: int
    text: str
    task_type: str = "unknown"
    expected_kind: str = "unknown"
    response_text: str = ""
    duration_s: float = 0.0
    status: str = "pending"     # pending | ok | timeout | crash | malformed
    error: str = ""


@dataclass
class CaseResult:
    case_name: str
    source: str
    case_dir: str
    netlist_lines: int = 0
    prompts: list[PromptResult] = field(default_factory=list)
    started_at: float = 0.0
    finished_at: float = 0.0
    verdict: str = "pending"    # pending | pass_flow | partial | fail_flow
    workdir: str = ""
    stderr_path: str = ""
    log_path: str = ""           # the <case_name>.log captured from system cwd


def discover_cases(source: str, cases: Optional[list[str]]) -> list[Path]:
    roots: list[tuple[str, Path]] = []
    if source in ("official", "all"):
        official = REPO_ROOT / "private" / "official_0510"
        if official.is_dir():
            roots.append(("official", official))
    if source in ("community", "personal", "all"):
        community = REPO_ROOT / "tests"
        if community.is_dir():
            roots.append(("community", community))

    found: list[Path] = []
    for tag, root in roots:
        for d in sorted(root.iterdir()):
            if not d.is_dir():
                continue
            if tag == "official" and not d.name.startswith("test"):
                continue
            if tag == "community" and not d.name.startswith("case_"):
                continue
            if not (d / "requests.txt").exists():
                continue
            if cases:
                name = d.name.replace("case_", "")
                if name not in cases and d.name not in cases:
                    continue
            found.append(d)
    return found


def build_workdir(case_dir: Path, meta: dict, workdir: Path) -> None:
    """Symlink netlist + any other files into workdir per meta.runtime."""
    rt = (meta or {}).get("runtime", {}) or {}
    mount = rt.get("netlist_mount")

    if mount:
        src = case_dir / mount["source"]
        tgt = workdir / mount["target"]
        tgt.parent.mkdir(parents=True, exist_ok=True)
        if not src.exists():
            raise FileNotFoundError(f"netlist not found: {src}")
        tgt.symlink_to(src.resolve())
    else:
        # No meta. Default mount: copy the layout of the case_dir relative to
        # repo_root. Works for community tests/case_<name>/design.v style.
        rel = case_dir.relative_to(REPO_ROOT)
        for f in case_dir.iterdir():
            if f.is_file() and f.suffix == ".v":
                tgt = workdir / rel / f.name
                tgt.parent.mkdir(parents=True, exist_ok=True)
                tgt.symlink_to(f.resolve())


def load_meta(case_dir: Path) -> dict:
    p = case_dir / "meta.yaml"
    if p.exists():
        return yaml.safe_load(p.read_text()) or {}
    return {}


def load_prompts(case_dir: Path) -> list[str]:
    raw = (case_dir / "requests.txt").read_text(encoding="utf-8").splitlines()
    return [ln for ln in raw
            if ln.strip() and not ln.lstrip().startswith("#")]


def prompt_timeout(task_type: str) -> int:
    return BASIC_TIMEOUT_S if task_type == "basic" else OTHER_TIMEOUT_S


def run_case(case_dir: Path, system_cmd: str,
             results_dir: Path) -> CaseResult:
    """Run a single testcase end-to-end. Returns a CaseResult."""
    meta = load_meta(case_dir)
    prompts = load_prompts(case_dir)

    # Map prompt id -> task_type / expected_kind from meta if present.
    prompt_meta: dict[int, dict] = {}
    for pm in meta.get("prompts", []) or []:
        prompt_meta[pm["id"]] = pm

    netlist_file = next(
        (f for f in case_dir.iterdir() if f.is_file() and f.suffix == ".v"
         and f.name != "design.v.bak"),
        None,
    )
    netlist_lines = 0
    if netlist_file is not None:
        try:
            netlist_lines = netlist_file.read_text(
                encoding="utf-8", errors="ignore").count("\n")
        except OSError:
            pass

    res = CaseResult(
        case_name=case_dir.name,
        source=meta.get("source", "unknown"),
        case_dir=str(case_dir),
        netlist_lines=netlist_lines,
        started_at=time.time(),
    )

    case_results_dir = results_dir / case_dir.name
    case_results_dir.mkdir(parents=True, exist_ok=True)
    res.stderr_path = str(case_results_dir / "system.stderr")
    res.log_path = str(case_results_dir / "system.log")

    workdir = Path(tempfile.mkdtemp(prefix=f"bench_{case_dir.name}_"))
    res.workdir = str(workdir)

    try:
        build_workdir(case_dir, meta, workdir)
    except Exception as e:
        res.verdict = "fail_flow"
        for i, text in enumerate(prompts, start=1):
            pr = PromptResult(id=i, text=text, status="crash",
                              error=f"workdir setup failed: {e}")
            res.prompts.append(pr)
        res.finished_at = time.time()
        return res

    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = f"/lib64/:{env.get('LD_LIBRARY_PATH','')}"
    stderr_fh = open(res.stderr_path, "w", encoding="utf-8")
    try:
        proc = subprocess.Popen(
            system_cmd, shell=True, cwd=str(workdir),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=stderr_fh, env=env, text=True, bufsize=1,
        )
    except OSError as e:
        stderr_fh.close()
        res.verdict = "fail_flow"
        for i, text in enumerate(prompts, start=1):
            pr = PromptResult(id=i, text=text, status="crash",
                              error=f"spawn failed: {e}")
            res.prompts.append(pr)
        res.finished_at = time.time()
        return res

    case_start = time.time()
    try:
        for i, text in enumerate(prompts, start=1):
            pm = prompt_meta.get(i, {})
            task_type = pm.get("task_type", "unknown")
            expected_kind = (pm.get("expected", {}) or {}).get("kind", "unknown")

            pr = PromptResult(id=i, text=text, task_type=task_type,
                              expected_kind=expected_kind)

            if time.time() - case_start > CASE_HARD_CEILING_S:
                pr.status = "timeout"
                pr.error = "case hard ceiling exceeded"
                res.prompts.append(pr)
                for j, t in enumerate(prompts[i:], start=i + 1):
                    res.prompts.append(PromptResult(
                        id=j, text=t, status="timeout",
                        error="skipped after prior ceiling timeout"))
                break

            t_send = time.time()
            try:
                proc.stdin.write(text + "\n")
                proc.stdin.flush()
            except (BrokenPipeError, OSError) as e:
                pr.status = "crash"
                pr.error = f"stdin write failed: {e}"
                res.prompts.append(pr)
                break

            deadline = t_send + prompt_timeout(task_type)
            collected: list[str] = []
            saw_end = False
            inside_response = False
            response_buf: list[str] = []
            while True:
                if time.time() > deadline:
                    pr.status = "timeout"
                    pr.duration_s = time.time() - t_send
                    pr.error = (f"no #END {i} within "
                                f"{prompt_timeout(task_type)}s")
                    break
                line = _readline_nonblocking(proc.stdout, deadline)
                if line is None:
                    pr.status = "timeout"
                    pr.duration_s = time.time() - t_send
                    pr.error = (f"no #END {i} within "
                                f"{prompt_timeout(task_type)}s")
                    break
                if line == "":
                    pr.status = "crash"
                    pr.error = "system stdout closed (process exited?)"
                    pr.duration_s = time.time() - t_send
                    break
                stripped = line.rstrip()
                collected.append(stripped)
                if stripped == f"#RESPONSE {i}":
                    inside_response = True
                    continue
                if stripped == f"#END {i}":
                    saw_end = True
                    break
                if inside_response:
                    response_buf.append(stripped)

            if pr.status == "pending":
                if saw_end:
                    pr.status = "ok"
                    pr.response_text = "\n".join(response_buf)
                    pr.duration_s = time.time() - t_send
                else:
                    pr.status = "malformed"
                    pr.error = (f"got data but no matching #END {i}; "
                                f"raw: {collected[:5]}...")
                    pr.duration_s = time.time() - t_send

            res.prompts.append(pr)
            if pr.status == "crash":
                break

        # All prompts done — close stdin, wait briefly for graceful exit.
        try:
            proc.stdin.close()
        except Exception:
            pass
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()

    finally:
        stderr_fh.close()

        # System writes its <case>.log to cwd per contest §3.3; may also nest
        # one inside testcase/<name>/ if it took the prompt path literally.
        case_id = _extract_case_id_from_prompts(prompts)
        log_candidates = list(workdir.rglob("*.log"))
        if case_id:
            preferred = [p for p in log_candidates
                         if p.name == f"{case_id}.log"]
            if preferred:
                log_candidates = preferred
        if log_candidates:
            try:
                shutil.copy2(log_candidates[0], res.log_path)
            except OSError:
                pass

        # Preserve system-written .v files (modification/optimization outputs).
        # The original netlist mounted via symlink is excluded by the is_symlink
        # check — anything else is system-authored.
        artifacts_dir = case_results_dir / "artifacts"
        artifacts_made = False
        for v in workdir.rglob("*.v"):
            if v.is_symlink():
                continue
            if not artifacts_made:
                artifacts_dir.mkdir(parents=True, exist_ok=True)
                artifacts_made = True
            try:
                shutil.copy2(v, artifacts_dir / v.name)
            except OSError:
                pass

        if not os.environ.get("BENCH_KEEP_WORKDIR"):
            try:
                shutil.rmtree(workdir, ignore_errors=True)
            except OSError:
                pass

    res.finished_at = time.time()
    statuses = {p.status for p in res.prompts}
    if statuses == {"ok"}:
        res.verdict = "pass_flow"
    elif "ok" in statuses:
        res.verdict = "partial"
    else:
        res.verdict = "fail_flow"
    return res


def _readline_nonblocking(stream, deadline: float, poll_interval: float = 0.05) -> Optional[str]:
    """Read a line from a pipe, returning None on timeout, "" on EOF."""
    result: list = [None]
    def reader():
        try:
            result[0] = stream.readline()
        except Exception:
            result[0] = ""
    t = threading.Thread(target=reader, daemon=True)
    t.start()
    t.join(max(0.05, deadline - time.time()))
    if t.is_alive():
        return None
    return result[0] if result[0] is not None else ""


def _extract_case_id_from_prompts(prompts: list[str]) -> Optional[str]:
    """Find 'case name is <X>' or 'testcase <X>' in the first prompt."""
    if not prompts:
        return None
    m = re.search(r"case name is (\w+)", prompts[0])
    if m:
        return m.group(1)
    m = re.search(r"testcase\s+(\w+)", prompts[0])
    if m:
        return m.group(1)
    return None


def render_result_book(results: list[CaseResult], out_path: Path,
                       run_meta: dict) -> None:
    total_prompts = sum(len(r.prompts) for r in results)
    total_ok = sum(1 for r in results for p in r.prompts if p.status == "ok")
    total_timeout = sum(1 for r in results for p in r.prompts
                        if p.status == "timeout")
    total_crash = sum(1 for r in results for p in r.prompts
                      if p.status == "crash")
    total_malformed = sum(1 for r in results for p in r.prompts
                          if p.status == "malformed")
    case_pass = sum(1 for r in results if r.verdict == "pass_flow")
    case_partial = sum(1 for r in results if r.verdict == "partial")
    case_fail = sum(1 for r in results if r.verdict == "fail_flow")

    if results:
        first_start = min(r.started_at for r in results)
        last_finish = max(r.finished_at for r in results if r.finished_at) \
                      or first_start
        total_wall_s = last_finish - first_start
        ended_iso = time.strftime("%Y-%m-%dT%H:%M:%S",
                                  time.localtime(last_finish))
    else:
        total_wall_s = 0.0
        ended_iso = "n/a"

    def fmt_dur(s: float) -> str:
        if s < 60:
            return f"{s:.1f}s"
        if s < 3600:
            return f"{s/60:.1f}m ({s:.0f}s)"
        return f"{s/3600:.2f}h ({s:.0f}s)"

    lines = [
        "# Benchmark Result Book",
        "",
        f"- **Run id**: `{run_meta.get('run_id')}`",
        f"- **Started**: {run_meta.get('started_iso')}",
        f"- **Ended**: {ended_iso}",
        f"- **Total wall time**: {fmt_dur(total_wall_s)}",
        f"- **System cmd**: `{run_meta.get('system_cmd')}`",
        "",
        "## Aggregate",
        "",
        f"- **Cases**: {len(results)} total — "
        f"{case_pass} pass_flow, {case_partial} partial, {case_fail} fail_flow",
    ]
    if total_prompts:
        ok_pct = 100 * total_ok / total_prompts
        lines.append(
            f"- **Prompts**: {total_prompts} total — "
            f"**{total_ok} ok** ({ok_pct:.1f}%), "
            f"{total_timeout} timeout, {total_crash} crash, "
            f"{total_malformed} malformed"
        )
    else:
        lines.append("- **Prompts**: 0 total")
    lines += [
        "",
        "## Summary",
        "",
        "| Case | Source | Prompts | OK | Timeout | Crash | Malformed | Verdict | Wall |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        n = len(r.prompts)
        ok = sum(1 for p in r.prompts if p.status == "ok")
        to = sum(1 for p in r.prompts if p.status == "timeout")
        cr = sum(1 for p in r.prompts if p.status == "crash")
        mf = sum(1 for p in r.prompts if p.status == "malformed")
        wall = r.finished_at - r.started_at if r.finished_at else 0.0
        lines.append(
            f"| `{r.case_name}` | {r.source} | {n} | {ok} | {to} | {cr} | "
            f"{mf} | **{r.verdict}** | {wall:.1f}s |"
        )

    lines.append("")
    lines.append("## Per-case detail")
    lines.append("")

    for r in results:
        lines.append(f"### {r.case_name}")
        lines.append("")
        lines.append(f"- source: `{r.source}`  netlist_lines: {r.netlist_lines}  "
                     f"verdict: **{r.verdict}**")
        lines.append(f"- stderr: `{r.stderr_path}`")
        lines.append(f"- system .log: `{r.log_path}`")
        lines.append("")
        for p in r.prompts:
            lines.append(f"#### Prompt {p.id} — {p.task_type} / "
                         f"{p.expected_kind} — **{p.status}** ({p.duration_s:.1f}s)")
            lines.append("")
            lines.append("**Request:**")
            lines.append("")
            lines.append("> " + p.text.replace("\n", "\n> "))
            lines.append("")
            if p.response_text:
                lines.append("**System response:**")
                lines.append("")
                lines.append("```")
                lines.append(p.response_text)
                lines.append("```")
                lines.append("")
            if p.error:
                lines.append(f"**Error:** `{p.error}`")
                lines.append("")
        lines.append("---")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system-cmd", default=DEFAULT_SYSTEM_CMD,
                    help="command to invoke the system-under-test "
                         "(also reads BENCH_SYSTEM_CMD env var)")
    ap.add_argument("--source", choices=["official", "community", "personal", "all"],
                    default="all")
    ap.add_argument("--cases", default=None,
                    help="comma-separated case names (e.g. test01,test10)")
    ap.add_argument("--output-dir", type=Path, default=None,
                    help="results dir (default: results/run_<timestamp>/)")
    ap.add_argument("--list-only", action="store_true",
                    help="just print what would run, don't execute")
    args = ap.parse_args()

    cases_filter = None
    if args.cases:
        cases_filter = [c.strip() for c in args.cases.split(",")]
    case_dirs = discover_cases(args.source, cases_filter)

    if args.list_only:
        for d in case_dirs:
            print(d)
        return 0

    if not case_dirs:
        print("error: no cases matched filter", file=sys.stderr)
        return 1

    run_id = time.strftime("%Y%m%d_%H%M%S")
    output_dir = args.output_dir or (REPO_ROOT / "results" / f"run_{run_id}")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[run] {len(case_dirs)} cases -> {output_dir}")
    print(f"[run] system_cmd: {args.system_cmd}")

    run_meta = {
        "run_id": run_id,
        "started_iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "system_cmd": args.system_cmd,
        "source_filter": args.source,
        "cases_filter": cases_filter,
    }
    (output_dir / "run_meta.json").write_text(
        json.dumps(run_meta, indent=2), encoding="utf-8"
    )

    results: list[CaseResult] = []
    for d in case_dirs:
        print(f"[case] {d.name} ...", flush=True)
        r = run_case(d, args.system_cmd, output_dir)
        results.append(r)
        # Persist per-case JSON immediately so we don't lose data on crash.
        (output_dir / f"{d.name}.json").write_text(
            json.dumps(asdict(r), indent=2), encoding="utf-8"
        )
        n = len(r.prompts)
        ok = sum(1 for p in r.prompts if p.status == "ok")
        wall = r.finished_at - r.started_at
        print(f"        {ok}/{n} ok, {wall:.1f}s, verdict={r.verdict}")

    book = output_dir / "result_book.md"
    render_result_book(results, book, run_meta)
    print(f"[done] result book: {book}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
