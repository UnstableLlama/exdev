# Astra tracking — administrative only

<!-- cycle-status -->
Current journal status: `ready`.
Next position: `172`.
Handover: `null`.
Advancement pause: `null`.
<!-- /cycle-status -->

Never supply this file, verdicts, or ledger material to a teacher. Read this top
section after a reset; search `reviews/ASTRA-REGISTER.md` for specific obligations.
The walk journal is authoritative for position, active attempts and stop status.

## Current boundary

- 164/001 is approved, unassisted; 165 and 166 are approved for ancestor retrieval only; 167 is approved for ancestor retrieval only; 168 is approved for ancestor retrieval only; 169 is approved for ancestor retrieval only; 170 is approved for ancestor retrieval only; 171 is approved for ancestor retrieval only on guidance 5. Guidance adoption is authorized; guidance 7 accepted, 172 launching detached. 162/001 is approved, unassisted; 163/001 rejected/superseded; reviewer-assisted 163/002 approved; 153/002 active,
  reviewer-assisted; 153/001 rejected/superseded. 39/005 remains active;
  113/002 is active and 113/001 excluded.
- Token-cost A/B/C and fixes accepted; part D applied by Fable (90k compaction),
  window restarted. Fable monitors runs 159–163.
- All approvals are ancestor retrieval only. Canonical/training remain false.
- 158 discovery is complete; Mistral-Large-Instruct-2407 is mirror-inspected
  non-match. Four Mixtral reference bundles recovered. Wrong-cutoff report 001
  is excluded. No teacher-facing changes for this implementation.

## Procedure

1. Read AUTHOR-INSTRUCTIONS and this current section after reset. Never print the journal whole; extract only `status`, `next_position`, `handover`, `advancement_pause`, or the specific record needed.
2. Read the new verdict; verify its request/artifact hashes before recording it.
3. Use `python3 -m teacher.cycle --state reports/teacher-walk-001.json --approve VERDICT`
   for a first-attempt unassisted pending approval. Replacements/assisted runs stay manual.
4. Record open work here and append dated acceptances/closures in ASTRA-REGISTER; never erase history.
5. Confirm no advancement pause. Launch escalated: `setsid -f python3 -m teacher.cycle_notify --state reports/teacher-walk-001.json --notify-thread "$CODEX_THREAD_ID"`, with launch output redirected to a unique reports log.
6. Confirm the new supervisor log exists, then end the turn. Do not wait or poll. Inspect the result and reports on its queued completion message; the message grants no permission to bypass a stop. An open window consumes queued messages; otherwise they wait until resumed.
7. A named stop requires judgement. Never change ready status merely to bypass it.
8. Architecture/discovery, unresolved references and curator attestations stay manual.
9. Read the draft, coverage, run arguments and generated cycle report.
10. Complete the request skeleton's judgement paragraphs, limits and ledger hashes.
11. File via `teacher.walk --publish-review-request PATH > /tmp/exdev-publish-result.json`; this command emits the whole journal, so never display its stdout. Extract only needed status keys from the saved JSON.
12. Wait for its verdict; no next full-review commit or silent prose repair.

## Standing conditions

- Contract 8 / guidance 7 / Codex 0.167.0; Linux aarch64 and Python 3.14.4
  under the recorded user decision. Record architecture and Python in provenance.
- Salience-v3-paths: report path-only qualifying/selected counts and truncation
  on every request. Stop before a teacher if any path-qualified row is cut by
  cap 20; propose ordering. Do not rewrite previous bound packets.
- Discovery enumerates every official publisher, not model-name matches only;
  distinguish missing root config from inaccessible evidence. Read all matching
  configs. Architecture trigger stops the cycle for manual recovery.
- Hash-verified mirrors are generally permitted under decision 98 points 2–4,
  not limited to Cohere. Historical nonmatching official hashes require the
  separate accepted historical-mirror procedure, not an improvised exemption.
- Curator-attestation and unresolved bundles must be named in full-review requests.
  Covered-merge first live use was 153 and accepted. Registry triggers cannot waive.
- Official HF raw/normalized headers: 16 MiB; mirror headers: 4 MiB. Larger needs review.
- Shared blob store stays read-only; verify links and hashes. No packet rewrites.
- Separate repo_read counts from run file reads; identify scalar checks and
  incomplete/binary coverage accurately. No runtime claims from source alone.
- Full host-enabled suite required for implementation requests; boundary audit
  and two rebuild comparisons required for this token-cost change.
- Reviewer observations stay administrative. Ledger validator still rejects that
  origin; preserve the label and disclose the limitation, never relabel to pass.

## Open administrative work

- Guidance-6 trial authorized by `reviews/verdicts/guidance-6-trial.decision.md` (SHA256 `9ba58a40c5cbcd533171324a09a0010b729e1f9c9287ec83bd222a3f12011848`). 164 is filed; the version gate, v5 identity check and host-enabled suite are complete. `reviews/requests/guidance-6-implementation-001.md` is accepted as a trial gate. Start the trials after the running 165 cycle finishes and its request is filed; snapshot walk artifacts then, so 165 does not confound the isolation comparison. Then four fresh unassisted unpublished scratch trials at 154, 158, 163 and control 156, outside walk packet/run directories, no journal attempts or ancestor approval, no reviewer material. File `guidance-6-trial-001.md`. Walk adoption requires a later user decision. Reviewer-only success criteria remain excluded from all teacher inputs.

- 164/001 approved for ancestor retrieval only; verdict recorded manually with all 29 request hashes verified. Discovery 003 and all eleven complete mirror bundles validated. Post-authoring replay failed on an argument error already serialized by the teacher; manual exact session-semantics replay validated all 35 calls and all immutable hashes. Original failure remains recorded. Warning-name r001 accepted. Logits-padding-width-mismatch r002 adds the reviewer-observed Gemma3 case; include it with the next request, never teacher input.

- Guidance-6 gate implemented and filed in reviews/requests/guidance-6-implementation-001.md; 280 host-enabled tests pass, v5 system and full opening byte-identical. Walk default stays 5. Acceptance recorded below; trial locations and exclusions remain as above. Compare manifests with only guidance_version changed (163 source is unassisted 001); one first-result session per position, at most one disclosed mechanical retry; compare draft/transcript/coverage/tool counts/model turns with approved runs (163 baseline output is assisted 002). Prove no changes to retrieval/runs or journal runs/approved_entries.

- Permanent administrative replay fix filed in reviews/requests/tool-replay-errors-implementation-001.md; all 35 live transcript results replay identically. Request ACCEPTED; it changes no teacher input. Report acceptance in 165. Existing detached 165 supervisor and child confirmed running; do not duplicate the launch.

- 163/002 approved reviewer-assisted; Qwen3 MoE component-migration r001 accepted. Warning-name r001 filed from rejected 001 with reviewer source confirmation, accepted by 164; excluded from teacher input. Its omission and assisted status are canonical-use conditions.

- `exllamav3-compare-q-inference-mask-context--r001.json` accepted by 163/001 verdict: reviewer_observation/new_requirement, source only, never teacher input.
- 162 canonical-use condition: correct the claim of independent edits and explain that the in-place mask requires inference mode supplied by main. Authored run stays immutable.
- Notification success change accepted by 162 verdict.

- Discussion-history cache: separately requested, nonblocking, still owed. This
  cycle intentionally retains fresh history retrieval; no cache semantics changed.
- Padding-target r003 accepted: fixed at 161, source-confirmed; wording corrected.
  Unconditional-deferral r003 accepted by token-cost-detach-001, suspected/source only.
- New notify module/test hashes and 278-test result included in 162 request;
  first live detached cycle completed and its queued notification arrived.
- Older ledger obligations remain: `ASTRA-REGISTER.md` preserves verdict follow-ups
  and journal dispositions. Do not treat repeated “still owed” as closure.
- Top-p114 identity/fix115, older reviewer conditions and unresolved legacy
  ledger-origin repairs must be reconciled against ledger files before closing.
- 71 FP32 intermediate, 72 partial-RoPE introduction/header linkage, and image/
  loader/caller canonical limits remain where their verdicts require them.
- Closed-catalog checks at positions 560 (issue99) and 1100 (issue233) remain due.
- Canonical use of assisted entries requires a separate selection decision.

## Manual preparation without temporary scripts

For an architecture stop, use the repository functions `teacher.cycle.recover_inputs`
and `teacher.cycle.index_parent` with the journal position and pinned Git SHA,
`data/evidence/github`, `reports`, `data/exllamav3-v5/records` and `store`.
They recover discussions/check truncation and index the preceding graph without
starting a teacher. Existing bundles stop for manual validation. Complete reference
discovery and any required review before using `prepare_packet`/`author` manually.
Never clear a pause or change ready status merely to bypass these checks.

## Implementation verdicts recorded 2026-11-15

- `guidance-6-implementation-001` ACCEPTED; verdict SHA256 `2f8e32719257c11ebc231a21a8b42c9dd26cc44a77b09be913085a7170d4033b`; all 9 request hashes verified.
- `tool-replay-errors-implementation-001` ACCEPTED; verdict SHA256 `0c5e20346ab827b1065eb650d24cff5422a9f515b325fd71d11675509b416367`; all 8 request hashes verified.

- 165 request filed: reviews/requests/commit-000165-001.md. Trial supervisor reports/guidance-6-trial-supervisor-001.py runs 154,158,163,156 sequentially, stops on any failure for inspection, queues completion. No automatic retry. Snapshot files under .teacher/trials/guidance-6-001; source 163/001, output comparison 163/002.

- 165 verdict verified: SHA256 `fb1682601a0168d7496b8388b92815b8f55f9b7823e0587fe99a2444fd9ee290`; all 14 request hashes match. APPROVED for ancestor retrieval only; padding-width r002 accepted. Approval application via --approve is deferred until the running trial snapshot completes, to preserve the required walk isolation comparison. Then file guidance-6-trial-001 and continue 166 detached.
- Both 165 findings serialized as pending ledger candidates, introduced at 3873d40a: reports/defect-ledger/exllamav3-compare-q-no-reference-finalization--r001.json, reports/defect-ledger/exllamav3-compare-q-cache-clear-argument-mismatch--r001.json. Include with next request. Perplexity-only behavior explicitly regresses from working at 162.

- Guidance-6 four trials complete, one session each/no retries; 74 calls replay identically. All 222,999 walk-file inventory records and journal runs/approved_entries unchanged across trial snapshots. Filed reviews/requests/guidance-6-trial-001.md; await trial verdict, no adoption. 165 approval subsequently applied via --approve; continue 166 guidance 5. Both 165 ledger candidates remain to include with 166 request.

- Trial verdict assessed: `reviews/verdicts/guidance-6-trial-001.md`, SHA256 `40416d0f227fc5c71e79b0bc2f1d3b721913e03cd1a467a6237ae71c1e044146`; all 55 request hashes verified. Conduct accepted; 163 and main 158 gap found, 154 missed, control clean, 74 vs 52 calls. No trial output approved, no guidance adoption. Proposed wording correction and fourth paragraph require user decisions; do not implement or pass reviewer criteria to teachers. Continue 166 guidance 5, existing detached cycle only.

- 166 completed on guidance 5; request reviews/requests/commit-000166-001.md filed, awaiting verdict. 22 replayed calls, 1/1 sections, seven configs read; scalar stand-in only. Both 165 ledger candidates included. No 167 before verdict. Qwen3 MoE fix attribution pending review of 166.

- 166/001 APPROVED for ancestor retrieval only; verdict SHA256 c6e9e4ee684d72d219a0b43986d0802a34dfd86267bae568758d00accfc1fac2; all 13 request hashes verified, approval applied via --approve. Both 165 ledger r001 records accepted. Qwen3 MoE component-migration r002 filed as pending candidate for the 167 request: fix 08858bc8, affected 163–165, reviewer-confirmed source inspection only. Guidance remains 5; 167 launching detached.

- 167/001 request filed at reviews/requests/commit-000167-001.md; unassisted guidance 5, 14 exact replays, 3/3 sections, no ancestor prose reads. Nonpositive code-block index finding pending review. Qwen3 MoE r002 included with evidence hashes. Await verdict; do not start 168.

- 167 approved for ancestor retrieval only; all 18 request hashes verified; verdict SHA256 73b3a4577f3ff6b54090cf52e4d2e90e1c0fe78b5a82838adbb1c8488d7362ab. Qwen3 MoE r002 accepted. Canonical-use condition: inherited empty-block feedback from 137 omitted; do not alter authored run. New nonpositive-codeblock-index r001 and empty-codeblock-feedback r002 (167 affected, reviewer-only addition) pending review with 168. Continue guidance 5; reviewer material excluded from teacher input.

- 168/001 request filed at reviews/requests/commit-000168-001.md; all 20 hashes verified, 14 exact replays, 1/1 task sections, one ancestor prose read. No findings; scalar accounting only. Nonpositive-codeblock-index r001 and empty-codeblock-feedback r002 included for review. Await verdict; do not start 169.

- 168/001 APPROVED for ancestor retrieval only; verdict SHA256 0af0691e0515a494150bd61588d07cf4a3e8134a23a5cabcd3d90db7b0ce1b9f, all 20 request hashes verified, approval applied via --approve. Nonpositive-codeblock-index r001 and empty-codeblock-feedback r002 accepted. No new findings or canonical-use conditions; older obligations remain. Continue 169 detached on guidance 5; reviewer-only notes excluded from teacher input.

- 169/001 request filed at reviews/requests/commit-000169-001.md; 12 artifact hashes verified, eight exact replays, incomplete 4/9 text-section coverage explicitly disclosed (five story/passage fixtures unread), zero ancestor reads. Unsupported-cache-default-argument finding pending review; run executes extracted parent add_args AST, not full script or model. No new ledger candidates. Await verdict; do not start 170.

- 169/001 APPROVED for ancestor retrieval only; all 12 request hashes verified; verdict SHA256 64df74c9d14426c5cc8f411da8d6509f2df448a017c39b5675a5a4f35ed37ecd. Canonical-use conditions: describe altered-text tasks and name replacement; five unread story sections must be read or remain explicitly disclosed. Authored run immutable; reviewer notes never teacher input. Unsupported-cache-default-argument r001 prepared for next request, introduced 0488385e, verified by isolated execution of parent helper. Continue 170 detached guidance 5.

- 170/001 request filed at reviews/requests/commit-000170-001.md; all 16 hashes verified, ten identical replays, 1/1 task sections, approved 169 ancestor read. No findings; parent helper and reconstructed changed helper executed in isolation. Unsupported-cache-default-argument r001 included; fix attribution awaits review. Await verdict; do not start 171.

- 170/001 APPROVED for ancestor retrieval only; all 16 request hashes verified; verdict SHA256 fb6c3da34087620c4a4ccaaf39c0435d45208eb0629dcd4e4eb95af8f038cb6b. Unsupported-cache-default-argument r001 accepted; r002 prepared for the next request with fix 2432c64e, reviewer source-confirmed, affected 169 only. No new canonical-use conditions. Continue 171 detached guidance 5; reviewer-only notes excluded from teacher input.

- User adopted guidance via reviews/verdicts/guidance-6-adoption.decision.md, SHA256 fc6620e760801c060f85975a5fa73558a05dd4129e09119108c7392188454d7b. Finish and file the existing 171 cycle under guidance 5 first; do not launch 172. Then implement guidance_version 7 with adopted A and unchanged B/C; preserve v5/v6 byte identity, set prepare default to 7, run full host-enabled suite, file reviews/requests/guidance-7-adoption-001.md with patch and identity/text checks, await acceptance before another commit. No fourth paragraph authorized. Existing approved entries remain unchanged.

- 171/001 request filed under guidance 5; journal awaiting_full_review. Guidance-7 adoption decision SHA256 fc6620e760801c060f85975a5fa73558a05dd4129e09119108c7392188454d7b implemented and filed in reviews/requests/guidance-7-adoption-001.md. New prepare default is 7; versions 5 and 6 unchanged. All 280 host-enabled tests pass, legacy opening/tools/effort identical, adopted text exact. Do not launch 172 until adoption implementation accepted and 171 approved.

- 171 approval recorded via --approve; verdict SHA256 3c6b52f6c60cfed0eb3e48cbdcdbe008a1a64ad0a1954bc4cd925fe1f33444f0. All 19 request hashes match. Cache-default r002 accepted. Both 165 identities now have pending r002 records adding 475dfcca as affected; include both and commit171 evidence copies with the next request. Guidance-7 adoption request already filed; no 172 until its verdict.

- Guidance-7 adoption ACCEPTED, verdict SHA256 d86c96de3bb9eb9a4e3bfb1aa38315e4ed227038820deaa475e3536ed7ffd59b; all 10 request hashes verified. No journal advancement pause set; administrative stop cleared by acceptance. Continue 172 detached on guidance 7. Requests must name guidance 7, report ancestor reads/tool counts, and quote any teacher statement that instructions cannot be followed with available tools. Both 165 r002 candidates remain due with the next request.
