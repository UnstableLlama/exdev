# Review of exdev at 45b7af1: feedback for Astra

Scope: all code under `scripts/` and `graph/`, the tests, the reports, and all 25 entries plus 3 snapshots, compared against the two plan documents. I cloned exllamav3 at the pinned tip `bd1f519`, reran the miner over the full history, and checked entry claims against the real source.

## What holds up

- **The miner reproduces exactly.** My independent run gave 2,264 commits and the same per-type and noise counts as `reports/mining-summary.json`.
- **The entries are factually accurate where I checked.** The four upstream defects the entries point out are all real: `proxy_err_2` assigned but `proxy_err` returned (000012), the `"EXL3"` / `"exl3"` producer-consumer mismatch (000019), `human_time(1800)` giving `1 hour, -30 minute` (000022), and the `int(delta2 / delta1)` progress expression (000024).
- **Gaps are stated, not hidden.** Draft and source-gap statuses are honest, and the work stopped at 25 entries as instructed.
- **The graph layer follows the plan.** Pinned and checksummed backend, the four-commit validation run before the walk, cutoff enforced outside model arguments, source isolation via archive export, evidence-bearing binding edges. All 34 tests pass.

## Fix before writing entry 26

### 1. The issue/PR cutoff rule will discard almost every issue body

Entries 000009 and 000010 excluded the body of issue #2 because its `updated_at` was after the commit, in one case by one second. Closing an issue updates `updated_at`, so every issue closed by its fix will fail this test. The bug reports are where the "Problem" field is supposed to come from.

Use the GitHub GraphQL fields `lastEditedAt` and `userContentEdits` on the issue and on each comment. If the body was never edited, or the last edit predates the cutoff, it is eligible. Then redo 000009 and 000010 with the real report.

### 2. "Entries already written" is not the same as "ancestors"

The walk is topological, which is right for parents-before-children. But a branch commit is placed next to its merge, not at its date. Measured over the pinned history:

- 608 commits are walked after at least one commit that is not their ancestor (up to 741 such commits visible).
- 489 commits are walked after a commit with a later date. Worst case is position 689, placed after a commit dated 94 days later.

`encyclopedia.write` only checks `link < position`. So an entry for an old branch commit can read and link to entries describing mainline work that did not exist when it was written. The graph tools already do this correctly with `Timeline.authorize`. Apply the same ancestry check to the entry context and to `links`.

### 3. Merges need a policy

- 168 merge commits; only 19 are flagged noise. The other 149 are typed as feature, bugfix and so on.
- Their first-parent diffs total 5.8 MB and mostly repeat the branch commits. 134 records share a byte-identical diff with another record.
- 000009 and 000010 already show the result: two "bugfix" entries for one fix.

Proposed rule: a merge gets an identity row and a list of the entries it brings in. It gets analysis only when it contains something its branch commits do not (conflict resolution, visible with `git show --remerge-diff`), or when it is `-s ours` (position 2248 is one). The same applies to `symbol_events`: a first-parent diff at the merge records every branch change a second time, so mark those events as arriving via merge.

### 4. Take process notes and disclaimers out of the entry text

The entries are the corpus that training samples will be generated from. Right now the student would learn to write sentences like these:

- "The extractor incorrectly emitted `collections/turboderp` as a repository candidate... will be covered by a regression test." (000008)
- "The lowercase phi candidate is again a numerical variable rather than a model reference." (000024)
- "This is the final entry of the requested first-25 review batch." (000025)
- "Performance classification is a reviewed correction from the default feature tag." (000013)
- "This is an algorithm-level mapping, not a claim that every equation is proven equivalent." (000001)

Move miner corrections and review bookkeeping to a separate `review_log` field that is never rendered into training text. Make confidence structured: a level, a list of things read, a list of things run, a list of things inferred. Drop the two boilerplate paragraphs that 16 entries share verbatim in Source Notes and Confidence; an empty source list already says it.

### 5. Reasoning mostly restates the diff

The plan defines Reasoning as "why this approach, and which alternatives the code or discussion rules out". Most entries describe what changed. 000013 is the model to follow: it names the assumption (unimodality), notes the search interval widened from the old grid, and says what that changes. 000023 ("Skip GC") is the opposite: it lists the five removed calls and never says why skipping cleanup helps a converter that just gained ETA reporting, or what the risk is.

Where the reason cannot be recovered, say "not recoverable from the parent state" once in the structured confidence field and keep the prose short.

### 6. The root entry needs to be decomposed

Commit one adds 186 files and 61,017 lines: about 520 KB of source across 180 non-calibration files. It has a 6 KB entry. Everything later builds on it, and the entry itself lists what is missing.

- Split it into sub-entries (000001.a onward) per subsystem: loader, modules, quantizer, extension kernels, generator, cache, tokenizer, conversion, each of the five architectures.
- For Llama, Mistral, Qwen2, Phi3 and Gemma2, do the HF reads the plan requires. The miner cannot supply the repos (see below), so pick the canonical reference repo per architecture at the commit date and record that choice as an inference.
- Do the QTIP and QuIP# paper-to-code mapping at function level: which algorithm became `ldlq`, `block_ldl`, `quantize_tiles`, and where EXL3 departs.

### 7. Snapshots 000018 and 000024 are deltas

Both open by saying they supplement the previous snapshot. The plan wants each snapshot to stand alone (layout, data flow, supported architectures, open problems), because Codebase Q&A samples take one snapshot as input. Three snapshots in three days of history is also too often. Suggest: full standalone snapshots at tagged releases and at real structural changes (the TP loader refactor around position 370 is the kind of thing that qualifies), and fold the two deltas into their entries.

### 8. Build the teacher sandbox and the nine repo tools next

The graph tools are done and frozen, but `repo_read`, `repo_list`, `repo_grep`, `git_show`, `git_log`, `hf_fetch`, `safetensors_header`, `web_fetch` and `run` are not implemented, and nothing enforces no-hindsight on the entry author. The same session that writes entries also indexed the tip, and committed reports name later symbols (`QSAPlanes`, `BC_GatedMLP`) and list every later reference by position (`reports/external-references.json`).

Before entry 26: implement the nine tools with the same cutoff guard as `GraphTools`, write entries only through them, and keep tip-revealing reports out of the teacher's reach. This matters more than the full graph walk, because every entry written without it has to be trusted on process alone.

## Miner

- **It hangs on the root commit when stdin is open.** `git hash-object -t tree --stdin` inherits stdin and waits. I hit this on my first run. Pass `stdin=subprocess.DEVNULL`, or use `git hash-object -t tree /dev/null`.
- **Type tags are weak outside the first 25.** 1,349 of 2,264 (60%) fall to the `feature` default. `fix|bug|correct` are unanchored, so "debug", "suffix", "prefix" and "incorrect" all tag as bugfix ("chat.py: Add debug mode", "Module: Remove debug output"). In a random sample of 16 "new architecture support" tags, about 6 were wrong ("Add size estimation script", "compare_q.py: Add AnyPrecision models", "Add batch image ingestion").
- **The spot check was not a sample.** It covered positions 1 to 25 only, and the rule fixes are phrases from those commits (`golden section`, `skip gc`). Either sample about 100 subjects across the history from message and file list only, or state plainly that the heuristic tag is provisional and the entry author sets the real type.
- **Reference extraction cannot drive the HF requirement.** Across the whole history it found 5 HF repos and 3 papers, against roughly 85 architecture additions. Resolving "architecture class to reference HF repo at date" has to be an explicit teacher step.
- `whitespace_only` is computed with an extra `git diff` per commit and never used.

## Graph pipeline

- **Estimate storage before the full walk.** `timeline.sqlite` keeps the full node and edge JSON per commit in `commits.snapshot`, plus one `occurrences` row per symbol per commit, plus the `.json.gz` and `.db.gz` per commit. The tip snapshot has 13,806 nodes and 61,436 edges. My rough estimate is tens of GB for 2,264 commits; I did not measure it. Measure the 25-commit store, extrapolate with the node counts from the validation run, and consider storing only events plus periodic full snapshots in SQLite.
- **`Class` events are noisy.** The body hash covers the whole class, so any method edit also emits a `changed` event for the class.
- **`repo_map` is thin and its argument is misnamed.** It emits qualified name and file:line only, no signatures, and `token_budget` is counted in bytes. The schema is marked frozen; treat v1 as provisional until the walk and a first trace dry-run have exercised it.
- `Timeline.ancestors` runs one query per ancestor on every tool call. Fine at 25 commits; cache it before trace generation.

## Smaller items

- Entry Markdown links to `../../data/...`, which is gitignored, so the "raw diff" link is dead for anyone reading the repo. Link to the upstream commit URL as well.
- The code is written as dense one-liners with semicolons (`graph/tools.py`, `graph/index_commit.py`). It works, but it is hard to review. Format it normally.
- The Wayback lookups for 000001 and 000008 "failed via the web tool". Retry against the availability API directly before recording a permanent gap.

## Suggested order

1. Miner fixes: stdin, merge policy, ancestry-checked links.
2. Issue cutoff via GraphQL edit history.
3. The nine repo tools and the sandboxed teacher runner.
4. Entry schema changes: `review_log`, structured confidence, no boilerplate.
5. Redo entries 1 to 25 under the new rules, with the root decomposed. Report again.
6. Storage estimate, then the full graph walk in the background.
