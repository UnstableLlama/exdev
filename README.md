# exdev

exdev builds a historical Encyclopedia and code graph of a software repository, then uses that evidence to prepare training data for developer models.

**Repository history → Encyclopedia + code graph → training data → trained models**

The current source project is [exllamav3](https://github.com/turboderp-org/exllamav3), created by **Turboderp** and developed with its contributors. exdev provides separate tooling and annotations; it is not authored or endorsed by Turboderp.

## What it does

- **Mine repository history:** extract commit records, first-parent diffs, merge provenance and referenced evidence in parent-before-child order.
- **Build historical code graphs:** store commit-specific symbols, call relationships and supplemental Python-to-native binding edges.
- **Author explanations:** give isolated teacher sessions source, graph data and reviewed ancestor explanations restricted to each task’s historical cutoff.
- **Preserve evidence:** retain drafts, transcripts, provenance and review decisions, with retrospective defect findings kept separate from historical context.

Source code, explanations and graph relationships share commit and symbol identifiers. This lets later training examples use evidence available at the relevant point in history.

## Project maturity

Mining and graph indexing cover the pinned 2,264-commit exllamav3 history. Graph indexing has completed locally; completion of the full final audit is not yet confirmed.

The Encyclopedia and teacher workflow are under active review. Drafts and approval for ancestor retrieval do not imply approval for canonical publication or training. No training traces have been generated and no models have been trained. A wiki-style Encyclopedia and interactive graph viewer are planned.

Operational progress, review decisions and run artifacts live in [`reports/`](reports/), [`reviews/`](reviews/) and [`.teacher/runs/`](.teacher/runs/), rather than this overview.

## Working with the repository

The miner requires **Python 3.12+ and Git**, with no third-party Python packages. Run commands from the repository root:

```sh
# Run the default test suite; host-only sandbox checks are opt-in.
python3 -m unittest discover -s tests

# Mine the pinned source history.
python3 scripts/mine.py mine --out data/exllamav3-v5

# Inspect an Encyclopedia entry.
python3 scripts/encyclopedia.py show 1

# Export a commit’s first-parent tree without Git history.
python3 scripts/mine.py parent COMMIT_SHA worktrees/parent
```

The miner pins each extraction to its manifest tip and rejects incompatible miner versions. Use a new output directory for a new extraction version.

Graph indexing additionally requires the checksum-pinned Linux amd64 backend described in the [graph setup guide](graph/README.md). Teacher execution requires Bubblewrap, libseccomp, enabled user namespaces and the provider setup described in the [teacher guide](teacher/README.md). Its restricted source execution profile does not support Torch or GPU workloads.

Raw records, source checkouts, prepared packets and graph databases remain local in ignored directories. Summary reports and teacher review artifacts are tracked. A fresh checkout therefore needs the relevant data and runtime preparation before graph or teacher commands can run.

## Documentation

| Topic | Guide |
| --- | --- |
| Project design and teacher workflow | [Work order](EXL3%20Dev%20Model%20Plan%20and%20Teacher%20Work%20Order.md) |
| Historical explanations | [Encyclopedia index](encyclopedia/README.md) |
| Graph setup, indexing and queries | [Graph guide](graph/README.md) |
| Isolated authoring and review artifacts | [Teacher guide](teacher/README.md) |
| Historical context and retrieval | [Ancestor context](docs/ancestor-context.md) |
| Isolation and evidence boundaries | [Boundary review guide](docs/teacher-boundary.md) |
| Retrospective defect records | [Defect retrospectives](docs/defect-retrospectives.md) |
| Planned browsing interfaces | [Human browser plan](docs/human-browser-plan.md) |

## Attribution and licensing

Original exdev tooling and commentary are [MIT-licensed](LICENSE). Upstream exllamav3 code and diffs retain [Turboderp’s MIT notice](LICENSES/exllamav3-MIT.txt). The graph backend is **codebase-memory-mcp v0.12.1**, by DeusData; see [backend attribution](ATTRIBUTION.md#graph-backend).

See [NOTICE](NOTICE) and [ATTRIBUTION.md](ATTRIBUTION.md) for credits, license scope and external-source handling.
