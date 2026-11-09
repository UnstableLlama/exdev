# Human-readable Encyclopedia and graph viewer

Status: planned for a later phase; no website or viewer is implemented. This adds a human-facing use for exdev's source, Encyclopedia and graph data without changing the current priority: reliable bindings, historical indexing, query tools and symbol links.

exdev is a project by UnstableLlama. The source history studied here is exllamav3, by Turboderp and its contributors. Both credits should remain clearly distinguished in the interface.

## Wiki-style reading

Generate a browsable website from the existing Markdown/JSON entries and structured indexes. Keep repository files as the editable source of truth rather than maintaining a separate, manually synchronized wiki.

- Provide an overview, chronological commit index, subsystem pages and symbol pages, with search by name, path, commit and topic.
- Give each entry a stable URL, previous/next navigation in the published topological ordering, explicit parent links, and links to the upstream commit and source lines at that exact revision. Previous in the reading order does not necessarily mean Git parent.
- Link explanations to the symbols they discuss, and symbol pages back to relevant explanations and change history.
- Show the selected revision, author, source provenance, draft/review status and unresolved evidence prominently. Missing entries should appear as not yet authored, not as empty completed explanations.
- Preserve source attribution and license notices in published exports. Render repository text as content, not executable HTML or scripts.

## Interactive HTML graph viewer

Build a browser view over the same commit-specific graph exports used by the query tools.

- Start from a symbol or subsystem, then expand a bounded neighborhood of callers, callees and dependencies. Avoid loading the entire history or rendering every node at once.
- Offer filters for file, language, symbol kind and edge type. Distinguish backend edges, supplemental binding edges and unresolved candidates; show evidence and parsing gaps on inspection.
- Selecting a node should open its source location, Encyclopedia links and symbol history. Keep the chosen commit in navigation and shareable URLs.
- Add a commit selector and an explicit comparison view for additions, removals, body edits and moves. Default comparisons to the actual first parent, with other merge parents selectable.
- Provide a searchable text/list alternative and keyboard navigation so graph layout is not the only way to find information.

A static HTML site with versioned JSON exports is the initial design direction, suitable for local serving or later static hosting. Choose the site generator, graph renderer and hosting service when implementation starts; no framework or deployment is committed by this plan. Large snapshots should be partitioned and loaded on demand. A local query service can be considered later if static exports become impractical.

## Data contracts to prepare now

The indexing layer should support both model tools and human views without a second extraction pipeline:

- Store repository identity, full commit SHA, parent SHAs and deterministic traversal position on snapshot metadata.
- Use commit-scoped symbol identifiers and preserve qualified names, enclosing scope, file paths, line ranges and source hashes. Record rename/move relationships explicitly rather than assuming a name is a permanent identity.
- Record edge type, origin, source evidence and resolution status. Preserve partial-parse diagnostics and distinguish absent data from a confirmed absence of relationships.
- Give entries stable identifiers and structured symbol links. Retain review status, citations and historical cutoffs in exports.
- Version export schemas and publish a build manifest with the source tip, coverage, indexer version and checksums. Keep generated site artifacts separate from authored records and local caches.

The human site may offer an explicitly labeled overview of all indexed history. An as-of-commit view must limit graph data, links, search results and explanations to that revision's permitted ancestry. A present-day retrospective must be visibly labeled and excluded from historical teacher context. The viewer never relaxes the enforced cutoff of training tools.

## Delivery order and acceptance checks

1. After entry and symbol-link schemas settle, generate a small wiki-style reading view from the existing reviewed/draft records, preserving their status.
2. Once graph snapshots and temporal queries are reliable, add symbol pages and a focused interactive graph view.
3. Add historical comparisons, broader search and optional public hosting after export size and usability have been measured.

Before publishing, verify that deep links resolve at the correct revision, entry/symbol links agree with their source records, draft and parsing-gap labels survive export, and historical views reveal no later data. Exercise a merge comparison, a renamed symbol, a missing snapshot and a source-gap entry. Validate keyboard/text navigation and demonstrate that a large snapshot loads a bounded neighborhood rather than the entire graph.

This phase does not require finishing every Encyclopedia entry before a first reading preview, but it must accurately display incomplete coverage. Deployment is a separate later task; documenting this plan does not publish a site.
