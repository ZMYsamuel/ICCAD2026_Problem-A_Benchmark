# ICCAD 2026 Problem A — Benchmark

A community submission archive for **ICCAD 2026 Problem A: LLM-Assisted Netlist Exploration and Transformation**.

Each participant runs the 40 official Cadence testcases through their own system, then submits the captured output here. By comparing submissions side-by-side, the class can cross-reference answers and reason about correctness without a single golden oracle.

## Repository structure

```
ICCAD2026_Problem-A_Benchmark/
├── official_testcase/          # 40 official Cadence testcases (public)
│   └── testNN/
│       ├── testNN.v            # gate-level Verilog netlist
│       ├── requests.txt        # official prompts (one per line)
│       ├── meta.yaml           # task_type + expected.kind metadata
│       ├── README.md           # testcase brief
│       └── <github-username>/ # your submission folder
│           ├── testNN.log      # REQUIRED — system output
│           ├── *.v             # OPTIONAL — output Verilog
│           └── submission.yaml # OPTIONAL — run metadata
├── tests/                      # community-contributed testcases
├── runner/run_bench.py         # submission runner
├── .github/
│   ├── scripts/validate_submission.py
│   └── workflows/submission-validate.yml
├── CONTRIBUTING.md
└── LICENSE
```

## Quickstart — run the benchmark locally

```bash
# 1. Set your system command
export BENCH_SYSTEM_CMD="./your_system --config llm_config.yaml"

# 2. Run the runner against one or all official testcases
python3 runner/run_bench.py --source official --cases test01
# Output goes to: results/run_<timestamp>/test01/system.log
# (results/ is gitignored — it never gets pushed)

# 3. Copy the log into your submission folder and open a PR
#    See CONTRIBUTING.md for the full workflow.
```

The runner reads `official_testcase/testNN/meta.yaml` to set up the correct working directory, then invokes `$BENCH_SYSTEM_CMD` with each prompt from `requests.txt` in sequence.

## Submitting your results

See [CONTRIBUTING.md](CONTRIBUTING.md) for step-by-step instructions, including how to fork this repo and open a pull request.

A GitHub Actions CI check validates the submission format automatically when you open a PR.

## Traditional Chinese

[中文說明請見 README.zh-TW.md](README.zh-TW.md)
