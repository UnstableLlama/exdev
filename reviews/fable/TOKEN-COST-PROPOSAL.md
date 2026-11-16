# Token cost: measurement and proposal

From Fable, 2026-11-15. The user asked for this ("i like that idea, can you implement it, and then carefully watch
the next few results, to make sure we dont suffer any quality loss"). The user's worry: at the present rate the
remaining walk needs about twenty weeks of token allowance. The measurement agrees.

Nothing here touches what a teacher sees. Packets, standing instructions, the teacher session, the evidence rules
and the review gate stay exactly as they are. Only the orchestration around them changes.

## What I measured (your thread's own log, commits 131 to 156)

| Per commit | Typical |
|---|---|
| Model calls | 15 to 31, about 22 |
| Input tokens | 1.7 to 5.2 million, about 3.4 million; 99.5% cached re-reads |
| Output tokens | about 4 thousand |
| Context at each call | grows from about 90k to 245k, compacts, starts again |

The thread has used 278 million tokens since 2026-11-14 and hit the usage limit at commit 153. About 2,100
commits remain.

Commit 156 as an example, fifteen calls at 113k to 126k context each:

- one to read `AUTHOR-INSTRUCTIONS.md` and the verdict; one to record the approval;
- five that only wait (`duration_ms` sleeps) and four that only poll a log;
- one each to start preparation, the walk, and validation plus replay;
- one to write the request, by copying `/tmp/exdev-file155.py` and substituting numbers.

So the cost is the number of calls times the size of the conversation each call re-reads. The work itself is small.

Two side findings: the per-commit scripts live only in `/tmp` (404 files, copied forward by text substitution),
so a machine restart or a context reset loses the procedure; and "follow-ups remain tracked" is, as far as I can
see, tracked in your conversation rather than in a file.

## Proposal

**A. One blocking driver for the mechanical part, in the repository.** A single command (for example
`python3 -m teacher.cycle --state reports/teacher-walk-001.json`) that does, in order and without the model in
between: preparation (discussion recovery, catalog selection, architecture trigger), the stop checks you make now
(truncation, a firing trigger, an unresolved bundle, a `curator_attestation` outcome, free disk), the walk,
validation, replay, and the hashes. It blocks until finished and prints one short summary: status, the counts and
hashes the request needs, and the paths of the draft and reports. It stops with a named status, having started no
teacher, whenever one of the checks needs judgement. Recording an approval is a second small command taking the
verdict path. No sleeping or polling by the model.

**B. A request skeleton generated from that summary.** The driver writes the mechanical parts of the request
(run, packet, upstream line copied from Git, validation counts, tool counts, catalog report, hash list). You write
the paragraphs that need judgement: what the draft explains, findings, ledger candidates, anything unusual.

**C. A durable tracking file.** One file (for example `reviews/ASTRA-TRACKING.md`) holding every owed follow-up,
the standing conditions from accepted implementations, and the procedure in a dozen lines. Updated when a verdict
adds or closes an item. `AUTHOR-INSTRUCTIONS.md` should tell you to read it after any context reset.

**D. A smaller conversation.** Once A to C are accepted, I will set `model_auto_compact_token_limit` in
`~/.codex/config.toml` so your conversation compacts at about 60k instead of about 245k, and restart your window
at a commit boundary. This is safe only after C exists, which is why it comes last.

Expected effect: about 6 calls at about 45k instead of about 22 at about 155k, roughly a tenfold reduction. This is
an estimate; I will measure it.

## What must not change (I will check each)

- Byte-identical packets and standing instructions for the same commit, old procedure against new. Show this for
  at least two already-approved commits by rebuilding into a scratch location and comparing manifests.
- The same stop conditions, each with a test.
- Every hash and count the requests carry today.
- The unassisted property: nothing from `reviews/verdicts`, the ledger or the tracking file reaches a packet.
- The suite passes, with the new tests added.

## How to proceed

1. Do not interrupt a commit in progress. Finish the current one and file its request as usual.
2. Then implement A, B and C, and file `reviews/requests/token-cost-implementation-001.md` with the report, the
   test result and the two rebuild comparisons. Do not start the next commit until that verdict.
3. After acceptance I apply D, and I compare the next five commits with the previous five: calls and tokens per
   commit, sections read, tool calls, ancestor reads, entry length, findings, and my own review results. If quality
   drops I will say so and we go back.

## Addendum after the first live cycle (159 and 160), 2026-11-15

First reading, your thread from the fixes verdict to the 160 request: 33 calls, 1.38M input tokens, largest
context 51k. Before: 156 took 14 calls and 1.72M, 157 took 17 calls and 2.24M, each for one commit. So about a
third of the old cost per commit, and the entries are as good as before.

What is left: of those 33 calls, about 20 only waited on the blocking command. The exec tool returns after at
most about 50 seconds, so a cycle of eight minutes still costs a call every 50 seconds, each re-reading about
45k tokens.

**Part E (proposed): do not wait at all.** Start the cycle detached and end your turn; let the cycle wake you.

- A small wrapper (for example `python3 -m teacher.cycle --state … --notify-thread <id>`, or a shell wrapper)
  that runs the cycle with output to a log under `reports/`, and when it exits for any reason, success, named
  stop or exception, queues one message to your thread with `codex queue --thread <id> --resume`, carrying the
  status and the summary path. The notification must be sent from a `finally`/`trap` so a crash still wakes you.
- You start it with `nohup … &` (or `setsid`), confirm it started, and stop. No polling.
- If the notification itself cannot be sent, the wrapper writes `reports/cycle-notify-failed-<position>.txt`.
  I will also notice a long silence from my side.

Nothing a teacher sees changes; this is only how the driver is launched. If you agree it is sound, implement it
after filing 161's request, file `reviews/requests/token-cost-detach-001.md`, and wait for that verdict before
162. If you see a reason it cannot work from your sandbox (for example `codex queue` not reachable from an
escalated command), say so in the request instead and we keep the current way.
