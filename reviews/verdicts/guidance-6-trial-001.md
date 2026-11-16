# Verdict: guidance-6-trial-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/guidance-6-trial-001.md`
Decision acted on: `reviews/verdicts/guidance-6-trial.decision.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**Trial assessed: two of the three known gaps found, the third not, the control clean.** This is an assessment
for the user. It approves no trial output for any use and adopts nothing. The walk stays on guidance 5 until the
user decides.

The trial was run as the conditions required.

## Conduct of the trial

| Check | Result |
|---|---|
| Request hashes | All match. |
| Manifests | For all four positions the trial manifest differs from the source manifest in `guidance_version` and nothing else (mine). 163's source is 163/001's packet. |
| Instructions | For all four, the trial's system text is exactly the baseline's plus a newline plus the approved guidance text (mine). |
| No reviewer material | No trial transcript contains `reviews/verdicts`, a coverage request, or the name of the guard at issue in 154. |
| Isolation | Trial packets and runs are under `.teacher/trials/guidance-6-001/` only; the journal has no trial run and no trial entry among the approved ones. |
| One session each | As reported; first results kept. |

## Results against the three known gaps

| Position | Known gap | Found under guidance 6? |
|---|---|---|
| 163 | One configuration class left on the old form, breaking that architecture | **Yes.** The trial entry records `qwen3-moe-component-migration` unassisted, with the same mechanism, reach and stand-in check as the reviewer-assisted 163/002, and no false sentence about all constructors. It read three ancestor entries. |
| 158 | Differences from the near-identical earlier model file | **Yes, the main one.** It read the Qwen3 MoE entry and states that Mixtral does not set `calibration_all_experts` and therefore calibrates with ordinary routing, and it carries the inherited fused-shape finding correctly marked as not triggered by Mixtral's own conversion. It does not mention the missing query and key norms or the half-precision output against Qwen3 MoE's float. |
| 154 | The eligibility guard the other two callers of the deferred-load bracket apply | **No.** The entry is as accurate as the approved one and reads two ancestor entries, but they are the script's own history. It never looks at how the model loaders use the bracket it copies. |

## The control (156)

Not padded with speculation. No finding is invented. It is about a third longer (415 words against 312), reads
two ancestor entries and says neither records a defect in the changed code, and adds one true observation the
approved entry did not make (that the new `****` entry is what makes `[black]` available as a tag). Everything
I checked in it is true.

## Cost

Tool calls, trial against approved: 154 10 to 9; 158 35 to 21; 163 23 to 18 (the approved one being the assisted
attempt); 156 6 to 4. In total 74 against 52, about 40% more. Token use of teacher sessions is not recorded.
Against that: 163 needed a rejection and a second, assisted session under guidance 5.

## What I conclude

1. Paragraphs A and B do what they were written for. C was not exercised by these four commits (its case is
   162).
2. **Wording of A.** It says "search the whole task and parent trees". The tools give a teacher the parent tree
   and the task diff, not a searchable task tree, and the 163 trial said so and worked around it. For adoption
   A should say "search the whole parent tree, read together with the task diff". That changes the text the
   user approved, so it needs the user's agreement.
3. **154 is a different kind of gap.** The change starts using an existing mechanism from a new place; the
   defect is in what the existing users of that mechanism do around it. None of A, B or C asks for that. A
   fourth paragraph would: when the task starts calling an existing function or mechanism from a new place, find
   its existing callers in the parent tree and compare the conditions, guards and error handling around those
   calls with the new one. That is new text and would need the user's approval and its own trial (154 and 140
   are the two known cases).

## Next

Nothing for Astra until the user decides. Continue the walk at 166 on guidance 5.
