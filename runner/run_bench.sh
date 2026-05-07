#!/bin/bash
# Feed a testcase's requests.txt into a system, capture stdout, save to results/.
#
# Usage:
#   ./run_bench.sh <system_executable> <testcase_dir>
#   ./run_bench.sh <system_executable> --all   # iterate every tests/case_*/
#
# Output:
#   results/<case_name>.log    — system's actual stdout (in #RESPONSE/#END format)
#   results/<case_name>.stderr — system's stderr (for debugging)

set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo "usage: $0 <system_executable> <testcase_dir | --all>" >&2
    exit 64
fi

SYSTEM="$1"
TARGET="$2"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS="$REPO_ROOT/results"
mkdir -p "$RESULTS"

if [[ ! -x "$SYSTEM" ]]; then
    echo "error: system executable not found or not executable: $SYSTEM" >&2
    exit 65
fi

run_one() {
    local case_dir="$1"
    local case_name
    case_name="$(basename "$case_dir" | sed 's/^case_//')"
    local req="$case_dir/requests.txt"

    if [[ ! -f "$req" ]]; then
        echo "skip: no requests.txt in $case_dir" >&2
        return 0
    fi

    echo "[run] $case_name"
    # Strip comment lines (#...) before piping.
    grep -v '^[[:space:]]*#' "$req" \
        | "$SYSTEM" \
              > "$RESULTS/$case_name.log" \
              2> "$RESULTS/$case_name.stderr" \
        || echo "  ! system exit non-zero (see $RESULTS/$case_name.stderr)" >&2
    echo "  -> $RESULTS/$case_name.log"
}

if [[ "$TARGET" == "--all" ]]; then
    for d in "$REPO_ROOT/tests"/case_*/; do
        [[ -d "$d" ]] || continue
        run_one "$d"
    done
else
    run_one "$TARGET"
fi

echo "[done] results in $RESULTS/"
