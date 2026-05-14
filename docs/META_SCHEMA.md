# `meta.yaml` Schema — Optional Per-Testcase Metadata Sidecar

`meta.yaml` is an **optional** sidecar file that sits next to the existing four required files (`design.v`, `requests.txt`, `golden.log`, `README.md`) inside a `tests/case_<name>/` directory.

It exists for one reason: to let tooling (the Python runner, future LLM-judge, future analytics) reason about each prompt **structurally** instead of having to text-parse `requests.txt`.

The old shell runner ignores it; the new Python runner reads it when present.

## When to add a `meta.yaml`

- **Always** for new testcases authored after 2026-05-14. Format-correct contributors should include it.
- **Optional** for existing testcases — backfill as time permits.
- **Required by tooling**: only when the testcase is the target of an automated grader. Without `meta.yaml`, the runner can still execute the testcase and capture output, but cannot grade it beyond flow-level (crash / timeout / malformed protocol).

## File layout

```yaml
# tests/case_<name>/meta.yaml
schema_version: 1
source: community            # one of: official_0510 | community | personal
contributor: <name or handle>  # optional
tags: [path_query, dff]      # optional, free-form filter labels

prompts:
  - id: 1
    task_type: basic
    expected:
      kind: ack
      status: human_verified
  - id: 2
    task_type: basic
    expected:
      kind: ack
      status: human_verified
  - id: 3
    task_type: analysis
    expected:
      kind: yes_no
      value: false
      counterexample: "c -> U2 -> U4 -> U5 -> out0"  # optional
      status: human_verified
  - id: 4
    task_type: optimization
    expected:
      kind: cost_improvement
      baseline_metric: gate_count
      baseline_value: 142
      status: review_pending
```

## Field reference

### Top-level

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | int | yes | Currently always `1`. Bumped if breaking schema changes ship. |
| `source` | enum | yes | `official_0510` for official contest cases; `community` for PR-contributed; `personal` for the maintainer's own. |
| `contributor` | string | no | Free-form handle. |
| `tags` | list[string] | no | Filterable labels (e.g. `path_query`, `dff`, `multi_clock`). Used by `runner --tag <tag>`. |
| `prompts` | list | yes | One entry per non-comment line in `requests.txt`. `id` field must be `1..N` in order. |

### Per-prompt

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | int | yes | Matches `#RESPONSE <id>` in `golden.log`. 1-indexed, monotonic. |
| `task_type` | enum | yes | `basic` \| `analysis` \| `modification` \| `optimization`. Maps to contest §4.{1,2,3}. |
| `expected` | object | yes | See `expected.kind` table below. |

### `expected.kind` — 10 values

| kind | Used for | Future grader strategy |
|---|---|---|
| `ack` | Read design / write design / set testcase name — basic ops returning an acknowledgment. | Pass if system responded at all and didn't crash. |
| `yes_no` | Boolean analysis questions. `value: true/false`; optionally `counterexample: "<text>"`. | String-extract yes/no from response and compare to `value`. |
| `number` | Single-number answers (max depth, gate count, fanout count, etc.). | Regex-extract integer and compare to `value`. |
| `gate_count` | "Count all gates broken down by type" — answer is a dict. `value: {and: 12, nand: 3, ...}`. | Parse expected key:value pairs from response; compare each. |
| `signal_list` | "List all DFFs", "Report every gate connected to ...". `value: [list of signal/instance names]`. | Extract list, compare as set (order-insensitive unless `ordered: true`). |
| `path_list` | "List every path from A to B". `value: [[node, node, node], ...]`. | Each path is a node sequence; compare as a set of sequences. |
| `boolean_expr` | "What Boolean function does output X compute?" `value: "a & (b | c)"` in some canonical form. | Parse expression, build truth table, compare against system's expression's truth table. |
| `equivalence` | "Verify functional equivalence" / "Prove the transformed design is equivalent to the pre-transformation netlist." `value: true` for must-be-equivalent. | Run ABC `cec` on the designs the system was asked about. Independent of the system's text response. |
| `cost_improvement` | Optimization tasks. `baseline_metric: gate_count`, `baseline_value: 142`. | Post-run: load the system's output netlist, compute the same metric, pass iff new ≤ baseline (and ABC cec confirms equivalence). |
| `free_text` | Anything that doesn't fit above: descriptive paragraphs, Boolean-function-via-prose, justified path enumerations with reasoning. | LLM-judge required. No deterministic grader available. |

### `expected.status` — 3 values

| status | Meaning | Grader behavior |
|---|---|---|
| `unverified` | Reference answer field `value` is empty / unknown. The author hasn't determined the correct answer yet. | Runner records system output, marks "no reference"; grader skipped. |
| `review_pending` | Reference answer `value` was filled by looking at *some* system's output and assumed to be correct, but hasn't been independently verified. | Runner records and grades, but flags result with `caveat: review_pending`. Disagreement does NOT mean the system failed — might be the reference that's wrong. |
| `human_verified` | A human has independently verified `value` is correct for the design. | Runner grades against `value` confidently. Disagreement = system bug. |

Always default new prompts to `unverified`. Promote to `review_pending` after seeing a plausible system answer. Promote to `human_verified` only after walking through the derivation manually.

## Validation rules

- `prompts[*].id` must be `1..N` contiguous, matching the count of non-comment lines in `requests.txt`.
- Every `#RESPONSE <id>` in `golden.log` must have a corresponding `prompts[*].id` in `meta.yaml` (so the runner can locate the reference).
- `task_type=optimization` requires `expected.kind in {cost_improvement, equivalence}`.
- `expected.kind in {gate_count, signal_list, path_list, boolean_expr}` may have `value: null` only if `status: unverified`.

The Python runner enforces these on load.

## Example: official `test01` after conversion

The official `test01` has 3 prompts (set-testcase / load / write). All three are basic ops, all three are `ack`. Trivial:

```yaml
schema_version: 1
source: official_0510
prompts:
  - { id: 1, task_type: basic, expected: { kind: ack, status: human_verified } }
  - { id: 2, task_type: basic, expected: { kind: ack, status: human_verified } }
  - { id: 3, task_type: basic, expected: { kind: ack, status: human_verified } }
```

## Example: official `test10` first 5 prompts

```yaml
schema_version: 1
source: official_0510
tags: [path_query, depth]
prompts:
  - { id: 1, task_type: basic, expected: { kind: ack, status: human_verified } }
  - { id: 2, task_type: basic, expected: { kind: ack, status: human_verified } }
  - id: 3
    task_type: analysis
    expected:
      kind: yes_no
      value: null              # unknown until reviewed
      status: unverified
  - id: 4
    task_type: analysis
    expected:
      kind: yes_no
      value: null
      status: unverified
  - id: 5
    task_type: analysis
    expected:
      kind: path_list
      value: null
      status: unverified
  # ...
```
