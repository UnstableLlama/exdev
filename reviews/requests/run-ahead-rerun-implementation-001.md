# Implementation proposal: run-ahead reruns with expanded ancestor selection

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Please approve this design before implementation. No teacher or validator change is proposed. The one-off 277/002 recovery remains separate and is authorised; it waits for active 278 to finish.

Add an explicit rerun mode to the prepared forward route. It must bind a rejected forward queue item, its actual original packet and run, a reviewer rerun authorization path/hash, and a fresh attempt/new packet at the same position. Require the existing recovery stop/retry-only state, no active teacher, and no existing output directory. Preserve rejected history and ascending approval order. An ordinary identical-packet retry keeps its current guard.

For expanded-selection reruns, compare the new manifest against the original packet from the rejected queue item, never a caller-selected substitute. All manifest fields must match except exactly this allowed set: `ancestor_entries`, `approved_ancestor_selection`, `ancestor_catalog_blob`, `ancestor_search_blob`, `ancestor_search_graph_commits`. Each old ancestor reference must occur unchanged in the new sequence in source-history order; require a strict increase in approved ancestor coverage. Reject removals, altered prose/chapter hashes, duplicates, reordered entries, non-ancestors, task/cutoff/guidance/evidence changes, and any unapproved or changed approved artifacts. Validate the new selection through the existing approval/hash verifier and sparse-manifest adapter. Check derived catalog/search/graph coverage against the approved projections using the existing builder on a temporary packet, rather than trusting the five-key exception alone. Preserve every original blob byte for byte; new blobs must be the approved prose or regenerated retrieval metadata. Do not admit reviewer material, old annotations or old transcripts as teacher inputs.

Bind original/new packet manifests, rejected run, authorization, comparison report, selected approved runs and orchestration hashes into the queue item and run provenance. Report added ancestor SHAs/counts, sparse status, and positions run ahead of in the review request. The teacher is a fresh unassisted session, with no rejected attempt or reviewer text supplied. Keep the existing validation-repair policy unchanged. Completion still requires a new review; failure stops the queue. No automatic rerun and no relaxation of capacity, one-session, publication or approval rules.

Tests will cover a valid sparse-to-complete expansion; an expansion that remains sparse; original-packet substitution; changed source/evidence/guidance/cutoff; removed/modified/reordered/duplicate ancestor entries; unauthorized/non-ancestor additions; tampered derived metadata or original blobs; reused output; wrong position/recovery state; and preservation of history/provenance bindings. Run the full host-enabled suite before the implementation request. Submit implementation, diff, tests and suite results separately; no live use until accepted. Until then each expanded-selection rerun needs its own mechanics authorization.

No implementation edits in this request. Latest accepted host-enabled suite: 332 tests. No commit or push.

## SHA256

- reviews/verdicts/commit-000277-retry-recovery-002.md: `b0cc28955f808b840d24946a624e8107341d2d4bfb503e81edd695b55d0a16ca`
- orchestration/run_ahead.py: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
- orchestration/ancestor_selection.py: `d28216a56e79cd9ab0de457967cc5218622a8a3c198f798f1490826c06302d2c`
- reports/commit-000277-retry-packet-002.json: `6245360e485dd13ecb4e517faf806ed1c0de06583f5b64cefef1d76ef90f8faf`
