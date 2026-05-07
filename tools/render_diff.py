#!/usr/bin/env python3
"""Render a side-by-side comparison of two contest-format `.log` files.

Each `.log` consists of `#RESPONSE <id>` ... `#END <id>` blocks. This script
parses both files into ordered (id, body) pairs and emits a Markdown table
with one row per response id, golden in the left column, system in the right.

Usage:
    python3 render_diff.py <system.log> <golden.log> [> diff.md]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_RE_RESPONSE = re.compile(r"^#RESPONSE\s+(\d+)\s*$", re.IGNORECASE)
_RE_END = re.compile(r"^#END\s+(\d+)\s*$", re.IGNORECASE)


def parse_log(path: Path) -> Dict[int, str]:
    """Parse a contest-format log into {id: body_text}."""
    out: Dict[int, str] = {}
    if not path.exists():
        return out
    text = path.read_text(encoding="utf-8", errors="replace")
    cur_id: Optional[int] = None
    cur_lines: List[str] = []
    for raw in text.splitlines():
        m_start = _RE_RESPONSE.match(raw)
        if m_start:
            if cur_id is not None:
                out[cur_id] = "\n".join(cur_lines).strip()
            cur_id = int(m_start.group(1))
            cur_lines = []
            continue
        m_end = _RE_END.match(raw)
        if m_end:
            if cur_id is not None:
                out[cur_id] = "\n".join(cur_lines).strip()
                cur_id = None
                cur_lines = []
            continue
        if cur_id is not None:
            cur_lines.append(raw)
    # Tail (no trailing #END)
    if cur_id is not None:
        out[cur_id] = "\n".join(cur_lines).strip()
    return out


def _md_cell(text: str) -> str:
    """Markdown table cell: replace newlines with <br>, escape pipes."""
    return text.replace("|", "\\|").replace("\n", "<br>") or "_(empty)_"


def render(system: Dict[int, str], golden: Dict[int, str], system_path: Path,
           golden_path: Path) -> str:
    all_ids = sorted(set(system) | set(golden))
    lines: List[str] = []
    lines.append(f"# Benchmark diff: `{system_path.name}` vs golden `{golden_path.name}`")
    lines.append("")
    lines.append(f"- **System log:** `{system_path}`")
    lines.append(f"- **Golden log:** `{golden_path}`")
    lines.append(f"- **Response count:** system={len(system)}, golden={len(golden)}")
    if not all_ids:
        lines.append("")
        lines.append("_No responses parsed in either file._")
        return "\n".join(lines) + "\n"
    lines.append("")
    lines.append("| ID | Golden (reference) | System output |")
    lines.append("|----|--------------------|---------------|")
    for rid in all_ids:
        g = golden.get(rid, "")
        s = system.get(rid, "")
        lines.append(f"| {rid} | {_md_cell(g)} | {_md_cell(s)} |")
    lines.append("")
    # Quick stats: how many ids match exactly (after whitespace strip).
    exact = sum(1 for rid in all_ids
                if golden.get(rid, "").strip() == system.get(rid, "").strip()
                and rid in golden and rid in system)
    lines.append(f"_Exact-text matches: {exact} / {len(all_ids)}._ "
                 f"(Note: NL answers can be semantically equal without exact match — "
                 f"this number is a sanity floor, not a score.)")
    return "\n".join(lines) + "\n"


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("system_log", type=Path, help="System's <case_name>.log")
    p.add_argument("golden_log", type=Path, help="Reference golden.log")
    args = p.parse_args(argv)

    sys_d = parse_log(args.system_log)
    gold_d = parse_log(args.golden_log)
    print(render(sys_d, gold_d, args.system_log, args.golden_log))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
