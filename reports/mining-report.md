# Mining and first-25 review report

Pinned upstream tip: `bd1f519172406a9560bd5c90e61000691bb69a07`. Retrieved 2026-11-09T21:12:04.160362+00:00.

**2,264 commits**, one raw record per commit reachable from the pinned default-branch tip; **88 flagged as noise**. Unmerged branches and unreachable objects are outside this walk.

| Type | Count |
| --- | ---: |
| bugfix | 497 |
| docs | 79 |
| feature | 1,349 |
| new architecture support | 85 |
| noise | 88 |
| performance | 109 |
| refactor | 57 |

## Reference inventory

[Every extracted reference and its commit positions](external-references.json) is recorded as JSON. The list includes URLs, paper links, HF repository candidates, issue/PR references and model-name candidates. Embedded calibration-text URLs are listed separately. Candidates are not claims that a model is supported or that a source was consulted.

| Reference kind | Distinct values |
| --- | ---: |
| embedded_data_urls | 2,581 |
| hf_repositories | 5 |
| issue_pr_numbers | 178 |
| model_name_candidates | 424 |
| papers | 3 |
| qualified_issues | 12 |
| urls | 2,235 |

## Tagging spot-check

All first 25 diffs were reviewed in chronological order. [Reviewed labels](../seeds/type-reviews.json) override automatic guesses and retain a review reason. The final records also retain automatic_type. The sample is concentrated at the start of history, not a statistically representative accuracy estimate.

Rule corrections: do not classify executable examples as documentation merely by directory name; recognize VRAM, golden-section search and skipped GC as performance clues; identify docstring changes; restrict formatting noise to checked documentation presentation changes; never infer Python semantic equivalence from whitespace-insensitive diffs. Binary patch payloads no longer generate model/issue matches. Calibration references are segregated, Markdown URL endings are parsed more carefully, and HF collection pages are not treated as model repositories.

Context-sensitive corrections include the JIT manifest fix (000017), the two halves of the capitalization change (000019–000020), and formatting-only entry 000003. The contributor commit and merge at 000009–000010 have the same diff and must not be treated as independent fixes during future sample generation.

## Encyclopedia checkpoint

25 entries and snapshots at 000001, 000018 and 000024 are present. No entry beyond 25 and no training traces were generated. [Index and temporal rules](../encyclopedia/README.md).

Four entries explicitly carry source gaps: 000001 (root-source research), 000008 (historical HF collection membership), 000009 and 000010 (historical issue body). Other entries are drafts pending review, not certified training examples. Root work still lacks the full historical HF non-weight inventories/safetensors headers, exhaustive architecture-reference comparisons and some paper/kernel details. These requirements are not represented as complete.

## Validation

[Verification results](verification.json) cover all record identities, checksums, DAG ordering, database counts, tag totals and exact tree replay for the first 25 diffs. Eight standard-library tests cover extraction, conservative tagging, roots, resume, parent exports, merges, tamper detection and packaged upstream notice presence. Small CPU checks additionally support entries 000012, 000015, 000022 and 000025.

No upstream CUDA build, complete model import, tiny-model quantization or multi-GPU correctness benchmark was performed. Patch applicability alone does not establish runtime correctness; observed intermediate defects remain documented.

## Licensing

Original exdev work uses MIT. Copied upstream notices preserve Turboderp’s copyright. Each mining output includes a NOTICE, ATTRIBUTION.md and LICENSES/exllamav3-MIT.txt; records include the historical LICENSE blob ID or null when absent. External sources retain their own terms. See [attribution](../ATTRIBUTION.md). Raw source caches and full mined diffs remain ignored local artifacts.
