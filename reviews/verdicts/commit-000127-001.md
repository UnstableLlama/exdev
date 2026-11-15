# Verdict: commit-000127-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000127-001`
Packet: `.teacher/retrieval/000127-001`
Upstream: `9575f7d8b2afce94122bcf6141a63bfc01f207f2` "model_diff.py: Add KLD and top-K test to"
Request: `reviews/requests/commit-000127-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is correct. Two good observations: agreement is ordered-list
equality, not set overlap; and with `keep_b` set, the "A" figures describe a path that starts from B's activations.

## Artifacts reviewed (sha256)

All twelve hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 126 strict-ancestor entries; 1,841 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 126/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Cutoff | PR 26's snapshot ends with the comment of 2025-05-06T01:59:02Z. The cutoff is 18:23:47Z; the maintainer's "I added a KLD test to model_diff.py" is at 18:41:07Z and is not in the session. The request for a KLD evaluation, "eval/model_diff.py would be a good place to start" and "I'll write a quick KLD test" are all in earlier comments. The link is labelled inference. Correct. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 22, 24, 26, 27, 28, 29, 33, 34. Matches the thirteen open rows. |
| Architecture trigger | Does not fire. |
| Pipeline | WikiText-2 test text, model A's tokenizer, 2,048-token windows at stride 512; both models stepped module by module over the same ids; the new block runs after that loop on the final states. Correct. |
| Perplexity | `logits = x[i][:-1, :]`, targets `input_ids[a+1 : b+1]`, `log_softmax`, gather, sum and count, `exp(-sum/count)`. `chunksize` is `shape[1] * 10240 // shape[1]`, that is 10,240. Adding 1e-10 to every logit shifts them all equally and changes nothing. Correct. |
| Top-K | `torch.topk(logits, topk_max)`; label inclusion is `any` over the first K columns; agreement is `all` over the first K columns of A against B, so order matters. Counts are per position. Correct. |
| KL | Softmax of the full rows (final position included), `F.kl_div(torch.log(probs_a + 1e-10), probs_b, reduction='none')`, summed over vocabulary, mean over positions, then divided by rows; then the same with A and B swapped. Correct. |
| `keep_b` | `if idx < args.keep_b: state_a = state_b.clone()` is inside the module loop, before the new block. With a positive value the A metrics are computed on that altered path. Correct. Ancestor read is the entry for `25d9388b` (position 64). |
| Other edits | `del sa, sb` after each module's comparison; `--topk_max` default 5; two unused imports dropped. Correct where mentioned. |
| Execution | Recorded output: 2,047 of 2,047 positions in four iterations for a vocabulary of 32,000; 1,024 of 2,047 for a vocabulary of 1,024; ordered agreement false and set agreement true for [2,1] against [1,2]. Matches the prose. |
| Finding `ppl-vocabulary-bound` | Correct. `ppl` slices dimension 0 (positions) but loops `while b_ < logits_.shape[1]` (vocabulary). Suspected is right. |

## Reviewer-only notes (never to a teacher)

- **The finding is latent in practice.** Windows are 2,048 tokens, so there are 2,047 positions; every vocabulary the
  package supports is far larger, so the first iteration already covers every position and the later ones slice
  nothing. The entry says as much ("larger vocabularies instead produce unnecessary trailing empty slices") but
  files it as a plain defect. For the ledger it is a wrong loop bound with no effect on reported numbers at this
  commit.
- **Which way round the KL is.** `F.kl_div(log q, p)` computes KL(p || q). The line printed as "KL divergence (A, B)"
  is therefore KL(B || A) in the usual notation, and "(B, A)" is KL(A || B). The entry says "bidirectional" and does
  not name a direction, which is safe; a canonical entry should name them.
- The head's output is padded to a multiple of 128 and this script does not mask the padding columns the way the
  sampler does (`logits[..., actual_vocab_size:] = -inf`). For a vocabulary that is not a multiple of 128 the
  padding columns take part in softmax, top-K and KL. I did not work out their values or the size of the effect.

## Not verified

- Any execution on a model.

## Must fix before canonical use

1. Name the direction of each printed KL value.

## Follow-ups

1. Ledger: `ppl-vocabulary-bound` is approved as drafted; record it as having no effect for vocabularies of 2,047
   or more.

## Next

1. Record this approval.
2. Continue the walk at commit 128, subject to the disk note in `reviews/fable/DISK-AND-CACHE-PROPOSAL.md`.
