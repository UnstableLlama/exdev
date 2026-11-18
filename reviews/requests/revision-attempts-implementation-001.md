# Revision attempts implementation 001 — proposed mode

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Requested scope: ancestor retrieval only; canonical and training remain false.

This request specifies the implementation and required tests. It is a design proposal: production code is unchanged, tests have not been implemented or run, and no revision is ready for live use. A completed implementation and passing host-enabled suite must be filed for acceptance before any revision teacher session. The active 255/003 remains the already-authorized fresh reviewer-assisted attempt. No teacher was launched for this request; no prose, packet, approval or journal was edited. Nothing is committed or pushed.

## Inputs and eligibility

Add a separate supervisor entry point `author_revision`; ordinary `author` stays fresh. Require a named rejected attempt or declined replacement at the same position, an explicit pointer-only coverage request, and no prior revision reservation for that rejection. Reserve the single revision atomically before starting a teacher; a failed revision does not silently free the reservation. Fresh retries remain available only through their existing authorization path.

Use the identical original packet bytes, including its manifest; do not attach revision metadata to that packet. Keep the new coverage file and revision descriptor outside it, hash-bound in the new run. If the packet contains an earlier attempt-specific coverage attachment, stop for review of how to represent the new attachment rather than rewriting the packet or silently supplying two coverage requests. Admission may inspect administrative rejection authorization, but that authorization and verdict text must never enter teacher context.

Bind the prior draft.json, draft.md, raw-transcript.json and provenance.json by SHA256. Extract the previous model's final JSON annotation and require that reassembly reproduces draft.json and rendering reproduces draft.md. Supply only that annotation and the previous attempt's tool call/result pairs, plus the inspected pointer-only coverage request. Exclude previous prompts, reasoning, commentary, verdicts, review.json, ledger material and other attempts' annotations. Extraction is mechanical and must not edit annotation prose. Refuse incomplete, ambiguous or failed annotation extraction.

## Exact proposed revision instruction

> You are revising your own previous annotation for this position. The historical packet is unchanged. The supplied previous annotation and tool records belong only to the named prior attempt. Write a complete replacement annotation using the ordinary editorial schema; do not return a patch. Keep the mechanisms and supported findings that the previous annotation established, examine the supplied pointer-only coverage request, and correct any claims you find unsupported. Cite every retained or added statement using a supplied prior evidence ID or a new tool evidence ID. Previous prose itself is not evidence. Prior tool records describe checks performed in the previous attempt, not checks newly executed in this session; preserve their source/execution distinctions and limitations. New findings and changes must be supported by permitted historical evidence. Nobody else will edit your prose. Do not mark this entry approved, canonical, or training eligible.

This is an additional mode instruction, not an alteration of guidance versions 5–12 or the walk default. Include the exact serialized revision payload and instruction in the saved initial input, with hashes in provenance. Treat prior annotation/tool-result content as data, not new standing instructions. Preserve the adopted teacher model, reasoning effort, historical tools and isolation boundary.

## Evidence IDs and transcript representation

Keep the new session's raw-transcript.json truthful: imported calls must not appear as calls the new teacher made. Save a separate immutable prior-evidence.json with a deterministic mapping from each original call ID to `prior:<source-transcript-sha256>:<original-id>`, call arguments, exact result bytes and result digest. Mechanically remap annotation citation fields for presentation, preserving the original bytes separately. Never rewrite prose or arbitrary strings. New IDs must not use the reserved prior namespace; reject collisions, duplicate IDs, unmatched results and fabricated imports.

Extend the citation resolver to merge this verified imported ledger with the actual new-session ledger. The prior annotation is context, not an evidence record. Failed tools and catalog-only records keep their existing restrictions. Existing source, execution, ancestor, cutoff and coverage checks still apply. Prior calls may satisfy coverage only where the exact same packet and exact successful result support it; distinguish prior and new coverage/call counts in the report.

## Validation and replay

Validate source hashes, packet identity, same position/SHA, runtime provenance, coverage hash, extraction and ID mapping before launch and again before approval. Revalidate the prior annotation under its own original validation rules; do not assume that a rejected attempt's claims are true merely because its schema passed. Final revision validation uses the combined evidence ledger and ordinary editorial schema, without weakening checks for fresh runs.

Replay imported historical calls against the original packet and compare exact result bytes through the existing replay path. Replay new calls separately; report both totals. Repository/scalar run provenance remains attributed to its original session. Never execute a prior run command merely to construct the revision prompt; perform replay in the existing isolated validator. If exact validation or replay cannot represent an old record, stop and file the mismatch rather than normalize it to pass. Hash checks do not establish factual truth; the reviewer still assesses retained content and any loss.

## Provenance and approval

Record attempt_kind=revision, reviewer_assisted=true, revision_of_run, position, SHA, original packet path/manifest hash, prior artifact hashes, imported-evidence hash and ID-map version, coverage path/hash, exact revision-input hash, model/server runtime, effort, guidance, architecture, Python version and implementation hashes. Keep administrative rejection authorization separately bound and outside the teacher input. The usual trial exclusion and model gates remain. Store the reservation and outcome without modifying the rejected attempt. A revision never auto-approves or automatically supersedes an active entry.

## Request template additions

Each request must state “reviewer-assisted revision of RUN”, identify the rejected/declined attempt and any active entry retained pending verdict, bind both transcripts and annotations, original manifest, imported evidence, ID map, coverage, exact input, validation/replay report and provenance. Include a source-cited side-by-side list of content kept, added, removed or corrected, including findings; the author describes differences without editing prose or adding reviewer facts to teacher input. Explicitly disclose missing earlier content. A revision dropping true content may be declined. Include normal limits, ledger candidates and run-ahead positions if applicable. Scope remains ancestor retrieval only.

## Required automated tests and acceptance evidence

- Fresh-run input, guidance and approval behavior remain unchanged; revision requires explicit mode and same-position rejection/declined-replacement authorization.
- Identical packet required; missing/changed draft, transcript, provenance, coverage or imported evidence fails closed; source files remain byte-identical.
- Final-annotation extraction/reassembly/render checks, malformed or multiple finals, and no annotation available.
- Only allowed prior annotation and call/results enter input; fixtures with verdict, ledger, prior commentary and other attempts are excluded; coverage still passes pointer-only admission.
- Namespaced prior and new citations both resolve; unknown, duplicate, colliding, fabricated, failed-tool, catalog-only and wrong-attempt references fail.
- Exact replay of imported and new calls; mismatch, wrong cutoff, coverage gaps and unsupported old formats fail without an automatic rerun or weakened validation.
- Imported execution remains attributed to the prior session; actual new transcript and call counts contain only new calls; complete imported coverage is distinguished from new reads.
- Atomic one-revision reservation under concurrent launch, failure and recovery; no second revision after failure without a new request; single teacher-session lock retained.
- Revision labels, server runtime, provenance hashes, request bindings and replacement supersession remain enforced; trial runs remain unapprovable.
- Mock transport end-to-end revision writes a complete independently generated annotation and preserves both attempts; no live teacher needed for implementation testing.

Run `EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests` and bind its report alongside focused test results and the implementation patch before requesting live-mode acceptance. This proposal does not claim those checks have passed.

## Related sequencing

Run-ahead is separately requested in reviews/requests/run-ahead-implementation-001.md and remains unavailable in current single-handover tooling. Until that implementation is accepted, retain sequential gates. The revision work is non-blocking for the walk; after 255/003, replacement 234 and 256 onward retain their authorized order.

## Decision binding

- reviews/verdicts/revision-attempts-001.decision.md: `9781753d43b8936772c42d9efdc06db29d167ddaa19bc98d7904e72b4221041b`

Reply in `reviews/verdicts/revision-attempts-implementation-001.md`.
