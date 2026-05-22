# Contributing

There are three things you can contribute to this repo. The mechanics are the same for all three — fork, branch, push, PR. Only the file you add changes.

| What you want to do | Where the files go |
|---|---|
| Submit your system's answer to an **official** testcase | `official_testcase/testNN/<your-github-username>/` |
| Submit your system's answer to a **community** testcase | `tests/<case_folder>/<your-github-username>/` |
| Add a new community testcase | `tests/<case_folder>/` (directly) |

You can mix any of these in a single PR. Each one is independent — uploading a testcase doesn't require uploading an answer at the same time, and vice versa.

---

## Folder rules

### Official testcase folder — `official_testcase/testNN/`

Maintainer-owned. The netlist, `requests.txt`, `meta.yaml`, and `README.md` are locked. Submitters only add their own answer subfolder.

### Community testcase folder — `tests/<case_folder>/`

Anyone can create, anyone can edit. The folder must contain:

- At least one `*.v` netlist file (any filename).
- `requests.txt` — first line must declare the case_name, matching the folder name:
  ```
  This is the beginning of testcase <case_name>. Please output a copy of the log into <case_name>.log.
  ```
  `<case_name>` must equal the folder name. You may optionally use a `case_` prefix on the folder (e.g. folder `case_foo/` with `case_name` either `case_foo` or `foo`).
- `README.md` — optional.

### Answer subfolder — `<root>/<case>/<your-github-username>/`

- The folder name must equal your GitHub username, exactly. CI uses the PR author's GitHub login as the source of truth.
- Required file: `<case_name>.log` — your system's captured output, formatted as `#RESPONSE N` / `#END N` blocks.
- Optional: any output `*.v` files, any `submission.yaml` for run metadata.

`<case_name>` is whatever's declared in the parent folder's `requests.txt` first line — for `official_testcase/test01/` it's `test01`, for `tests/case_demo01/` it's `demo01`.

---

## Full workflow

### Step 1 — Fork and clone

Fork this repo via the GitHub UI, then:

```bash
git clone https://github.com/<your-github-username>/ICCAD2026_Problem-A_Benchmark.git
cd ICCAD2026_Problem-A_Benchmark
git checkout -b submission/<your-github-username>
```

### Step 2 — Produce your output

For an answer submission, run the benchmark runner against your system:

```bash
export BENCH_SYSTEM_CMD="./your_system --config llm_config.yaml"

# One testcase
python3 runner/run_bench.py --source official --cases test01

# All official testcases
python3 runner/run_bench.py --source official

# A community testcase
python3 runner/run_bench.py --source community --cases case_demo01
```

The runner writes output to `results/run_<timestamp>/<case>/system.log`. The `results/` folder stays on your machine — it's gitignored.

For a new testcase contribution, just author the files directly.

### Step 3 — Place the files

```bash
# Answer submission (official example)
CASE=test01
USER=<your-github-username>
RUN_DIR=$(ls -dt results/run_*/ | head -1)

mkdir -p official_testcase/${CASE}/${USER}
cp ${RUN_DIR}/${CASE}/system.log \
   official_testcase/${CASE}/${USER}/${CASE}.log
```

For a community answer, swap the root to `tests/` and use the community case folder name.

For a new community testcase, create `tests/<case_folder>/` directly with your `.v` and `requests.txt`.

Optionally add `submission.yaml` to your answer folder to record run metadata:

```yaml
system_name: cada0001_alpha
version: v0.3.2
commit_hash: abcdef0
run_timestamp: 2026-05-25T14:30:00+08:00
notes: |
  Optional free-form notes about this run.
```

### Step 4 — Commit and push

```bash
git add <the-files-you-added>
git commit -m "submission: <your-github-username> test01"
git push origin submission/<your-github-username>
```

### Step 5 — Open a pull request

On your fork's GitHub page, click **Compare & pull request**. Fill in the PR template and submit.

### Step 6 — If CI fails

CI runs a structural check on your PR (folder names, required files, log format). It's not a correctness gate.

If the check fails, read the error message and try to fix it locally. Most failures are simple:

- Folder name doesn't match your GitHub login → rename.
- Log block IDs don't match prompt count → re-run the system.
- `requests.txt` case_name doesn't match folder name → fix the first line.

If you've tried and the error looks like a benchmark-side issue (a maintainer file CI flags that you didn't touch, an env problem, something that doesn't reproduce locally), ping `@ZMYsamuel` in the PR comments.

---

## License

By contributing, you agree your submission is published under the repo's MIT license.
