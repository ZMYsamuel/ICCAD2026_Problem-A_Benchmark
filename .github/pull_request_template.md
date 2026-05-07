<!-- Thanks for adding to the benchmark! Please complete the checklist below. -->

## Testcase summary

- **Path:** `tests/case_<name>/`
- **What this testcase exercises:** <e.g. multi-clock-domain DFFs, deep XOR chain depth query, redundant-gate optimization>
- **Contributor:** <your name / handle>

## Checklist (please tick all)

- [ ] Created `tests/case_<name>/design.v`, `requests.txt`, `golden.log`, and `README.md`.
- [ ] `requests.txt` first line follows the contest spec format: `This is the beginning of testcase <case_name>. Please output a copy of the log into <case_name>.log.`
- [ ] Number of `#RESPONSE` blocks in `golden.log` equals the number of (non-comment) lines in `requests.txt`.
- [ ] Each `#RESPONSE` has a matching `#END` with the same id.
- [ ] `design.v` is flat (single top module), uses primitive gates only, parseable by pyverilog.
- [ ] I can justify every golden answer (numerical answers come with a derivation in `README.md`).
- [ ] No closed-source IP, no copyrighted designs, no NDA-protected material.

## Optional notes

<anything else the reviewer should know — design quirks, why a particular phrasing was chosen for a question, etc.>
