# Astra tracking — administrative only

<!-- cycle-status -->
Current journal status: `awaiting_full_review`.
Next position: `196`.
Handover: `{"full_review": ".teacher/runs/commit-000196-002", "request": "reviews/requests/commit-000196-002.md", "sampled_mechanical": []}`.
Advancement pause: `null`.
<!-- /cycle-status -->

Never supply this file, verdicts, or ledger material to a teacher. Read this top
section after a reset; search `reviews/ASTRA-REGISTER.md` for specific obligations.
The walk journal is authoritative for position, active attempts and stop status.

## Current boundary

- 164/001 is approved, unassisted; 165 and 166 are approved for ancestor retrieval only; 167 is approved for ancestor retrieval only; 168 is approved for ancestor retrieval only; 169 is approved for ancestor retrieval only; 170 is approved for ancestor retrieval only; 171 is approved for ancestor retrieval only on guidance 5. Guidance adoption is authorized; guidance 7 accepted, 172 approved, 173–175 approved; 176 launching detached. 162/001 is approved, unassisted; 163/001 rejected/superseded; reviewer-assisted 163/002 approved; 153/002 active,
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

- Contract 8 / guidance 8 / Codex 0.167.0; Linux aarch64 and Python 3.14.4
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

- 172/001 request filed at reviews/requests/commit-000172-001.md; first live guidance-7 walk run, eight exact replays, 1/1 sections, one ancestor chapter (543c4b27), three full parent file reads. Synthetic scalar check only, no run file reads or real GGUF/cache execution. Two suspected findings await review. Both 165 r002 affected-revision candidates and evidence included. No teacher tool/instruction incompatibility reported. Await verdict; do not start 173.

- 172 APPROVED ancestor-only; verdict SHA256 dc27c9449ff1241042504a9a48e4db966112654f6f5ce769b18dc475d6b53de6; request hash and all 23 artifact hashes verified, approval applied via --approve. Both 165 r002 records accepted; r003 candidates add 07ffea7f as affected, include with next request. Canonical-use conditions (reviewer-only): CLI clear uses the wrong two-argument key, cached test_ppl results bypass even the storage helper, and the entry omits the two unchanged 165 defects. Never teacher input. File suspected source-only ledger candidates for embedding-order and cached-accounting with their stated real-GGUF/execution limits; identities/origins to be checked before filing. Older ledger work and discussion-history cache remain owed/nonblocking. Continue 173 detached on guidance 7.

- 173/001 request filed: guidance 7, eight exact replays, 1/1 sections, two complete parent reads, one ancestor entry (165); scalar checks only/no run file reads. Both 165 r003 candidates and 172 embedding-order/cached-accounting r001 candidates filed with evidence hashes. Pending 173 findings and cache-key fix attribution await verdict. No teacher instruction/tool incompatibility reported. Do not start 174.

- 173 APPROVED ancestor-only; verdict SHA256 66f4d122bfb67b85920701692be8ff8d5c1274a03e06fa9580c0ba92e13e97f6, request hash and all 25 artifacts verified. Four submitted ledger candidates accepted. Prepared r004 candidates: e1d2fa11 fixes cache-clear mismatch and is affected by no-reference finalization. Include both plus evidence with 174 request; also file suspected filtered-reference-dependency identity with stated missing-file/execution limits. No canonical-use conditions for 173. Continue 174 detached guidance 7; older ledger work and discussion-history cache remain owed/nonblocking.

- 174/001 request filed: guidance 7, 26 identical replays, 1/1 task sections, two ancestor prose reads; model.py and model_diff.py partial reads explicitly disclosed. Integer indexing/shape checks only, no tensor/loader/model execution; three suspected findings await review. All 25 artifact hashes verified. Three 173 ledger follow-ups filed (both 165 r004 revisions and filtered-reference-dependency r001). No teacher instruction/tool incompatibility reported. Await verdict; do not start 175.

- 174 APPROVED for ancestor retrieval only; verdict SHA256 d96de6287381d094d3a22417e9c2099d569e1e158b11046bbfcbeb6e16bec623; request and all 25 artifacts verified, approval applied via --approve. All three ledger candidates accepted. Canonical-use notes: deferred scaling loss occurs on the default unsliced file-backed path; model.py and model_diff.py partial reads remain disclosed (relevant code was read). Reviewer-only notes never teacher input; authored run immutable. Pending next request: suspected/source-only ledger candidates for FP8 dtype support, deferred scaling and conditional scale orientation; check identity/introduction and retain actual-checkpoint, half-product and execution limits. Older ledger work and discussion-history cache remain owed/nonblocking. Continue 175 detached guidance 7.

- Guidance-8 trial authorized by reviews/verdicts/guidance-8-trial.decision.md (SHA256 941c51728fcf206d1757fbb943fdeaf852919139f9d2718caeaac37e2bef97b5). Patch staged, NOT APPLIED, at reports/guidance-8-implementation-001.patch; version-7 pre-edit snapshot saved in reports/guidance-8-v7-before.json. Apply only after live 175 finishes its implementation-hash validation; do not invalidate the active run. Then verify exact decision paragraph and unchanged v7 opening/tools/effort, full host-enabled suite, file guidance-8-implementation-001 request. Walk default remains 7, no advancement pause. After acceptance run four fresh unassisted unpublished trials at 154,140,157,156 under .teacher/trials/ between commits; same cutoff evidence, no reviewer material or journal attempts/ancestor approval. File guidance-8-trial-001 with drafts/transcripts/coverage/tool and token counts. Adoption requires another user decision.

- 175/001 filed: guidance 7, 10 exact replays, 2/2 sections, two ancestor entries, one full and one partial parent file read. Scalar arithmetic only, no run file reads. Inherited filtered-reference finding and no-reference fix attribution await review. Twelve artifact hashes verified. No new ledger candidates; 174 identities still owed. No 176 before verdict. Guidance-8 patch subsequently applied after completed run validation; original run and packet untouched.

- Guidance-8 trial gate implemented after 175 completed; request reviews/requests/guidance-8-implementation-001.md filed. All 280 host-enabled tests pass (24.418s); v7 complete opening/tools/effort byte-identical to pre-edit snapshot, v5/v6 snapshots unchanged, v8 paragraph exact decision and bundle validates. Walk default stays 7, no advancement pause; no trials until implementation verdict. Four trials and reporting remain owed as specified; no adoption. 175 review pending; 176 requires its approval.

- 175 APPROVED ancestor-only; verdict SHA256 c31aaca9731fa38a69b26e620481d9f99291c33e4b691546a3b9e3f9eeabbd0a; request and all 12 artifacts verified, --approve applied. Two implementation-hash differences explicitly accepted as guidance-8 edits after run validation. Prepared no-reference-finalization r005 with fix c0a2028f and filtered-reference-dependency r002 adding it as affected; include both and commit175 evidence with next request. Three 174 identities remain owed. Canonical-use notes (reviewer-only, never teacher input): --kld with no reference now reaches a missing kld key in plot; only one of the two Llama3 data specs changes tokenizer path. Guidance-8 request already filed, trials await acceptance; walk remains 7. Continue 176 detached.

- Guidance-8 implementation ACCEPTED as a trial gate; verdict SHA256 f07371b2fbe5abd2c0d89cb69939394659731f102e4647e72a00adfbc9d952c3; request and all 10 artifact hashes verified. Walk stays guidance 7. Prepare four fresh unpublished unassisted trials at 154,140,157,156 with unchanged cutoff evidence; launch only after running 176 finishes and its request is filed. No reviewer material, journal attempts or ancestor approval. Record token events administratively without changing teacher input. No adoption.

- 176/001 request filed: guidance 7; 48 identical replays, 38/38 sections, one ancestor chapter. Parent convert_model.py partial read disclosed; separate run-based source scan and scalar enumeration, no GPU/model execution. Both 175 ledger follow-ups included; 174 identities still owed. Await verdict, no 177. Guidance-8 trials launch between commits; defer journal/run approval writes until trial isolation snapshots complete.

- 176 APPROVED ancestor-only; verdict SHA256 1dcb904e968250bc53754fc7a2e42769c2caeaaea3d4030f6b3605b4b0c07ca9; request and all 27 artifact hashes verified. Both 175 ledger candidates accepted. Approval application via --approve and 177 launch await completion of the active guidance-8 trial isolation snapshot (currently first trial); do not modify walk runs/journal during it. Reviewer-only two-multiplier-resume-inconsistency r001 prepared for next request, source-only/suspected; inherited cost-buffer record still needs 176 affected revision. Three 174 identities remain owed. Canonical notes: divergent resume dispatch and MUL1 test scale 1.0 versus library 1.24371088; never teacher input. After trials, file trial request, apply 176 approval, continue 177 detached guidance 7.


## 2026-11-15 — guidance-8 trial filed; 176 approved

Filed reviews/requests/guidance-8-trial-001.md (SHA256 dacce61139830920100b67023c0e7715107eaddb9c2e6ec656496f4a332fcbdc). All four sessions completed once; 74/74 tool calls replay identically; walk snapshots unchanged. Trial assessment pending; no adoption or ancestor approval. Applied commit-000176-001 approval, verdict SHA256 1dcb904e968250bc53754fc7a2e42769c2caeaaea3d4030f6b3605b4b0c07ca9; ancestor retrieval only. Launching 177 detached on guidance 7. Include prepared two-multiplier-resume-inconsistency r001 and evidence with 177 request. Cost-buffer affected revision and three 174 identities remain owed. Reviewer material stays out of teacher inputs.


## 2026-11-15 — guidance-8 assessment recorded

reviews/verdicts/guidance-8-trial-001.md SHA256 `76f239ad8ce2b9b24ff66e2e8848d65a26b14692ba48d7abadad091ed298473f`: trial passes, assessment only, NOT adoption; no trial output approved for ancestor retrieval, canonical use or training. Request and all 59 listed artifact hashes verified. Walk remains guidance 7 pending a user decision file. Existing detached 177 continues; do not duplicate it. Reviewer trial observations remain administrative and excluded from teacher input.


## 2026-11-15 — guidance-8 adoption authorized, pending implementation

User decision `reviews/verdicts/guidance-8-adoption.decision.md` SHA256 `4c86a92b200686f892eb3b840e460520e3f82085c51417b4034a7f141bc6e494` adopts the trialled version-8 text unchanged. Existing detached 177 must finish and be filed under guidance 7. Then change prepare default to 8, run the full host-enabled suite, verify fresh packet instructions equal guidance 7 plus exact paragraph D and historical 5/6/7 reproduction, and file reviews/requests/guidance-8-adoption-001.md with patch and evidence. Do not start 178 or any further walk commit until adoption implementation is accepted, even if 177 is approved. Existing packets/runs remain untouched. After a few guidance-8 commits, report cost and effect against 172–176.


## 2026-11-15 — 177 and guidance-8 adoption filed

177/001 finished unassisted under guidance 7; request filed, 19/19 replays identical and 2710 read-only blobs verified. Includes reviewer-originated two-multiplier-resume-inconsistency r001. Awaiting verdict. Guidance-8 adoption request filed at reviews/requests/guidance-8-adoption-001.md: prepare default 8, unchanged trial text and historical inputs, 280 host-enabled tests pass. Explicit advancement_pause set; no 178 until adoption acceptance and 177 approval. Cost-buffer affected revision and three 174 identities remain owed. Cost/effect comparison with 172–176 owed after a few version-8 commits.


## 2026-11-15 — 177 approved; adoption pending

Recorded reviews/verdicts/commit-000177-001.md, SHA256 `b470443ac1d1c0ed4ee58ce17b68f1f2ac978df3c0ebb5c8e64cc7ad1bf239c8`, after verifying request and all 12 artifact hashes. Ancestor retrieval only; canonical/training false. Two-multiplier-resume-inconsistency r001 accepted, source-only suspected reviewer observation. Sorted-argmax identity gains 8b0df691 as affected (owed); cost-buffer affected revision and three 174 identities remain owed. guidance-8-adoption-001 is already filed. Next position 178, explicit adoption advancement pause retained; no teacher launch before acceptance.


## 2026-11-15 — guidance-8 adoption accepted

Recorded reviews/verdicts/guidance-8-adoption-001.md, SHA256 `24fee78ffec696fec253ca06f6aff2a2e59ebd1b7e1a585f3f893d7377fbc183`; request and all 10 artifact hashes verified. Cleared adoption pause; launching 178 detached on guidance 8. Requests must name guidance 8, report tool counts and ancestor reads. Cost/effect comparison against 172–177 owed after a few commits. Trial outputs remain unapproved and excluded from ancestor context. Existing ledger obligations remain open.


## 2026-11-15 — 178 filed, guidance 8

Filed reviews/requests/commit-000178-001.md, awaiting verdict; no 179. Nine calls replay identically, 2720 read-only blobs verified, task 1/1 fully read. Two ancestor reads are chunks of one root generation chapter. Both repo_read windows truncated; scalar run reads no files. Inherited optional-output finding, no new ledger candidate. Sorted-argmax/cost-buffer identity records were not located by filename/content search; reconcile register history before creating revisions. Their affected follow-ups and three 174 identities remain open. Cost/effect comparison against 172–177 remains owed after a few guidance-8 commits.


## 2026-11-15 — 178 approved; root ledger identities prepared

178 approved for ancestor retrieval only, verdict SHA256 `bd6e8432eb1bce48ff6f0f0f4c570b51b6af2ba15c62717366ad60d3ff529b1b`; request and all artifacts verified. Reviewer correction resolves identity search: no prior sorted-argmax or cost-buffer records. Created exllamav3-first-pass-cost-buffer--r001 and exllamav3-sorted-argmax--r001, suspected/source-only authoring observations introduced at root 543c4b27, affected root plus 176/177 respectively. Include both and their four evidence copies with 179 request for ledger review. Optional-output root identity remains older-batch work; three 174 identities remain owed. Launching 179 detached on guidance 8. Canonical/training remain false; ledger never teacher input.


## 2026-11-15 — 179 filed

Filed reviews/requests/commit-000179-001.md on guidance 8, awaiting verdict; no 180. All 17 calls replay identically, 2725 read-only blobs verified, task 1/1 read; one ancestor prose read. Disclosed partial conversion/native reads and scalar-only numerical comparison. New root first-pass-cost-buffer r001 and sorted-argmax r001 filed with evidence for ledger acceptance. Optional-output and three 174 identities remain owed. Cost/effect comparison against 172–177 pending after a few guidance-8 commits.

- 179/001 APPROVED for ancestor retrieval only; verdict SHA256 db468d8a43e8bdf64d0bd8e5e556c67ab79634d210a5045a5e831653f541b466, request hash and all 16 artifact hashes verified; approval applied via --approve. First-pass-cost-buffer r001 and sorted-argmax r001 accepted (root-introduced, suspected/source-only). No canonical-use conditions for this entry. Optional-output identity and three 174 identities remain owed; reviewer material excluded from teacher input. Continue 180 detached on guidance 8.

- 180/001 request filed at reviews/requests/commit-000180-001.md: unassisted guidance 8, all ten artifact and 44 implementation hashes verified, 15 identical replays, 7/7 task sections, one complete parent file and one approved ancestor entry read. Standard-library helper transcription only, no run file reads or profiler/package/GPU execution. Two path-only closed rows selected/read, no truncation. No new findings or ledger candidates; optional-output and three 174 identities still owed. Await verdict; do not start 181.

- 180/001 APPROVED for ancestor retrieval only; verdict SHA256 7c1c198cf99154f5b58fd84740606a6492ec384bc3325a367ba475b30d599e58, request hash and all ten artifact hashes verified, approval applied via --approve. Clean, no canonical-use conditions or new ledger work. Optional-output identity and three 174 identities remain owed. Continue 181 detached on guidance 8; reviewer material excluded from teacher input.

- 181/001 request filed at reviews/requests/commit-000181-001.md: unassisted guidance 8, ten artifact and 44 implementation hashes verified; nine identical replays; 1/1 task sections, two full parent files and one root conversion chapter read. Three run calls read/extract the parent allocator and apply the two task substitutions with synthetic objects; no full conversion or GPU check. Remaining-unequal-KV and inherited exact-budget findings await review. No ledger candidates submitted; older optional-output and three 174 identities remain owed. Await verdict; no 182.

- 181/001 APPROVED for ancestor retrieval only; verdict SHA256 98c480bffa9f7e836504642c4ed733d4dc9f5099d137db3eeb3c0852351c7560, request hash and all ten artifact hashes verified, approval applied via --approve. Canonical-use condition (reviewer-only): allocator budget already equals target plus carried bits plus one; the 1792-cost candidate exceeds the actual 1791 available bits, so its exclusion is not a missed exact fit. Potential defect is returned-surplus drift (reviewer observed 1,2,3,4,5 across repeated base-only calls), not the claimed exact-match exclusion; root wording has the same gap. Hold inherited-boundary ledger filing pending qualified treatment; never feed this correction to a teacher or edit the immutable draft. File a suspected remaining-unequal-KV identity with extracted-function/synthetic-size execution limits and establish its introduction. Older optional-output and three 174 identities remain owed. Continue 182 detached on guidance 8.

- 182/001 request filed at reviews/requests/commit-000182-001.md: guidance 8, ten artifact and 44 implementation hashes verified; 16 identical replays, 5/5 task sections. Four complete parent files plus partial kernel map (4900–7267), one complete approved ancestor entry. Scalar arithmetic only/no run file reads, CUDA, equivalence or speed check. One path-only closed row selected/read, no truncation. No new findings/candidates; inherited fused-buffer condition retained. Older ledger work remains owed, inherited budget-boundary filing held for plus-one qualification. Await verdict; no 183.

- 182/001 APPROVED for ancestor retrieval only; verdict SHA256 4e1f01e7f50c0ea0469358357fa68c5fd091295f753eb67b5eb8131f6513b0d1, request hash and all ten artifact hashes verified, approval applied via --approve. Three reviewer-only canonical-use conditions: fused K/V skips Linear.forward capture hooks (Q still runs its hook; all three share one key); without indices the wrapper does not tie output-slot count to pointer-list length (attention supplies two and two); the 32-token cutoff matches LinearEXL3.forward's existing reconstruction crossover. Preserve immutable draft; none of this enters teacher input. No ledger change. Optional-output, three 174 identities and 181 remaining-unequal identity remain owed; budget-boundary record stays held. Continue 183 detached guidance 8.

- 183/001 request filed at reviews/requests/commit-000183-001.md: guidance 8, ten artifact and 44 implementation hashes verified, 16 identical replays, 1/1 sections, two complete parent files and two ancestor prose reads. Scalar pairing algebra only/no run file reads or Torch/CUDA/test execution. Three source-only suspected findings await review (optional K, discarded test outputs, inherited partial width). One closed path-only row selected/read, no truncation. No ledger candidates submitted; older obligations remain open and budget-boundary held. Await verdict; no 184.

- 183/001 APPROVED for ancestor retrieval only; verdict SHA256 d44c8f640346a4b7cf21f324c122d7898ea8d477ddefc9e851ca777dc988cf95, request hash and all ten artifact hashes verified, approval applied via --approve. All three findings confirmed; no canonical-use conditions. Ledger follow-up: optional-K introduced at 6693b501, discarded reference-test results and partial-reference-width inherited with their introductions to be established/reconciled against existing identities; all suspected/source-only, no Torch/CUDA execution. Older optional-output, three 174 identities and 181 remaining-unequal identity remain owed; budget-boundary record still held. Continue 184 detached guidance 8; reviewer material excluded from teacher input.

- 184/001 request filed: reviews/requests/commit-000184-001.md; guidance 8, 23 identical replays, 5/5 task sections, one ancestor prose read. Four partial parent reads and scalar-only execution disclosed; no run file reads or GPU execution. Three suspected findings await review (all-expert cardinality, dtype override, persistent output alias). All 10 artifact hashes and 44 unchanged implementation hashes verified; no new ledger candidates, older obligations retained. Await verdict; do not start 185.

- 184 APPROVED for ancestor retrieval only; verdict SHA256 fd986397334c8880263bb04d601c980ebebf69292816c5cf9101fac3039d9501, request and all 10 artifact hashes verified; approval applied via --approve. All three findings confirmed. Canonical-use conditions (reviewer-only): routing gate is always LinearFP16 (qmap=None, half output, pad_to=1); prior forward adds bias and uses hgemm on input/output dtype mismatch, while native routing does neither. gate_tensor captures the weight at load and would miss later replacement, but no such replacement exists in this tree. Never teacher input; authored run immutable. Ledger follow-ups: file output-dtype and persistent-output-alias identities as suspected source-only behaviour changes, add 8357593c as affected to the all-experts identity; earlier owed work stands. Continue 185 detached on guidance 8.

- 185/001 request filed: reviews/requests/commit-000185-001.md; guidance 8, 45 identical replays, 7/7 task sections, four ancestor prose reads. Eight full parent reads, five partial reads and one missing-file error disclosed; scalar-only execution, no run file reads or GPU execution. Six finding groups await review. Two closed path-only rows both selected/read, no truncation. All 10 artifact hashes and 44 unchanged implementation hashes verified. No new ledger candidates; 184 and earlier obligations retained. Await verdict; do not start 186.

- 185 APPROVED for ancestor retrieval only; verdict SHA256 a99fd7a9943efe06d9210668c3423ebc549892f3b9c6c569fa1301be7c517450; request and all 10 artifact hashes verified, approval applied via --approve. All six finding groups confirmed. Canonical-use conditions (reviewer-only, never teacher input): native wrapper checks only q_norm dimensions/length, does not enforce paired k_norm; q_norm alone reaches null K norm, and K norm length/dtype-by-presence is not tied to head width (Attention always passes both). Constructor asserts equal norm epsilon but not bias; currently moot under overwritten settings, revisit after that fix. Ledger owed: three new suspected source-only identities for overwritten settings, warp-sum store race (store order not established), and padded reads; reconcile inherited frequency identity and add affected revisions for inherited reference/MLP findings. All earlier owed items stand. Continue 186 detached on guidance 8.

- 186/001 request filed: reviews/requests/commit-000186-001.md; guidance 8, 19 identical replays, 4/4 task sections, one ancestor prose read. Six full and two partial parent reads disclosed; scalar-only execution, no run file reads or CUDA execution. Three suspected findings await review; existing zero-cap/Boolean identities to reconcile. All 10 artifact hashes and 44 unchanged implementation hashes verified. Assessment sampled=true but no sampled mechanical handover. No new ledger candidates; earlier obligations retained. Await verdict; do not start 187.

- 186 APPROVED for ancestor retrieval only; verdict SHA256 b6a263268247b3f8708ebacfea2f474ec656d1f4ef9e688327f669ed238bbf49; request and all 10 artifact hashes verified, approval applied via --approve. All three findings confirmed. Canonical-use conditions (reviewer-only, never teacher input): explicitly describe single-GEMM lower clamp as repairing its zero-block case; kernel-table comment that shape 1 is unused is now stale. Ledger guidance retained: exllamav3-gemm-zero-grid-cap gains 1284d43c as affected for multi path with expanded range below 24 tiles; record single-path clamp as partial repair while multi remains open. exllamav3-boolean-dimension-threshold gains 1284d43c as affected. Stale five-argument selector declaration may be filed as a new suspected source-only compatibility identity. Revisions not yet filed; all earlier obligations remain owed. Continue 187 detached on guidance 8.

- 187/001 request filed: reviews/requests/commit-000187-001.md; guidance 8, 45 identical replays, 2/2 task sections, three ancestor entries. Eleven full and three partial repo reads disclosed; eleven complete config reads, no headers; scalar-only execution, no run file reads. One inherited conditional finding awaits review. Ten skeleton hashes, eleven config blob hashes and 44 unchanged implementation hashes verified. No new ledger candidates; earlier obligations retained. Await verdict; do not start 188.

- 187 APPROVED for ancestor retrieval only (clean); verdict SHA256 26a888ee649098f68af4e0815a206eaa4d6732df86fda08d3528082f58c3e2fc; request and all 21 artifact hashes verified, approval applied via --approve. Inherited all-experts finding confirmed; no canonical-use conditions. Optional ec839e16 affected-revision addition belongs to the existing all-experts identity if tracking every revision, not a new defect. Earlier owed ledger and administrative work remains open. Reviewer-only comparison with other models stays out of teacher input. Continue 188 detached on guidance 8.

- 2026-11-15: 188/001 filed for ancestor retrieval only: reviews/requests/commit-000188-001.md (SHA256 8e61f0118a5ce2b7efbb702727a511163d6a9b73e732eef6db99acca03cace66). Unassisted guidance 8; both sections, six complete parent-file reads, two ancestor prose reads; 16 identical replays and 2814 read-only blobs verified. Ten artifact and 44 unchanged implementation hashes checked. Scalar element-count check only, no tensor/CUDA/performance execution. No new ledger candidates; earlier obligations remain open. Journal awaiting_full_review at 188; do not start 189 before verdict.

- 2026-11-15: 188 APPROVED for ancestor retrieval only; verdict SHA256 88033355d6be3994e833259fadf4858e7c77ba9d3252ce8333a03ef57fb56ed5; request and ten artifact hashes verified, approval applied via --approve. Reviewer-only kernel-attribute cache identity filed as pending reports/defect-ledger/exllamav3-kernel-attribute-cache-device--r001.json (suspected, source only; reviewer_observation preserved despite validator limitation). Include with 189 request; never teacher input. No fix recorded: wait until dc69b167 is reached and approved. Canonical-use conditions: state suspected multi-device finding with undocumented per-device semantics limit; explain null scratch pointer when suh is passed without A_had after guard removal. Authored run unchanged. Earlier owed work remains open. Continue 189 detached on guidance 8.

- 2026-11-15: 189/001 request filed for ancestor retrieval only (SHA256 ea5e5eafd3448dd5a9dc854e00b91d5208b08d62b7a4eca58dd774191eb6f189). Unassisted guidance 8; one complete section, three complete parent files plus one beyond-EOF read, two ancestor prose reads. Ten identical replays, 2821 read-only blobs, ten artifact hashes and 44 unchanged implementation hashes verified. No execution. Includes reviewer-only kernel-attribute-cache-device r001 and verdict evidence for review; no later fix recorded. Earlier obligations remain open. Await verdict before 190.

- 2026-11-15: 189 APPROVED for ancestor retrieval only (clean); verdict SHA256 3322de37ed23fe9ca5f543419fc0ecf50a0da7be2039dcb4ac99a78e30a2fd94; request and all twelve artifact hashes verified, approval applied via --approve. No findings or canonical-use conditions. Kernel-attribute-cache-device r001 accepted as filed: reviewer_observation, suspected, source only, fixes empty; never teacher input. Earlier owed ledger and administrative items remain open. Continue 190 detached on guidance 8.

- 2026-11-15: 190/001 filed for ancestor retrieval only: reviews/requests/commit-000190-001.md (SHA256 c24ccc7f46dce723f22a7220537c23230162db56bbf7c9ce7547a58a1dc79408). Unassisted guidance 8; two complete sections, five complete parent files, one ancestor chapter. Eleven identical replays, 2828 read-only blobs, ten artifact and 44 unchanged implementation hashes verified. Scalar offsets over 255 shapes only; no tensor/CUDA execution. Two inherited suspected findings pending review (dtype dispatch and test argument mismatch); no new ledger candidates. Earlier obligations remain open. Await verdict before 191.

- 2026-11-15: 190 APPROVED for ancestor retrieval only; verdict SHA256 c6cba5f99c5d4c7b76446388bd1237b91a1ce0492f75bae1727fb773c03972d4; request and ten artifact hashes verified, approval applied via --approve. Both inherited findings confirmed. Ledger follow-up remains due: reconcile dtype-dispatch and test-argument identities, add c94905bf as affected where identities exist, otherwise file at established introductions. Canonical-use condition (reviewer-only): removing the Python flattening view removes its rejection of strides incompatible with flattening; native dense-pointer reads have no contiguity guard. Reviewer reports tree callers supply freshly produced or viewed contiguous tensors. Preserve the distinction between incompatible strides and all non-contiguous tensors; no execution demonstrated. Authored run unchanged; this observation never teacher input. Earlier owed ledger and administrative work remains open. Continue 191 detached on guidance 8.

- 2026-11-16 UTC: 191/001 request filed at reviews/requests/commit-000191-001.md (SHA256 26ea77bab0b75cdb3f4834acfb30d748fdd38c06d33715f735513146fd9bc013); unassisted guidance 8, ten artifact hashes and 44 unchanged implementation hashes verified, 19 identical replays, 2,835 shared blobs, 1/1 task sections and two ancestor prose reads. Partial generator reads, three separate run file-read scopes and truncated discussion openings disclosed. Two suspected findings (prefill-counted-as-output and empty-filtered-dataset), scalar checks only; no inference/dataset execution. No new ledger candidates; prior obligations remain open. Journal awaiting_full_review; no 192 before verdict.

- 2026-11-16 UTC: 191/001 APPROVED for ancestor retrieval only (clean); verdict SHA256 55cffd892d2f613aa54db5f43816d04724633cb31f7690584707fd60c502ed49. Request and all ten artifact hashes verified; approval recorded via --approve. Both findings confirmed, no canonical-use conditions. Ledger follow-up: prefill-counted-as-output and empty-filtered-dataset may be filed as suspected identities introduced at 460e201cc332ff93a4d65d7b1ca1f897ad372685; source/scalar evidence only, no dataset or generation execution. Earlier owed items remain open. Reviewer material stays out of teacher input; canonical/training false. Continue 192 detached on guidance 8.

- Guidance-9 trial decision read: reviews/verdicts/guidance-9-trial.decision.md. Trial only; walk default remains 8. Active 192 must finish validation and have its request filed before applying staged reports/guidance-9-implementation-001.patch (implementation files unchanged). Baseline captured in reports/guidance-9-v8-before.json; base hashes in reports/guidance-9-staging-001.json; verification script prepared at reports/guidance-9-verify-001.py. Next: verify base hashes, apply patch, verify exact paragraph and unchanged v8 inputs, run full host-enabled suite, file reviews/requests/guidance-9-implementation-001.md. No advancement pause. After acceptance run five fresh unassisted scratch trials at 184,188,190,189,178 under .teacher/trials/ with same cutoff evidence, no reviewer inputs, no journal attempts, publication or ancestor approval; file guidance-9-trial-001 with drafts/transcripts/coverage/tool and token counts. Reviewer success criteria remain administrative only. Adoption requires a later user decision.

- 192/001 request filed at reviews/requests/commit-000192-001.md; ten artifact and 44 implementation hashes verified before guidance-9 edits, 18 identical replays, 2,843 shared blobs. One task section, one complete ancestor chapter in two reads; partial generator.py read and recovered missing-path lookup disclosed. Two suspected findings, scalar-only checks; no run file reads. No new ledger candidates; older obligations remain open. Await verdict; no 193.

- Guidance-9 trial gate applied only after 192 validation and request filing; reviews/requests/guidance-9-implementation-001.md filed. Exact decision paragraph verified; v8 full opening/tools/effort byte-identical, legacy v5/v6 unchanged, 280 host-enabled tests pass (27.945s). Version 8 remains walk default, no advancement pause. All 191/192 request artifacts remain unchanged. Five trials await implementation acceptance, then run between walk commits under .teacher/trials/ with the recorded isolation requirements. No adoption.

- 192/001 APPROVED for ancestor retrieval only (clean); verdict SHA256 3a0becbfd09ac70458d04fe843348fcfd3225d5a3343c54bc9b515bfa0c56d47; request and all ten artifact hashes verified, --approve recorded. Both findings confirmed; no canonical-use conditions. Ledger follow-ups owed: new disabled-options-unbound identity introduced 33466d785591bdd69dd43821e22730a55f0067f9 (suspected, branch transcription); new reported-probabilities-not-final identity (suspected, source-only); root optional-output enabled-branch failure ends here when that identity is filed. Do not record any unbound-return fix before the walk reaches it. Reviewer hindsight excluded from teacher input. Older obligations stand. Guidance-9 implementation request is already filed, trials await its acceptance; walk remains guidance 8, continue 193 detached.

- Guidance-9 trial gate ACCEPTED; verdict SHA256 7c57c8c7bd79414079cd371945b13f8d43e632c728b07fa9aa6269f421c81a0c; request hash and all ten artifact hashes verified. Prepared reports/guidance-9-trial-supervisor-001.py (syntax checked; five source manifests are version 8 and unassisted). Do not launch while 193 runs: after it completes, inspect and file 193, then launch trials detached between commits. Supervisor snapshots walk artifacts and journal runs/approved_entries, creates fresh packets differing only in guidance_version=9, records tool/token metrics, stops on failure without retry, and queues completion. Targets 184,188,190 and controls 189,178; unpublished/unapproved, never ancestor context or journal attempts. No reviewer inputs. File guidance-9-trial-001 after completion. Walk stays on 8; no adoption or advancement pause.

- 193/001 filed at reviews/requests/commit-000193-001.md: 13 identical replays, 2,850 shared blobs, ten run/evidence hashes and 44 implementation hashes verified; two implementation changes are accepted guidance-9 gate. Guidance 8 unchanged. Partial job.py/generator.py coverage and scalar branch checks disclosed. Fix attribution and inherited probability finding await verdict; no new ledger candidates, older work remains. Launching accepted guidance-9 trials at 184,188,190,189,178 via reports/guidance-9-trial-supervisor-001.py between commits. Preserve journal runs/approved_entries and all walk packets/runs until its isolation snapshot completes; if 193 verdict arrives meanwhile, verify and track it but defer approval application/194 launch until trial completion. No adoption.

- 193/001 verdict verified: APPROVED for ancestor retrieval only (clean), SHA256 e9ea38e8ed61c813c381c119efd02e28759eb5db71261fbe78395b2974a4dbc3; request hash and all 14 listed artifacts match. No canonical-use conditions. Reviewer confirms cf220845799b12c9475232e2cb309db360f083d3 fixes the 192 disabled-options-unbound identity; record that fix and add 193 as affected to reported-probabilities-not-final when filing those owed records. Earlier ledger obligations stand. Guidance-9 trial supervisor remains running (184 in progress at check). Defer --approve and 194 launch only until its after-snapshot completes, preserving the required walk runs/approved_entries comparison. On queued trial completion: inspect/report trials, apply this verified approval with --approve, then continue 194 detached on guidance 8. No adoption, no advancement pause, no reviewer input to teachers.

- Guidance-9 trials completed and filed in reviews/requests/guidance-9-trial-001.md; 83 exact replays, identical walk snapshots. Assessment pending, not adoption; walk guidance 8. Commit 193 approval recorded; 194 authorized detached. Ledger follow-ups remain owed: cf220845 fixes 192 unbound-return and affects reported-probability identity.

2026-11-16: Guidance-9 trial assessment recorded: mixed/partial pass, not adoption or approval of trial outputs. Verdict reviews/verdicts/guidance-9-trial-001.md SHA256 c5e27b57c37bc03c23f4f80e33549a57cde55985bf670e1cee0e9632dfa4f0f5; request and all 72 artifact hashes verified. Walk stays guidance 8 pending user decision. Reviewer observations remain administrative only; 194 detached cycle already launched, no duplicate.

- 194/001 filed for ancestor-only review, guidance 8; two inherited RoPE findings, scalar bounds check only. Await verdict before 195; no new ledger candidates, older obligations remain open.

2026-11-16: 194/001 approved for ancestor retrieval only, clean; verdict SHA256 e0becf32ee24bb922d7ed4c8bb4f5f4b3b036e0025ccd429cd4539a2430c0d14, request and ten artifact hashes verified. Canonical/training remain false. Ledger follow-up: add 8b1fccf7 as affected to both 185 RoPE identities once filed; earlier owed work remains. 195 authorized detached on guidance 8.

- 195/001 filed for ancestor-only review on guidance 8. Two new suspected findings (cache rotation vector partition and unused test dtype) await verdict before ledger filing. Eight exact replays; ancestor search truncation disclosed. No 196 before approval; older ledger work remains open.

2026-11-16: 195/001 approved ancestor retrieval only; verdict SHA256 07c8cef9695b27a37bbc1c01309118df9728b12c35ab404ff0308a1905002545; request and ten artifact hashes verified. Both findings confirmed at source level, remain suspected without GPU execution. Canonical-use condition: empty order is accepted, order[0] reads empty storage and unsigned rotate_len-1 wraps; must be stated as a finding before canonical use, not merely a precondition. Reviewer-only observation, never teacher input; authored run unchanged. Ledger identities owed for vector partition and unused test dtype, introduced 965f5b2f; empty-order may be a second partition trigger with reviewer provenance. Earlier owed items remain open. 196 authorized detached on guidance 8; canonical/training false.

- Guidance-10 trial decision read (SHA256 `9d1dcc4ec73d6465424184fe490b32f8f830ff3ca6a785ed6757f3fd7741c5fb`). Trial only, walk stays 8; version 9 must reproduce unchanged. Patch staged, NOT applied while 196 runs: reports/guidance-10-implementation-001.patch, base hashes in reports/guidance-10-staging-001.json. Pre-edit actual v8/v9 openings captured in reports/guidance-10-v8-before.json and guidance-10-v9-before.json; verifier reports/guidance-10-verify-001.py prepared. After 196 completes validation and its request is filed: verify base hashes, apply staged patch, run verifier with PYTHONPATH=., run full host-enabled suite, file reviews/requests/guidance-10-implementation-001.md. Only after acceptance run three fresh unassisted unpublished trials 188,189,178 under .teacher/trials/, never journal/ancestor context, then file guidance-10-trial-001 with artifacts, coverage, tool/token counts. Reviewer criteria excluded from teachers. No walk pause set.

- 196/001 failed final annotation validation: source_inspection verification cited repo_grep and run only; no draft/coverage/review produced. Original run untouched and packet/provenance implementation hashes verified before guidance-10 patch. Recovery request reviews/requests/commit-000196-001.md filed; asking for fresh unassisted same-packet 002, no output repair, no retry launched, no advance to 197. Standing 113 exception specifically concerns corrupted call IDs, so not silently extended to evidence-type errors.
- Guidance-10 gate applied after 196 exited and recovery request filed. reviews/requests/guidance-10-implementation-001.md filed; 280 host-enabled tests pass (31.537s), exact decision text, v8/v9 full openings byte-identical, v5/v6 legacy unchanged, failed196 opening and all 7 request artifact hashes unchanged. Walk default stays 8, v9 unchanged. Wait for implementation acceptance before the three scratch trials (188,189,178); recovery of196 separately awaits verdict.

- 196 recovery CONFIRMED: reviews/verdicts/commit-000196-001.md SHA256 `e5956cc81c489c53a39fd8aaab091115caefed2800e9040a991070482198f253`; request and all 7 artifact hashes verified. Fresh unassisted 196/002 authorized on original immutable packet/opening; failed001 remains excluded. No failed annotation or reviewer material supplied. If002 fails, stop/request; no third attempt. Standing rule now permits ONE fresh same-packet unassisted retry after final citation validation failure (missing ID or wrong evidence kind); disclose next request, preserve failure. A second consecutive failure requires review. If a third occurrence of this same rule arises, propose an implementation change; no validator/instruction change now.

- Guidance-10 implementation ACCEPTED as trial gate: reviews/verdicts/guidance-10-implementation-001.md SHA256 `b4cb18c07c361c7c4eb04d5af2117b0585903da1c78f0dd6cc60ea21a70e1ff0`; request hash and all 11 artifact hashes verified. Walk stays 8, not adoption. Three fresh unassisted trials188,189,178 authorized under .teacher/trials/, no journal attempts/approval/ancestor context/reviewer input. 196/002 already running; no duplicate. Launch trials after196/002 request is filed, before another walk commit, to preserve snapshot isolation.

- 196/002 request filed: reviews/requests/commit-000196-002.md. Fresh unassisted same-packet retry, exact opening, failed001 preserved;19 identical replays,2877 shared blobs,1/1 task sections. Two inherited suspected native findings; partial model/science/RoPE reads disclosed, one AST file-read/scalar run separate from9 repo_reads. Await verdict; no197. Guidance-10 three-session supervisor launching between commits: hold walk journal/run mutations during its before/after snapshot, then file trial request and apply any queued196 verdict.

- 196/002 APPROVED for ancestor retrieval only (clean): reviews/verdicts/commit-000196-002.md SHA256 `f8bc955321da43b631f55beca23f468c861891989bd23463819a8666c85c61d4`; request and all14 artifact hashes verified. Failed001 remains failed/excluded. a39fdfc4 confirmed fix of185 normalization-settings identity; add196 affected to the two native185 identities. No canonical conditions. Reviewer note about a finding present only in failed001 is not a ledger candidate or teacher input. Approval application and197 launch deferred only until active guidance-10 trial snapshot completes (188 currently running); preserve journal/runs for isolation. On trial completion, inspect/file trial request, then apply this verdict as instructed and launch197 detached on8. Do not lose this authorization.
