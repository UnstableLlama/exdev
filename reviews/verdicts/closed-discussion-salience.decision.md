# User decision: offer closed discussions that are salient to the task

Recorded by: Fable (independent reviewer; file mailbox)
Decided by: the user, in chat, 2026-11-13, answering my question "Should the catalog also list issues closed in the 7 days before a commit's cutoff?":
- "yes i reccomend salience gating, not time gating, if you think thats reasonable"
Changes: `commit-000017-001.decision.md`, item 1 ("issues and PRs created at or before the cutoff and not closed before it"). Decides the question left open under "Not included" in `evidence-index-and-config-reading.decision.md`.
Relates to: `reviews/verdicts/commit-000069-001.md`

Canonical and training remain false throughout. Nothing in this file is teacher input except the catalog rows and the one guidance sentence described below.

## Why

At commit 69 the discussion that explains the commit was closed 15 seconds before the commit's timestamp, so the catalog dropped it at exactly the commit it explains. Everything in it was older than the cutoff.

The user chose a gate on relevance to the task, not on how recently the discussion closed. I think that is reasonable and the better of the two: a time window lists every recently closed discussion whether or not it bears on the task, and misses a relevant one that closed earlier. The cost is that the gate has to be defined mechanically, so that trusted code and not the teacher or the reviewer decides what is listed. The definition below is mine; Astra may propose changes to it in the implementation request, but not a time window and not a judgement call.

## Decision 1: a second catalog of closed discussions, gated by term overlap with the task

What the reviewer will check:

1. **Candidates.** Every issue and pull request created at or before the task's cutoff and closed at or before it. No age limit.
2. **Content as of the cutoff.** Title, body and comments at or before the cutoff only, by the same history recovery used for the open catalog. Fail closed: if as-of-cutoff content cannot be established, the item is not a candidate.
3. **Task terms, from the task alone.** Trusted code extracts a term set from the task commit: the words of its message, the changed file paths and their base names, and the identifiers on added or removed lines of the diff. Lower-cased; a fixed stop list removes common words and anything shorter than a stated minimum. Nothing from later commits, reviews, verdicts or the ledger.
4. **Score.** A deterministic overlap score between the task terms and the candidate's as-of-cutoff text. Terms that occur in many candidates must count for less than rare ones (so "model" or "error" does not carry a row). The formula is Astra's to choose and must be documented and tested.
5. **Gate.** A candidate is listed only if its score reaches a fixed, documented threshold. Then the top rows by score up to a cap, with a truncation flag and paging, as for the open catalog.
6. **What a row carries.** Number, kind, title, author login, created and closed times, state `closed`, the path hint already used for open rows, and the matched terms (so the teacher can see why it is listed). No score, no bodies, no excerpts, no prose.
7. **Kept distinct.** A separate field from the open catalog and from referenced evidence, so a reader can tell open from closed and author-made links from mechanical ones.
8. **Read on demand** with the existing tool, serving content as of the cutoff, logged in the transcript like any other read.
9. **Navigation, not instruction.** One guidance sentence, sent only when the field is present: these are closed discussions listed because their text shares terms with the task; a listing is not a statement that the discussion is related; any link drawn is labelled inference with its concrete basis, and the item's own title and framing are reported faithfully. The existing reading rule for catalog rows applies to them.
10. **Bound into the contract.** The closed catalog, its matched terms and the objects it can serve are hashed into the walk input contract. Packets built before this decision keep their recorded context and replay.
11. **Tests.** A closed discussion sharing a rare task term is listed; one sharing only common terms is not; a term that appears only in a comment after the cutoff does not count; a discussion closed after the cutoff stays in the open catalog and is not duplicated; the cap and paging; fail-closed content; contract binding; the legacy case.
12. **Documented** in `docs/ancestor-context.md`, including that matched terms expose words taken from discussion text.

Expected result on the known case: at commit 69, issue 16 is listed, matched on terms such as "truncation" and "tokenizer". I have not checked what else would be listed there.

## Decision 2: audit before any re-authoring

For approved commits 2 to 68, produce one report listing, per commit, the closed discussions the new rule would have listed, with their matched terms. Report only. I will read it and say which entries, if any, missed on-point discussion and should be re-authored. Do not re-author anything from the audit automatically.

The report is also the check on the threshold: if most commits list several unrelated rows, the gate is too loose; if commit 69 does not list issue 16, it is too tight.

## Decision 3: commit 69

Attempt 002 is in flight with a coverage request that points only at the parent tree and the evidence index. Finish it and have it reviewed under the rule in force. After the implementation is accepted, re-author commit 69 once more under the new catalog, unassisted, and stop for review. Whichever approved attempt is fuller will be in force.

## Order of work

1. Finish and submit `commit-000069-002`. Review as usual.
2. Do not author commit 70 yet. Implement Decision 1 with tests and send one implementation request, with the audit report from Decision 2 attached.
3. After acceptance, re-author commit 69 under the new contract, then resume the walk at commit 70.

Required architecture fixes 1 and 2 are still due before position 100.

If building this shows a serious cost, a conflict with the no-hindsight boundary, or that term overlap cannot separate relevant from irrelevant discussions at a sensible threshold, say so in a request file before proceeding. The user's instruction leaves the mechanism to my judgement, so a better mechanical gate is welcome; a time window is not, without going back to him.
