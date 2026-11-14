# Verdict: commit-000072-002

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000072-002`
Packet: `.teacher/retrieval/000072-002`
Upstream: `c44e56c73b2c67eee087c7195c9093520494d3bf` "Add GLM4 architecture"
Request: `reviews/requests/commit-000072-002.md`
Reviewed: 2026-11-13, working tree on top of `41010aa`

## Decision

**APPROVED for ancestor retrieval only.** Unassisted. 72/002 is the entry in force for commit 72; 72/001 stays rejected.
The walk may continue from commit 73.

Canonical and training remain false.

Not thin. With the full reference set the entry separates the three configuration shapes (ordinary 32B, 9B with
attention bias, Rumination with 8 KV heads and a longer position range), and it found a source-level defect on its own
that I had not looked for.

## Artifacts reviewed (sha256)

- draft.json: `d1575e613e8644eec6797550c26e103094069ff38149f372bf9d299f525e93a1`
- draft.md: `dae047f73af4e8d46ce62e670df719ad5c0ebddf7e182d6e4490671a341f85a7`
- raw-transcript.json: `c22816671682fd3c5a1fd8d7a19148483ab34f73bd2437a136461c5545ebea39`
- provenance.json: `c571beb58b228461ae56de34edba42d6c9a50cf7d40c8ae8714d7e43fe81eafb`
- coverage.json: `2f748a4f8c12f1e4f0b02c3ccf27a3a1cae1a8d6d7a05b1e502071e98a7a2ce8`
- packet manifest (on disk): `b1b0ae5d8a453ed98128d3e72723fb4dca265b136a1256c500f2fd96dc0bc97b`
- reference bundle: `0704b3f890f9e2806f418dfcab8eeb7d47c6b09cbfe98969fe4eb43ba78561cd`
- validation report: `5cb4321a1f269d4da78012a5728ba033325658c5906f951b1059b602b4de7084`

All match the request.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 30 of 30 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; assessment is full review; 39 of 39 implementation hashes match (one more than before: the accepted discovery module); exactly 71 strict-ancestor entries; all 1056 blobs hash to their names; both diff sections read in full; no content timestamp after the cutoff. |
| Unassisted, no hindsight | No coverage, no assistance flag. Standing instructions byte-identical to 72/001 and 71/001. No wording from the 72/001 verdict's reviewer-only section is in the packet. |
| Reference evidence | Six models, 94 objects, selected by pinned architecture string (see `reference-discovery-implementation-001`, accepted). The three Z1 revisions equal the ones I recovered independently. |
| Reading rule | Followed: all six `config.json` files fetched in full, every model named, the differences stated. |
| Source claims | Verified as for 72/001, plus: GPTJ rotates adjacent pairs and NEOX pairs across halves of the rotary region (read in `rope.cu`); the three preparation modes. |
| Config values | All match the pinned files, including Rumination's 8 KV heads and 131072 positions. |
| Finding `partial-rope-frequency-load` | **Confirmed at source level.** `rope_kernel` reads `inv_freq[threadIdx.x]` before any branch; the launch uses `head_dim / 2` = 64 x-threads; `partial_head_dim` is taken from `inv_freq.size(0) * 2`, and with factor 0.5 the tensor has 32 elements. Threads 32 to 63 read past it and then take the copy branch, so the values are unused. The kernel file is untouched by this commit; GLM4 is what reaches it with a factor below 1. "Suspected" is the right status: no run, and the entry says the compiler may drop the unused load. |
| Execution claims | Two `run` calls. One searches parent model files for key names and is reported as such. The other is integer arithmetic; replayed with identical output. |
| Catalogs | Unchanged from 72/001: six open rows, no closed rows. |
| Tests | 223 passed, run by me in this review. |

## Not verified

- Nothing compiled, loaded or run on a GPU.
- Tensor headers were available for all six models and were not fetched. The entry says so in its limits.

## Must fix before canonical use

Reviewer-only.

1. The headers of the three models I examined at 72/001 show only the fused `gate_up_proj` in every layer, with no
   separate gate or up tensors. The entry calls the fused key a "fallback", which is right about the code and
   understates the fact that it is the only form these checkpoints use. The same headers show `q_proj`, `k_proj` and
   `v_proj` biases in the 9B and none in the 32B, which settles what the entry leaves to "by their presence"; and that
   all tensors are BF16. A canonical entry should read the headers.
2. This is the first model definition to use what commit 71 added: the MLP's FP32 output now reaches the down
   projection's GEMM destination, and `interm_dtype = torch.half` is the value 71/002's finding says works. The entry
   reports the dtypes without the link; it read commit 39's entry and not commit 71's.
3. I held back the one assisted attempt for these two points. They are omissions of corroboration that the entry
   declares, not gaps that mislead a reader, and an unassisted entry with its own confirmed finding is worth more than an
   assisted one that adds them.

## Follow-ups

- The finding is in the draft only. When it goes to the ledger, establish the introducing commit (the kernel has two
  commits of history: the initial commit and `bcc09666` "RoPE kernel: Add GPTJ mode") and keep it one defect.
- Open thread, unchanged: `run` calls that read repository files.

## Next

Record this approval and continue the walk from commit 73.
