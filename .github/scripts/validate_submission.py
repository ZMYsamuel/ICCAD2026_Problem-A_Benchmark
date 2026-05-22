#!/usr/bin/env python3
"""CI validator for official testcase submissions.

Reads PR_AUTHOR and BASE_SHA from the environment (set by the GitHub Actions
workflow), then checks every changed file against the submission rules:

  1. All changed paths must be under official_testcase/.
  2. Maintainer-owned files (testNN.v, requests.txt, README.md, meta.yaml)
     cannot be modified.
  3. Every other changed path must be inside a folder whose name matches the
     PR author's GitHub login.
  4. For each (testNN, user) pair touched by the PR, testNN.log must exist
     and contain correctly paired #RESPONSE N / #END N blocks whose count
     equals the number of prompts in requests.txt.

Exit 0 on success, 1 on the first failure.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

MAINTAINER_FILES = {"requests.txt", "README.md", "meta.yaml"}

RESPONSE_RE = re.compile(r"^#RESPONSE\s+(\d+)\s*$", re.MULTILINE)
END_RE      = re.compile(r"^#END\s+(\d+)\s*$",      re.MULTILINE)


def get_changed_files(base_sha: str) -> List[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "{}...HEAD".format(base_sha)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True, check=True, cwd=str(REPO_ROOT),
    )
    return [f for f in result.stdout.splitlines() if f.strip()]


def count_prompts(requests_txt: Path) -> int:
    count = 0
    for line in requests_txt.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            count += 1
    return count


def validate_log(log_path: Path, expected_count: int) -> Optional[str]:
    """Return an error string, or None if the log is valid."""
    text = log_path.read_text(encoding="utf-8")

    response_ids = [int(m) for m in RESPONSE_RE.findall(text)]
    end_ids      = [int(m) for m in END_RE.findall(text)]

    if response_ids != end_ids:
        return (f"mismatched #RESPONSE / #END markers: "
                f"RESPONSE ids={response_ids}, END ids={end_ids}")

    expected_ids = list(range(1, expected_count + 1))
    if response_ids != expected_ids:
        return (f"expected {expected_count} response block(s) with ids {expected_ids}, "
                f"got {response_ids}")

    return None


def main() -> int:
    pr_author = os.environ.get("PR_AUTHOR", "").strip()
    base_sha  = os.environ.get("BASE_SHA", "").strip()

    if not pr_author:
        print("ERROR: PR_AUTHOR environment variable is not set.")
        return 1
    if not base_sha:
        print("ERROR: BASE_SHA environment variable is not set.")
        return 1

    try:
        changed_files = get_changed_files(base_sha)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: git diff failed: {e.stderr}")
        return 1

    if not changed_files:
        print("OK: no changed files in official_testcase/ — nothing to validate.")
        return 0

    # (testNN, user) pairs we need to fully validate
    submission_pairs = set()  # type: Set[Tuple[str, str]]

    for path_str in changed_files:
        # Rule 1: must be inside official_testcase/
        if not path_str.startswith("official_testcase/"):
            print(f"ERROR: submission PR touched non-submission path: {path_str}")
            return 1

        parts = path_str.split("/")
        # parts[0]="official_testcase", parts[1]=testNN, parts[2]=user_or_maintainer_file, ...
        if len(parts) < 3:
            print(f"ERROR: unexpected path (too shallow): {path_str}")
            return 1

        testnn   = parts[1]
        sub_name = parts[2]  # either a maintainer file or the user folder name

        # Rule 2: maintainer-owned files at official_testcase/testNN/<file>
        if len(parts) == 3:
            # Direct child of testNN/ — might be a maintainer file
            filename = parts[2]
            if filename in MAINTAINER_FILES or filename == f"{testnn}.v":
                print(f"ERROR: cannot modify maintainer-owned file: {path_str}")
                return 1
            # If it's neither a maintainer file nor a directory entry, it's unexpected.
            # We still fall through to the user-folder check below.

        # Rule 3: the second-level folder must equal PR_AUTHOR
        user_folder = sub_name
        if user_folder != pr_author:
            print(f"ERROR: submission folder '{user_folder}' does not match "
                  f"PR author '{pr_author}'")
            return 1

        submission_pairs.add((testnn, pr_author))

    # Rule 4: validate each (testNN, user) pair
    for testnn, user in sorted(submission_pairs):
        log_path      = REPO_ROOT / "official_testcase" / testnn / user / f"{testnn}.log"
        requests_path = REPO_ROOT / "official_testcase" / testnn / "requests.txt"

        if not log_path.exists():
            print(f"ERROR: required log file missing: "
                  f"official_testcase/{testnn}/{user}/{testnn}.log")
            return 1

        if not requests_path.exists():
            print(f"ERROR: requests.txt not found for {testnn} — "
                  f"is the testcase correctly installed?")
            return 1

        expected_count = count_prompts(requests_path)
        err = validate_log(log_path, expected_count)
        if err:
            print(f"ERROR: {testnn}/{user}/{testnn}.log — {err}")
            return 1

    n_files = len(changed_files)
    n_pairs = len(submission_pairs)
    print(f"OK: validated {n_files} file(s) across {n_pairs} testcase/user pair(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
