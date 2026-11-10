# Chapter revisions and cross-references

Keep every authored attempt immutable: draft, transcript, source packet identity and provenance. A review can accept a chapter as a template while requesting a later replacement; that does not approve it as a complete canonical root entry.

For this restart, use fresh reruns rather than hand repair or a model editing its previous answer. Incorporate general editorial guidance into standing instructions and task assignments. Do not provide administrative review prose, previous answers, expected numerical answers or later-commit defect findings as teacher context. Preserve the old run and create a new packet/output directory. Record which run replaces which in an administrative assembly manifest only after review; preserve both regardless of outcome.

Run the remaining nine chapters with the updated instructions, then rerun the quantizer last. Its task requires a successful `run` computation of procedural-codebook statistics derived from inspected source. The validator enforces a successful execution; editorial review must still verify that the computation actually answers the assigned question. Other chapters should execute meaningful small standard-library checks when feasible, distinguishing scalar checks from real GPU execution.

Each new chapter packet supplies a catalog of chapter IDs and assigned topics, not sibling draft prose. Model output includes `related_chapters`, restricted to that catalog and excluding itself. These references are separate from ancestor SHA links and are navigation, not evidence. A standalone chapter renders missing siblings as “assembly link pending”; once chapters are combined, the renderer resolves present targets to local anchors. Assembly must reject dangling references before publication. Deterministic candidate assembly is implemented in `teacher.assembly`; the user-supplied assembly acceptance is recorded separately and ancestor export uses bounded retrieval.

This lets quantization and GEMM explain opposite sides of the same packing/layout interface without passing unreviewed sibling prose between sessions. Rerunning the quantizer last permits checking its references against the chapters selected for assembly administratively; it does not permit injecting their unapproved content into the fresh teacher session. Any later design for supplying same-commit reviewed prose needs its own explicit context contract.

Avoid relative directions such as “described below” in generated limitations; name the function or mechanism instead. The rendering slip in the original quantizer draft is preserved in that immutable attempt and addressed by the standing instructions for its rerun.

## Review-directed assignments and audit provenance

The root generation 004 revision is accepted as chapter material in `reports/root-chapter-selection-001.json`. Its focus names areas identified by review; that intervention is recorded in its immutable packet. It must not be represented as unaided defect discovery. Attempt 003 remains preserved, including its draft-token cutoff observation.

For the chronological commit walk, freeze each task's focus from the commit and eligible source evidence before review. Do not rewrite a commit-specific assignment using reviewer findings, even if only naming where to look. General instruction improvements can apply prospectively, but never inject that task's review conclusions or locations into its audit teacher. If directed repair/revision is needed, keep it a separately labeled editorial workflow, not an independent audit observation. This is an operating rule; semantic review is still needed to enforce assignment provenance.

Administrative extraction must preserve observations from all attempts, including unselected attempts, with original run IDs, hashes, source evidence and verification scope. Deduplicate by mechanism, not just finding ID. The generation inventory is an extraction starting point, not a retrospective ledger and never a historical teacher input. The other nine selected chapters have been administratively extracted into `reports/findings/root-legacy-extraction-001.json`; those records remain pending extraction review.

A findings list is non-exhaustive. An empty list means none noticed, not that the commit is clean. Audit datasets must retain this distinction and must not use missing findings as a negative ground-truth label.

## Root assembly candidate

`teacher.assembly` checks the exact accepted artifacts against the selected chapter manifest, replays each original final response with its original packet, checks complete assigned coverage and identical root source/cutoff, and requires every planned chapter exactly once. It rejects changed packets, draft edits, mismatched source, missing chapters and unresolved navigation.

The output is explicitly `root_chapter_assembly_v1`, not a silently upgraded v2/v3 teacher annotation. Each original annotation retains its schema version and prose. Evidence IDs receive a chapter prefix to prevent cross-session collisions; the combined ledger keeps their original values. The renderer groups problem/reasoning/impact, claims, source notes, authoring-time findings and limitations by chapter. All related-chapter links resolve locally. Administrative extraction and retrospective inventories are not imported.

The current candidate is `.teacher/assemblies/root-002/entry.md`. The initial build is retained in `root-001`; both entry JSON and Markdown are byte-identical. Provenance records the accepted selection, original packet and artifact hashes and assembler hash. See `reports/root-assembly-validation-002.json` for independent reverse-namespace/prose/evidence checks.

The user-supplied review accepts root-002, with hash-bound approval for ancestor retrieval. It is not a canonical replacement or training sample. The new assembly approval/export path supports this format. Its full serialized entry is 275,210 bytes, exceeding the existing 262,144-byte inline limit even before other ancestors are added. The new retrieval path removes old evidence references from exported prose and uses a bounded, searchable catalog. Its independent boundary review remains pending; the inline limit is unchanged.
