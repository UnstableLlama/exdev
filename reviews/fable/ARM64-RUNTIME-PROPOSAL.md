# Proposal: run the teacher sandbox on Linux arm64

From Fable, 2026-11-14. For Astra and the user. Not a verdict and not teacher input.

## Why

The user moved the walk to an Apple Silicon laptop; the original Linux amd64 machine is busy. macOS has no Bubblewrap.
An x86-64 Linux VM under Rosetta passes 216 of 223 tests: the seven `run` tests fail because the kernel is arm64 and
refuses an x86-64 seccomp filter (`seccomp_load` returns EINVAL). The user chose a native arm64 Linux VM
(OrbStack machine `exdev-arm`, Ubuntu 24.04, Python 3.12.3, bubblewrap 0.9.0, Codex 0.167.0 aarch64 musl).

## What I tried, on a throwaway copy only (`~/scratch/exdev-armtrial`)

`arm64-runtime-trial.patch` in this directory, 14 lines over three files:

- `teacher/runner.py`: choose the multiarch library directory and loader by `platform.machine()` (x86_64 unchanged).
- `teacher/codex_transport.py`: also bind `/usr/lib/aarch64-linux-gnu` when it exists.
- `teacher/worker.py`: `fork` and `vfork` are not syscalls on aarch64; skip those two names when the resolver says so.
  `clone`, `clone3`, `unshare`, `setns` and `ptrace` are still required and still denied.

Results with the patch on arm64:

- `EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests`: 223 tests, OK, 8.3 s.
- Graph tools (`repo_map`, `graph_search`) on packet 000074-001 run in the sandbox. The pinned graph backend is still
  the x86-64 static binary with the same checksum; it runs through Rosetta.
- Replaying 74/001`s `run` call returns byte-for-byte the recorded stdout.
- `reviews/fable/check.py 000074 001` on the untouched checkout reproduces every hash in the 74/001 verdict.

## What is not done

- The working checkout `~/git/exdev` is unpatched. Astra owns this code: implement it (this diff or its own) and file an
  implementation request as usual.
- I wrote the trial, so my review of the same diff is not independent. The boundary tests are the check; the user
  should know that.
- `teacher/audit_boundary.py` still reports the runtime as "Linux amd64 Bubblewrap", and provenance does not record the
  machine architecture. Runs from 75 on should say arm64 so they can be told apart from 2-74.
- No live teacher run has been made on arm64. Codex and gh are not signed in on this machine yet.
- The graph backend depends on Rosetta being available in the VM. If it is not, graph tools fail closed.
