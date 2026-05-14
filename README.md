# ICCAD 2026 Problem A — Open Benchmark

A community-built benchmark suite for **ICCAD Contest 2026 Problem A: LLM-Assisted Netlist Exploration and Transformation**.

The contest asks teams to build a system that accepts natural-language requests, interprets them, and executes analysis or transformation flows on a gate-level Verilog design. This repo collects testcases — designs paired with NL request sequences and reference answers — that anyone can use to evaluate their own system.

> 繁中版說明請見 [README.zh-TW.md](README.zh-TW.md).

## Goals

1. **Reduce overfitting to a single team's eval set.** Adversarial testcases from many contributors cover corner cases no single team would think of alone.
2. **Match the contest's I/O format exactly** (see §3 of the problem statement). Any system that can pass these testcases is wired up correctly for the real evaluator.
3. **Open enough to invite all teams / all participating advisors.** Public, MIT-licensed, no NDA, no team-affiliation gating.

## Repository layout

```
ICCAD2026_Problem-A_Benchmark/
├── README.md                       # this file (English)
├── README.zh-TW.md                 # Traditional Chinese (Taiwan) translation
├── CONTRIBUTING.md                 # rules for adding new testcases
├── TODO.md                         # deferred work / known gaps
├── LICENSE                         # MIT
├── docs/
│   ├── META_SCHEMA.md              # optional per-case meta.yaml schema
│   └── MANUAL_REVIEW_WORKFLOW.md   # how to author golden answers
├── tests/
│   └── case_<name>/
│       ├── design.v                # gate-level Verilog (one top module, primitives only)
│       ├── requests.txt            # one NL request per line, fed to the system via stdin
│       ├── golden.log              # reference output, formatted as #RESPONSE/#END (per contest §3.3)
│       ├── meta.yaml               # OPTIONAL: per-prompt task_type + expected.kind
│       └── README.md               # design description + question intent
├── runner/
│   ├── run_bench.py                # Python runner (recommended) — selectors, timeouts, result book
│   └── run_bench.sh                # legacy shell runner (single-case, kept for backward compat)
├── tools/
│   ├── convert_official.py         # convert official testcase release → benchmark schema
│   └── render_diff.py              # golden vs actual side-by-side Markdown diff
└── results/                        # generated per-run output (gitignored)
    └── run_<timestamp>/
        ├── result_book.md
        ├── run_meta.json
        └── <case>/{system.log, system.stderr, artifacts/*.v, ...}
```

## Format conformance with the contest spec

| Contest spec (problem statement §3)                                               | This repo                                                                                         |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| System reads NL requests from **stdin**, one per line                             | `tests/<case>/requests.txt` is exactly that stream                                                |
| System writes responses to **stdout** delimited by `#RESPONSE <id>` / `#END <id>` | `tests/<case>/golden.log` is the reference response stream in this exact format                   |
| System also writes a copy to `<case_name>.log`                                    | The runner captures the system's actual log into `results/<run>/<case>/system.log` for inspection |
| Testcase begins with `This is the beginning of testcase <name>. ...`              | First line of `requests.txt` follows this pattern                                                 |
| Per-prompt timeout: 60s for basic ops, 300s for others                            | `runner/run_bench.py` enforces both, marks per-prompt `status: timeout`                           |

## Quick start

```bash
# 1. Clone & enter
git clone https://github.com/ZMYsamuel/ICCAD2026_Problem-A_Benchmark.git
cd ICCAD2026_Problem-A_Benchmark

# 2. Install runner dependencies (PyYAML only)
python3 -m pip install pyyaml

# 3. Point the runner at your system binary (per contest spec §3.1
#    your binary should be named cada<team-number>_alpha).
#    Easiest: put this in your shell rc so the runner "just works":
export BENCH_SYSTEM_CMD="/abs/path/to/your_team_alpha -config /abs/path/to/llm_config.yaml"

# 4. Run one case
python3 runner/run_bench.py --source community --cases case_demo01

# 5. Run every community case
python3 runner/run_bench.py --source community

# 6. Inspect the result book
ls results/run_*/result_book.md
```

The runner produces a `result_book.md` per run containing per-case timing, per-prompt request + system response + reference answer (when present in `meta.yaml`), and aggregate pass/fail stats.

## `runner/run_bench.py` — CLI reference

```
python3 runner/run_bench.py [flags]
```

| Flag                  | Default                                                                     | Description                                                                                                                                                                                                                                          |
| --------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--system-cmd <str>`  | `$BENCH_SYSTEM_CMD` env var, or `./your_team_alpha -config llm_config.yaml` | Shell command to invoke the system under test. Required — runner cannot work without a real binary path. The runner spawns this command in a temp workdir per case, pipes `requests.txt` to its stdin, and reads `#RESPONSE/#END` lines from stdout. |
| `--source <enum>`     | `all`                                                                       | Which corpus to draw cases from. `community` → `tests/case_*/` (public, this repo). `official` → `private/official_0510/test*/` (gitignored, see below). `personal` → reserved. `all` → both.                                                        |
| `--cases <csv>`       | _(none)_                                                                    | Comma-separated case names to filter (e.g. `test01,test10,case_demo01`). Matches against the case directory's name with or without the `case_` prefix.                                                                                               |
| `--output-dir <path>` | `results/run_<timestamp>/`                                                  | Override where the result book + per-case artifacts get written.                                                                                                                                                                                     |
| `--list-only`         | off                                                                         | Print the discovered case directories and exit without running. Useful for sanity-checking selectors.                                                                                                                                                |

The runner inherits the **environment** of whoever invokes it, so anything the system reads at startup (API keys, `LD_LIBRARY_PATH`, config files via your shell wrapper) is whatever the shell already has set. The runner only injects `LD_LIBRARY_PATH=/lib64/:$LD_LIBRARY_PATH` so PyYAML on NTHU workstations works.

### Switching LLM providers (OpenAI ↔ Claude)

The runner is provider-agnostic. To switch which LLM your system talks to:

1. Edit your system's config file (whatever `--system-cmd` points at via `-config <path>`) and set `provider: "openai"` or `provider: "anthropic"`.
2. Make sure the corresponding API key is exported (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`).
3. Re-run the runner — no flag changes needed.

Contest §6.2 specifies `gpt-4o-mini` and `claude-haiku-4-5` as the two evaluated providers, so testing both is recommended.

### Hybrid public/private corpus

The runner supports two parallel test corpora:

- `tests/case_<name>/` — public, MIT-licensed, this repo. Contributed by anyone.
- `private/official_0510/test<NN>/` — gitignored. The 40 official testcases released 2026-05-10 by Cadence. Do **not** commit; redistribution rights are unclear. Use `tools/convert_official.py` to convert the official release into the schema, dropped into `private/`.

```bash
# Convert the official 0510 release (default expects ~/official_docs/A_release\ testcase_0510/)
python3 tools/convert_official.py            # all 40
python3 tools/convert_official.py --cases test01,test10  # subset

# Run private corpus (only works after conversion; never pushed to GitHub)
python3 runner/run_bench.py --source official
```

## Contributing a testcase

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full mandatory format. Short version:

1. Create `tests/case_<your_name>/` with `design.v`, `requests.txt`, `golden.log`, and `README.md`.
2. (Optional but recommended) add `meta.yaml` per [docs/META_SCHEMA.md](docs/META_SCHEMA.md) — this lets future automated graders score your testcase.
3. Open a PR. CI will validate format, Verilog parsability, and `#RESPONSE` counts.
4. Maintainer reviews **the design, the questions, and the golden answers**. Golden answers must be provably correct — be ready to walk through any non-obvious calculations.

## License

[MIT](LICENSE) — copy, modify, redistribute freely. Cite the repo if you use it in a paper.

## Status

- 2026-05-07: Initial scaffold + 6 sample testcases derived from the contest problem statement examples and a small demo design.
- 2026-05-14: Python runner + meta.yaml schema + `case_c17` (ISCAS85) + `case_spec_gaps` (spec §4.3 transformation patterns).
- See [TODO.md](TODO.md) for deferred work (CI validation, LLM-judge for automated scoring, dual-provider side-by-side runs).
