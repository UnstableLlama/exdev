# Exllama Encyclopedia: Repo Graph Index

As of 2026-11-09. Companion to "EXL3 Dev Model: Plan and Teacher Work Order".

## Decision

Use **codebase-memory-mcp** as the per-commit code graph builder. Build the time dimension ourselves, in the miner, on top of it.

This choice comes from the tool's documentation, not from running it. The validation step at the end of this document is a cheap test to run before committing to it.

## What the graph is for

The Encyclopedia says why each change was made. The graph says what is connected to what, and when each symbol changed. Together they let the student look up structure by query instead of loading whole files into context.

- The graph is built mechanically at every commit. It costs no teacher tokens and is repeatable.
- Diffing consecutive graphs gives every function and class a timeline of the commits that touched it.
- Encyclopedia entries link to graph symbols, so the Encyclopedia can be queried by symbol as well as by date.
- Graph queries become tools in the shared tool set, so the student is trained to use them.

## Why codebase-memory-mcp

| Need | What it offers |
| --- | --- |
| Scriptable in a loop over commits | Every tool can be called from the command line with JSON arguments; no agent or MCP client needed |
| No model in the loop | No built-in LLM, no API keys, single static binary |
| License | MIT |
| Languages | Type-aware call resolution for Python, C, and C++; CUDA is parsed but not benchmarked |
| Speed | Vendor figure: about 6 seconds for a full index of Django |
| Storage | SQLite; the storage directory can be redirected with `CBM_CACHE_DIR` |
| Query surface | Structured search, call-path tracing, and a read-only Cypher subset |

## Why not the alternatives

- **agentforge-graph.** Has history, changed-since, and as-of-commit features built in. But it lists ten languages with no C or CUDA, requires Python 3.13 or newer, has one maintainer, and is marked beta. Its main selling points are web-framework routes and ORM models, which an inference library does not have.
- **Aider's repo map.** A ranked outline rendered to a token budget. Useful as a view, but it is not a store that can be queried. We produce an equivalent view from the graph instead.
- **RepoGraph and related papers.** Evidence that code graphs help agents on repository-level tasks. Not something to build an implementation on.

## The gap we fill ourselves

codebase-memory-mcp is a snapshot tool. Its change detection covers uncommitted changes in a working tree, not history. The chronology is therefore our own layer: index at every commit, diff, and store symbol events. This also means we control the format the training traces see.

## Scaffold

### Layout

```
exllama-encyclopedia/
  miner/walk.py          # commit walk, one record per commit
  graph/index_commit.py  # checkout -> index -> export nodes and edges
  graph/diff.py          # consecutive-commit graph diff -> symbol events
  graph/bindings.py      # custom pass: Python -> compiled extension edges
  store/timeline.sqlite  # commits, symbols, symbol_events, entry links
  store/graphs/<sha>.db  # per-commit graph, compressed
  tools/                 # the student-facing tool implementations
```

### Per-commit loop

```
for sha in git rev-list --reverse HEAD:
    checkout sha into ONE fixed path
    CBM_CACHE_DIR=store/graphs/<sha> \
      codebase-memory-mcp cli index_repository '{"repo_path": "<fixed path>"}'
    export nodes + edges with: codebase-memory-mcp cli query_graph '{...}'
    run graph/bindings.py to add Python -> extension edges
    diff against the previous commit's export
    write symbol_events(sha, symbol, added | removed | changed | moved)
```

### Timeline database

| Table | Columns |
| --- | --- |
| `commits` | sha, parent_sha, date, position, type tag, noise flag |
| `symbols` | qualified name, kind, first_seen_sha, last_seen_sha |
| `symbol_events` | sha, qualified name, event (added, removed, changed, moved), file, line range |
| `entry_links` | sha, qualified name (links an Encyclopedia entry to the symbols it discusses) |

### Student tools to add to the shared tool set

These are our own thin wrappers. The student learns our names, not the backend's.

| Tool | Backed by | Purpose |
| --- | --- | --- |
| `graph_search` | `search_graph` | Find symbols by name pattern, kind, or file |
| `graph_trace` | `trace_path` | Who calls a function and what it calls |
| `graph_query` | `query_graph` | Read-only Cypher for anything else |
| `symbol_history` | timeline database | Commits that touched a symbol, in order |
| `repo_map` | PageRank over call edges | Ranked outline of the repo at a commit, sized to a token budget |

All five take a commit argument during trace generation, so the teacher only ever sees the graph as of the parent commit.

## Implementation notes

1. **One fixed checkout path and project name.** Qualified names are built from the project and path. A path that changes per commit would make every symbol look new at every commit.
2. **Wrap, do not expose.** Keeping our own tool names lets the backend be swapped later without retraining.
3. **Pin the binary version.** The tool list has shifted between releases; one recent issue reports some tools missing from the MCP tool list and one that works only from the CLI.
4. **"Changed" needs extra work.** A node-set diff shows additions and removals, not edited function bodies. Map each commit's diff hunks onto symbol line ranges, or hash each function's source.
5. **The Python-to-extension boundary.** Calls from Python into compiled C++ or CUDA code are the edges most likely to be missed. `graph/bindings.py` parses the binding definitions and adds those edges.
6. **Index explicitly.** The background watcher does not run in CLI mode, which is fine here because every index is triggered by the loop.

## Validation step, before the full walk

1. Install a pinned release of codebase-memory-mcp.
2. Index exllamav3 at HEAD and at three older commits spread across the history.
3. For a handful of call chains you know by heart, run `trace_path` and compare.
4. Check that qualified names for unchanged symbols are identical across the four commits.
5. Check how many Python-to-extension calls are missing, to size the bindings pass.

If Python call resolution is poor, it will show within an hour. The project's own benchmark places Python in its 75 to 89 percent tier, so some misses are expected.

## Addition to the teacher work order

Insert between "Start mining" and "Start the Exllama Encyclopedia":

- Extend the miner to build the per-commit graph and the timeline database as described above.
- Run the validation step and report the results before the full walk.
- Freeze the five graph tool schemas alongside the rest of the shared tool set.
- When writing each Encyclopedia entry, record `entry_links` for every symbol the entry discusses.

## Caveats

- Token-saving and speed figures are the project's own claims.
- Nothing here has been run against exllamav3 yet.

## Sources

- codebase-memory-mcp README: https://gitea.com/dasdas/codebase-memory-mcp
- Codebase-Memory paper (arXiv:2603.27277): https://arxiv.org/html/2603.27277
- codebase-memory-mcp issue #1500: https://github.com/DeusData/codebase-memory-mcp/issues/1500
- agentforge-graph on PyPI: https://pypi.org/project/agentforge-graph/0.3.3/
- RepoGraph (arXiv:2410.14684): https://arxiv.org/html/2410.14684v2
- Aider architecture overview: https://pyshine.com/aider/
