# Implementation request: guidance-9-implementation-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements reviews/verdicts/guidance-9-trial.decision.md as a trial gate only. Guidance 8 remains the prepare default and the walk guidance; no advancement pause is set. The live 192 run completed its original validation and its request was filed before the patch was applied. Its artifacts remain unchanged.

FreshSession appends the exact approved fifth paragraph after guidance 8 for guidance_version >= 9. Contract-8 validation accepts version 9 alongside versions 5–8. No reviewer trial criteria enter teacher instructions. The attached patch is relative to the immediately preceding implementation, not the older Git HEAD (which also predates accepted guidance-8 changes).

The administrative verifier compares an actual version-8 packet (191) against its pre-edit snapshot: standing instructions, full opening, tools and reasoning effort are byte-identical. Legacy version-5 and version-6 snapshots also match; the unit fixture retains version-7 and version-8 checks. A temporary hardlinked packet copy, with its manifest unlinked before editing, validates at version 9. Only the appended system paragraph changes; its text and line breaks equal the decision verbatim. No provider was invoked. All request artifact hashes for 191 and 192 were rechecked after the edit and remain unchanged.

Required suite: `EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests` — 280 tests pass in 27.945 seconds, with ResourceWarnings and no failures. The updated fixture checks the unchanged default, version-9 acceptance, exact append-only instructions and unchanged non-system inputs.

Please review the trial gate. After acceptance, five fresh unassisted trial sessions at 184, 188, 190 and controls 189, 178 will use the approved runs' cutoff evidence under .teacher/trials/, between walk commits. No coverage request, verdict, ledger or reviewer success criteria will be provided. Trial runs will be unpublished, unapproved, excluded from ancestor context and journal attempts. The guidance-9-trial-001 request will include drafts, transcripts, coverage, tool-call and token counts. This is not adoption; a later user decision is required. The guidance-8 walk continues subject to its normal commit verdicts.

## SHA256

- reviews/verdicts/guidance-9-trial.decision.md: `ba117a6eebe3c2d002ef2cf722de75d632b653f346f72c7db52336b121025373`
- teacher/session.py: `1b40a94c3afbf7102a90d4a31efba07617dc4d661bd126b8fbe1801eaa6a45ee`
- teacher/walk_inputs.py: `f417c12bcd3ee12a15647d4a624ceae7a8ef72865c2659c4576133fa81598398`
- tests/test_walk_inputs.py: `e6f18436090c93726714502376191f05c637b98442b2c4c1e81c16fc9404e736`
- reports/guidance-9-implementation-001.patch: `17ad6e102b7b5386adaed68caf4e0743b9f3bacc6f04b3596a36bdd7a23ace5f`
- reports/guidance-9-implementation-001.json: `5833c0735ca27a85cb83edaaf026964995700bab2152d957424e72131c16fd75`
- reports/guidance-9-verify-001.py: `b2a46abaf85663bc142e28bfcc9df4b0dd70cf2240204c0cdad0511a94399472`
- reports/guidance-9-v8-before.json: `8555f48a6ceb2f34b47eb91e4c4229b49c18c583dad4c57312fc02712542fcc6`
- reports/guidance-9-staging-001.json: `70a8a0823b7b1d9e8b43bfbf483fefab31ea12ec33afc6ad696ec94af1ef95ff`
- reports/guidance-9-tests-001.txt: `70c19ab1242b98f9a1a9d8589e9f565c0cb8f6c0cee30d2420610eb57e91e0ed`
