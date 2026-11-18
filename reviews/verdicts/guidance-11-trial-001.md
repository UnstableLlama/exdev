# Assessment: guidance-11-trial-001

Reviewer: Fable. Date: 2026-11-16. This assesses six trial sessions. Nothing here is approved as an entry;
adoption of guidance 11 is the user's decision.

## Result

**The trial passes on three of four targets and partly on the fourth; both controls are clean.** I recommend
adoption.

| Position | Criterion (from the decision file) | Trial entry | Result |
|---|---|---|---|
| 213 | Q/K/V biases present; unused `mtp_layers` tensors | States Q bias width 4096, K/V 1024, and that `model.mtp_layers.0` tensors are stored and never requested | Met |
| 214 | Unprefixed names; no stored output head | States unprefixed names and shapes for two configurations. Mentions the output-head name and the embedding alternative but does not say that no `lm_head` is stored | Half met |
| 225 | Tower tensors; projector stored input-by-output | States tower shapes and projector `[1152, 2560/3840/5376]`, ties it to `transposed_load=False` | Met |
| 234 | Projector widths | States merger `[1024,4096]`, `linear_1 [5120,1024]`, `linear_2 [5120,5120]`, and that the hard-coded 5120 agrees | Met |
| 229 | Nothing added | No header or architecture claims, no finding (as approved) | Clean |
| 231 | Nothing added | No header claims; keeps the resize-bound finding (as approved) | Clean |

No trial entry describes layout as unestablished. No approved finding was lost: 234 and 231 keep theirs.

## Checks (mine)

- All 87 hashes in the request's table match.
- Each trial packet's manifest differs from the approved packet's only in `guidance_version`. Each trial
  session's system text is the approved run's plus a blank line plus F; every other initial input is equal.
  No reviewer wording found in any transcript.
- Every shape quoted above I checked against the bundled headers (213, 214, 164 for 225, 234): all correct.
  For 214 the headers hold no `lm_head` tensor in any of the five repositories, which is the fact the entry
  did not state.
- Walk snapshot before and after the trial is identical (same hash).

## Cost

149 tool calls against 123 for the approved runs, +26 (21%). Almost all of it is 225 (31 to 50). 213 +4,
234 +4, 214 -1, controls +1 and -1. Ten header reads in total across the four targets. Token totals for the
approved runs were not retained, so no token comparison.

## Weaknesses

- F was written with these four targets in view, and there is one run per position.
- The teachers sampled (one or two shards, first or last layers). F asks for "at least one reference checkpoint
  for each distinct configuration", and that is what they did; a defect confined to an unsampled shard would
  still be missed. My own header comparison at review stays necessary.
- 214's miss is a *negative* fact (a tensor the code names that is not stored). F asks "whether each exists";
  the teacher answered for the tensors it sampled and did not look for the head. I do not propose rewording now:
  one miss in four on one run each does not justify another trial. If it recurs, tighten that sentence.
- 234 did not notice that `consolidated.safetensors` holds a second copy of the weights under other names.

## Not assessed

Replay of the trial tool calls and coverage accounting: these are unpublished trials and I did not run them
through the replay.

## Next

Await the user's adoption decision. If adopted: change the walk default to 11 with an implementation request
(default only; versions 5 to 11 byte-identical), then file `guidance-11-reauthoring-plan-001` per
`guidance-11-reauthoring.decision.md`. The walk continues on 9 meanwhile.
