# Attribution and license scope

**exdev is an independent project by UnstableLlama.** Its original tooling and explanatory annotations are credited to UnstableLlama and exdev contributors.

The upstream project exdev studies is **[exllamav3](https://github.com/turboderp-org/exllamav3), created by Turboderp and developed with its contributors**. The code changes being studied belong to those authors. exdev contributes the mining tools, source organization and explanatory annotations.

## Original work and upstream work

Original exdev code and original commentary are offered under [MIT](LICENSE), with copyright attributed to UnstableLlama and exdev contributors. Upstream exllamav3 code and diffs retain **Copyright (c) 2025 Turboderp** and their MIT terms. The exact upstream license is preserved in [LICENSES/exllamav3-MIT.txt](LICENSES/exllamav3-MIT.txt), copied from commit [`bd1f519172406a9560bd5c90e61000691bb69a07`](https://github.com/turboderp-org/exllamav3/blob/bd1f519172406a9560bd5c90e61000691bb69a07/LICENSE).

The MIT notice must accompany copies or substantial portions of the covered software. Keep the upstream notice with redistributed code, patches, mined records containing code, and any future trace bundles containing that material. Preserve additional file-level notices too. [MIT license text](https://opensource.org/license/mit).

The historical walk first encounters a top-level `LICENSE` at commit `6551825ec4f61156ab5ca82b686811a9493ba290` (entry 000004). The first three trees have no top-level license file. Record that absence accurately; the later notice is not evidence that a license file existed in those earlier trees. The packaging notice is separate from the teacher's historical evidence.

## Credit in the Encyclopedia

Every entry records the upstream SHA, parents, author and dates, and links to its raw change. Commentary must distinguish direct evidence, upstream statements, and exdev's inferences. A teacher explanation is not a recovered private thought process. Neither the project name nor this attribution implies endorsement by Turboderp.

The first entry also draws on work by the authors of **QTIP** and **QuIP#**, the **Marlin** developers, and contributors to **FlashAttention, FlashInfer, Transformers, Tokenizers, PyTorch and TabbyAPI**. Per-entry source notes and revision ledgers identify the specific material consulted; those credits do not claim that all their code is distributed here.

## External material

Papers, websites, issue/PR comments, HF repositories, datasets, tokenizers, model files and third-party code do not automatically inherit either exdev's MIT license or exllamav3's MIT license. Keep their source URLs, revisions, retrieval dates, applicable licenses and notices. Source availability alone is not a redistribution grant. A repository's top-level license is not a substitute for inspecting separately attributed or bundled third-party material.

Downloaded source responses, complete mined diffs, calibration data, parent exports and cloned upstream Git objects currently remain local under ignored `data/`, `worktrees/` and `.sources/` directories. They are not included merely by publishing the tooling and original annotations. Before a future dataset/model release, establish the terms for the actual included material and the selected base model; this repository does not yet assign a license to a trained model or a mixed-source dataset.

A redistribution bundle should include this notice, the upstream license, source and author metadata, and applicable third-party notices. Unresolved rights or provenance are recorded as unresolved rather than silently relabeled MIT.

## Graph backend

The validation tooling uses [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp), copyright (c) 2025 DeusData, under [MIT](LICENSES/codebase-memory-mcp-MIT.txt). The exact release and checksums are recorded in `graph/backend.lock.json`. The downloaded binary remains ignored under `.tools/`; its release also includes `THIRD_PARTY_NOTICES.md`, which must accompany any redistribution of that binary. This backend attribution is separate from Turboderp's ownership of the indexed source.

## QTIP reference evidence

Root authoring evidence includes source excerpts from [Cornell-RelaxML/QTIP](https://github.com/Cornell-RelaxML/qtip/tree/bd5fa8a9b7c9b2af080a2fe0c0acd60dcd7c15a1), pinned to `bd5fa8a9b7c9b2af080a2fe0c0acd60dcd7c15a1`. The original repository's [GPL v3 license](LICENSES/qtip-GPL-3.0.txt) is retained for that reference code, including excerpts in recorded tool transcripts. exdev's MIT license does not relicense those excerpts. Paper and model evidence retains its source URLs and revision metadata; those materials retain their own licenses.

The Gemma 2 reference metadata comes from [Unsloth's public mirror](https://huggingface.co/unsloth/gemma-2-2b/tree/25319945f7fd83b8b903e12081777b7eef2ba993), pinned before the root cutoff. It is identified as mirror evidence, without asserting byte identity with Google's gated repository.
