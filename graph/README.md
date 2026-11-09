# Historical graph validation

Run `python3 -m graph.validate` from the repository root. This indexes exactly four
snapshots: root, positions one-third and two-thirds through the pinned mined
history, and its pinned tip. Snapshots are processed in increasing miner position.
It does not run the full history walk or generate Encyclopedia/training content.

Prerequisites: the existing mined records in `data/exllamav3-v5/records`, the
bare source repository, a clean detached worktree at `.graph-work/exllamav3`,
and the Linux amd64 portable backend extracted at `.tools/cbm-v0.12.1`.
Download the asset named in `backend.lock.json` from that repository's v0.12.1
release and verify its archive checksum before extraction. Keep the bundled
LICENSE and THIRD_PARTY_NOTICES.md. The validator checks the binary checksum
before execution. The backend needs permission to create its local Unix socket.

The checkout path and project name remain fixed. Each index attempt uses a clean
cache; exports are paginated through `query_graph` and checked against the
project's SQLite counts. Backend raw responses, stderr, source hashes, binding
call-site candidates and a SQLite backup are saved under ignored
`data/graph/validation/<sha>/`. A complete result can be reused on rerun.
Delete only that snapshot's `result.json` to deliberately regenerate it.

The binding probe handles direct `m.def("name", &function)` definitions and Python
imports of `exllamav3_ext`. It resolves only unique native function definitions;
ambiguous targets and calls outside indexed functions remain unresolved. It does
not yet insert supplemental edges. Local Python bare-name calls are a diagnostic
candidate set, not a comprehensive or manually labeled accuracy benchmark.
Dynamic dispatch, import aliases beyond this pattern, lambdas and class bindings
need separate evaluation.

Stable-name comparisons require identical file, kind, simple name and exact
source-range hash, with an unambiguous match on both sides. They ignore line
shifts, exclude edited bodies and do not establish rename/move behavior.

The four snapshots are tool-validation artifacts, not teacher context. No events
are attributed to the gaps between them. Production indexing must walk parents
before children, diff against the actual first parent (retaining all merge
parents), and restrict every student query to its authorized historical commit.
The validation probe remains separate from the chronological integration described below.

Later training should combine commit-pinned source, Encyclopedia explanations
and graph relationships. Their shared commit/symbol provenance must prevent
later explanations or graph states entering earlier development examples.


## Chronological indexing and tools

`python3 -m graph.index_commit --stop-position 25` indexes from the root through
an explicit miner position. Raise the position to resume the walk. Each source
checkout is an archive plus an empty local Git repository, preventing the backend
from discovering upstream future refs or exdev history. A single-writer lock
protects the fixed checkout. Generated source trees carry an ownership marker;
the indexer refuses to replace an unowned directory.

Snapshots and compressed backend databases live under ignored `store/graphs/`.
Exports are count-checked before completion, the compressed database has a checksum,
and the timeline import is transactional. Reruns verify and reuse complete snapshots;
changed inputs or missing parents are rejected. A crash before publication can
leave a generated cache/log directory, but cannot mark that commit imported.

`graph/bindings.py` supplements direct pybind function calls, retaining source and
binding file/line/hash evidence. It rejects ambiguous native targets, conservatively
withholds shadowed aliases, and records unsupported calls. It does not yet resolve
class bindings, indirect aliases or module-level callers. Counts from this stricter
pass differ from the initial feasibility probe; see `reports/bindings-v1.json`.

`graph/timeline.py` stores commits, symbol occurrences, first-parent events and
entry links. It tracks source-bearing functions, methods, classes, structs and
enums. Source hashes include docstrings and formatting; a changed hash does not
necessarily mean changed behavior. Unique exact-body/name/kind matches may suggest
moves; ambiguous matches remain additions/removals. Rename-plus-edit inference is
not implemented. `first_observed_sha` and `last_observed_sha` are index observations,
not proven lifetimes or teacher-facing historical facts.

The five tool schemas are frozen in `schema/graph-tools-v1.json`. Invoke only
`GraphTools.invoke` from a trusted runner whose cutoff is fixed outside model
arguments. Every request requires a commit at or ancestral to that cutoff. Pass
the task commit's parent as cutoff when generating a development task; root tasks
need an empty-repository context. Validation-only snapshots are rejected.

- `graph_search`: deterministic name/file glob filtering over the normalized snapshot.
- `graph_trace`: bounded call traversal over backend and supplemental edges, preserving edge origin/evidence.
- `graph_query`: the backend's read-only Cypher subset over a disposable copy of the authorized database, augmented with supplemental edges. It verifies the archived database checksum first.
- `symbol_history`: events for an exact qualified name within the chosen commit's ancestry. Move events retain the previous qualified name; aliases are not silently merged.
- `repo_map`: deterministic PageRank over call edges, with UTF-8 bytes used as a conservative token-budget upper bound rather than a tokenizer-specific exact count.

Search and trace use normalized exports rather than calling the backend's search
and trace APIs. This keeps supplemental edges and historical snapshots consistent.
The API guard is not an operating-system sandbox: a future teacher runner must
not expose the raw store, source repository, arbitrary shell or mutable cutoff.
Only graph tool schemas are frozen; the original shared repository/source tool set
still needs implementation and integration before training traces are generated.

For example, after indexing the root:

```sh
python3 -m graph.tools --cutoff 543c4b27714c6a677a6e714c452d62532f634cff \
  --tool graph_search \
  --args '{"commit":"543c4b27714c6a677a6e714c452d62532f634cff","name_pattern":"*.quantize_tiles"}'
python3 -m graph.link_entries
```

The explicit link seed produces `encyclopedia/symbol-links.json` and transactional
`entry_links` rows. For removed symbols, `sha` in that table identifies the parent
snapshot containing the symbol; the exported record separately retains the entry
commit. Future consumers must filter by the entry commit as well as source revision.
Entries about module-level code or documentation can intentionally have no
function/class links. These links do not upgrade draft explanations to reviewed.

The first 25 chronological snapshots and all five tools have been exercised against
real data. See `reports/graph-integration.json` for counts and boundary checks.

## Independent read-only audit

`python3 -m graph.verify` captures the completed prefix at startup and audits it
without altering the indexer's live source tree or backend cache. Use
`--stop-position N` to limit the prefix, or `--out PATH` to choose the report.
The command checks exact node/edge multisets against archived SQLite databases,
source-range hashes against upstream Git archives, binding-edge reproduction,
actual Git parents, stored first-parent events, symbol occurrences, fingerprints
and foreign keys. Its report states the verified final position; newer snapshots
may have been indexed while the audit ran.

`python3 -m graph.finalize_walk` follows the existing walk recorded in
`store/walk-status.json` and runs the audit when that run completes. It never
restarts the walk. If the run fails, disappears or is replaced, the watcher
records a failure rather than asserting completion. Watcher status is in
`store/final-audit-status.json`; a successful complete audit is saved as
`store/final-graph-audit.json`. Indexing completion and audit completion are
separate states. A full-history completion claim requires both to succeed at
the requested final position.


## Timeline schema v2 and merge provenance

The timeline references canonical `graphs/<sha>.json.gz` files through
`commits.snapshot_path`; it no longer duplicates their full JSON inside SQLite.
Reads verify the stored fingerprint. Run `python3 -m graph.migrate_timeline` only
with the indexer stopped; it acquires the index lock, validates every archive,
retains a v1 database backup, updates transactionally and compacts the result.
Existing snapshots and first-parent events are unchanged by migration.

`symbol_event_provenance` exposes the preserved events with `origin` set to
`merge_arrival` or `direct_commit` and all parent identities. `symbol_history`
returns these fields too. A merge-arrival event is not automatically a new
independent change for training. See the [authoring remediation policy](../docs/review-remediation.md).
