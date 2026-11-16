# Verdict: commit-000192-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000192-001`
Packet: `.teacher/retrieval/000192-001`
Upstream: `33466d785591bdd69dd43821e22730a55f0067f9` "Generator: Add probs and top tokens/probs"
Request: `reviews/requests/commit-000192-001.md` (sha256 `d73e62c7456a28b312abb0e9023c0080219a6d5f93bbbef73013300b48b44906`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and both findings are true as stated. The entry correctly treats the root
entry's optional-output finding as changed by this commit rather than carried over: the enabled branches now
work and the disabled path is the one that breaks.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 18 of 18 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 191 strict-ancestor entries; 2,843 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 18 of 18 recorded tool calls identical, including the `run` call and one recorded failed lookup. |
| Unassisted | Standing instructions byte-identical to 191/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-25T17:59:49Z; my query agrees. One closed row by path alone, selected, described as a shared-file inference. |
| The change | When either option is on, a float softmax of the logits is taken; the chosen token's probability is gathered when `return_probs` is set; a full descending sort is sliced to `return_top_tokens` when that is positive. The `None` assignments now sit inside the outer `if`. Correct. |
| Finding: unbound when disabled | The constructor defaults are `return_probs = False` and `return_top_tokens = 0`; the outer `if` is then skipped and the `return` names three variables that were never assigned. `Generator.iterate_gen` is the one active caller. True; introduced here; it is the default path. |
| Finding: not the final distribution | The parameter documentation says "final sampling probabilities". The softmax is taken from the `logits` argument after `sampler.forward` returns; the sampler masks padded vocabulary in place but clones before applying blocked and allowed tokens and does temperature and min-p on separate state. True. |
| Execution | Branch transcription over the four option combinations and a two-logit probability example; labelled as stand-ins. |

## Reviewer knowledge (hindsight, never to a teacher)

The next upstream commit, `cf220845`, three minutes later and with the same title, moves the three `None`
assignments above the `if`. When the walk reaches it, the entry should recognise the fix from this entry.

## Not verified

- Any generation run; multi-sequence shapes.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: a new identity for the unbound-return finding (suspected; branch transcription; introduced at
   `33466d78`); a new identity for the reported-probability finding (suspected, source-only). The root
   optional-output identity, when filed, should say its enabled-branch failure ends at this commit. Do not record
   a fix for the unbound return before the walk reaches it.
2. Earlier owed items stand; `guidance-9-implementation-001` is expected.

## Next

1. Record this approval with `--approve`.
2. Proceed to 193.
