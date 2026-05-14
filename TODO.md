# TODO — Deferred Work

Tracking items intentionally left for later iterations. Everything here is *out of scope* for the current commit set; revisit when the corresponding precondition is satisfied.

## Automation (CI)

Inspired by `sys-nthu/ast26-quiz`'s contribution flow.

- **Format validator** — verify `requests.txt` first line matches contest spec, `#RESPONSE`/`#END` ids are sequential and matched, response count == request count.
- **Verilog parse check** — pyverilog round-trip on every `tests/case_*/design.v` in PR.
- **Schema validator for `meta.yaml`** — ids referenced exist in `requests.txt`, status enum is one of `unverified` / `review_pending` / `human_verified`.
- **LLM-as-judge** — automated similarity scoring between system output and golden answer using Claude API. Only run on PRs touching `golden.log` to verify reviewer's stated answer is consistent with the design. **Not** a grader for system runs.

## Runner enhancements

- **Side-by-side dual-provider run** — same testcase under both OpenAI and Anthropic in a single invocation, output as two columns in the result book. Currently the runner is single-provider per invocation.
- **Reproducibility N-run mode** — run each testcase N times (default 3), report answer variance / pass-rate per prompt. Useful because LLM responses are non-deterministic.
- **Per-prompt token / cost accounting** — surface `tokens_used` / `$_spent` per prompt in the result book when the system reports them.
- **Concurrency** — `--jobs N` to run N testcases in parallel. Wall-time savings matter once routinely running the official 40.

## Result book enhancements

- **Pass/fail aggregate** at the top of the result book, color-coded.
- **Tagging filter on render** — render only `task_type=analysis` rows, etc.
- **Historical comparison** — diff a new run against the previous result book to catch regressions.

## Testcase coverage gaps

Currently in `tests/`:

- 6 cases derived from the contest problem-statement examples and a small handful of hand-crafted designs.
- 2 cases added 2026-05-14: `case_c17` (ISCAS85) and `case_spec_gaps` (spec §4.3 transformation patterns).

Light on: multi-clock domain, scan chain, retiming-relevant, deep XOR trees, very-large netlists (>10k gates). Contributions especially welcome here.

Adversarial twists especially welcome: instance literally named `out0`, dangling gates, constant outputs, signals named like Verilog keywords.

## Open questions to contest organizers

Uncertainties about the contest spec itself, not the benchmark. Resolutions get folded into the schema and CONTRIBUTING.md once received.

1. Definition of `cost` for optimization tasks (gate count? depth? AIG nodes?).
2. Hard requirements vs soft objectives — how to interpret implicit constraints.
3. Multi-PO optimization scope — when shared fanout prevents in-place change, is duplicating logic acceptable.
4. Counterexample format for analysis questions.
