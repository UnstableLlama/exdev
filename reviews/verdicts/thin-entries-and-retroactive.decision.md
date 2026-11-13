# User decision: reject thin entries, and apply today's decisions retroactively

Recorded by: Fable (independent reviewer; file mailbox)
Decided by: the user, in chat, 2026-11-13:
- "go ahead and reject stuff you think is thin, dont be shy about telling it to pad out stuff when it needs it"
- "please go ahead and include these decisions retroactively as well"
Builds on: `reviews/verdicts/evidence-index-and-config-reading.decision.md` (sha256 `3ee7c2ca36719b021e5d90124751bfa6ffd86bb434213fce81c357805ff57b6b`)
Changes: the approval policy's statement that there is no task-specific reviewer steering of the teacher. See Decision 1 for exactly how far.

Canonical and training remain false throughout.

## Decision 1: the reviewer may reject an entry as thin, and say what to cover

Until now a draft was approved if everything it said was true, however much it left out, and nothing from a review reached the teacher. The user has changed both.

**Rejection for thinness.** A verdict may now be `REJECTED: thin` when an entry is true but leaves out things a reader of that commit needs, judged against the size and consequence of the change. A small change with a short accurate entry is not thin.

**Coverage requests.** With such a rejection the reviewer writes a coverage request, and that text is given to the teacher for the re-authoring. To keep the no-hindsight boundary and keep the teacher doing the work, a coverage request is limited as follows. The reviewer will hold itself to this and Astra should refuse a request that breaks it:

1. **Pointers and questions only.** It may name parts of the task diff, files in the parent tree, ancestor entries, or attached or indexed evidence that the entry did not examine, and it may ask what the entry does not answer ("say what is loaded on each pass of this loop").
2. **No conclusions.** It does not state the answer, a suspected defect, or what the reviewer found.
3. **Nothing after the cutoff.** It refers only to material the teacher is allowed to see: the task, its strict ancestors and cutoff-eligible evidence. No later commit, issue or fix, and nothing learned from one.
4. **Not a quota.** It does not ask for length. It asks for specific coverage.

**How it reaches the teacher.** As a separate, clearly labelled field in the opening context of the re-authoring attempt, verbatim, hashed into the walk input contract, with one fixed instruction sentence saying these are a reviewer's requests for coverage, not statements of fact. The request file lives at `reviews/verdicts/commit-NNNNNN-AAA.coverage.md` where AAA is the attempt it is for.

**Marked in the record.** A run authored with a coverage request records that in its provenance (the request's path and hash), and its review record carries a flag saying it was reviewer-assisted. Anything that later selects entries for canonical use or training can then tell assisted entries from unassisted ones. That choice is not made here.

**Unchanged.** Verdicts, canonical items, reviewer findings and the defect ledger still never reach a teacher. Only the coverage request file does.

## Decision 2: apply today's decisions to earlier commits

The user wants the new rules applied retroactively. I am scoping that to the commits where my verdicts show the rules would change the entry. Re-authoring all 61 would mostly reproduce what exists.

After implementing the evidence index, the configuration-reading rule (both in the earlier decision file) and the coverage-request mechanism above, re-author these, in this order, each as a new attempt under strict no-hindsight packets, each stopping for full review:

| Commit | Attempt | Why | Coverage request |
|---|---|---|---|
| 39 | 003 | Four reference models attached, one read. The new rule says read every configuration. | None. The general rule is the whole remedy. |
| 44 | 002 | Reads commit 39's entry, which will change. The reference models are older than its cutoff and were not offered. | None. |
| 45 | 002 | Did not say where empty blocks come from; the reference models bear on reach. | `commit-000045-002.coverage.md` |
| 55 | 002 | The thinnest approved entry: six files, no ancestor read, several unexamined consequences. | `commit-000055-002.coverage.md` |

Rules, as for the earlier re-authorings:

- Each packet is built for its own commit: its strict ancestors (using approved replacements where they exist, so 44 uses 39's new attempt, and so on), its own cutoff, the new evidence index.
- The currently approved attempts stay approved and unchanged until a replacement is approved, then are marked superseded for future retrieval.
- After each, list the later runs whose transcripts read the superseded entry. Do not re-author dependents automatically; the reviewer will say.
- Commit 39 attempt 002's verdict said "do not re-author commit 39 a third time", to avoid tuning rules until the teacher finds a defect the reviewer knows about. The user has since decided the general configuration-reading rule and asked for it to apply retroactively. That is a general rule applied uniformly, which is the same footing as the catalog-hints re-authoring, so that instruction is withdrawn for this purpose. If attempt 003 still does not notice the head-count line, it is approved or rejected on the same terms as any other entry and there is no fourth attempt aimed at it.

## Order of work

1. Record the commit 61 approval.
2. Implement, with tests: the evidence index and the configuration-reading rule (earlier decision), and the coverage-request field and provenance flag (this decision). Send one implementation request.
3. Re-author 39, 44, 45, 55 in that order, each reviewed before the next.
4. Resume the walk at commit 62 under the new contract.

From commit 62 on, expect some rejections. That is the intended effect.
