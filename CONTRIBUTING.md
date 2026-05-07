# Contributing a Testcase

Thanks for adding to the benchmark! This document specifies the **mandatory format** for new testcases.

## Layout

Each testcase lives in `tests/case_<unique_name>/` and contains exactly four files:

```
tests/case_<unique_name>/
├── design.v          # gate-level Verilog (REQUIRED)
├── requests.txt      # NL requests, one per line (REQUIRED)
├── golden.log        # reference responses (REQUIRED)
└── README.md         # design description + question intent (REQUIRED)
```

All four are required. PRs missing any file will be asked to revise.

## File specs

### `design.v`

- Single top module per file (no hierarchy).
- Primitive gates only (`and`, `or`, `not`, `nand`, `nor`, `xor`, `xnor`, `buf`, `dff`).
- 2-input gates except `buf` / `not` (1 input).
- DFF positional ports: `dff inst (q, d, clk, rst_n)`.
- `input` / `output` ports may be scalar or bus (`input [31:0] a;`).
- Must be parseable by [pyverilog](https://github.com/PyHDI/Pyverilog) — the `runner/` validation script confirms this.

You may include a comment block at the top describing the circuit (e.g. ASCII topology diagram, expected depth, intended boolean function).

### `requests.txt`

One natural-language request per line. Comment lines beginning with `#` are stripped before sending to the system.

**The first line MUST be**:

```
This is the beginning of testcase <case_name>. Please output a copy of the log into <case_name>.log.
```

(Per contest spec §3.3 — this is how the system learns the testcase identifier and where to write its log.)

Subsequent lines are the actual questions. They can be analysis (§4.2 of the problem statement), transformation (§4.3), or basic operations (§4.1, e.g. "Load design.v from this directory").

Common request patterns are catalogued in the contest problem statement §4. You may reuse them or invent new variations — wording is unconstrained.

### `golden.log`

Reference responses, in the **exact format the contest expects**:

```
#RESPONSE 1
<reference text for the testcase initialization>
#END 1
#RESPONSE 2
<reference text for question 2>
#END 2
...
```

- IDs start at 1, monotonically increasing.
- The number of `#RESPONSE <id>` blocks must equal the number of non-comment lines in `requests.txt`.
- Each block contains the **canonical** answer. For numerical analysis questions (e.g. "max depth = 4"), state the number plus a brief justification. For transform questions, describe the result and any properties that should hold post-transform.

**Note on golden answers**: They are *reference*, not auto-graded. Natural-language answers have legitimate ambiguity (e.g. "yes, the path passes through G_mid" vs "Yes, every path goes through G_mid"). Reviewers compare manually for now; an LLM-based similarity judge is in development.

### `README.md` (per testcase)

Two sections:

```markdown
## Design

<short description of the circuit — what it computes, why it's interesting,
 ASCII topology if useful>

## Questions

<for each numbered question, one bullet listing what's being tested,
 and any non-obvious reasoning behind the golden answer>

## Contributor

<your name / handle / email — optional but appreciated>
```

## What makes a good testcase?

- **Real problem coverage**: At least one question should exercise a non-trivial property (e.g. a path query that requires graph traversal, not just summary stats).
- **A single transform task**: If you include a transformation, also include a follow-up analysis or write that exercises post-transform state.
- **Tight boundaries**: Avoid huge designs (>1000 gates) unless that scale is itself the point — the system should be able to answer in reasonable wall time.
- **Adversarial twists welcome**: Naming patterns that resemble keywords (e.g. an instance literally named `out0`), gates with no fanout (dangling), constant outputs, multiple clock domains — these stress the system's robustness.

## What's NOT allowed

- Closed-source cell libraries.
- Hierarchical Verilog (must be flat).
- Non-deterministic golden (e.g. "any path of length ≥ 3" — pick one specific path).
- Submitting a question whose golden you cannot justify; if asked "why is this 5", you should be able to walk through the derivation.

## PR process

1. Fork & branch.
2. Add your `tests/case_<name>/` directory with all 4 files.
3. (Optional but encouraged) Run `python3 tools/validate.py tests/case_<name>/` locally if such a script exists.
4. Open a PR. CI should pass (format, parse, response count match).
5. A maintainer reviews — primarily **the golden's correctness**, since that's the part that has to be trusted. Be ready to explain any non-obvious answers.
6. On merge, your testcase becomes part of the public benchmark.

## License

By contributing, you agree your testcase is published under the repo's MIT license — anyone can use it for any purpose.
