# exdev

**exdev is an independent project by UnstableLlama**, building a specialist development model through repository history, an explanatory Encyclopedia, and code graphs.

The upstream project studied here is **[exllamav3](https://github.com/turboderp-org/exllamav3)**, created by **Turboderp** and developed with its contributors. That credit applies to exllamav3. exdev's tooling and annotations are separate work, and exdev is not authored or endorsed by Turboderp.

Original tooling and commentary: [MIT](LICENSE). Upstream code and diffs: retain Turboderp's [MIT notice](LICENSES/exllamav3-MIT.txt). See [NOTICE](NOTICE) and [ATTRIBUTION.md](ATTRIBUTION.md) for scope, credits and external-source handling.

## Current status

The [work order](EXL3%20Dev%20Model%20Plan%20and%20Teacher%20Work%20Order.md) defines the project. The miner has processed 2,264 commits at pinned tip `bd1f519172406a9560bd5c90e61000691bb69a07`. The first 25 Encyclopedia entries and three structural snapshots are drafts awaiting revision following review. The rewrite will use fresh sandboxed authoring contexts; a candidate isolated runner is implemented and awaiting boundary review and model/graph integration. No training traces have been generated.

```sh
python3 -m unittest discover -s tests
python3 scripts/mine.py mine --out data/exllamav3-v5
python3 scripts/encyclopedia.py show 1
# Export a chosen commit's first parent, with no .git history:
python3 scripts/mine.py parent COMMIT_SHA worktrees/parent
```

Raw records, the SQLite index, source checkouts and graph databases remain local under ignored directories. The repository includes summary reports and the extracted reference inventory. The miner pins a run to its manifest tip and refuses incompatible miner versions. Use a new output directory for a new extraction version. A root commit exports an empty parent directory. Merge diffs are against the first parent and retain all parent SHAs. The walk is topological, with parents before children, rather than a timestamp sort that could put a child before its parent.

[Mining report and complete reference inventory](reports/mining-report.md) · [Encyclopedia index](encyclopedia/README.md) · [Verification results](reports/verification.json)

Requires Python 3.12+ and Git. No third-party Python packages are needed for the miner or its tests. GPU execution belongs to later validation work.

## Graph validation checkpoint

The [graph work order](exllama-encyclopedia-graph-index.md) adds commit-specific code graphs using a pinned, checksum-verified release of **codebase-memory-mcp v0.12.1**, by DeusData. See [backend attribution](ATTRIBUTION.md#graph-backend).

Validation is complete at commit positions **1, 755, 1,509 and 2,264**:

- Exported node and edge counts match all four snapshot databases.
- Selected Python call-trace checks pass with test code included.
- At the pinned tip, the diagnostic probe finds 2,902 of 3,000 simple Python call candidates. This is a narrow coverage check, not an overall accuracy score.
- All 1,106 uniquely resolved Python-to-native call sites at the tip need supplemental edges; 80 files have partial parsing diagnostics.
- The original validation checkpoint passed all 13 tests; the integrated pipeline now passes 73 tests with host sandbox tests enabled. No GPU execution or training has been performed.

Read the [validation report](reports/graph-validation.md) for evidence and limitations, and the [validation setup](graph/README.md) to reproduce the probe. Raw backend responses and snapshot databases remain local. These validation worktrees share full Git history and are not teacher-facing artifacts.

## Historical graph integration

The chronological pipeline passed its initial **25-commit integration checkpoint** and an independent audit through **commit 165**. The full 2,264-commit graph walk is continuing; the local status file below records its live progress. It stores isolated snapshots, adds evidence-bearing Python-to-native edges, records first-parent symbol events, and links the existing Encyclopedia entries to symbols.

- **695 symbol events and 62 entry links** in the first batch; SQLite foreign-key checks pass.
- All five graph tools are implemented with [frozen version-one schemas](schema/graph-tools-v1.json). The trusted caller sets the historical cutoff outside model arguments.
- Read-only Cypher queries and call traces include supplemental binding edges. Real-data checks reject future commits and mutation queries.
- Rerunning the first 25 commits verifies and reuses completed snapshots without duplicate imports.

See the [integration report](reports/graph-integration.md), [tool and indexing instructions](graph/README.md), and [entry/symbol links](encyclopedia/symbol-links.json). Snapshot databases and the timeline remain local under ignored `store/`.

The full graph-history walk is running locally. It resumes from the verified prefix, processing parents before children:

```sh
python3 -m graph.walk --stop-position 2264
# Progress and completion/error status are written to store/walk-status.json.
```

An independent [source/database audit](reports/graph-audit.json) has verified the first 165 commits. `python3 -m graph.verify` audits the currently completed prefix; `python3 -m graph.finalize_walk` waits for the active walk and audits its full result. Live audit status and final results remain local under `store/`.

The Encyclopedia still stops at 25 draft entries. No training traces have been generated. The nine repository/source tools and operating-system isolation are implemented as a review candidate; live model and graph-tool integration remain unfinished. See the [teacher runner](teacher/README.md) and [boundary review guide](docs/teacher-boundary.md). Later training will combine **repository code, Encyclopedia explanations and graph relationships**, joined by commit and symbol, using only evidence available at the historical cutoff.

## Planned human-facing views

Alongside the model tools, we plan a **wiki-style Encyclopedia website** and an **interactive HTML graph viewer**. Readers will be able to browse commits, explanations and symbols, explore call relationships, and compare historical revisions. Both views will use the same source records and commit/symbol links as the training infrastructure, with draft status, evidence gaps and upstream credit visible.

This is later-phase work; no viewer is implemented yet. See the [human browser plan](docs/human-browser-plan.md) for the proposed experience, data contracts and delivery order.


## Review remediation

[Fable's original review](astra-review.md), covering commit `45b7af1`, shifted the next priority to historical authoring correctness:
ancestor-only context and merge provenance, eligible issue evidence, then the
sandboxed teacher tools. The first 25 drafts will be redone in fresh restricted
contexts before a trace dry run. The review is preserved as historical feedback; some findings have since been addressed. See the [agreed remediation order and completed fixes](docs/review-remediation.md).

The [measured storage projection](reports/graph-storage-projection.md) is about
47.2 GiB for the original full-history layout. Removing duplicate uncompressed
snapshot JSON from SQLite reduces that estimate to 36.7 GiB. Schema v2 references
the existing compressed snapshots; migrated data through commit 165 passed the
source audit and resume check. The graph walk continues in the background.

Eligible issue/PR evidence for entries 9 and 10 has been recovered with content-edit cutoffs. Entry 9 receives historical edit-event text, not a claimed reconstruction of the complete issue body. See the [recovery report](reports/github-evidence-recovery.json). No drafts were rewritten by this administrative session.
