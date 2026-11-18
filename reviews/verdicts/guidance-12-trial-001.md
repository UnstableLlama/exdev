# Assessment: guidance-12-trial-001

Reviewer: Fable. Date: 2026-11-16. Assessment of six trial sessions (Sol, medium). Nothing is approved as an
entry; adoption of guidance 12 is the user's decision.

## Result

**Partial pass. The added sentence does what it says for the checkpoint a teacher opens, and all four target
entries now state the head-loading mechanism. It does not make teachers compare that tensor across all
reference checkpoints, so differences between checkpoints are still missed. Controls are clean. Cost is
noticeably higher on architecture commits.**

| Position | Criterion | Guidance-12 entry | Result |
|---|---|---|---|
| 214 | No stored output head | Reads the complete 1B header: "`lm_head.weight` is absent; `Linear.load` can instead load `model.embed_tokens.weight` through `alt_key`"; also notes absent biases and scale tensors | Met |
| 98 | No `lm_head` anywhere; tied path always | States the mechanism and that `lm_head.weight` is absent from the Aya-23-8B shards it read. Not stated for the other nine repositories | Partly met |
| 110 | Split between checkpoints that store `lm_head` and those that rely on the fallback | Reads the complete 0.6B header, states the mechanism ("Linear tries the primary `lm_head` weights before `model.embed_tokens`. Qwen3-0.6B contains both, so its explicit head is used"). Does not find that 4B and three Base models store none | Mechanism restored; split not found |
| 103 | No `lm_head` anywhere; tied path always | States that the alternate key "supports a missing head" and expressly declines to say the head is absent, because it read representative shards only | Not met |
| 243 | Nothing added | Same three findings as the approved entry, no header claims | Clean |
| 245 | Nothing added | No findings, no header claims | Clean |

## Checks (mine)

- All hashes in the request match; each trial packet's manifest is at guidance 12; provenance `gpt-6.1-sol`.
- The header statements quoted above agree with the headers I checked at 98/002, 110/002 and the
  guidance-11 trial.
- New and true at 98: the constructor's test is `has_tensor("lm_head")`, an exact-name test that a real
  checkpoint's `lm_head.weight` does not satisfy, so the alternate key is always installed when tying is on;
  `Linear.load` tries the primary key first, so an explicit head still wins. I confirmed both in the source.
  This is the detail I recorded as reviewer knowledge at 234.
- Findings retained: 98 keeps the Q/K normalisation finding (and adds two); 110 keeps the FP8 point, now as a
  finding; 103 keeps the mismatch diagnostic and moves the non-applicable partial-rotation item to prose.
- What it would have changed: a guidance-12 entry like this one for 110 states the tied-head mechanism that
  110/002 dropped, so it would not have been declined on that ground.

## Cost

265 tool calls against 218 for the comparison runs (+22%). The one paired token figure, 214, went from 0.88M
to 2.46M, because reading a complete header is expensive. On Sol that is about 13 credits against about 5;
the increase applies to architecture commits only.

## Weaknesses

Wording written with these targets in view; one run each; at 98 and 214 the comparison run was Astra's, so
model and wording both changed.

## What remains uncovered

Whether a tensor is present in *each* reference checkpoint (the 110 split, the 98 and 103 "none anywhere").
Teachers read one checkpoint per configuration, as paragraph F tells them to. Closing that would need either
a further instruction to check branch-deciding tensor names in every reference checkpoint, at more cost, or
it stays with the reviewer, who has all headers on disk and checks them anyway.

## Recommendation

Adopt 12. It restores the mechanism in every target, produced one clean pass and one new true observation,
harmed nothing, and costs little on Sol. Leave the cross-checkpoint comparison with the reviewer for now.

## Next

Await the user's decision. Replacements stay paused until then.
