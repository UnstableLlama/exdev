# 256 approval: exact run identifier needed in verdict

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

The accepted recovery bindings are applied; original bindings are retained in the recovery report. Ordinary queue approval now passes the historical-state and implementation checks, but refuses the unchanged 256 verdict with `Verdict must identify run and decision`. Its existing check requires the literal `.teacher/runs/commit-000256-001` in the verdict, which currently identifies the run only by its title. Please add the exact run path to reviews/verdicts/commit-000256-001.md. No decision change or gate change is requested.

No approval was recorded and the dependency-gap pause remains. No teacher started. After the verdict identifier is added I will rerun ordinary approval, clear the authorised pause, and launch257. No commit/push.

The257 request will name this recovery report, explain the255 manual selection omission and queue transaction, and include the256 serialization fix ledger revision.

Bindings:

- reviews/verdicts/commit-000256-001.md: `53aa4adca50b5cbb0917574c9da515fda8d9bf4bac4dc6888224fe5fe240c1db`
- reviews/verdicts/run-ahead-legacy-status-implementation-001.md: `c8a29b002023ae86bb273970be5cfc9ff35f3110328f3c983f0c02062e41f1fe`
- reports/run-ahead-legacy-status-001/recovery.json: `3907ffb165549b2e17a356bc90333da1c932e6b0948069be34ee5a7073b55567`
- reports/run-ahead-legacy-status-001/commit-000256-001.recovery-request.md: `1049c0ebe2760ed08b85734fce5ed10d06db10854c1b393b46bc226ac7769c88`
- orchestration/run_ahead.py: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
