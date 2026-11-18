# Assessment: teacher-model-trial-001 (GPT-6.1-Sol as teacher)

Reviewer: Fable. Date: 2026-11-16. Assessment of three trial sessions. Nothing is approved as an entry and
nothing is adopted; the teacher model is the user's decision.

## Result

**On these three commits Sol's entries are as accurate as Astra's and slightly more thorough. Sol used more
tool calls and, where both were measured, more tokens. Whether it uses less of the account's quota is not
shown by this trial.**

| Position | What the Astra entry has | Sol entry | Result |
|---|---|---|---|
| 213 | Q/K/V biases, unused MTP tensors, shapes for two checkpoints | Same facts, all correct; adds the stored `lm_head`, per-model position limits, and that the compile path does not carry the MTP tensors | Equal or better |
| 231 | Floating-point overshoot of the bounding box | Same finding with a concrete case `(1,97)` in a `(112,84)` box giving `(14,91)`, and a 40,000-pair sweep with 1,563 overshoots | Equal |
| 239 | `None` class placeholders reach `isinstance` and raise | Same finding; also notes the GPTQ block resets all three names, transitive misses are caught, and the llama.cpp adapter's broader bare `except` | Equal or better |

Nothing invented in any of the three. Limits sections are honest in all three.

## Checks (mine)

- All hashes in the request match. Provenance and the server-confirmed runtime record `gpt-6.1-sol`, medium,
  `trial_only`. For 213 and 239 the system and user messages are identical to the Astra comparison run's;
  for 231 the user message is identical and the system text differs only by guidance (9 against 11), as
  disclosed.
- 213: every shape and config value I checked is right (biases 4096/1024/1024, `lm_head [151680,4096]`, MTP
  `input_proj [4096,8192]`, BF16 throughout, 65536 positions for RL-0530 and 32768 for the others, theta
  640000, untied embeddings, `compile.py` calling `get_additional_compiled_tensors`).
- 231: I recomputed the helper's arithmetic. `97/(97/84)` is `84.00000000000001`; the result is `(14,91)`;
  my own sweep of 1 to 200 on both axes gives exactly 1,563 overshoots.
- 239: the finding is the one I verified for the approved entry.
- `codex_transport.py` follow-up: the Astra path copies the catalog bytes again; hash bound in the request.

## Cost

| Position | Astra calls | Sol calls | Astra tokens | Sol tokens |
|---|---:|---:|---:|---:|
| 213 | 29 | 40 | 1.60M | 2.53M |
| 231 | 7 | 9 | not kept | 0.27M |
| 239 | 17 | 22 | not kept | 0.86M |

Calls +34% (71 against 53). On the one paired token figure Sol used 58% more, about 95% of it cached input
in both cases.

**Quota (my reading of Astra's Codex session log, which records the account's weekly meter to the nearest
1%).** The three Sol sessions (18:02 to 18:10 UTC, 3.65M tokens) did not move the meter: 62% before and
after. Astra's six guidance-11 trial sessions (16:41 to 16:58, 10.2M tokens) coincided with a rise of about
2 to 3 points, which also includes Astra's own orchestration. At that rate Sol's sessions would have cost
about 0.9 of a point, which the meter cannot distinguish from zero. So this is compatible with Sol being
cheaper per token and does not prove it.

**The larger observation:** today the meter rose steadily, about one point every 12 to 13 minutes from 15:00
to 18:00 UTC, whether or not a teacher session was running (for example 17:00 to 17:23, with no teacher
running, it rose two points). Teacher sessions occupied well under a third of that time. Astra's own Codex
session, which reads requests, writes requests and supervisors and runs the suite, appears to be a large
share of the spend, possibly the larger one. Changing only the teacher model would not touch that.

## Weaknesses

Three positions, one run each. Two of the three are small commits. Sol ran with a cloned Astra catalog
profile. No hard commit (a new architecture with a subtle defect, or a kernel change) was tried.

## Recommendation to the user

Quality is not the obstacle on this evidence. Before switching, measure quota properly: one more Sol session
on a large commit with the meter read immediately before and after and nothing else running. Separately,
consider the orchestrator's share.

## Next

Await the user. Walk continues on Astra; replacements stay on hold.
