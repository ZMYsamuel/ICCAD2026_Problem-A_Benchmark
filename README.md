# ICCAD 2026 Problem A — Open Benchmark

A community-built benchmark suite for **ICCAD Contest 2026 Problem A: LLM-Assisted Netlist Exploration and Transformation**.

The contest asks teams to build a system that accepts natural-language requests, interprets them, and executes analysis or transformation flows on a gate-level Verilog design. This repo collects testcases — designs paired with NL request sequences and reference answers — that anyone can use to evaluate their own system.

## Goals

1. **Reduce overfitting to a single team's eval set.** Adversarial testcases from many contributors cover corner cases nobody-team would think of alone.
2. **Match the contest's I/O format exactly** (see §3 of the problem statement). Any system that can pass these testcases is wired up correctly for the real evaluator.
3. **Open enough to invite all teams / all participating advisors.** Public, MIT-licensed, no NDA, no team-affiliation gating.

## Repository layout

```
ICCAD2026_Problem-A_Benchmark/
├── README.md             # this file
├── CONTRIBUTING.md       # rules for adding new testcases
├── LICENSE               # MIT
├── tests/
│   └── case_<name>/
│       ├── design.v          # gate-level Verilog (one top module, primitives only)
│       ├── requests.txt      # one NL request per line, fed to the system via stdin
│       ├── golden.log        # reference output, formatted as #RESPONSE/#END (per contest §3.3)
│       └── README.md         # design description + question intent
├── runner/
│   └── run_bench.sh      # invokes a system per testcase; collects <case>.log for review
└── tools/
    └── render_diff.py    # renders golden.log vs system <case>.log side-by-side as Markdown
```

## Format conformance with the contest spec

| Contest spec (problem statement §3) | This repo |
|---|---|
| System reads NL requests from **stdin**, one per line | `tests/<case>/requests.txt` is exactly that stream |
| System writes responses to **stdout** delimited by `#RESPONSE <id>` / `#END <id>` | `tests/<case>/golden.log` is the reference response stream in this exact format |
| System also writes a copy to `<case_name>.log` | `runner/run_bench.sh` captures the system's actual log into `results/<case_name>.log` for inspection |
| Testcase begins with "This is the beginning of testcase `<name>`. Please output a copy of the log into `<name>.log`." | First line of `requests.txt` follows this pattern |

## How to run a benchmark against your system

```bash
# 1. Make sure your system is invokable as ./your_team_alpha (per contest spec §3.1).
# 2. From repo root:
./runner/run_bench.sh /path/to/your_team_alpha tests/case_demo01/

# 3. Inspect side-by-side:
python3 tools/render_diff.py results/case_demo01.log tests/case_demo01/golden.log > diff.md
```

The runner produces `results/<case>.log` containing the system's actual output. The diff renderer puts golden vs actual side-by-side — **scoring is human-eyeballed for now**, since natural-language responses have legitimate ambiguity (the same answer can be phrased in many ways). A future automated **similarity-judge LLM agent** is on the TODO list.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short:

1. Create `tests/case_<your_name>/` with `design.v`, `requests.txt`, `golden.log`, and `README.md`.
2. Open a PR. CI validates format, parsability, and #RESPONSE counts.
3. The maintainer reviews **the design, the questions, and the golden answers**. Golden answers must be **provably correct** for the design (you'll be asked to walk through any non-obvious calculations).

## License

[MIT](LICENSE) — copy, modify, redistribute freely. Cite the repo if you use it in a paper.

## Status

- 2026-05-07: Initial scaffold + 6 sample testcases derived from the contest problem statement examples and the maintainer's Week-4 demo design.
- TODO: similarity-judge LLM agent for automated scoring; CI validation workflow; broader testcase coverage (multi-clock, scan-chain, retiming).
