# Defect records and retrospective annotations

Status: structured authoring-time findings are implemented; new packets use editorial v4. An administrative append-only ledger and evidence-eligibility selector now have their first fix-derived record. The training sample-policy engine remains a design, not an implemented feature. Historical authoring and original commit diffs remain unchanged.

## Two views, one source history

Historical entries explain a change using the task diff, strict-ancestor source and approved prose, and external evidence eligible at that commit. A teacher may discover a defect by inspecting or computing from those permitted inputs. This is an authoring-time observation, not evidence that the upstream author knew about it then.

A separate retrospective ledger records what later evidence establishes about earlier code. The human viewer can overlay **Later defect findings** and link introductions, observations and fixes. That overlay never edits the historical explanation or enters historical ancestor context. A historical/as-of view hides ineligible labels, counts, links and search results as well as their prose.

No later fix is assumed to exist for the root quantizer findings. Locate and verify actual fixes when the chronological walk reaches them; do not search ahead to furnish the historical teacher with answers.

## Record contract

Use a stable defect ID and append-only revisions. Each revision carries:

| Field | Meaning |
| --- | --- |
| `defect_id`, `revision_id`, `supersedes` | Stable identity and auditable corrections; no silent overwrite. |
| `origin` | `authoring_observation` or `fix_derived`; preserve both discovery and later confirmation events. |
| `classification` | `defect`, `behavior_change`, `new_requirement`, `external_compatibility`, or `unresolved`. Compatibility changes can expose a real earlier defect, but require evidence of the earlier contract. |
| `status` | `suspected`, `confirmed`, `disputed`, or `refuted`; independent of whether a fix is known. |
| `description`, `trigger`, `expected_behavior`, `actual_behavior` | Concrete failure and the contemporaneous contract under which it is wrong. |
| `introductions` | Zero or more candidate/confirmed repository+SHA references, affected paths/symbols/ranges, and per-candidate rationale. Unknown origin is allowed. |
| `observations`, `fixes` | Repository+SHA references, issue or review observations, and independently checked fixes, reverts or partial fixes. A commit message saying “fix” is insufficient. |
| `verification` | Source argument, reproducer and results, environment, counterexamples, limits and reviewer decision. Keep source inspection distinct from execution and numerical measurement. |
| `evidence` | Immutable content references/hashes, source revisions, historical availability dates, retrieval dates and the complete prerequisite evidence closure. |
| `recorded_at`, `reviewed_at`, `reviewer` | Modern administrative chronology, separate from evidence availability in the historical source. |
| `affected_revisions` | Verified revision set or ancestry predicates with exceptions; never a bare interval of walk positions. |

A later fix does not automatically establish the introduction or prove the repair correct. Blame on removed/changed lines proposes candidates; renames, refactors, copied code, external contracts and merge resolutions require inspection. Verify that the candidate contains the defect and, where recoverable, its relevant parents do not. Use unknown or a bounded candidate set when that cannot be established. Fix verification should reproduce failure before and success after under the same relevant conditions when feasible; a checked source-level proof can also support confirmation without pretending a test ran.

A defect may survive on one branch after being fixed on another, be partially repaired, or return after a revert. Report ancestry-aware affected revisions and branch-specific duration. Do not label every commit between two topological positions as affected. Keep introduction, inherited presence and independent regression distinct.

## Evidence and cutoff rules

Sample selection gets an explicit training/evaluation cutoff and repository revision allowlists. All evidence supporting a label revision—including the fixing commit, external issue edits, reproduction inputs and any cross-repository dependencies—must be eligible. Date alone is insufficient: unrelated or held-out branches are not authorized simply because their timestamps are early. Apply the same exclusion to the sample prompt, target, rationale, metadata and selection policy.

Choose the latest *eligible* ledger revision, not the latest present-day revision with some fields removed. A post-cutoff fix cannot label, filter or reclassify a pre-cutoff example. Otherwise even dropping examples would leak later information into training-set selection. Human present-day overlays may show such knowledge, clearly labeled; evaluation and historical views may not.

A modern computation from wholly eligible source inputs can support an eligible authoring observation; its `recorded_at` is modern, but it does not consume future code. A claim learned from a later fix cannot be backdated by subsequently writing a reproducer against old code. Record how the claim was obtained and every evidence dependency. Cross-cutoff retrospective knowledge stays excluded even when its conclusion seems reproducible from older material.

Retrospective findings never enter historical ancestor prose. A fix author can legitimately describe an introduction among its allowed ancestors; the trusted administrative stage extracts a proposed ledger record from that explanation. It does not inject the resulting retrospective label into intervening entries. Authoring-time observations remain in their original entry with their evidence and uncertainty, and can be cited by legitimate descendant contexts.

## Sample-generation policy

Do not train a reconstruction target to emit a known defective diff followed by an error note. Apply defect policy before traces are authored, and record the eligible label revision IDs and policy version in sample provenance.

| Eligible finding | Reconstruction policy | Other sample uses |
| --- | --- | --- |
| Confirmed defect introduced or modified in the target behavior | Exclude the complete target by default. | Review/diagnosis example with the defect in the input; localization/repair ending in the verified real fix. |
| Suspected or disputed defect relevant to the target | Hold for review; do not present it as a confirmed bug or silently certify the target. | Explicitly uncertain investigation examples only under a separately reviewed task policy. |
| Refuted finding or non-defect behavior change | No automatic defect exclusion; retain rationale and provenance. | Contract-change explanation if useful. |
| Defect only inherited in untouched code | Assess whether it affects this target's correctness or reproducer. Do not discard every descendant automatically. | Localized review/repair as justified. |

Excluding a hunk is an optional future refinement, not a default shortcut: prove the remaining patch is coherent, applicable and meaningful, validate it, and label it as a derived partial target. Otherwise omit the whole reconstruction example. Do not synthesize a historically nonexistent “corrected commit” and pass it off as upstream history. Verified later fixes are genuine repair targets only when the fixes and their evidence are eligible for the split; the repair target itself must also pass defect policy.

## Acceptance checks before enabling the ledger

- A later fix can enrich a present-day viewer without changing an earlier entry or its packet hash.
- A label supported only after the split cutoff changes neither training samples nor their inclusion decisions.
- An early-timestamp fix on a held-out/sibling branch remains ineligible.
- Refuted and corrected records are selected by eligible revision, not overwritten globally.
- Merge inheritance, partial fixes and regressions yield correct affected-revision sets.
- Missing introduction or fix identity remains unknown; a `bugfix` tag or blame result alone never confirms a defect.
- Reconstruction targets with eligible confirmed defects are excluded or explicitly validated as derived partial patches; review targets identify the defect without producing the buggy implementation as the desired answer.

## Implemented authoring-time findings (editorial v3)

New CLI-prepared packets select editorial schema v4, retaining v3 findings and adding the summary. Old packets without an explicit version retain v2 validation; their immutable drafts and transcripts are not upgraded. The low-level packet builder retains its legacy default; callers must explicitly select v3 before authoring if they bypass the CLI.

The top-level `findings` array records local IDs, suspected status, classification, concrete description/trigger/expected/actual behavior, historical commit/path/symbol locations, inspected-source evidence and verification records. No observations is represented by an empty array. Teachers cannot mark findings confirmed or fix-derived. These observations are not the later retrospective ledger, and do not automatically filter training examples.

Verification methods distinguish `source_inspection`, `scalar_transcription` (including numerical models and hand-transcribed algorithm fragments), and `repository_execution`. Computations require successful non-timeout run evidence; source evidence is independently required. Locations are restricted to the task or allowed ancestors. All evidence IDs must identify successful calls in the current session.

The validator cannot prove that a cited read supports the prose, that a source location is accurate, that an execution used the actual implementation, or that every defect was extracted from free text. Review must check those facts. A root task has an empty first-parent checkout: a scalar model of a kernel is not repository execution. Existing v2 observations remain in their original prose. The nine accepted legacy chapters now have a separate administrative extraction in `reports/findings/root-legacy-extraction-001.json`; this does not backfill their authored schema or hand-repair any draft.

The renderer displays findings with their evidence and verification limits. Review status and training eligibility remain administrative. See `reports/root-chapter-review-002.json` for the user-supplied Fable chapter review; the requested generation replacement is a separate fresh attempt.

## Normalization and impact before ledger ingestion

The administrative extraction is accepted for fidelity and provenance in `reports/findings/root-legacy-extraction-001-review.json`; this does not confirm every defect. `schema/finding-taxonomy-v1.json` defines a common normalization policy for later ledger ingestion. Preserve original categories and teacher classifications alongside normalized values. Potential defects map to suspected defect candidates; unchecked contracts, semantic differences, unsupported features and caveats remain unresolved until their contract is adjudicated. Unsupported configuration is an observation kind, not automatically a defect or a new requirement. Mistral/Phi3 window observations are explicitly flagged for that interpretation.

Impact is separate from classification and confidence: high, medium, low or unknown, with a domain, trigger, supported-input reachability, scope, rationale and evidence. Unknown is the default. A help-text error and a numerical algorithm error can both be defects without receiving the same impact assessment. The normalization policy remains specified for bulk ingestion; the first fix-derived ledger record has an explicit build-impact assessment. The older extracted inventory has not been bulk-ingested. Existing authored schemas and reviewed records remain unchanged.

## First fix-derived ledger record

`reports/defect-ledger/exllamav3-missing-exl3-gemv-header--r001.json` records the missing header introduced in the root and removed by commit 6. It is extracted administratively from the accepted fix explanation, with source/tree snapshots, diff, original transcript and approval hashes. The affected revisions are the five individually checked ancestors of the fix, not an inferred interval. Confirmation is by source inspection and user-supplied Fable review; no native build was run.

`ledger.retrospectives.append` requires evidence hashes and creates a new revision file exclusively. Corrections supersede the existing leaf. `eligible_revisions` checks every dependency against both a timezone-aware cutoff and an explicit repository/SHA allowlist before resolving supersession. It is not connected to teacher packet building or training selection. The first-record tests cover future fixes, held-out branches, evidence tampering and correction visibility; general merge/regression analysis and the training policy engine remain unimplemented.

The root cross-chapter consistency limitation is in `.teacher/assemblies/root-002/known-limits.md`, an administrative companion excluded from ancestor export. Original root artifacts and existing packet hashes are unchanged.
