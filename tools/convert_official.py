#!/usr/bin/env python3
"""Convert official 0510 testcase release into benchmark-repo layout.

Source: <official_docs>/A_release testcase_0510/testcase/testNN/
        ├── testNN.v
        └── prompt.txt

Destination: <repo_root>/private/official_0510/testNN/
             ├── testNN.v       (symlink to source)
             ├── requests.txt   (= prompt.txt, comments-free)
             ├── golden.log     (empty stub — all responses status: unverified)
             ├── meta.yaml      (per-prompt task_type + expected.kind heuristic guess)
             └── README.md      (auto-gen: source attribution + per-prompt summary)

The classification of task_type and expected.kind is a *heuristic first pass* —
edit meta.yaml by hand to refine after.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

OFFICIAL_ROOT_DEFAULT = Path.home() / "official_docs" / "A_release testcase_0510" / "testcase"
REPO_ROOT_DEFAULT = Path.home() / "ICCAD2026_Problem-A_Benchmark"


# Heuristic keyword classifiers. First-match-wins, ordered by specificity.
# Stay conservative: when in doubt, drop to free_text so a human review fills it.

BASIC_PATTERNS = [
    r"\bthis is the beginning\b",
    r"\bcase name is\b",
    r"\bload the design\b",
    r"\bwrite the (current )?design\b",
    r"\boutput file\b",
]

OPTIMIZATION_VERBS = [
    "optimize", "minimize", "reduce", "shrink", "remap",
    "remove (unused|dangling|floating)", "eliminate", "collapse", "balance",
    "restructure", "merge",
]

MODIFICATION_VERBS = [
    "insert", "replace", "rename", "change the identifier",
    "update the name", "remap the entire design",
]

ANALYSIS_VERBS = [
    "does ", "is ", "verify", "determine whether", "report",
    "list ", "enumerate", "compute", "calculate", "find",
    "what is", "what type", "how many", "which ", "check ",
    "provide a complete enumeration", "prove", "express",
]


def classify_task_type(text: str) -> str:
    """basic | analysis | modification | optimization"""
    low = text.lower()
    for pat in BASIC_PATTERNS:
        if re.search(pat, low):
            return "basic"
    for v in OPTIMIZATION_VERBS:
        if re.search(rf"\b{v}\b", low):
            return "optimization"
    for v in MODIFICATION_VERBS:
        if re.search(rf"\b{v}\b", low):
            return "modification"
    for v in ANALYSIS_VERBS:
        if re.search(rf"\b{v}", low):
            return "analysis"
    return "analysis"  # safe default — at worst grader skips


def classify_expected_kind(text: str, task_type: str) -> str:
    """ack | yes_no | number | gate_count | signal_list | path_list |
       boolean_expr | equivalence | cost_improvement | free_text"""
    low = text.lower()
    if task_type == "basic":
        return "ack"
    if task_type == "optimization":
        if re.search(r"\bequivalen", low):
            return "equivalence"
        return "cost_improvement"
    if task_type == "modification":
        return "equivalence"
    # analysis
    if re.search(r"\b(does|is|verify|determine whether|check whether|"
                 r"prove|report yes or no)", low):
        return "yes_no"
    if re.search(r"\b(count|how many|number of|total .* count|"
                 r"compute the .* depth|maximum .* depth|longest .* depth|"
                 r"critical path depth|fanout of)", low):
        if re.search(r"broken down by gate type|by gate type", low):
            return "gate_count"
        return "number"
    if re.search(r"\blist (every|all)|enumerate|report every|"
                 r"list all .* (gates?|flip-flops?|inputs?|outputs?|"
                 r"signals?|primary outputs|primary inputs)", low):
        if "path" in low:
            return "path_list"
        return "signal_list"
    if re.search(r"\bpaths? (originating|between|from .* to .* )", low):
        return "path_list"
    if re.search(r"\b(transitive (fanin|fanout) cone|cone of)", low):
        return "signal_list"
    if re.search(r"\bboolean function|express it in terms of", low):
        return "boolean_expr"
    return "free_text"


def parse_prompt_file(path: Path) -> list[str]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        out.append(line)
    return out


def make_meta_yaml(prompts: list[str], source_tag: str, case_name: str) -> str:
    # The official prompts reference the netlist as `testcase/<case_name>/<case_name>.v`.
    # `runtime.netlist_mount` tells the runner where in its temp workdir the
    # netlist must appear so the system's relative path resolves.
    netlist_file = f"{case_name}.v"
    expected_path = f"testcase/{case_name}/{case_name}.v"

    lines = [
        "schema_version: 1",
        f"source: {source_tag}",
        "# Auto-generated. task_type and expected.kind are heuristic guesses.",
        "# Review each prompt and set status: human_verified once value is filled.",
        "runtime:",
        "  # Runner symlinks <case_dir>/<source> to <workdir>/<target> before launching system,",
        "  # then sets cwd=<workdir> so the prompt's relative path resolves.",
        "  netlist_mount:",
        f"    source: {netlist_file}",
        f"    target: {expected_path}",
        "prompts:",
    ]
    for i, text in enumerate(prompts, start=1):
        task_type = classify_task_type(text)
        kind = classify_expected_kind(text, task_type)
        lines.append(f"  - id: {i}")
        lines.append(f"    task_type: {task_type}")
        lines.append(f"    expected:")
        lines.append(f"      kind: {kind}")
        if kind == "ack":
            lines.append(f"      status: human_verified")
        else:
            lines.append(f"      value: null")
            lines.append(f"      status: unverified")
    lines.append("")
    return "\n".join(lines)


def make_empty_golden(n_prompts: int, case_name: str) -> str:
    out = []
    for i in range(1, n_prompts + 1):
        out.append(f"#RESPONSE {i}")
        out.append(f"(unverified — fill in after reviewing system output)")
        out.append(f"#END {i}")
    return "\n".join(out) + "\n"


def make_readme(case_name: str, prompts: list[str], netlist_lines: int) -> str:
    body = [
        f"# {case_name} — official 0510 release",
        "",
        f"**Source**: Cadence Design Systems, official release 2026-05-10.",
        f"**Netlist**: `{case_name}.v` ({netlist_lines} lines)",
        "",
        "## Prompts",
        "",
    ]
    for i, p in enumerate(prompts, start=1):
        body.append(f"{i}. {p}")
    body.append("")
    body.append("## Notes")
    body.append("")
    body.append("Golden answers are placeholders until human-reviewed. "
                "See `meta.yaml` for per-prompt task_type / expected.kind "
                "heuristic classifications.")
    body.append("")
    return "\n".join(body)


def convert_one(src_dir: Path, dst_dir: Path, source_tag: str) -> dict:
    case_name = src_dir.name
    src_v = src_dir / f"{case_name}.v"
    src_p = src_dir / "prompt.txt"
    if not src_v.exists() or not src_p.exists():
        raise FileNotFoundError(
            f"missing {src_v.name} or {src_p.name} in {src_dir}"
        )

    dst_dir.mkdir(parents=True, exist_ok=True)

    # Symlink uses absolute path so private/ relocation doesn't break links.
    dst_v = dst_dir / f"{case_name}.v"
    dst_v.unlink(missing_ok=True)
    dst_v.symlink_to(src_v.resolve())

    prompts = parse_prompt_file(src_p)
    (dst_dir / "requests.txt").write_text("\n".join(prompts) + "\n",
                                          encoding="utf-8")
    (dst_dir / "golden.log").write_text(
        make_empty_golden(len(prompts), case_name), encoding="utf-8"
    )
    (dst_dir / "meta.yaml").write_text(
        make_meta_yaml(prompts, source_tag, case_name), encoding="utf-8"
    )
    netlist_lines = src_v.read_text(encoding="utf-8", errors="ignore").count("\n")
    (dst_dir / "README.md").write_text(
        make_readme(case_name, prompts, netlist_lines), encoding="utf-8"
    )

    return {"case": case_name, "prompts": len(prompts),
            "netlist_lines": netlist_lines}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=OFFICIAL_ROOT_DEFAULT,
                    help="source testcase root (contains testNN/ subdirs)")
    ap.add_argument("--dst", type=Path,
                    default=REPO_ROOT_DEFAULT / "private" / "official_0510",
                    help="destination directory")
    ap.add_argument("--source-tag", default="official_0510",
                    help="value written to meta.yaml `source:` field")
    ap.add_argument("--cases", default=None,
                    help="comma-separated list of case names to convert "
                         "(default: all testNN/ subdirs of --src)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.src.is_dir():
        sys.exit(f"error: source dir not found: {args.src}")

    if args.cases:
        case_names = [c.strip() for c in args.cases.split(",")]
        case_dirs = [args.src / c for c in case_names]
    else:
        case_dirs = sorted(
            d for d in args.src.iterdir()
            if d.is_dir() and re.match(r"test\d+$", d.name)
        )

    stats = []
    for d in case_dirs:
        dst = args.dst / d.name
        if args.dry_run:
            print(f"[dry] would convert {d.name} -> {dst}")
            continue
        try:
            s = convert_one(d, dst, args.source_tag)
            stats.append(s)
            print(f"[ok]  {s['case']:<8} prompts={s['prompts']:<3} "
                  f"netlist_lines={s['netlist_lines']}")
        except Exception as e:
            print(f"[err] {d.name}: {e}", file=sys.stderr)

    if stats:
        print(f"\nconverted {len(stats)} testcases, "
              f"{sum(s['prompts'] for s in stats)} prompts total")


if __name__ == "__main__":
    main()
