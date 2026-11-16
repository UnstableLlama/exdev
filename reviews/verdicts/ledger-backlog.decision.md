# Decision: clear the defect-ledger backlog before the walk continues

Recorded by Fable (reviewer) on 2026-11-16.

## The user's words

I told the user the owed ledger work (records for confirmed findings, and fixes to mark on records the walk has
already passed) had grown to about thirty items and was growing by one or two per commit. I recommended: finish
208, pause the walk, file everything owed in one batch for my review, and from then on file each commit's ledger
items with the next commit's request. I asked: "Tell Astra to pause after 208 and clear the ledger backlog before
continuing?" The user answered:

> Yes, clear it now

## What is decided (my reading, stated so the user can correct it)

1. The commit in progress (208) finishes and gets its verdict as usual. No 209 packet or run starts until the
   backlog request below is accepted.
2. Astra files every ledger item owed by a verdict's "Follow-ups" or carried in `reviews/ASTRA-REGISTER.md`:
   a record (or revision) for each finding a verdict approved for filing, and the fix on each record whose fixing
   commit the walk has already approved. Items a verdict explicitly holds (for example the budget-boundary
   identity held for the `+1` qualification) stay held and are listed as such.
3. Nothing is recorded from history beyond the walk's position: no fix before the walk has approved the fixing
   commit, and no reviewer hindsight as evidence.
4. Reviewer-identified items keep origin and wording that mark them as reviewer observations; they never become
   teacher input.
5. One request, `reviews/requests/ledger-backlog-001.md`, with: a table of every owed item, the verdict that
   owes it, the record file and revision that discharges it (or "held", with the reason); the hashes of every
   file added or changed; the ledger validation output; and the suite if any code changed.
6. Afterwards, standing rule: a commit's ledger items are filed with the next commit's request, so the register
   never carries more than one commit's worth.

## How I will check it

Each record against the verdict it comes from (identity, introducing commit, status, reach and limits as the
verdict states them; no claim the verdict does not support), each fix against the approving verdict, that no
owed item is missing from the table, and that no teacher packet can see reviewer-only material.
