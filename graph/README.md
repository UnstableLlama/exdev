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
The timeline, five student wrappers, supplemental binding edges and Encyclopedia
symbol links are subsequent integration work, not implemented by this probe.

Later training should combine commit-pinned source, Encyclopedia explanations
and graph relationships. Their shared commit/symbol provenance must prevent
later explanations or graph states entering earlier development examples.
