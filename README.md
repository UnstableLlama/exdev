# exdev

Tools and an annotated history for studying **[exllamav3](https://github.com/turboderp-org/exllamav3), created by Turboderp and its contributors**. The goal is a specialist development model grounded in real upstream changes. This is an independent project; explanations are exdev annotations, not statements or endorsements by the upstream authors.

Original tooling and commentary: [MIT](LICENSE). Upstream code and diffs: retain Turboderp's [MIT notice](LICENSES/exllamav3-MIT.txt). See [NOTICE](NOTICE) and [ATTRIBUTION.md](ATTRIBUTION.md) for scope, credits and external-source handling.

## Current status

The [work order](EXL3%20Dev%20Model%20Plan%20and%20Teacher%20Work%20Order.md) defines the project. The miner has processed 2,264 commits at pinned tip `bd1f519172406a9560bd5c90e61000691bb69a07`. The first 25 Encyclopedia entries and three structural snapshots are ready for review. No training traces have been generated. Entries with source gaps are explicitly drafts.

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
- All 13 tooling tests pass. No GPU execution or training has been performed.

Read the [validation report](reports/graph-validation.md) for evidence and limitations, and the [validation setup](graph/README.md) to reproduce the probe. Raw backend responses and snapshot databases remain local. These validation worktrees share full Git history and are not teacher-facing artifacts.

## Next work

1. Add Python-to-C++/CUDA binding edges with explicit source evidence and unresolved cases.
2. Build source-hash diffs and the temporal database against each commit's actual parent.
3. Implement the five commit-restricted graph tools and link Encyclopedia entries to symbols.
4. Walk the full graph history from the first commit forward, processing parents before children.

The graph timeline and student-facing tools are not implemented yet. Later training will combine **repository code, Encyclopedia explanations and graph relationships**, joined by commit and symbol. Historical examples must use only evidence available at their cutoff, including isolated Git metadata; future explanations and graph states must not leak into earlier tasks.
