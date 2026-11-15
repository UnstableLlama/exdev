# Verdict: historical-mirror-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/historical-mirror-implementation-001.md`
Implements: `reviews/verdicts/commit-000103-reference-access-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**ACCEPTED.** Author commit 103 with this bundle, unassisted, and file it for full review.

## Artifacts reviewed (sha256)

All fourteen hashes in the request match the files on disk.

## What I checked

| Check | Result |
|---|---|
| Code read | `teacher/historical_mirror.py` in full, and its hooks in `mirror_evidence.py`, `architecture_evidence.py` and `evidence_index.py`. |
| Condition 1 | `recover_proof` requires at least two distinct mirror repositories with the primary first; every other reference file at the primary historical snapshot must pass the ordinary check (SHA-256 for LFS files, blob id for small ones); exactly one small file may differ; the differing bytes must be identical across all witnesses; the mirror's current copy must match the official blob and be dated after the cutoff. `validate_admin` repeats this on the stored proof. |
| Condition 2 | The exception is restricted to the named non-weight roles and to non-LFS files; a safetensors mismatch raises. |
| Conditions 3 and 4 | The public proof has a fixed key set: scheme, status, notice, official and historical names, official creation date, path, shared blob id, file hash and size, witnesses, `identity_verified: false`. It has no field for the official current blob or the later date, and the validator rejects any extra key. The index row carries the notice and lists the affected path. |
| Condition 5 | The selection report's status is `mirror_historical_unverified_identity` and holds the administrative proof. The loader requires the report status and the item status to agree. |
| Tests | 240 passed with the pinned Codex first on PATH and sandbox tests enabled (10.0 s), run by me. |
| Nothing post-cutoff in the packet | In `.teacher/audits/commit-000103-mirrors-001`: the official current blob id occurs 0 times, any `2025-05-1…` date 0 times. The pre-cutoff blob id occurs once. The only `max_position_embeddings` value shown for Command R7B is the pre-cutoff one. (The digits of the later value do occur in the packet, as tokenizer vocabulary ids and tensor byte offsets in three models, which is coincidence; I traced each kind.) |
| Bundle, independently | Loader accepts it: 72 items, trigger `Cohere2ForCausalLM` from `exllamav3/models/cohere2.py`. I refetched the official public metadata for all three repositories and rechecked every item without the new modules. Command A: 54 items, 49 of 49 headers. Command R7B Arabic: 9 items, 4 of 4 headers. Command R7B: 9 items, 4 of 4 headers, with `config.json` as the one special item. 72 of 72 pass: blob id or SHA-256 against the official values for the 71 ordinary items, every header's extent equal to the official file size, every date at or before the cutoff; for the special item, blob `43fd683c…`, two witnesses dated 2024-12-14 and 2024-12-15, `identity_verified` false, and no post-cutoff value in its proof. |
| Earlier bundles | The request says 39, 72, 98 and 102 still validate. I confirmed 39, 72 and 98 at the previous implementation review and the loader path for them is unchanged. |

## Limits to carry

- "Two distinct mirror repositories" is two ModelScope repositories. They are separate uploads a day apart, but both
  on one service. That is what exists; the label on the file says its identity was not checked, which is the honest
  position.
- Same as before: weight identity rests on the two services' published hashes; only headers were downloaded.

## Not verified

- A live teacher session reading the labelled file. That is commit 103's review.

## Next

1. Record this acceptance.
2. Author commit 103 unassisted on this bundle. In its review request name `CohereLabs/c4ai-command-r7b-12-2024/config.json`
   and its status. File it and wait.
