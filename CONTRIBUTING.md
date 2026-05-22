# Contributing

This repo has two contribution tracks. Read the one that matches your goal.

---

## Track 1 — Submit your system's output for official testcases

This is the primary use case. You run your ICCAD 2026 system against the 40 official Cadence testcases, then submit the captured output so the class can cross-reference results.

### Prerequisites

- A GitHub account.
- Your ICCAD 2026 system ready to run (`$BENCH_SYSTEM_CMD`).
- Basic familiarity with git and GitHub.

### Step 1: Fork and clone

1. Click **Fork** on the top-right of this repo's GitHub page.
2. Clone your fork locally:

   ```bash
   git clone https://github.com/<your-github-username>/ICCAD2026_Problem-A_Benchmark.git
   cd ICCAD2026_Problem-A_Benchmark
   ```

### Step 2: Create a branch

```bash
git checkout -b submission/<your-github-username>
```

### Step 3: Run the benchmark runner

```bash
export BENCH_SYSTEM_CMD="./your_system --config llm_config.yaml"

# Run a single testcase
python3 runner/run_bench.py --source official --cases test01

# Or run all 40 official testcases
python3 runner/run_bench.py --source official
```

The runner writes output to `results/run_<timestamp>/testNN/system.log`.  
The `results/` folder is gitignored — it stays on your machine only.

### Step 4: Copy the log into your submission folder

```bash
# Replace test01 and <your-github-username> with the actual values
CASE=test01
USER=<your-github-username>
RUN_DIR=$(ls -dt results/run_*/ | head -1)   # latest run

mkdir -p official_testcase/${CASE}/${USER}

cp ${RUN_DIR}/${CASE}/system.log \
   official_testcase/${CASE}/${USER}/${CASE}.log
```

Optionally add metadata:

```bash
cat > official_testcase/${CASE}/${USER}/submission.yaml << 'EOF'
system_name: cada0001_alpha
version: v0.3.2
commit_hash: abcdef0
run_timestamp: 2026-05-25T14:30:00+08:00
notes: |
  Optional free-form notes about this run.
EOF
```

You may also include output Verilog files (any filename, any `*.v`) if your system produced them — these are optional and not validated by CI.

### Step 5: Commit and push

```bash
git add official_testcase/${CASE}/${USER}/
git commit -m "submission: ${USER} ${CASE}"
git push origin submission/${USER}
```

### Step 6: Open a pull request

1. Go to your fork on GitHub.
2. Click **Compare & pull request**.
3. Fill in the PR template checklist and submit.

A CI check will automatically validate your submission format. Fix any reported errors before requesting a review.

### Submission rules (enforced by CI)

| Rule | Detail |
|------|--------|
| Folder name | Must equal your GitHub login exactly (case-sensitive). |
| Required file | `official_testcase/testNN/<your-username>/testNN.log` |
| Log format | `#RESPONSE N` / `#END N` blocks, IDs 1, 2, …, K; K = number of prompts in `requests.txt`. |
| Optional files | Any `*.v` file (any name); `submission.yaml`. CI does not validate their contents. |
| Immutable files | Do not modify `testNN.v`, `requests.txt`, `README.md`, or `meta.yaml` inside any `official_testcase/testNN/`. CI will reject the PR. |

---

## Track 2 — Add a community testcase to `tests/`

If you want to contribute a new testcase design and question set for others to use:

### Layout

Each testcase lives in `tests/case_<unique_name>/` with exactly four files:

```
tests/case_<unique_name>/
├── design.v          # gate-level Verilog (REQUIRED)
├── requests.txt      # NL requests, one per line (REQUIRED)
├── golden.log        # reference responses (REQUIRED)
└── README.md         # design description + question intent (REQUIRED)
```

### `design.v` requirements

- Single top module per file (no hierarchy).
- Primitive gates only: `and`, `or`, `not`, `nand`, `nor`, `xor`, `xnor`, `buf`, `dff`.
- 2-input gates except `buf` / `not` (1 input).
- DFF positional ports: `dff inst (q, d, clk, rst_n)`.
- Must be parseable by [pyverilog](https://github.com/PyHDI/Pyverilog).

### `requests.txt` requirements

One natural-language request per line. Lines starting with `#` are treated as comments and skipped.

**The first line must be:**

```
This is the beginning of testcase <case_name>. Please output a copy of the log into <case_name>.log.
```

### `golden.log` format

```
#RESPONSE 1
<reference answer for prompt 1>
#END 1
#RESPONSE 2
<reference answer for prompt 2>
#END 2
```

- IDs start at 1, monotonically increasing.
- Count of `#RESPONSE` blocks must match the non-comment line count in `requests.txt`.

### PR process

1. Fork → branch → add `tests/case_<name>/` with all 4 files.
2. Open a PR. A maintainer will review the golden answers for correctness.
3. On merge, the testcase becomes part of the public benchmark.

### What makes a good community testcase?

- At least one non-trivial query (path traversal, cone analysis, clock domain check).
- Adversarial twists encouraged: dangling gates, constant outputs, multiple clock domains.
- Avoid designs larger than ~1000 gates unless scale itself is the test.
- Every golden answer must be justifiable step-by-step.

## License

By contributing, you agree your submission is published under the repo's MIT license.
