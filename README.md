# ICCAD 2026 Problem A — Benchmark

[![Validate PR Contents](https://github.com/ZMYsamuel/ICCAD2026_Problem-A_Benchmark/actions/workflows/submission-validate.yml/badge.svg)](https://github.com/ZMYsamuel/ICCAD2026_Problem-A_Benchmark/actions/workflows/submission-validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A community submission archive for **ICCAD 2026 Problem A: LLM-Assisted Netlist Exploration and Transformation**.

Each participant runs the testcases through their own system, then submits the captured output here. By comparing submissions side-by-side, the class can cross-reference answers and reason about correctness without a single golden oracle.

## Goals

1. **Reduce overfitting to a single team's eval set.** Adversarial testcases from many contributors cover corner cases no single team would think of alone.
2. **Match the contest's I/O format exactly** (see §3 of the problem statement). Any system that passes these testcases is wired up correctly for the real evaluator.
3. **Open enough to invite all teams and advisors.** Public, MIT-licensed, no NDA, no team-affiliation gating.

## Repository structure

```
ICCAD2026_Problem-A_Benchmark/
├── official_testcase/          # 40 official Cadence testcases (maintainer-locked)
│   └── testNN/
│       ├── testNN.v            # gate-level Verilog netlist
│       ├── requests.txt        # official prompts (one per line)
│       ├── meta.yaml           # task_type + expected.kind metadata
│       ├── README.md           # testcase brief
│       └── <github-username>/ # your submission folder
│           ├── testNN.log      # REQUIRED — system output
│           ├── *.v             # OPTIONAL — output Verilog
│           └── submission.yaml # OPTIONAL — run metadata
├── community_testcase/         # community-contributed testcases (anyone may add/edit)
│   └── <case_name>/
│       ├── <case_name>.v       # netlist (any filename — at least one .v required)
│       ├── requests.txt        # prompts; first line declares case_name
│       ├── README.md           # OPTIONAL
│       └── <github-username>/<case_name>.log + optional *.v + submission.yaml
├── runner/run_bench.py         # submission runner
├── .github/
│   ├── scripts/validate_submission.py
│   └── workflows/submission-validate.yml
├── CONTRIBUTING.md
└── LICENSE
```

## Format conformance with the contest spec

| Contest spec (problem statement §3) | This repo |
|---|---|
| System reads NL requests from **stdin**, one per line | `requests.txt` in each testcase folder is exactly that stream |
| System writes responses to **stdout** delimited by `#RESPONSE <id>` / `#END <id>` | Submission log (`testNN.log` / `<case_name>.log`) must be in this exact format |
| Per-prompt timeout: 60 s for basic ops, 300 s for others | `runner/run_bench.py` enforces both; marks per-prompt `status: timeout` |
| Testcase begins with `This is the beginning of testcase <name>. …` | First line of every `requests.txt` follows this pattern |

## Requirements

- **Python 3.7+** to run `runner/run_bench.py`. On the NTHU CAD workstation the default `python3` is 3.6 — use `python3.9` instead.
- Your system under test and its dependencies (API keys, `LD_LIBRARY_PATH`, etc.) must be set up before invoking the runner. The runner inherits the shell environment.

## Quickstart — run the benchmark locally

```bash
# 1. Set your system command — must be an ABSOLUTE path because the runner
#    executes each case inside a temporary workdir, not the repo root.
export BENCH_SYSTEM_CMD="/absolute/path/to/your_system -config /absolute/path/to/llm_config.yaml"

# 2. Run the runner (use python3.9 on the NTHU CAD workstation)
python3.9 runner/run_bench.py --source official --cases test01      # one official case
python3.9 runner/run_bench.py --source community --cases demo01     # one community case
python3.9 runner/run_bench.py --source all                          # everything

# Output goes to: results/run_<timestamp>/<case>/system.log
# (results/ is gitignored — it never gets pushed)

# 3. Copy the log into your submission folder and open a PR
#    See CONTRIBUTING.md for the full workflow.
```

## `runner/run_bench.py` — CLI reference

| Flag | Default | Description |
|---|---|---|
| `--system-cmd <str>` | `$BENCH_SYSTEM_CMD` env var, or `./your_team_alpha -config llm_config.yaml` | Shell command to invoke the system under test. The runner spawns this command per case in a temp workdir, pipes `requests.txt` to stdin, and reads `#RESPONSE`/`#END` lines from stdout. |
| `--source <enum>` | `all` | Which corpus to draw cases from: `official` → `official_testcase/test*/`; `community` → `community_testcase/*/`; `all` → both. |
| `--cases <csv>` | _(none — run all)_ | Comma-separated case names to run (e.g. `test01,test10,demo01`). |
| `--output-dir <path>` | `results/run_<timestamp>/` | Override where the result book and per-case artifacts are written. |
| `--list-only` | off | Print the discovered case directories and exit without running. Useful for sanity-checking selectors. |

The runner inherits the shell's environment. Make sure any API keys and `LD_LIBRARY_PATH` settings your system needs are already exported before invoking the runner.

## Submitting your results

See [CONTRIBUTING.md](CONTRIBUTING.md) for step-by-step instructions, including how to fork this repo and open a pull request.

A GitHub Actions CI check validates the submission format automatically when you open a PR. The check is structural only — it verifies folder names, required files, and log format; it is not a correctness gate.

## FAQ / Troubleshooting

**`SyntaxError: future feature annotations is not defined`**
Your `python3` is older than 3.7. On the NTHU CAD workstation, run with `python3.9` explicitly.

**`spawn failed` or `No such file or directory` for your system binary**
`BENCH_SYSTEM_CMD` must use an **absolute path**. The runner executes each case inside a temporary directory; relative paths will not resolve.

**`[fatal] config not found: …`**
Double-check the config filename passed to your system. A common mistake is writing `config.yaml` when the actual file is `llm_config.yaml`.

**CI fails with "submission folder does not match PR author"**
Your answer subfolder name must match your GitHub login exactly (case-sensitive). Rename the folder to match.

**CI fails with "expected N response block(s)"**
The number of `#RESPONSE`/`#END` blocks in your log must equal the number of non-comment lines in `requests.txt`. Re-run your system against the full testcase.

## Traditional Chinese

[中文說明請見 README.zh-TW.md](README.zh-TW.md)
