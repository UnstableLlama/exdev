# Historical graph integration: first 25 commits

The production path now starts at the upstream root and proceeds in the miner's parent-before-child order. It has indexed positions 1–25, ending at `825408b22bf0` (full SHA in the stored snapshot), and a second run verified/reused every snapshot without duplicate imports.

| Item | Verified result |
|---|---:|
| Indexed commits | 25 |
| Observed symbol names | 662 |
| Commit-specific symbol occurrences | 16,236 |
| First-parent symbol events | 695 |
| Encyclopedia symbol links | 62 |
| SQLite foreign-key errors | 0 |
| Tooling tests | 34 passing |

Each backend index receives only an archived source tree and an empty local Git repository. Future upstream objects/refs and the enclosing exdev history are absent. Normalized graph exports are checked against SQLite counts; compressed database checksums and transactional imports support resumption. The indexer requires parent snapshots, so the gaps between preliminary validation samples cannot become fictitious commit events.

## Binding pass

The conservative v1 pass supplements direct pybind function calls, grouping call-site evidence into unique edges. It intentionally accepts fewer cases than the preliminary probe and leaves ambiguity explicit.

| Validation position | Supplemental edges | Supported call sites |
|---|---:|---:|
| 1 | 25 | 34 |
| 755 | 73 | 94 |
| 1,509 | 156 | 193 |
| 2,264 | 676 | 1,014 |

See [binding results](bindings-v1.json) for unresolved categories. Direct top-level extension imports and direct unqualified `m.def` function pointers are supported; class bindings, indirect aliases, overloaded/ambiguous targets and module-level callers need further work. Partial CUDA parsing remains a limitation. These edges describe static relationships, not proof that a call executes successfully.

## Five graph tools

The [version-one schemas](../schema/graph-tools-v1.json) are frozen. All five require a commit and enforce ancestry against a trusted caller's cutoff; model arguments cannot supply or change that cutoff. Search/trace use normalized snapshots, history uses the temporal database, the repository map uses PageRank, and read-only Cypher uses the pinned backend database with supplemental edges added to a disposable copy.

Real-data checks verified a Python `quantize_tiles` → CUDA `quantize_tiles` edge through both trace and Cypher query. The backend rejected a mutation query, and a root-cutoff caller could not request commit 25. The map respects its conservative byte-based token budget. [Machine-readable integration evidence](graph-integration.json) retains these results.

The test suite covers branch ancestry, first-parent merge diffs, deletion/reintroduction, unique versus ambiguous move candidates, source isolation, resume conflicts, binding evidence and shadowing, bounded tool results, and atomic/idempotent entry-link loading. This is not a security audit: the eventual teacher runner must also prevent access to raw files, shell commands and mutable cutoff configuration.

## Remaining work

The full 2,264-commit graph walk is resumable with `python3 -m graph.walk --stop-position 2264`; its live status is local at `store/walk-status.json`. This report records the verified 25-commit checkpoint, not completion of the full walk. Later commits may expose additional parsing, binding or indexing cases; a failure preserves completed snapshots for diagnosis and resumption.

The Encyclopedia remains at 25 draft entries. No training traces, GPU execution or human-facing site have been produced. The broader shared repository/source tools and sandboxed teacher runner remain to be implemented. Historical source hashes track textual changes, including formatting/docstrings; exact-body move candidates are conservative heuristics, not permanent identity proofs.
