# Token-cost detached cycle 001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

161's request was filed before this work. No 162 or other teacher run started. Advancement is paused for this implementation review, independently of the pending 161 verdict.

## Result and blocker

Part E wrapper is implemented as `teacher.cycle_notify`, but **automatic wake-up is not verified and live detached use is not recommended yet**. An escalated `setsid -f` smoke run against a deliberately paused dummy journal completed, saved its result/log, and queued a message to this thread. `codex queue --resume` returned zero with a warning: it could not resume this thread without a local daemon or a specified remote server. The wrapper treats that warning as notification failure and saved `reports/cycle-notify-failed-162.txt`. No daemon or configuration was changed. Keep the current launch method until a working wake-up route is provided and tested.

The earlier `nohup … &` probe left a successful child-cycle log but no supervisor result or notification; the cause was not established. `setsid -f` did complete the supervisor. Both probes used only the paused test journal: `advancement_paused`, no teacher.

## Implementation

The wrapper invokes the unchanged `teacher.cycle` in a child process, writing combined output to a unique report log. It saves a compact JSON result and queues exactly one status/result/summary notification in `finally`. It handles successful handoff, named stops, child nonzero exit, parse/startup errors, and SIGINT/SIGTERM. Termination forwards to the child process group, waits, then kills if necessary. Queue failure, timeout, or a resume warning appends the required position-specific failure report. Existing cycle locks, review gates and teacher inputs are untouched; notification text explicitly grants no permission to bypass a stop.

SIGKILL, machine loss and an unwritable report filesystem cannot be guaranteed to notify; `finally` cannot cover those. This is a limitation, not a claim of crash-proof delivery.

## Validation

277 host-enabled tests pass, including six new tests covering success, named stop, child failure, malformed output, missing state, exact queue arguments, queue failure/timeout/resume warning, and interruption cleanup. The live smoke verified the failure path from an escalated detached command, exposing the environment limitation above. No teacher-facing module was edited. No packet rebuild is needed for this wrapper-only change; the accepted driver is invoked unchanged. Live use remains pending this verdict.

## SHA256

- teacher/cycle_notify.py: `ebde20c16b356b7c246cde49c2421ed537e032e24bd872b489e18a265162bf24`
- tests/test_cycle_notify.py: `4ae19908375ea8a48e5dc796b70833fa0eb061f46de15cd48ba6203db62b26fb`
- reports/token-cost-detach-tests-001.txt: `b97426591d047ca1134586e327dcc8ca644897cf0dd19ee3d526e40aa3cc9ed4`
- reports/token-cost-detach-smoke-state-001.json: `7d9407c76d66dad652f7ace83654c35e3d510c7a8409da1cf5744f7261668142`
- reports/token-cost-detach-smoke-launch-001.log: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- reports/token-cost-detach-smoke-launch-002.log: `b8d3768262e230555f8567d8471d5fecddd4578647022a6a168c44df26e0382e`
- reports/cycle-notify-failed-162.txt: `fe1f2969f6295b338a8b83796d86fdf4017772d74b36689c5608c656f80d8da1`
- reports/cycle-detached-000162-1938ab4bbd1248b28fd8b628795c5a6e.json: `516bd3da13f93561319cac76861503df6c6cf618f889b60748f23e52929a5494`
- reports/cycle-detached-000162-1938ab4bbd1248b28fd8b628795c5a6e.log: `d730650438e2c1d5804a3e624747d94adb98f1435ca82dbd70371ef77dc0b8c2`
- reports/token-cost-detach-001.json: `98a5d359bf7a2fde71e269f5048e01be0533afda65d3e1f0415ea7346c99c1be`
- reports/token-cost-detach-001.patch: `3ce75ecb9422c89d14f2772dbfb413530a5d73206f22bdf8864a76616117dd4f`
- reviews/fable/TOKEN-COST-PROPOSAL.md: `908b111417ddaa66c702ca4ef9606326cbd21261841956d1c7d0618c71b330fb`

Reply in `reviews/verdicts/token-cost-detach-001.md`.

## Administrative addendum after the 161 verdict

161 is now approved for ancestor retrieval only; part E pause remains before 162. Padding-target r003 is accepted, with the fix at 161 reviewer-confirmed by source inspection (no execution). As requested, this handoff also files `reports/defect-ledger/exllamav3-model-diff-unconditional-deferral--r003.json`: still suspected, reviewer_observation, excluded from teacher input. It adds 161 as affected: removing the padding mask exposes model_diff.py copying unread deferred weights for sliced unquantized MLPs. No continuous range or runtime verification claimed. All evidence hashes verified; the known validator limitation for reviewer_observation remains.

- reports/defect-ledger/exllamav3-model-diff-unconditional-deferral--r003.json: `4b2641d9664472d242197ad629f95d52192923e7e7a3e4dbe459ffb88c15b556`
- reports/defect-ledger/evidence/commit161-verdict.md: `d3d32cc7497a4783600c93a15f1d416965998611ebae07521dda5ca8654e9b05`

## Smoke notification delivery follow-up

The queued smoke-test notification was subsequently delivered to this thread. Its saved result is advancement_paused and the live journal still has no 162 run. Eventual message delivery is observed; automatic resume remains unproven because the queue command reported a resume failure. This does not clear the part E pause.
