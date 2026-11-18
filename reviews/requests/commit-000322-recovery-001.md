# Failure handoff for commit 322

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Run: `.teacher/runs/commit-000322-001`.
Packet: `.teacher/retrieval/000322-001`.
Upstream: `ff21ee46edb9ba74d709257f482c809a7bd406d0` — "Transformer: Allow layers without input norms" (copied from Git).

The original final (15,501 bytes) and the single validator repair final (15,583 bytes) both failed with `Source inspection requires source evidence`. The plain-MLP allocation finding's source-inspection check cited repo_grep and run in the original final and only repo_grep in the repair final. Neither evidence set contains a source tool accepted for that check. No draft was published and no ledger records were filed.

322's queue stop is in force. This handoff documents the exact failure for future recovery review. The user's 00:45 UTC stop order remains in effect. A fresh 322 attempt awaits the user's resumption and a bound recovery decision.

## SHA256

- reports/run-ahead-detached-000322-79411d98ca614f92aaa877f51ff339d9.json: `2c179662085b7189b3a8e1833e4fd463e8dc57a4023e368dd7e79b6d44d7d42e`
- .teacher/admin/run-ahead/6d25a3c870a745ab9834f32a7a5edfc3.log: `5266c32b7538209f419b9170184db10b1cab67b17951fb1321a8ef64f584081d`
- .teacher/retrieval/000322-001/manifest.json: `6ae1f1a6bc628567b22718cc630d7d8a2e8dec516b3ed54419ff0854632d258f`
- .teacher/runs/commit-000322-001/status.json: `5c9212a8a1ae15548ed79fbbc877ae1904c6dec5e5a3e65ebfa40bd2a195696e`
- .teacher/runs/commit-000322-001/provenance.json: `2505da6029f2c5f02d14cf84bc3b34183d5a74b9605783d5f431b42b5b9edaaf`
- .teacher/runs/commit-000322-001/raw-transcript.json: `ca846a3eeb58be4b648a38bb8885661a4847e8fdbbdfb2259ebac991e00b15d8`
