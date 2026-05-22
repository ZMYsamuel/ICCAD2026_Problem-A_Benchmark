# Contributing

There are three things you can contribute to this repo. The mechanics are the same for all three — fork, branch, push, PR. Only the file you add changes.

| What you want to do | Where the files go |
|---|---|
| Submit your system's answer to an **official** testcase | `official_testcase/testNN/<your-github-username>/` |
| Submit your system's answer to a **community** testcase | `community_testcase/<case_name>/<your-github-username>/` |
| Add a new community testcase | `community_testcase/<case_name>/` (directly) |

You can mix any of these in a single PR. Each one is independent — uploading a testcase doesn't require uploading an answer at the same time, and vice versa.

---

## Folder rules

### Official testcase folder — `official_testcase/testNN/`

Maintainer-owned. The netlist, `requests.txt`, `meta.yaml`, and `README.md` are locked. Submitters only add their own answer subfolder.

### Community testcase folder — `community_testcase/<case_name>/`

Anyone can create, anyone can edit. The folder must contain:

- At least one `*.v` netlist file (any filename).
- `requests.txt` — your prompts, one per line. Content is up to you (the contest spec lets prompts reference any filenames you like).
- `README.md` — optional.

Folder name is up to you. Choose a short, descriptive name (e.g. `my_dff_test`, `alu_fanout`).

### Answer subfolder — `<root>/<case>/<your-github-username>/`

- The folder name must equal your GitHub username, exactly. CI uses the PR author's GitHub login as the source of truth.
- Required file: `<case_name>.log` — your system's captured output, formatted as `#RESPONSE N` / `#END N` blocks.
- Optional: any output `*.v` files, any `submission.yaml` for run metadata.

The expected log filename equals the parent case folder name:
- `official_testcase/test01/` → `test01.log`
- `community_testcase/demo01/` → `demo01.log`

---

## Full workflow

Every step below has a **CLI form** (shown) and a **GitHub-UI form**. The commands are a convenience, not a requirement — feel free to use whichever you're more comfortable with. The only thing that matters is the final folder layout and log format.

### Step 1 — Fork and clone

Fork this repo via the GitHub UI, then either clone locally or just edit files in the browser:

```bash
git clone https://github.com/<your-github-username>/ICCAD2026_Problem-A_Benchmark.git
cd ICCAD2026_Problem-A_Benchmark
git checkout -b submission/<your-github-username>
```

### Step 2 — Produce your output _(optional)_

You can produce your `.log` any way you like — running your system manually, piping prompts through your own harness, whatever fits your setup. The only requirement is that the resulting file uses the `#RESPONSE N` / `#END N` block format and has one block per non-comment line in `requests.txt`.

If you'd like a turnkey runner, this repo ships one:

```bash
# BENCH_SYSTEM_CMD must be an absolute path — the runner executes inside a
# temporary workdir, so relative paths will not resolve.
export BENCH_SYSTEM_CMD="/absolute/path/to/your_system -config /absolute/path/to/llm_config.yaml"

# One official testcase
# Note: use python3.9 on the NTHU CAD workstation (default python3 is 3.6, too old).
python3.9 runner/run_bench.py --source official --cases test01

# All official testcases
python3.9 runner/run_bench.py --source official

# A community testcase
python3.9 runner/run_bench.py --source community --cases demo01
```

The runner writes output to `results/run_<timestamp>/<case>/system.log`. The `results/` folder stays on your machine — it's gitignored.

For a new testcase contribution, just author the files directly.

### Step 3 — Place the files

You can drag-and-drop files via the GitHub web UI (`Add file → Upload files` on your fork), or do it locally:

```bash
# Answer submission (official example)
CASE=test01
USER=<your-github-username>
RUN_DIR=$(ls -dt results/run_*/ | head -1)

mkdir -p official_testcase/${CASE}/${USER}
cp ${RUN_DIR}/${CASE}/system.log \
   official_testcase/${CASE}/${USER}/${CASE}.log
```

For a community answer, swap the root to `community_testcase/` and use the community case folder name.

For a new community testcase, create `community_testcase/<case_name>/` directly with your `.v` and `requests.txt`.

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

If you uploaded files via the browser in Step 3, GitHub already committed them for you — skip this step. Otherwise:

```bash
git add <the-files-you-added>
git commit -m "submission: <your-github-username> test01"
git push origin submission/<your-github-username>
```

### Step 5 — Open a pull request

On your fork's GitHub page, click **Compare & pull request**. Fill in the PR template and submit. (This step is GitHub-UI only — there's no CLI shortcut unless you have the `gh` CLI installed.)

### Step 6 — If CI fails

CI runs a structural check on your PR (folder names, required files, log format). It's not a correctness gate.

If the check fails, read the error message and try to fix it locally. Most failures are simple:

- Folder name doesn't match your GitHub login → rename.
- Log filename doesn't match the expected name → rename to `<case_name>.log` (must equal the case folder name, e.g. `community_testcase/demo01/` expects `demo01.log`).
- Log block IDs don't match prompt count → re-run the system.

If you've tried and the error looks like a benchmark-side issue, ping `@ZMYsamuel` in the PR comments.

---

## License

By contributing, you agree your submission is published under the repo's MIT license.
