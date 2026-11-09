---
entry_schema_version: 1
training_traces_generated: 0
tool_schema_status: proposed_not_frozen
review_checkpoint: 25
---

# Exllama Encyclopedia

An independent, source-grounded annotation of **Turboderp and contributors' exllamav3 work**. See [attribution and license scope](../ATTRIBUTION.md). Commit authorship is preserved in each identity record; explanations are exdev commentary.

This first batch contains 25 chronological entries. Each has a readable Markdown view and a JSON record linking to the full local raw diff. Entries remain drafts until review; source gaps are explicit. The sequence stops at 000025 as requested in the work order.

## Evidence boundaries

The walk uses a pinned default-branch tip and reverse topological ordering, so every parent precedes its child. It includes merge commits and preserves all parents, using a first-parent diff for each merge. Dates are recorded in both author and committer forms. External-source cutoffs use the committer timestamp in UTC, not retrieval time. Git timestamps describe commit metadata; they are not proof of the exact date a repository was publicly accessible.

Authoring reads a commit's parent export, its actual diff and earlier entries. The root's parent is empty, so its added files are the evidence. Parent exports contain no `.git` directory. The authoring helper refuses to advance over missing prior entries. This is a workflow guard, not a security sandbox: the operator still has access to the mining repository. A future automated teacher runner needs enforced tool boundaries before traces are generated.

The full history is mechanically mined, but later diffs are not used to explain earlier entries. Administrative licensing checks against the pinned tip are separate from historical implementation evidence. The source-review batch has not progressed past 25.

External code is pinned to an eligible SHA. Papers are pinned to the latest revision known before the cutoff. Issue/PR comments created after the cutoff are excluded; text updated after the cutoff is conservatively withheld unless its earlier version is available. An issue's updated_at can reflect events other than a body edit, so this policy can exclude recoverable text; the entries disclose that limitation. Current HF collection membership is not substituted for a historical snapshot.

Source caches are local under `data/sources/`. Exact GitHub revision pins for the root are in [source-pins-000001.json](source-pins-000001.json). Calibration-text URLs are retained in the mining inventory but are not treated as architectural citations. Source gaps prevent a draft from being considered training-ready.

## Tool schema

The work order proposes repo_read, repo_list, repo_grep, git_show, git_log, hf_fetch, safetensors_header, web_fetch and run. Their inference/training wrappers and final argument schemas are **not yet implemented or frozen**. The miner and review utilities are preparation tools, not fabricated student tool-use traces. Freeze and record the actual schema here before generating the first trace.

## Snapshots

- [000001 — initial framework](snapshots/000001.md)
- [000018 — tensor-storage metadata interface](snapshots/000018.md)
- [000024 — multi-GPU conversion](snapshots/000024.md)

## Entries

- [000001 — Initial commit](entries/000001.md) · draft-source-gaps
- [000002 — Initial commit](entries/000002.md) · draft
- [000003 — Formatting](entries/000003.md) · noise
- [000004 — Add license](entries/000004.md) · draft
- [000005 — Typo](entries/000005.md) · draft
- [000006 — Fix include](entries/000006.md) · draft
- [000007 — Improve memory management slightly in compare_q.py](entries/000007.md) · draft
- [000008 — Link to model collection](entries/000008.md) · draft-source-gaps
- [000009 — Fix Issue #2, Error: setup script specifies an absolute path](entries/000009.md) · draft-source-gaps
- [000010 — Merge pull request #3 from async0x42/fix-setup-tools](entries/000010.md) · draft-source-gaps
- [000011 — Fix requirements](entries/000011.md) · draft
- [000012 — Reduce VRAM overhead of computing proxy error](entries/000012.md) · draft
- [000013 — Replace scale grid search with golden section search](entries/000013.md) · draft
- [000014 — Fix proxy_err](entries/000014.md) · draft
- [000015 — Fix double absolute path in convert_model.py](entries/000015.md) · draft
- [000016 — Fix @override import from typing (Python 3.11)](entries/000016.md) · draft
- [000017 — Explicitly include extension sources for JIT install](entries/000017.md) · draft
- [000018 — Add quantization_config.json](entries/000018.md) · draft
- [000019 — Consistent capitalization for "exl3" in quantization_config.json](entries/000019.md) · draft
- [000020 — Consistent capitalization for "exl3" in quantization_config.json](entries/000020.md) · draft
- [000021 — Fix docstring](entries/000021.md) · draft
- [000022 — More feedback from conversion](entries/000022.md) · draft
- [000023 — Skip GC while converting](entries/000023.md) · draft
- [000024 — Multi-GPU quantization](entries/000024.md) · draft
- [000025 — Fix time formatting](entries/000025.md) · draft

## Future web reading view

These Markdown and JSON records will also back a wiki-style human reading view, with commit navigation, symbol pages and links into an interactive graph viewer. The [human browser plan](../docs/human-browser-plan.md) describes this later phase. The repository records remain the source of truth, and draft/source-gap labels must carry through to the website.
