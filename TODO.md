# TODO — Deferred Work

Items intentionally left for later. Everything here is out of scope for the current implementation.

## Submission aggregation

- **N-way diff viewer** — a per-prompt renderer that shows all submissions for a given testcase side-by-side, so the class can compare outputs and reason about correctness.
- **Submission index** — a table in README (or a separate page) listing which users have submitted which testcases, with direct links to the logs.
- **Consensus answer derivation** — given N submissions for the same prompt, automatically surface the most common response as a community-derived reference answer.

## Automation

- **Auto-comment on PR** — after CI passes, post a summary comment on the PR listing which testcases / prompts were submitted and by whom.
- **"Promote" helper script** — a convenience script that copies `results/run_<ts>/testNN/system.log` → `official_testcase/testNN/<username>/testNN.log` automatically, reducing the manual copy step.
- **Repo template** — configure the repo as a GitHub template so new submitters can fork with one click.

## Runner enhancements

- **Reproducibility N-run mode** — run each testcase N times (default 3) and report answer variance across runs, useful since LLM responses are non-deterministic.
- **Concurrency** — `--jobs N` to run N testcases in parallel for faster batch runs.
- **Per-prompt cost accounting** — surface tokens used / dollars spent per prompt in the result book when the system reports them.
