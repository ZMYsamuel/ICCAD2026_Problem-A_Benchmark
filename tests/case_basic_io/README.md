# case_basic_io — Minimum-viable basic-ops smoke test

## Design

Single 2-input AND gate. Module: `simple_and`. No internal nets, no DFF, no transformation needed.

```
a ─┐
   ├─[AND U1]─ y
b ─┘
```

## Questions

3 questions, all from contest §4.1 (Basic Operations):
1. Testcase initialization.
2. Design read.
3. Design write-out.

This is the absolute minimum a contest-conformant system must handle. If a system fails this case, it cannot run any other testcase.

## Notes for reviewers

- The expected `simple_and` module name comes from the Verilog source — the system must report it correctly in the load response.
- Write path uses `/tmp/...` to avoid polluting the repo.

## Contributor

Maintainer (bootstrap).
