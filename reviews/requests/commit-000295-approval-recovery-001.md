# Approval recovery: commit 295/003 request fingerprint format

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Requested scope: administrative recovery and ledger review; ancestor retrieval only. Canonical and training remain false.

295/003 and 296/001 are approved, but neither approval has been recorded. The unmodified queue recorder refused 295/003 with `ValueError: Missing required request fingerprints`, before mutation. The published request uses a Markdown table for all 19 verified SHA-256 bindings; `orchestration.run_ahead.check_verdict` accepts only bullet lines. Its bound request digest still matches. No teacher run was started and no run, packet, journal or implementation file was changed for this recovery.

## Proposed exact recovery

Please authorize backing up the journal and published request, then replacing only `reviews/requests/commit-000295-003.md` with the bound candidate below and rebinding only that queue item's `request_sha256` to the candidate digest. The candidate preserves the entire original request and appends the same 19 bindings in the recorder's existing bullet syntax. The diff contains only that addition. Preserve the original bytes, both digests and this recovery decision in the administrative audit report; do not change run/packet files, orchestration code, verdicts or approval rules.

After authorization, verify the original digest and idle queue again, perform that exact format recovery, run the unchanged `check_verdict`, record 295 then 296 using the queue approval command, clear the existing retry stop against the 295 approval verdict, and resume at 297. If another check fails, stop and report it rather than bypass it. No implementation change or new teacher session is proposed; the accepted 332-test suite remains the latest suite result.

## Ledger records submitted

Four observation revisions preserve the existing identities at 295: FP32 MLP intermediate contract, odd activation tail, all-expert fused shape, and fused output dtype/workspace contract. The FP32 revision distinguishes the ordinary sparse destination corrected by the parent from opt-in GatedMLP reach with no located shipped builder. The fifth record is 296's new stale-reserve-docstring documentation discrepancy: defaults 0.5 versus docstring 0.25. All five passed schema and evidence validation with immutable copies of each run's draft, transcript and approving verdict. They make no GPU execution or checkpoint failure claim. No ledger material reaches a teacher.

## SHA-256 bindings

- reviews/requests/commit-000295-003.md: `015e07f9475cbb8182591c00357eb21412df4916e161d3137cc951b12857fb18`
- reports/commit-000295-003-request-fingerprint-candidate.md: `31e834e7819e30e25237041bb6b5f0d56bd186a51be18c77b498b64a0443da7d`
- reports/commit-000295-003-request-fingerprint.diff: `de46af8d73b349ea336e340c980e50dd63f6e433086ca21efe36d082d3f35d71`
- reports/commit-000295-approval-recovery-001.json: `52d9951f8ccc4e9447913bc93e9a7fba69bb51b7410bcdce3ad833cb004573f8`
- reviews/verdicts/commit-000295-003.md: `92ab6acfa2b48dc08d2855db320f5f87dd433624dc1343796a3e25a3a13439d7`
- reviews/verdicts/commit-000296-001.md: `497de6d68e18804f630e005b6d8d5e0e19fd2fc6f968c1f0125ff6e9d1344d5e`
- reports/defect-ledger/exllamav3-fp32-mlp-intermediate-contract--r003.json: `7b6bf69702921c84db1fab58d590e02f86ed513cd6d90def8de11d1a8cc01ae4`
- reports/defect-ledger/exllamav3-activation-odd-tail--r003.json: `3b25cc5585b1befe482af3176530217db25539cd7c1ad15107c5555882e83190`
- reports/defect-ledger/exllamav3-all-expert-fused-shape--r013.json: `da5cce5f3eac580b3a23ee3134766dd0b30f78eb806482edeb295d13556f3131`
- reports/defect-ledger/exllamav3-fused-output-dtype-override--r006.json: `47eeaa45218ab714518c10f7fb35db29d59d7c8ac66e5cbf94ef659829ebe5cf`
- reports/defect-ledger/exllamav3-stale-reserve-docstring--r001.json: `62dabc7b960b876efafdceee9ec3e578a18be19de3960ca2697c971ff4907fce`
- reports/defect-ledger/evidence/commit295-003-draft.json: `f0d63294d3ebc77c2d5ea87836ce8d0c31dba31f2f462b56cc355ac87ca9ddb6`
- reports/defect-ledger/evidence/commit295-003-transcript.json: `1a862a9ecff4e88378cc8ef13b8ef7902051f066c3c0c9b0fe8c3afaf4154303`
- reports/defect-ledger/evidence/commit295-003-verdict.md: `92ab6acfa2b48dc08d2855db320f5f87dd433624dc1343796a3e25a3a13439d7`
- reports/defect-ledger/evidence/commit296-001-draft.json: `f18f5cc759a2b6ba6978ea6c1b27473126f52f4cd48068dfededb906e34a9e7d`
- reports/defect-ledger/evidence/commit296-001-transcript.json: `7c8ff92d4f7cc42655180f65e13a717a25004529d5d27b41eaf2fff47fc836a3`
- reports/defect-ledger/evidence/commit296-001-verdict.md: `497de6d68e18804f630e005b6d8d5e0e19fd2fc6f968c1f0125ff6e9d1344d5e`
