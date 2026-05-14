# Manual Review Workflow — Verifying Reference Answers

Goal: walk through every prompt in the benchmark (≈511 prompts across 48 cases: 40 official + 6 + 2 community), fill `expected.value` in each `meta.yaml`, and promote `status` from `unverified` → `review_pending` → `human_verified`.

Doing this in one sitting is masochistic. The strategy below prioritizes maximum coverage per hour and uses the result book + an auto-helper to shortcut anything mechanically verifiable.

## Status semantics (recap)

| status | Meaning | When to use |
|---|---|---|
| `unverified` | `value` is `null`; correct answer not yet known | Default; converter output |
| `review_pending` | `value` filled, but the source is "system's own answer looked plausible" | Mid-pass labeling — useful for `path_list` where many valid answers exist |
| `human_verified` | `value` independently checked by you (not just confirmed against system) | Final state; this is what an auto-grader can trust |

Never grade against a `review_pending` reference and conclude the system is broken — the reference might be wrong.

## Three-pass approach

### Pass 1 — Auto-fill the deterministic 60% (target: 4-6 hours of YOUR time, mostly script-driven)

For each kind, ask "can I compute this from `design.v` alone, without running cada0001_alpha?":

| kind | Auto-computable? | How |
|---|---|---|
| `ack` | n/a (always human_verified) | converter already sets these |
| `gate_count` | **Yes** | `NetlistGraph` count by type — write a helper that produces the dict |
| `number` (depth) | **Yes** | `get_logic_depth(src, dst)` from the Python backend |
| `number` (fanout) | **Yes** | `len(graph.successors(net))` |
| `number` (cone size) | **Yes** | `get_cone_info(...).gate_count` |
| `signal_list` (list NAND gates etc.) | **Yes** | `find_instances_by_pattern("nand")` then filter |
| `signal_list` (fanout consumers) | **Yes** | graph successors |
| `yes_no` (path exists, every-path-through) | **Yes** | `find_path` / `does_every_path_pass_through` |
| `path_list` | **Partial** | enumerate paths via `nx.all_simple_paths` — order/multiplicity is the user choice |
| `boolean_expr` | **Yes** | ABC `print_sop` |
| `equivalence` | **Yes** | ABC `cec` between expected before/after netlists |
| `cost_improvement` | **Yes** | gate-count diff between original and system's output |
| `free_text` | **No** | Always manual |

**Write a helper script**: `tools/answer_helper.py <case_dir>` that loads `design.v` into NetlistGraph, runs each query referenced in the case's prompts, and outputs a draft `expected:` block per prompt. **You then eyeball + accept; the script does the typing.**

Skeleton:
```python
# tools/answer_helper.py
from eda.netlist_graph import NetlistGraph
from eda.verilog_parser import parse_verilog
import yaml, sys

def draft_answer(case_dir):
    g = parse_verilog(case_dir / "design.v")
    meta = yaml.safe_load((case_dir / "meta.yaml").read_text())
    for p in meta["prompts"]:
        kind = p["expected"]["kind"]
        if kind == "gate_count":
            p["expected"]["value"] = g.gate_count_by_type()
            p["expected"]["status"] = "human_verified"
        elif kind == "number":
            # Look at prompt text to figure out what to compute.
            # E.g. "maximum logic depth from N1 to N22" → call get_logic_depth("N1", "N22")
            ...
    # Print as YAML for user to copy back.
```

This is ~1-2 hours of script writing for ~200+ prompts of automated reference fill.

### Pass 2 — Eyeball the system response, mark `review_pending` (target: 2 hours)

Open the latest result book (`results/run_<id>/result_book.md`). For each non-`ack` prompt:

1. Read the system's response.
2. Plausibility-check by hand (does the number reasonable for the design size? does the yes/no fit topology?).
3. If plausible: copy the system's answer into `expected.value`, set `status: review_pending`.
4. If suspicious: flag for Pass 3, leave `status: unverified`.

**Tip**: open both `requests.txt` and `result_book.md` side-by-side. Use the result book's per-case detail section as your source.

`review_pending` is enough for a first-pass coverage and doesn't claim "correct" — only "plausible." Future you (or LLM judge) can re-evaluate later without trusting the existing reference.

### Pass 3 — Hard-verify the corner cases (target: as much time as you have)

What's left after Pass 1 & 2:
- `free_text` prompts (33 in official, 4-5 in community)
- `path_list` with many valid orderings
- Anything that looked suspicious during eyeballing
- All `equivalence` and `cost_improvement` claims need the system's output netlist (`results/<run>/<case>/artifacts/*.v`) checked via ABC `cec`. **This is the part where bugs hide.**

Walk through each, prove the answer with pencil-and-paper or by running an oracle. Promote to `human_verified`.

## Priority order across cases

If you can't do all 48 cases, do them in this order:

1. **Small + diverse** first: case_c17 (12), case_basic_io (3), case_demo01 (16), case_dff_clock (7). Total ~38 prompts, fast wins, tests the workflow.
2. **Official small cases**: test01 (3), test02 (4), test03 (4), test04 (4), test05 (4), test06 (5), test07 (6), test08 (7). Total ~37 prompts, exercises every kind once.
3. **Medium official**: test09-test20. Total ~150 prompts.
4. **Large stress cases**: test21-test40. Total ~280 prompts. Many are repeats of patterns, so Pass 1 auto-fill scales well.

Doing #1 + #2 first gives you a representative sample (~75 prompts) covering every `expected.kind` ── if the workflow has a hole, you find it early.

## What "good" looks like at the end of this

- Every prompt in every case has `status: human_verified` or `review_pending`.
- The 0% `unverified` rate means an auto-grader can fairly score the system.
- You have an answer-helper script you'll re-use for any new community contribution.
- You haven't trusted the system to grade itself anywhere (no circular validation).

## Time budget reality check

If we ballpark 30 seconds per prompt on Pass 1 (script-assisted) and 90 seconds per prompt on Pass 3 (hard verify):
- Pass 1 (200 prompts auto): 1.5–2 hours including helper script
- Pass 2 (200 prompts eyeball): 2–3 hours
- Pass 3 (111 hard prompts): 3 hours

Total: 6–8 hours spread across several sessions. Less if you skip Pass 3 on cases that aren't relevant for grading targets.

## Tooling roadmap (deferred — see TODO.md)

- `tools/answer_helper.py` — the Pass 1 helper described above.
- `tools/eyeball.py` — side-by-side renderer of result book + requests for Pass 2.
- LLM judge (ast26-quiz style) — for `free_text` and ambiguous responses; post-contest only.
