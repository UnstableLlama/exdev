# Decision: a second, harder comparison of Sol against Astra as teacher

Recorded by Fable (reviewer) on 2026-11-16.

## The user's words

After the switch to Sol was accepted the user wrote:

> i mean at lea=st try those, test it again

and, when I had misread that as a request to test the Codex model command:

> i mean have sol run some of the code walk that astra already did and compare results

## What is decided (my reading, stated so the user can correct it)

More commits that Astra already authored are authored again by Sol and compared, beyond the three of
`teacher-model-trial-001`. I read it as the teacher role (the sessions that write entries), since that is
what can be rerun and compared; the author's Codex session cannot be replayed this way. I chose harder
commits than the first trial, because that trial's stated weakness was that nothing hard was tried.

## The trial (mine)

Sol, medium, guidance 11, unassisted, on copies of the approved packets with only `guidance_version` changed,
under `.teacher/trials/teacher-model-001/` (new packet and run directories; the existing gate already confines
trials there and keeps them unapprovable). No reviewer material, prior drafts or ledger text.

| Position | Commit | Why |
|---|---|---|
| 185 | New RoPE kernel with fused head norm | CUDA kernel; Astra reported three new defects |
| 197 | Generator: periodically defragment paged cache | Generator logic; one new defect plus inherited ones |
| 210 | Reconstruct to empty tensor | A removed initialisation; one defect |
| 232 | GatedMLP: allow unpadded FP16 tensors | A new option reaching an old recorded defect |
| 234 | Support Mistral 3 architecture | New architecture with headers; one inherited defect |

Request `teacher-model-trial-002`: drafts, transcripts, coverage, tool calls and token totals beside the
approved runs' figures, findings side by side. Disclose that the approved runs were at guidance 8 or 9.

What I will judge (reviewer knowledge; must not reach a teacher): for each position, whether Sol reports
each finding I accepted from Astra, whether anything it adds is true, whether anything is false, and
whether it catches what I recorded Astra as missing (197).

## Meanwhile

The switch stands (`teacher-model-sol-adoption-001` accepted): the forward walk continues on Sol, each entry
with my full review. **Replacements wait again until this trial is assessed**, since they overwrite the
entry in force; this trial is short.
