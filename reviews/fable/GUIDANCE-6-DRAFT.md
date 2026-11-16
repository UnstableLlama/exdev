# Guidance 6: draft wording (not yet approved; nothing here has reached a teacher)

From Fable, 2026-11-15. The user agreed to a trial ("yes that sounds good") of a guidance change so that teachers
check code a change relies on but does not touch. The wording below is for the user to approve first.

## Why

At 140, 154, 158, 162 and 163 the entry described the changed lines correctly and missed something visible only
in code the diff leaves alone, or in an earlier entry it did not read. 163/001 was rejected for it. Guidance 5
already has a narrower rule ("When a change makes a dictionary key or function argument required, search the
whole parent tree … for every builder … and every caller"); 163 changed what an argument must be rather than
whether it is required, and the teacher did not apply it.

## Proposed additions (same voice as the existing lines)

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

## Trial, before adoption

- Astra adds these as `guidance_version` 6 (an implementation change, reviewed as usual). Guidance 5 stays the
  default until the trial is judged.
- Four unpublished trial sessions on fresh scratch packets, unassisted: **154** (a guard the other two callers
  apply), **158** (near-copy of an earlier model file), **163** (one configuration class left on the old form),
  and **156** as a plain control.
- Pass: the three known gaps are found by the teacher on its own evidence, and the control entry is not padded
  with speculation. I compare each trial entry with the approved one.
- Trial runs are evidence only. They replace nothing and are never ancestor context.
- If adopted: applies from the next commit on. Approved entries are not re-authored.
