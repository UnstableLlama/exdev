# Verdict: commit-000170-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000170-001`
Packet: `.teacher/retrieval/000170-001`
Upstream: `2432c64e68ba4e3cbeccc3eaeba44c97731132d3` "model_init: Add override for default cache size"
Request: `reviews/requests/commit-000170-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. No findings, and none are missing. The entry read 169's entry, says that the
unsupported-keyword failure recorded there is removed by this change, and checks the old default, the override,
the explicit option and the `cache = False` case.

Ledger record `exllamav3-unsupported-cache-default-argument--r001` is **accepted**.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 10 of 10 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 169 strict-ancestor entries; 2,622 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 10 of 10 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 169/001's. Guidance 5. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path or the tracking files. |
| Catalog | Twelve open rows at 2025-05-17T14:58:32Z; my query agrees. One closed row, by path, selected. |
| The change | `add_args` gains `default_cache_size = 8192`, documents it, and uses it for both the default and the help text of `-cs`. Correct. |
| Callers (mine) | Four in the task tree: `humaneval.py` and `chat.py` keep 8192, `ppl.py` passes `cache = False`, `longctx.py` passes 65,536. All agree with the new signature. |
| What it repairs | The call in `longctx.py` that raised at 169 now binds. The commits are twenty seconds apart. Correct. |
| Execution | Recorded output: the parent raises; with the change applied to the extracted helper, 8192 by default, 65,536 with the override, 4096 when given explicitly, no cache fields with `cache = False`. Matches the prose. |

## Ledger

- `exllamav3-unsupported-cache-default-argument--r001`: accepted. Please file r002 with the fix at `2432c64e`,
  reviewer-confirmed by source inspection; affected revision 169 only.

## Reviewer-only notes

- Hindsight confirmed: this is the uncommitted half of 169.

## Not verified

- A run of `longctx.py`.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. The ledger revision above.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval with `--approve`.
2. Continue at 171 on guidance 5.
