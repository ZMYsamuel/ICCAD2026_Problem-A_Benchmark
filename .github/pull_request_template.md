<!-- See CONTRIBUTING.md for full instructions on both contribution types. -->

## What type of contribution is this?

- [ ] Official testcase submission (Track 1)
- [ ] Community testcase contribution (Track 2)

---

## Track 1 — Official testcase submission

- [ ] My submission folder is named exactly after my GitHub username.
- [ ] The required `official_testcase/testNN/<username>/testNN.log` file is present.
- [ ] I have not modified any maintainer-owned files (`testNN.v`, `requests.txt`, `README.md`, `meta.yaml`).
- [ ] I ran the system locally and confirmed it produced output before submitting.

**Testcase(s) submitted:** <!-- e.g. test01, test02, test05 -->

---

## Track 2 — Community testcase contribution

- [ ] Created `tests/case_<name>/design.v`, `requests.txt`, `golden.log`, and `README.md`.
- [ ] `requests.txt` first line follows the format: `This is the beginning of testcase <case_name>. Please output a copy of the log into <case_name>.log.`
- [ ] Number of `#RESPONSE` blocks in `golden.log` equals the number of non-comment lines in `requests.txt`.
- [ ] Each `#RESPONSE N` has a matching `#END N`.
- [ ] `design.v` is flat (single top module), uses primitive gates only, parseable by pyverilog.
- [ ] I can justify every golden answer.
- [ ] No closed-source IP, copyrighted designs, or NDA-protected material.

---

## Notes

<!-- Anything the reviewer should know — design quirks, submission issues, etc. -->
