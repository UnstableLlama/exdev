# Approval recovery: commit 299/001 historical accepted implementation

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Requested scope: administrative recovery; ancestor retrieval only. Canonical and training stay false.

The unchanged host-enabled queue approval command stops at `Implementation hash mismatch: teacher/codex_adapter.py`. All 24 request bindings match. The verdict explicitly accepts the three expected historical implementation differences. No approval has been recorded. 300 is already running with accepted validator-keep-rest-v2; its process, packet and implementation must remain untouched while active.

Please review this exact recovery route, to apply only after 300 exits and the journal has no active session: verify the current live implementation against the accepted application report; back up the journal and 299 review.json; temporarily restore only teacher/codex_adapter.py, teacher/cycle.py and teacher/validation_repair.py from the bound accepted baseline copies. Verify every implementation hash in 299 provenance against disk. Run the unchanged host-enabled `python3 -m orchestration.run_ahead approve --state reports/teacher-walk-001.json --run .teacher/runs/commit-000299-001 --verdict reviews/verdicts/commit-000299-001.md`. In a finally block restore the exact accepted current bytes, verify all implementation hashes against the accepted application report, and retain before/after hashes and command result in an audit report. No teacher session may launch during the temporary restoration. Stop on any additional failure; do not waive a check, monkeypatch validation, edit provenance, manually record approval or replace 300's ancestor snapshot.

This uses previously accepted source on both sides; no implementation change is proposed. The request and verdict remain as published. No recovery has been applied, and no commit or push performed. After successful 299 recording, handle 300 in order using its original sparse packet.

SHA-256 bindings:

- reviews/requests/commit-000299-001.md: `98bacef7db4d49a70f872873eb3e8f28221e3d49f236a77f0f575c17590733cf`
- reviews/verdicts/commit-000299-001.md: `52668d3753de53029dbdb35c1d1806a33d609668edc4166b93ecf760ecb538af`
- reports/commit-000299-approval-recovery-001.log: `a3a40df6183f6565a8a280f374af7567758dd14f314ef977f1c036d0659255d8`
- reports/commit-000299-approval-recovery-001.json: `7b1500cf84b5a3bb9c09f529f8512cd57ed9f493c9d33f540e5fb68223a99c2d`
- reports/validation-repair-implementation-004-application.json: `764892c8af2835261e8a2d6d4c6e59fcb2f9ad993ee267d38301767829fedda2`
- reviews/verdicts/validation-repair-implementation-004.md: `14a3564a6790a74528fb7927a27aa5afef80d5fadaf8f12c239ea36ad65a8278`
- reports/validation-repair-implementation-004-baseline/codex_adapter.py: `9540b6701d5ceb44c28af78ec9f38fa80038637a37e10563c181c0696b14e190`
- reports/validation-repair-implementation-004-baseline/cycle.py: `5c3768624cb16f134a5428a34687bea7eb70bc2626f909065d3676626a246e9e`
- reports/validation-repair-implementation-004-baseline/validation_repair.py: `d6ce4f8944287bd1ef9cf42fbddba342597efa8122c19761e3ce66b4f44e27a4`
