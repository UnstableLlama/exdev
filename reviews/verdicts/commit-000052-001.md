# Verdict: commit-000052-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000052-001`
Packet: `.teacher/retrieval/000052-001`
Upstream: `70e79cc880a40aa0aa7a41cc80c574622a658197` "Option to load tensors from memory"
Request: `reviews/requests/commit-000052-001.md`
Reviewed: 2026-11-13, working tree on top of `dfebc8a`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

The walk may continue from commit 53.

## Artifacts reviewed (sha256)

If any differ, this verdict does not apply.

- draft.json: `4cd98d09c70e8cb47850a4efb8868f17d62ad55bcea144eaead74d1504df9af3`
- draft.md: `68711c62f37dc33a07a158d29f449dab511c83dce101f9cf7a26aec66cc05551`
- raw-transcript.json: `021f21a8ced8ce218e04db6be557ac7ab5ec7d7e2a908bffde66c62be0c420c3`
- provenance.json: `c26d7e305766bc72e2dd3382490fc05687a7990b61cf3afd2c3dd0454a6529b2`
- coverage.json: `ad35cbba04012142e5e5d5f9f1612f74b9a6bc97ab7ce75bd67fe253879aa6aa`
- packet manifest (on disk): `78252e43d242a17c02c071837e84ab7d53d2f65ff8676b8f9f6d5f3a5c1638b8`
- unreferenced bundle: `e268c3b421e89c3029b5b57769f98aee287a31fa869e3eceee8b4e7279401d20`
- validation report: `0bb8a3616ae18203ad52c230aedf967d26d2affb2e1a056cb5cc1a1ac29f04aa`

All eight match the request.

## Run checks

| Check | Result |
|---|---|
| Evidence hashes | 12 of 12 ledger entries match the transcript tool results, with matching tool and arguments. Every call made is in the ledger. |
| Final message, Markdown, policy | Final message equals the annotation; `draft.md` equals the render; assessment passes with full review (non-mechanical path, two findings, an execution claim). |
| Provenance | Manifest matches provenance. 35 of 35 implementation hashes match the working tree. Standing instructions are byte-identical to the commit 44 run. |
| Packet ancestry (on disk) | Exactly 51 entries, equal to the 51 strict ancestors. Nothing outside the ancestors and the task. All 577 blobs hash to their names. No blob contains the ledger id or the word "hindsight". |
| Opening context | Message, author name, parent `d908052e` (commit 51) and task SHA match Git. Cutoff `2025-04-13T14:24:35+02:00` is the committer date, the first commit of the next day. |
| Catalog | Four rows: 1, 4, 7, 10. Issue 14 was opened at 21:50 UTC that day, nine hours after this cutoff, and is correctly absent. No snapshot timestamp is later than the cutoff. Issue 7 read. |
| Source claims | Verified against the diff and the parent file. `new_tensors` starts as None; `set_new_tensors` stores the object given, without copying or merging. `has_tensor` and `get_tensor` check the memory mapping first, by truthiness, then fall back to the file map. In `get_tensor` the device default moves above the memory check and a memory hit returns `.to(device)` at once, before the file branch where the BF16 conversion sits. Five methods and `close` gain `assert self.new_tensors is None`. `has_tensor_group` now tests each source separately with `any` over sources. Nothing in the task tree calls `set_new_tensors` yet. |
| Truthiness versus None | The draft's point is correct and easy to miss: an empty dictionary is skipped by the lookups (falsy) but still trips the assertions (not None). |
| Scalar check | Re-ran the recorded command: output identical. A group with `trellis` only on disk and `su`, `sv` only in memory is rejected although each key is individually available; a complete group in either source is accepted. |
| Ancestor attribution | Two entries read and linked: `b73e159b` (the tensor-listing change) and the root loading chapter. Both are described accurately. |
| Issue note | Issue 7's title is quoted exactly and the note says no connection is established. |
| Tests | Full suite: 197 passed with pinned Codex 0.167.0 first on PATH (re-run by me). |
| Commit 51 records | `reports/commit-000051-review-001.json` binds my verdict by path and the correct SHA-256 and keeps canonical and training false. Both canonical items are recorded. |

## The two findings

**split-source-group (suspected, behaviour change).** Holds by source and by the transcription. The draft is careful on the one thing it cannot know: it says the group would be recognised "if group detection is intended to reflect individual lookup availability" and that whether per-source completeness is intentional is unestablished. `Linear.is_exl3_storage` is the concrete caller that needs a multi-member group. Right strength.

**inherited-native-read-wait (suspected, defect).** This is the standing inherited-defect rule applied correctly. The root loading chapter, which the teacher read, already describes it: a failed reader sets `load_failed` without notifying, while the copy worker waits only for a non-empty queue. I checked `stloader.cpp` in the parent tree: the reader sets the flag at the failure point, and the wait predicate is `!dq.empty()` with no reference to the flag. This commit changes only `safetensors.py`, so the native path is carried over unchanged for disk reads, and memory hits skip it. The draft says exactly that, locates the finding at the parent tree and states that no failure was injected.

## Not verified here

- Nothing was executed against PyTorch or the native loader.
- That each of the other 49 packet entries is the currently approved attempt for its commit.

## Must fix before any canonical use (not blocking ancestor retrieval)

1. The entry does not say that `VariantSafetensorsCollection`, in the same file, gets no way to set a memory mapping, nor which collection class the model loader actually uses. Reach of the new option depends on that.
2. "sizing, listing, prefix reads and close explicitly assert" is right; add that `close` asserting means a collection with a mapping installed cannot be closed until the mapping is cleared, which is a lifecycle constraint on any future caller.

## Follow-ups

1. **Ledger handling of inherited findings.** The read-wait observation now exists in the root chapter's prose and as a structured finding here. If it is extracted to the defect ledger, it should be one defect with two observations and an introduction at the root, not a new defect introduced at this commit. The finding's own location (the parent tree's `stloader.cpp`) supports that.
2. Carried and still open: required fixes 1 and 2 before position 100; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

## Next

Record this approval locally with the original packet and continue the walk from commit 53.
