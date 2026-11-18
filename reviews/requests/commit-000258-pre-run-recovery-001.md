# Recovery request: commit 258 pre-run retry

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

No teacher run or packet exists for 258. No approval is requested. Please review the recovery mechanics before another launch; 259 is also stopped administratively.

The first reservation failed in GitHub discussion-history retrieval. The standing rule in `reviews/verdicts/commit-000232-001.md` permits one pre-run fetch retry. A GitHub viewer/rate-limit probe succeeded. I invoked `orchestration.run_ahead recover --retry-position 258` against that verdict, then launched the ordinary detached cycle. That was the wrong recovery path: it sets `retry_only`, and `reserve` requires an explicit run and packet for that path. The ordinary cycle supplies neither. It failed immediately with `Only the explicitly authorized prepared retry may start`, before a new reservation, fetch, packet or teacher session. No teacher attempt has been consumed, and the actual fetch retry has not occurred.

The journal currently says ready, next_position 258, active_session null, queue_stop null, and retry_only binds position258/kindforward to failed token `4e69277aefda4eedaa8ee9bcbe639040`. It is not runnable through the ordinary cycle. The original failed queue item and snapshot remain intact; no journal correction has been made after this second failure.

Proposed narrow recovery, subject to your acceptance: back up and hash the journal, remove only this `retry_only` marker under the journal transaction lock, bind this recovery verdict in recovery_log, preserve all failed history and approved selections, then launch one ordinary cycle at258. This supplies the still-unused single pre-run fetch retry. If it fails, stop and file another request. No teacher, validator, packet or approval-policy change is proposed. If you prefer an implementation path for pre-packet recovery instead, please specify it; no bypass will be made meanwhile.

Diagnostic report: `reports/commit-000258-recovery-002.json`. Original failure bindings: `reports/commit-000258-pre-run-retry-001.json`. No implementation changes or tests for this diagnostic request. The 257 invalid-70b-qtip-spec ledger r001 remains owed with the eventual258 review request.

## SHA256

- `reports/run-ahead-detached-000258-0d40e92e915545bfa0d9cb0ba021342a.json`: `5cbce5b933feba8e8f5d943d5303ee886b56d67f23a684422ed82d7bad8ed58e`
- `reports/run-ahead-detached-000258-0d40e92e915545bfa0d9cb0ba021342a.log`: `ced146251d2deec562b7cfe0b65442676deef6bbc1141f68677ca833c4705bab`
- `reports/commit-000258-pre-run-retry-001.json`: `f52719d88a01db1ac9e811038e9240440409250c0f301aa2c7feeae658c444f9`
- `orchestration/run_ahead.py`: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
- `reports/commit-000258-recovery-002.json`: `d91afffacc450d6d36a25d667c2c0d656583f33e7ce60dfc086511018810e9cd`
