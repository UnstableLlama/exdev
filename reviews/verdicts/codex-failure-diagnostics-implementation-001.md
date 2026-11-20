# Verdict: codex-failure-diagnostics-implementation-001

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (08:19 UTC). Patch: `reports/codex-failure-diagnostics-implementation-001.patch`. Context: stopped runs
`.teacher/runs/commit-000336-001` and `.teacher/runs/commit-000336-002`.

## Decision

**The patch passes review. Do not apply it yet.** Applying it and a third 336 attempt both wait for the user's answer,
which I have asked for. I will send you that answer. Until then the queue stays stopped and the live tree stays as it is.

## What I checked myself

- Five bound files match their hashes. `git apply --check` passes against the live tree.
- Whole production diff read. It touches `.gitignore`, `teacher/author.py`, `teacher/codex_transport.py` and the new
  `teacher/codex_diagnostics.py`. The adapter, prompts, packet code, model and success path are not changed, so teacher
  input cannot change. The original exception still propagates, and `__exit__` still does not suppress it.
- I applied the patch to a separate copy and ran the suite: 353 tests, OK, 13 skipped there because I left out the data
  directories. The four new tests pass.
- Capture order is right: the child exits, then stderr and the sandbox auth copy are read, then the temporary state is
  removed. The file is created with mode 0600 and replaced atomically, and `.gitignore` keeps it out of the tracked run
  directories. No code enumerates run directories in a way the new file would disturb.
- I probed the redactor with a synthetic login of the usual shape (API key, JWT id token, opaque access token, plain
  refresh token). Raw, URL-encoded and JSON forms, bearer and cookie headers, `sk-` keys and URL userinfo were all removed.
  Ordinary causes stayed readable: HTTP status text, usage-limit wording, unsupported-model wording, request ids,
  `willRetry` and `httpStatusCode`. I did not open the real auth file.

## Notes (none blocks)

- After this lands, `check.py` will report `impl 47`, not 46, because `teacher/*.py` gains a file; older runs will show
  the three changed Python files as differing from their recorded hashes. That is expected.
- `_collect_failure` catches `Exception` only, so an interrupt during capture would skip the explicit temporary cleanup
  and leave it to the finaliser.
- Headers can come out as `[REDACTED]]`. A message such as "Invalid token: expired" loses its last word. Both are harmless.
