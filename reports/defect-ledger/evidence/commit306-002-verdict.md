# Verdict: commit-000306-002 (teacher Sol, guidance 12, reviewer-assisted; fresh rerun)

Reviewer: Fable. Date: 2026-11-17 (20:30 UTC). Upstream `50d7dfd9` "Cohere2: Use float32 intermediate and MLP output".
Run: `.teacher/runs/commit-000306-002`. Packet: `.teacher/retrieval/000306-002`.

## Decision

**Approved for ancestor retrieval only. 306/002 is the entry in force for commit 306.** Canonical and
training stay false. It is a reviewer-assisted entry (coverage request `commit-000306-002.coverage.md`,
questions only) and joins the list of assisted entries in force. One carried finding (odd activation tail),
none new. 306/001 is kept as history. You may now record 307's approval, then continue at 308.

This time the entry makes the central check itself: the receiver is `x` in `x += y2`; Cohere2 does not
set `Embedding.out_dtype`, whose default is float, so the residual is float32; the attention result is half
and is added into it in place; the block returns float32; the next block's norm takes a half branch input
and the final norm narrows to half for the head. So the wider down output keeps its range, the parent
already had the wide residual and only narrowed the MLP result before the addition, and the mixed-type
addition is rightly labelled inference. It read the Llama entry (289) and relates the two changes.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium, 45 implementation hashes equal to the accepted
set, 58 evidence calls all cited and none bad, replay 58 of 58, final equals annotation, 305 of 305
ancestors, 4390 blobs, nothing after the cutoff. The packet is the one I compared with 000306-001; blob
links restored under the authorised recovery; no teacher rerun. Repair enabled, unused.

## Run checks (mine, tree at `50d7dfd9`)

Every point above agrees with what I read before ordering the rerun: `Embedding.out_dtype` default float,
`ParallelDecoderBlock.forward` (`y` half from the input norm, `x += y1`, `x += y2`, `to2` with no dtype),
no `out_dtype` on the block or attention, final `LayerNorm` with `out_dtype = torch.half`.

## Must fix before canonical use

Nothing.
