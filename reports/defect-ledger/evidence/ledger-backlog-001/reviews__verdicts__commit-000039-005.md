# Verdict: commit-000039-005

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000039-005`
Packet: `.teacher/retrieval/000039-005`
Upstream: `75c7366bb2e2a7671e38d079f9e5f54945b78006` "Support DeciLM (Nemotron)"
Request: `reviews/requests/commit-000039-005.md`
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**APPROVED for ancestor retrieval only, as a reviewer-assisted entry.** It supersedes attempt 002 for future retrieval. Attempts 003 and 004 stay rejected. Commit 39 is closed: no further attempt.

Canonical and training remain false.

Every statement I checked is true, each model is discussed separately, and each dimension claim is supported by a tensor header and not by a configuration field alone. The head-count mismatch is reported as a suspected defect from the entry's own header comparison. The coverage request did not state it.

## Artifacts reviewed (sha256)

- draft.json: `f2e4964e8395aa58eb347482e234d741cdab11e640fab8e8afca2689b0c96649`
- draft.md: `a75cb8e42f775fcdae49387a4db6dc146b28eae52b1634fa5b9b19c33b2b4eb0`
- raw-transcript.json: `b0f54f57faf6429a3b3f9d241850fa4be7b557976f73fbbfe293b21e514fe9bb`
- provenance.json: `eeafa8bd9b08c5ead53015d2f26e60ee6a4ecb6710f423d5720d4a74fdd643a4`
- coverage.json: `87838cf0a91b609020b209f08ad34d3a44bde7e9479dd09ef20ac306d36c5063`
- packet manifest (on disk): `87d3d3a54140ed879ea8bb37d6399de18a7618426f80344eba56e15d0cb14aee`
- coverage request: `761034b3089351c4bc7eac1cb9c1b715c7f009cf0138147feb1781560c2b148a`
- references bundle: `4849f07bafae2218c58b69856fa7f68bfe5c536a366758601658a9bb36c4704e`

All match the request.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 31 of 31 ledger entries match the transcript; final message equals the annotation; Markdown equals the render; assessment is full review; 37 of 37 implementation hashes match; exactly 38 strict-ancestor entries; all 745 blobs hash to their names; no evidence timestamp after the cutoff. |
| Assistance is recorded | Provenance and the review record both carry `reviewer_assisted`; provenance and the manifest carry the coverage request's path and hash. |
| Only the coverage request was added | The opening context differs from attempt 004 by one new field, `reviewer_coverage_request`, which equals the coverage file byte for byte. The standing instructions differ by exactly one sentence: "The reviewer_coverage_request field holds a reviewer's requests for coverage, not statements of fact." |
| No hindsight | No blob in the packet contains the later fix's SHA (`3a7b4895`) or a defect-ledger id. |
| Coverage items 1 to 5 | All answered. Four configurations read in full (both Ultra files over two pages). A header with an active attention block and an active feed-forward block read for each model; for Ultra v1 the teacher saw the first shard lacked the key/value tensors and read the second. Assertion acceptance and empty blocks stated per model. |
| Per-model facts | Recomputed from the packet's configurations and headers. 51B: block 0 matches; block 1 stores key/value width 512 against a declared 2,048; first rejected block is 11 (attention `replace_with_linear`); no empty block. Both Ultra models: block 0 stores 1,024 against a declared 2,048; feed-forward shapes match (5,376); no rejected block; 81 empty blocks, the first at 9. Super: block 0 matches in every shape; no rejected block; no empty block. All as the draft says. |
| Constructor claims | Checked against `decilm.py` at the task: head-dimension fallback, SiLU requirement, block-count assertion, the assertions and their order, `n_heads_in_group` passed directly as the key/value head count, the feed-forward width formula, cache index counting, tied-head fallback. Correct. |
| Parent-tree claims | `Attention` declares key/value width as heads times head dimension; `GatedMLP` shapes; `TransformerBlock.forward` with both branches absent returns the input through the dtype conversion; `Model.prefill` stops at `last_kv_module_idx`. Correct. The truncated reads of `attn.py` and `model.py` reached the cited lines. |
| Converter claim | Correct at the parent: capture is guarded by `len(qmaps) > 0`, allocation by `if linears`, and `num_bits / module.weights_numel()` is unguarded. The draft marks the finding suspected and conditions it on the empty save returning normally. |
| Scalar check | Re-ran the recorded command: output identical. |
| Tests | 209 passed with Codex 0.167.0 first on PATH. |
| Dependents | Astra's scan is right as far as I can tell from earlier reviews: only `commit-000044-001` read attempt 002's prose. |

## Not verified

- Tensor shapes beyond the blocks the entry names. The entry says its comparison covers selected blocks.
- Whether saving an empty tensor dictionary succeeds. Nobody ran it; the entry says so.
- Any model load, conversion or inference.

## Must fix before canonical use

Reviewer-only. None of this goes to a teacher.

1. The entry is reviewer-assisted. Whoever selects entries for canonical use or training decides whether assisted entries qualify.
2. The head-count finding says the declared widths disagree with the headers and stops there. It does not say what `n_heads_in_group` means. The stored widths in the sampled blocks equal query heads divided by that field, times the head dimension. A canonical entry should say so or say it was not established.
3. The finding's trigger names "block 1 of the inspected 51B model". True as a statement about the declaration, but that model fails the block 11 assertion during construction and never reaches a load. One clause would make that clear.
4. The 51B comparison covers blocks 0 and 1. That model has other group sizes on later blocks which the entry did not sample.
5. The failed fetch of the Ultra safetensors index is in the transcript and not mentioned in the entry. It was not a configuration read, so the guidance did not require it.

## Follow-ups

- Defect ledger `exllamav3-decilm-kv-head-count`: this entry is an authoring-time observation at the introducing commit. Record it as another observation on the same defect, not a new one.
- The empty-block finding is the same hazard attempt 004 reported; one defect, two observations.

## Five attempts, for the record

| Attempt | Configurations read | Headers read | Head-count line |
|---|---|---|---|
| 001 | none offered | none | reported as written |
| 002 | 1 of 4 | 1 | corroborated on the coincident model |
| 003 | 1 of 4 | 1 | mismatch found on one model |
| 004 | 4 of 4 | none | code's reading stated as fact |
| 005 (assisted) | 4 of 4 | 5, covering all four | mismatch found on three models, labelled suspected |

## Next

1. Record this approval, mark attempt 002 superseded for future retrieval.
2. Author `commit-000044-002` (no coverage request; its packet uses 39/005), then stop for full review.
3. Then `commit-000045-002` and `commit-000055-002` with their coverage files, each reviewed before the next. Then resume at commit 62.
