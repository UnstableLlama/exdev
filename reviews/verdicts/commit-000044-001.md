# Verdict: commit-000044-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000044-001`
Packet: `.teacher/retrieval/000044-001`
Upstream: `3a7b4895e45b1eb2f291f8b09b0a5dac569e984c` "Fix DeciLM n_heads_in_group attn config"
Request: `reviews/requests/commit-000044-001.md`
Reviewed: 2026-11-13, working tree on top of `dfebc8a`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

**Ledger record `exllamav3-decilm-kv-head-count--r001` ACCEPTED** as a fix-derived record with status suspected. I recommend a revision `r002` that raises it to confirmed on the evidence in "Independent confirmation" below. That is a recommendation, not a condition of this approval.

The walk may continue from commit 45.

## Artifacts reviewed (sha256)

If any differ, this verdict does not apply.

- draft.json: `a4aedcd7190c57248646f00abec6ef7f94de0d18c4b9f701b7da78ed3406e339`
- draft.md: `81d6fb55ec50c9bc43625c7e02a3dbff4584dc216ac2627e7761be6e86efbd14`
- raw-transcript.json: `9a5a9c9639c679a24a4ebf472711c97ad5e99a956d16cd647affb6560cbf8324`
- provenance.json: `ec2b44fbf046ce3ca45d56c246c58577f73517ced944e6ff5b6c9b7dad8cff1c`
- coverage.json: `1b57d21d21f7530d523982da849019be63521776f049946fe86b141ed38593d2`
- packet manifest (on disk): `2b59bcdeddbeee375534541a3312f2f526f48e76a60d449a4c51f86fef39fa8f`
- unreferenced bundle: `a97e50bc0c31c70227c2cd90494df25c5ca089995e7d36ab006b3dc67258e7fc`
- ledger record r001: `f97817b1ea31158b2940f494f74f2480d88cd10850269c4f990699f7d952c540`
- validation report: `895abd3062d1598f92b24521c15064f02c787deab77f071dab680d0e29bd36bb`

All nine match the request.

## How the boundary held across the whole episode

This commit closes the sequence that began at commit 39, so it is worth stating once:

- The teacher for commit 39 (both attempts) was never told about the defect and did not find it.
- The teacher here received nothing about it either. Its standing instructions are byte-identical to the commit 41 attempt 002 run; no packet blob contains the word "hindsight"; the ledger work started after this run finished.
- This draft identifies the defect on its own, from the task diff, and it identifies why the earlier corroboration missed it, from the ancestor entry: "With 64 query heads and group size 8, both formulas give 8 KV heads, illustrating how one dimension check can miss the distinction." That is the correct explanation, reached without help.

So the historical entry stayed historical, and the fix's entry carries the finding, as the retrospective policy intends.

## Run checks

| Check | Result |
|---|---|
| Evidence hashes | 9 of 9 ledger entries match the transcript tool results, with matching tool and arguments. Every call made is in the ledger. |
| Final message, Markdown, policy | Final message equals the annotation; `draft.md` equals the render; assessment passes with full review. The findings array is empty, which is right: the defect is in an ancestor, not in this commit. |
| Provenance | Manifest matches provenance. 35 of 35 implementation hashes match the working tree. Contract v5, guidance version 2, no reference objects (no trigger; confirmed). |
| Packet ancestry (on disk) | Exactly 43 entries, equal to the 43 strict ancestors. Commit 39's entry is attempt 002 and commit 41's is attempt 002. Nothing outside the ancestors and the task. All 514 blobs hash to their names. |
| Opening context | Message, author name, parent `df30645b` (the merge, position 43) and task SHA match Git. Cutoff `2025-04-12T16:10:04+02:00` is the committer date. |
| Catalog | Four rows: 1, 4, 7, 10. Issue 12 and PR 13 closed the previous night; issue 14 was created the next day. Correct. No snapshot timestamp is later than the cutoff. Issue 7 read. |
| Source claims | Verified. The diff changes one line, from `cfg_attn["n_heads_in_group"]` to `config.num_q_heads // cfg_attn["n_heads_in_group"]`. In `attn.py` at the parent, K and V projections are built with `num_kv_heads * head_dim` outputs, all three decode paths reshape K and V with `num_kv_heads`, and `self.gqa` is set when the two head counts differ and passed to the SDPA call. Attention-free blocks never reach the changed line; checkpoint keys and `cache_layer_idx` are untouched. |
| Labels | The reading of `n_heads_in_group` as "query heads sharing one KV head" is labelled inference, correctly: the source shows the new expression, not a specification. The draft says no external specification or checkpoint was inspected in this session and that the expression adds no validation of the divisor. |
| Scalar check | Re-ran the recorded command: output identical. Four cases of old and new head counts and widths. |
| Ancestor attribution | The teacher read commit 39's entry (attempt 002), describes it accurately, bounds what its dimension check established, and links it. |
| Tests | Full suite: 197 passed with pinned Codex 0.167.0 first on PATH (re-run by me). |
| Commit 41 records | `reports/commit-000041-review-002.json` binds my verdict by path and the correct SHA-256 and keeps canonical and training false. The advancement pause is cleared. |

## Ledger record r001

| Check | Result |
|---|---|
| Schema and evidence | `ledger.retrospectives.validate` and `validate_evidence` both pass. The five evidence files hash to the recorded values, and the three run copies equal the run's own artifacts. |
| Origin and status | `fix_derived`, `suspected`, with the note that the curator had prior reviewer hindsight. Honest and correct. |
| Introduction | Commit 39 (`75c7366b`). Correct: it is the first ancestor containing `decilm.py`. |
| Affected revisions | I checked each of the fix's ancestors with Git. The original mapping is present at exactly four: `75c7366b` (39), `4c7b1e29` (40), `41717916` (41) and `df30645b` (43). It is absent at the fix and at the branch commit `5e46530b` (42), which has no `decilm.py`. The record lists the same four, and its 40 "unaffected" SHAs plus those four account for all 43 ancestors and the fix. |
| Cannot be backdated | The record depends on the fix. `eligible_revisions` excludes it at commit 39's cutoff and at one second before the fix, and includes it one second after. `historical_context_eligible` is false. |
| Description | Accurate. The trigger is stated as the non-coincident case, which is the right condition. |

## Independent confirmation (reviewer computation, administrative only)

The record says no external specification was inspected. I checked the fix against real checkpoints, using only the reference objects already attached to commit 39 (pinned before that commit's cutoff): for every active attention block, compare the `k_proj` width in the tensor headers with what each formula predicts.

| Model | Query heads | Attention blocks | Original mapping matches | Fixed mapping matches |
|---|---|---|---|---|
| Llama-3_1-Nemotron-51B-Instruct | 64 | 54 | 44 | 54 |
| Llama-3_1-Nemotron-Ultra-253B-v1 | 128 | 64 | 0 | 64 |

Examples from 51B: block 1 has group size 16 and a K width of 512 (original predicts 2048, fixed predicts 512); block 7 has group size 64 and a K width of 128 (original 8192, fixed 128). The 44 blocks where the original also matches are the group-size-8 blocks, the coincident case.

So the defect is real and the fix matches the published weights. A revision `r002` could set status confirmed with this as evidence (the reference bundle hash `4849f07bafae2218c58b69856fa7f68bfe5c536a366758601658a9bb36c4704e` and the comparison). It must stay `fix_derived` and keep its dependency on the fix: the evidence predates commit 39, but I ran the comparison because I knew about the fix, and the retrospective document says a claim learned from a later fix is not backdated by writing a check against older material.

## Not verified here

- No model was loaded or run.
- That each of the other 41 packet entries is the currently approved attempt for its commit.
- The source-scan evidence file was hashed, not re-derived line by line; I re-derived its conclusion with Git instead.

## Must fix before any canonical use (not blocking ancestor retrieval)

1. The entry describes the fix but never says in one plain sentence that commit 39 shipped a wrong head count for any model whose group size differs from its number of groups. The Problem line states the old behaviour without calling it wrong. With the ledger record in place, a canonical entry can say it.
2. "No external DeciLM configuration ... was inspected in this session" is true, yet four were attached to commit 39 and are part of this commit's eligible past. A canonical entry should use them.

## Follow-ups

1. **Evidence does not carry forward.** Reference objects attached at commit 39 were not offered to this teacher, although they are older than this commit's cutoff and directly relevant. Whether reference evidence attached at an ancestor should be re-offered to later commits that touch the same architecture file is a design question for the user. Not urgent.
2. **Existing ledger files.** Five older files under `reports/defect-ledger/` have origin `reviewer_observation`, which `validate` rejects ("Unknown origin"), so `eligible_revisions` fails if it is given the whole directory. This predates today's work. Either the validator should know that origin or those files belong elsewhere.
3. Required fixes 1 and 2 from the implementation verdict remain due before position 100.
4. Carried and still open: the future-only "read every attached configuration" question; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

## Next

Record this approval locally with the original packet, record the ledger acceptance, and continue the walk from commit 45.
