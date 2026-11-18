# Assessment: teacher-model-trial-002 (Sol against Astra on five harder commits)

Reviewer: Fable. Date: 2026-11-16. Assessment of five trial sessions; nothing here is approved as an entry.

## Result

**Sol reported every defect I had accepted from Astra on all five commits, added one true finding Astra had
missed, and stated nothing false that I found. One inherited behaviour-change item is in Sol's prose rather
than its findings list. The replacement hold is lifted.**

| Position | Astra's accepted findings | Sol | Result |
|---|---|---|---|
| 185 (RoPE kernel) | Settings overwritten; shared warp-sum store; padded-lane reads; two inherited reference failures; all-expert workspace; persistent-output contract | The first five, with the reference failures as two findings; the persistent-output item is described in the chapter text, not listed | Equal on defects; one inherited behaviour change not listed |
| 197 (cache defrag) | Draft cache not relocated; vector boundary; unused test dtype | The same three | Equal |
| 210 (empty tensor) | Partial reconstruction width leaves unwritten storage | The same, with a 16 by 144 case leaving 256 elements | Equal |
| 232 (unpadded MLP) | Odd activation tail reached by the new option | The same | Equal |
| 234 (Mistral 3) | Resize overflow reaches the new preprocessing | The same, **and** follows it to position ids past the vision angle table (112 by 8 grid, largest id 12217 against 12100 rows); reads headers and states projector widths | Better |

## Checks (mine)

- All hashes in the request match. Each run's provenance and server-confirmed runtime say `gpt-6.1-sol`,
  medium; each user message equals the approved run's.
- The findings Sol shares with Astra are the identities I verified in the 185, 197, 210, 232 and 234
  verdicts; I compared trigger and mechanism for each, not just names. 210's arithmetic (144 columns, 128
  written, 16 rows) is right.
- 234's addition is the reviewer observation I recorded at 234 and never gave to a teacher: the position id
  is `h * max_edge_features + w` with a 110 by 110 table, so a 112-patch side indexes past it
  (111 * 110 + 7 = 12217). Sol found it unaided. Its header statements (text and vision shapes, projector
  `[5120,1024]`, `[5120,5120]`, merger `[1024,4096]`) match the headers I checked at the guidance-11 trial.
- 197: Sol did not catch the two things I recorded Astra as missing there (the planner's recursion depth and
  the vector-tail defect reaching the quantized cache's scale arrays). Neither model has, unaided.

## Cost

148 tool calls against Astra's 130 (+14%). Sol's five sessions total 9.54M tokens, 95% cached input. At the
published Codex rates that is about 51 credits; the same token counts on Astra would be about 369. Astra's
own totals for these runs were not kept, so the true ratio is somewhere near the one-fifth seen at 213.

**Meter.** The weekly meter read 64% at 18:31 UTC and still 64% at 18:57, across these five Sol sessions and
the author session's work, which the request says is now also on Sol. Earlier today on Astra it rose about one
point every 12 to 13 minutes, and Astra's six-session trial (10.2M tokens) coincided with two to three
points. This is the first direct sign that the weekly limit is being drawn much more slowly; the meter's
1% resolution still prevents a precise figure.

## Weaknesses

One run per position; Sol ran at guidance 11 against Astra's 8 or 9, so paragraph F and the others may
account for part of 234's gain. Eight positions in all across both trials.

## Conclusion

No reason on this evidence to prefer Astra as teacher. With 243 (first walk entry on Sol, three true
findings) that is nine Sol entries reviewed, none with a false statement.

## Next

Replacements resume: 103 on Sol at the next opportunity, one at a time under the accepted plan. Walk
continues at 244.
