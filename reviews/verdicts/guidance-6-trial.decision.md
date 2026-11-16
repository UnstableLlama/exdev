# Decision: trial of guidance version 6

Recorded by Fable (reviewer) on 2026-11-15.

## The user's words

After I reported that 163/001 was rejected and that the teacher repeatedly misses things in code a change relies
on but does not touch, I asked whether to draft a guidance line. The user asked "do you think we should?"; I
said yes and described a trial; the user answered:

> yes that sounds good

I then showed the exact wording of three additions (A, B and an optional C) and the trial plan. The user asked
"should i?"; I recommended approving all three; the user answered:

> ok approve

## What is approved (my reading, stated so the user can correct it)

A trial of the three additions below as `guidance_version` 6. **Not** adoption for the walk: guidance 5 remains
the walk's guidance until I report the trial result and the user says to adopt.

**A. Changed contracts.**
When a change alters what a function, constructor, attribute or parameter accepts, returns or stores (its type,
shape, name or meaning), search the whole task and parent trees for every other definition, subclass, caller and
reader that supplies or consumes it, including files the task diff does not touch. Inspect each one and say, case
by case, whether it agrees with the changed form; name any that the diff leaves on the old form and state what
the inspected code would do with it. A search limited to the changed files cannot establish that the change is
complete.

**B. Earlier entries for code the task builds on.**
When the task modifies, copies or closely follows a file, class or function that an earlier commit introduced,
find that commit's entry with the ancestor tools and read it before finalizing. Say which entries you read and
what they establish about the code the task relies on, including any guard, precondition or recorded defect; if
you read none, say so.

**C. Edits that depend on each other.**
When one commit makes several edits, check whether any of them supplies a precondition another needs before
describing them as independent.

## The trial

1. Astra adds the three paragraphs, verbatim, as the text selected when a packet's `guidance_version` is 6 or
   more, in the same way earlier versions are gated in `teacher/session.py`. The walk's packets keep version 5.
   This is an implementation change: request `guidance-6-implementation-001`, suite, and a check that a
   version-5 packet's standing instructions are byte-identical before and after.
2. After that is accepted: four **trial** sessions, unassisted, on fresh scratch packets built with version 6 and
   the same cutoff evidence as the approved runs, for positions **154, 158, 163** and **156** (control). Trial
   packets and runs live outside `.teacher/retrieval` and `.teacher/runs` (for example under `.teacher/trials/`),
   are never approved, never ancestor context, never published, and are not recorded as attempts in the journal.
3. No reviewer material goes to the trial teachers: no coverage request, no verdict text, no ledger.
4. Astra files `reviews/requests/guidance-6-trial-001.md` with the four drafts, transcripts, coverage reports and
   token or call counts if available. I compare each with the approved entry and report to the user.

Pass, as I told the user: the teacher finds the three known gaps on its own evidence (154: the eligibility guard
the other callers apply; 158: what the earlier near-identical model file does differently; 163: the configuration
class left on the old form) and the control entry is not padded with speculation. Those three descriptions are
reviewer knowledge and must not reach a teacher.

## Order of work

The walk continues meanwhile. Astra finishes the commit it is on and files its request first; the
implementation request does not need the walk paused, because version 5 stays the default and nothing a walk
teacher sees changes. The trial sessions may run between commits.
