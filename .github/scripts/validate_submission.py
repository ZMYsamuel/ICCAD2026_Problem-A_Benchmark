#!/usr/bin/env python3
"""CI validator for benchmark contributions.

Reads PR_AUTHOR and BASE_SHA from the environment (set by the GitHub Actions
workflow), classifies each changed file by path, then dispatches to the right
validation flow:

  official_testcase/<case>/<file>          -> reject (maintainer-owned, immutable)
  official_testcase/<case>/<user>/<file>  -> answer validation
  community_testcase/<case>/<file>        -> community testcase folder validation
  community_testcase/<case>/<user>/<file> -> answer validation
  anything else                           -> reject

Answer validation checks: folder name == PR_AUTHOR, <case_name>.log exists,
and #RESPONSE N / #END N blocks pair up with ids 1..K, where K equals the
non-comment line count of requests.txt.

Testcase folder validation checks: requests.txt exists and at least one .v
file is present. We do not parse requests.txt content — official and community
testcases use different phrasings.

The expected log filename equals the folder name: `official_testcase/test01/` ->
test01.log, `community_testcase/demo01/` -> demo01.log.

Exit 0 on success, 1 on the first failure.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

OFFICIAL_ROOT  = "official_testcase"
COMMUNITY_ROOT = "community_testcase"

RESPONSE_RE = re.compile(r"^#RESPONSE\s+(\d+)\s*$", re.MULTILINE)
END_RE      = re.compile(r"^#END\s+(\d+)\s*$",      re.MULTILINE)


def get_changed_files(base_sha):
    # type: (str) -> List[str]
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "{}...HEAD".format(base_sha)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True, check=True, cwd=str(REPO_ROOT),
    )
    return [f for f in result.stdout.splitlines() if f.strip()]


def count_prompts(requests_txt):
    # type: (Path) -> int
    count = 0
    for line in requests_txt.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            count += 1
    return count


def derive_log_name(case_folder):
    # type: (str) -> str
    """community_testcase/demo01/ -> demo01.log; official_testcase/test01/ -> test01.log."""
    return case_folder + ".log"


def validate_log(log_path, expected_count):
    # type: (Path, int) -> Optional[str]
    """Return an error string, or None if the log is valid."""
    text = log_path.read_text(encoding="utf-8")

    response_ids = [int(m) for m in RESPONSE_RE.findall(text)]
    end_ids      = [int(m) for m in END_RE.findall(text)]

    if response_ids != end_ids:
        return ("mismatched #RESPONSE / #END markers: "
                "RESPONSE ids={}, END ids={}".format(response_ids, end_ids))

    expected_ids = list(range(1, expected_count + 1))
    if response_ids != expected_ids:
        return ("expected {} response block(s) with ids {}, "
                "got {}".format(expected_count, expected_ids, response_ids))

    return None


def validate_answer(root, case, user):
    # type: (str, str, str) -> Optional[str]
    """Validate that <root>/<case>/<user>/<log_name> exists and is well-formed."""
    requests_path = REPO_ROOT / root / case / "requests.txt"
    if not requests_path.exists():
        return ("requests.txt not found for {}/{} — is the testcase installed?"
                .format(root, case))

    log_name = derive_log_name(case)
    log_path = REPO_ROOT / root / case / user / log_name
    if not log_path.exists():
        return ("required log file missing: {}/{}/{}/{}"
                .format(root, case, user, log_name))

    return validate_log(log_path, count_prompts(requests_path))


def validate_testcase_folder(root, case):
    # type: (str, str) -> Optional[str]
    """Validate that <root>/<case>/ contains requests.txt and at least one .v."""
    case_dir = REPO_ROOT / root / case
    if not (case_dir / "requests.txt").exists():
        return "testcase folder {}/{} missing requests.txt".format(root, case)

    v_files = [p for p in case_dir.iterdir() if p.is_file() and p.suffix == ".v"]
    if not v_files:
        return "testcase folder {}/{} contains no .v netlist file".format(root, case)

    return None


def main():
    # type: () -> int
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
        print("ERROR: git diff failed: {}".format(e.stderr))
        return 1

    if not changed_files:
        print("OK: no changed files to validate.")
        return 0

    answer_pairs   = set()  # type: Set[Tuple[str, str, str]]   # (root, case, user)
    testcase_pairs = set()  # type: Set[Tuple[str, str]]        # (root, case)

    for path_str in changed_files:
        parts = path_str.split("/")
        if len(parts) < 3 or parts[0] not in (OFFICIAL_ROOT, COMMUNITY_ROOT):
            print("ERROR: PR touched non-submission path: {}".format(path_str))
            return 1

        root = parts[0]
        case = parts[1]

        # Path depth tells us if this is a maintainer-level file or in a user folder.
        # depth == 3: official_testcase/<case>/<file>     OR  community_testcase/<case>/<file>
        # depth >= 4: official_testcase/<case>/<user>/... OR  community_testcase/<case>/<user>/...
        if len(parts) == 3:
            if root == OFFICIAL_ROOT:
                print("ERROR: cannot modify maintainer-owned file in official_testcase: {}"
                      .format(path_str))
                return 1
            # Community testcase folder — anyone may add/edit
            testcase_pairs.add((root, case))
        else:
            user_folder = parts[2]
            if user_folder != pr_author:
                print("ERROR: submission folder '{}' does not match "
                      "PR author '{}' (path: {})"
                      .format(user_folder, pr_author, path_str))
                return 1
            answer_pairs.add((root, case, pr_author))

    # Validate community testcase folders first (an answer to a malformed testcase
    # would fail later anyway, but the folder error is more informative).
    for root, case in sorted(testcase_pairs):
        err = validate_testcase_folder(root, case)
        if err:
            print("ERROR: {}".format(err))
            return 1

    for root, case, user in sorted(answer_pairs):
        err = validate_answer(root, case, user)
        if err:
            print("ERROR: {}".format(err))
            return 1

    n_files     = len(changed_files)
    n_answers   = len(answer_pairs)
    n_testcases = len(testcase_pairs)
    print("OK: validated {} file(s) — {} answer pair(s), {} testcase folder(s)."
          .format(n_files, n_answers, n_testcases))
    return 0


if __name__ == "__main__":
    sys.exit(main())
