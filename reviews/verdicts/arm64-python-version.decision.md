# Decision: run the walk on Python 3.14

Recorded by Fable (reviewer) on 2026-11-14.

## The user's words

`reviews/verdicts/arm64-runtime-implementation-002.md` offered A (move to a VM whose system Python is 3.14, my
recommendation) or B (stay on 3.12.3). The amd64 machine that ran positions 2 to 74 is the user's NUC; it is at
their workplace and could not be checked. The user answered:

> ok i trust you

## What follows from it (my interpretation, not the user's words)

1. Option A. The walk continues on OrbStack machine `exdev-314`: Linux aarch64, Ubuntu 26.04, system Python 3.14.4,
   bubblewrap 0.11.1, Codex 0.167.0. I moved the working tree (uncommitted changes included), Codex state and the
   GitHub login from `exdev-arm` and removed that machine.
2. Evidence that 3.14 is the right match: replaying every recorded tool call of ten amd64 runs (70/001, 72/002,
   73/001, 74/001, 39/005, 55/002, 71/002, 69/003, 44/003, 17/003) on `exdev-314` gives 220 of 220 results
   byte-identical to the recordings, including the 55/002 `run` call that differed under 3.12.3. Full suite: 225
   passed. `graph_query` answers on packet 000074-001.
3. Not established: the NUC's exact Python patch version and its bubblewrap version. Check `/usr/bin/python3 --version`
   and `bwrap --version` there when it is next reachable and record them here.
4. `python_version` is now in run provenance and the boundary report (Astra added it after the 002 verdict).
5. With this settled, the block in the 002 verdict is lifted. Next: 39/006, then commit 75.
