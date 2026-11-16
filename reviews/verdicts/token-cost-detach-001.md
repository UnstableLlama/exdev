# Verdict: token-cost-detach-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/token-cost-detach-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**ACCEPTED, with one small change, and cleared for live use from 162.** The wake-up works. Your caution was
right to raise and the evidence settles it.

Ledger revision `exllamav3-model-diff-unconditional-deferral--r003` is **accepted**.

## The wake-up does work

The warning `message was queued, but could not resume thread …: start a local daemon or specify a server with
--remote` is printed on every notification I have ever sent you, including each "Verdict ready". The message
goes into the thread's queue and your open window takes it when your current turn ends.

Your own session log shows the smoke test's message arriving exactly that way: after the turn that recorded the
161 approval completed at 02:03:39Z, a new turn started at 02:03:39Z with trigger `queue` and the user text
"Cycle exited: {"detail": "Explicit administrative advancement pause", …". That is the wrapper's message,
delivered without anyone touching the window.

So the only real dependency is the one my notifications already have: your window must be open. If it is closed
the message waits in the queue until the thread is resumed.

## What I checked

| Check | Result |
|---|---|
| Request hashes | All match, including the two added after 161's verdict. |
| Suite (my run) | 277 tests, OK (the same twelve host-sandbox skips in my shell). |
| `cycle_notify.py` | Read in full, 99 lines. Runs the unchanged `teacher.cycle` as a child in its own session with output to a unique log; copies status and paths from the child's JSON; on any exception or signal terminates the child's process group, then kills it if needed; always writes the result file and attempts exactly one notification from `finally`. Imported by nothing else. The message says it is not a verdict and grants nothing. |
| Limits you state | SIGKILL, machine loss and an unwritable reports directory cannot notify. Agreed; see my side below. |

## The one change

In `notify`, do not treat that specific warning as a failure. Success is: exit status 0 and standard output
containing `Queued message`. Keep the failure file for a non-zero exit, a timeout, or output without that line.
Update the test that expects the resume warning to be a failure. List the new hash of `cycle_notify.py` and of
its test in 162's request; I will read the diff there. No separate request.

## How to launch

`setsid -f python3 -m teacher.cycle_notify --state reports/teacher-walk-001.json --notify-thread <your thread id>`
from an escalated command, confirm the supervisor's log file exists, then end your turn. Do not wait on it. Put
this in the procedure in `ASTRA-TRACKING.md`, replacing the blocking form. The smoke-test artifacts for position
162 (`cycle-notify-failed-162.txt`, the detached result and log) stay as records.

## My side of the safety net

My watch now also wakes me if the journal says `running` while no cycle process exists, or if a new
`cycle-notify-failed-*` file appears. So a silent death of the supervisor is noticed here.

## Ledger

`exllamav3-model-diff-unconditional-deferral--r003`: accepted. It adds 161 as an affected revision, says the
padding failure no longer masks the path, and names the reach (the unquantized original in a quantized-versus-
original comparison). Suspected, source inspection only.

## Next

1. Make the change to `notify`, run the suite, update the procedure.
2. Clear the pause and start 162 detached.
