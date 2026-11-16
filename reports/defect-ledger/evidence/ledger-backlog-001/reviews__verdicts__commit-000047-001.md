# Verdict: commit-000047-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000047-001`
Packet: `.teacher/retrieval/000047-001`
Upstream: `28b09f96df750c5943dd7aec83e7a1b8d1785b69` "VRAM optimization: Don't unswap weights until after LDL decomp."
Request: `reviews/requests/commit-000047-001.md`
Reviewed: 2026-11-13, working tree on top of `dfebc8a`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

The walk may continue from commit 48.

## Artifacts reviewed (sha256)

If any differ, this verdict does not apply.

- draft.json: `a000b2abe72feed3938e382ab3bd237791027c0c5560e32470ce5b4d4ca6527b`
- draft.md: `5eb158efa7fc0f6841dc2ff6c21c56bea19d3dc6768fceaa1a2dedc0f0f9b080`
- raw-transcript.json: `724a68bebc8d2812f9dec84325714a1460772d6c4bf334c0516a51ddf5bd164a`
- provenance.json: `ecf45b06904ed264dc9ca008868723d3d58add25cb81b1c687984a224ba76587`
- coverage.json: `7cc03e9358cce6a17c9341f78e8efbf0feaba7019a870763547ac348cb25dc2a`
- packet manifest (on disk): `4e7bf7eedd438b12eac9458290836e7576d7d8f62dfe094317fe5f49e1ec48f6`
- unreferenced bundle: `3480fc974002024efb2019de552c39d64740c6e99cb85d0e3d7180573ec66d5d`
- validation report: `e6daef9ee5cf6eaa73427c1411788dc56cc94c04347b940cb2b4d768c8c4888b`

All eight match the request.

## Run checks

| Check | Result |
|---|---|
| Evidence hashes | 15 of 15 ledger entries match the transcript tool results, with matching tool and arguments. Every call made is in the ledger. |
| Final message, Markdown, policy | Final message equals the annotation; `draft.md` equals the render; assessment passes with full review (non-mechanical paths, a finding, an execution claim). |
| Provenance | Manifest matches provenance. 35 of 35 implementation hashes match the working tree. Standing instructions are byte-identical to the commit 44 run. |
| Task sections | Four changed files; all four diff sections read in full. |
| Packet ancestry (on disk) | Exactly 46 entries, equal to the 46 strict ancestors. Nothing outside the ancestors and the task. All 538 blobs hash to their names. No blob contains the ledger id or the word "hindsight". |
| Opening context | Message, author name, parent `e5f9f22a` (commit 46) and task SHA match Git. Cutoff `2025-04-12T18:14:55+02:00` is the committer date, the same instant as commit 46 (the two were committed together). |
| Catalog | Four rows: 1, 4, 7, 10; identical to commit 46's, as it must be. No snapshot timestamp is later than the cutoff. Issue 7 read. |
| Source claims | Verified at parent and task. The converter still calls `swap_cpu` on every target linear and no longer calls `unswap_cpu` before `convert_exl3`. `convert_exl3` reads `self.inner.swap_device` before dropping the FP16 wrapper, converts the (CPU) weight to float32 and passes the saved device on. `quantize_exl3` uses that device when given, calls `finalize_capture_H`, moves the stored `L` to CPU and the working `L` to the device, and only then moves the weight. `finalize_capture_H` restores a swapped `H`, returns early if already finalized, otherwise averages, regularises, applies the input transforms and calls `block_ldl(H, 16)`. The new argument defaults to None, which keeps `weight.device`. `swap_cpu` and `unswap_cpu` now return instead of asserting when called twice. |
| Size arithmetic | Re-ran the recorded command: output identical. 4096 by 4096 float32 is 67,108,864 bytes, 64 MiB. The draft presents it as illustration, not a measured saving. |
| Impact label | The claim that deferring the weight "should reduce overlapping GPU allocations" is labelled inference and says peak VRAM was not measured. Correct strength. |
| Issue note | Issue 7's title is quoted exactly and the note says it establishes no motivation. |
| Tests | Full suite: 197 passed with pinned Codex 0.167.0 first on PATH (re-run by me). |
| Commit 46 records | `reports/commit-000046-review-001.json` binds my verdict by path and the correct SHA-256 and keeps canonical and training false. Both canonical items are recorded. |

## The CPU-bias finding

I traced it independently and it holds by source:

1. `LinearFP16.swap_cpu` moves both weight and bias to CPU.
2. Before this commit, `unswap_cpu` moved both back before conversion. This commit removes that call.
3. `convert_exl3` takes the bias with `get_bias_tensor()` while it is still on CPU, and `quantize_exl3` moves only the weight.
4. `LinearEXL3.__init__` stores the bias as given, apart from a dtype conversion. `LinearEXL3.forward` does `x += self.bias` on the output.
5. The converter runs a forward pass through the converted module immediately afterwards to advance the calibration state.

So for a linear layer that has a bias, the converter's own next step adds a CPU tensor to a GPU tensor. The draft marks this suspected, states the trigger (swapped, biased, GPU-resident layer), separates the converter path from the test caller that never swaps, and says no biased-layer run was made. That is the right strength: the data flow is established by source; the runtime error is not observed.

I did not check whether upstream changed this later. That would be hindsight, and it is not needed to accept a suspected finding stated with its limits.

## Not verified here

- No conversion, profiling or GPU run. Torch is not installed in this environment, so the device mismatch was not reproduced.
- That each of the other 44 packet entries is the currently approved attempt for its commit.

## Must fix before any canonical use (not blocking ancestor retrieval)

1. The finding's reach is left as "affected model coverage ... not tested". The parent tree has evidence on which architectures carry biases (for example the comment in `exllamav3/models/qwen2.py` about detecting `*.bias` tensors). A canonical entry should say which registered architectures build biased linears, by source inspection.
2. The finding should be executed against the task tree before any canonical use, or kept explicitly as suspected.
3. The Problem line says the old order "kept the weight matrix resident during LDL decomposition". Resident on the GPU is what is meant; say so.

## Follow-ups

1. The teacher made no ancestor read and recorded no link, although commit 45 and earlier entries describe the same converter loop. Report-only.
2. Carried and still open: required fixes 1 and 2 before position 100; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

## Next

Record this approval locally with the original packet and continue the walk from commit 48.
