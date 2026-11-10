# Historical authoring runner

This is a boundary-review candidate, not a completed authoring service. Initial live root-entry attempts are retained as separate review candidates; no canonical entries have been rewritten and no training traces generated. The [source and retrieval tool schemas](../schema/repo-tools-v1.json) remain unfrozen.

The trusted curator builds one packet per task. `packet.py` exports strict ancestors of all task parents as content-addressed blobs, ancestor diffs, the explicit task diff and approved external evidence. It does not export `.git`, source mirrors, existing Encyclopedia drafts, `astra-review.md`, administrative reports or conversation history. `entry_analysis` mode deliberately reveals the task diff: it must not be reused as a code-prediction student's input packet.

`evidence.py` uses content-edit timestamps, not general update timestamps. `recover_github.py` paginates GitHub edit histories, comments and reviews. GitHub describes `UserContentEdit.diff` as a summary of changes; eligible historical text is therefore labeled `edit_event_text`, never asserted to be a reconstructed full body. Raw external retrievals and prepared source packets remain ignored local artifacts. Teacher run outputs under `.teacher/runs/` are tracked for review. The committed recovery report contains provenance and hashes rather than source bodies.

## Prepare and verify

Run from the repository root:

```sh
python3 -m teacher.recover_github
python3 -m teacher.packet --task 5567364846845473185e60bb7c4dd0aea786574a --destination .teacher/000009 --evidence data/evidence/github/000009-eligible.json
python3 -m teacher.packet --task d43424e20171a6de5eed75dee0eb263b397e8c48 --destination .teacher/000010 --evidence data/evidence/github/000010-eligible.json
EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests
python3 -m teacher.graph_packet --packet .teacher/000009
python3 -m teacher.graph_packet --packet .teacher/000010
python3 -m teacher.audit_boundary
```

Recovery requires authenticated `gh` and network access. `--reuse` reprocesses existing raw retrievals. Packet destinations must be new. The runner requires Linux amd64, system Python, libseccomp and Bubblewrap with user namespaces enabled. Nested execution sandboxes may block namespace creation; run integration checks in the host environment. Ordinary test discovery skips eleven host-only tests unless the environment flag is set. The host-enabled suite passed all 147 tests.

`python3 -m teacher.runner --packet .teacher/000009` reads one JSON request from stdin: `{"tool":"repo_list","arguments":{"commit":"ANCESTOR_SHA"}}`. Packet selection and cutoff are trusted configuration, never model arguments. Consult the schema for complete arguments.

## Isolation and tool behavior

Each tool call gets fresh Bubblewrap namespaces, no network, a cleared environment, no capabilities, read-only packet and runtime mounts, and disposable `/work` and `/tmp`. Mounted host runtime paths are the system Python executable, matching standard library, `/usr/lib/x86_64-linux-gnu` and loader; application mounts contain only the worker and tool schema. `/proc` and `/dev` are namespace-local. No host home, credentials, repository or administrative directory is mounted. Errors never fall back to host execution.

Repository reads allow ancestor trees only; `git_show` additionally permits the explicit task change. External fetch tools serve only curator-approved cached objects, with no live retrieval fallback. HF artifacts require immutable revision identifiers and approved non-weight/header roles. Header tools expose bounded tensor-header data rather than weights. Blob hashes, paths, request sizes and output sizes are checked.

`run` materializes the first-parent source tree and applies optional disposable file replacements. It runs isolated standard-library Python only, with time, memory, file-size and output limits. A seccomp filter denies process/thread creation and namespace changes. This profile cannot execute Torch, GPU workloads or threaded tests. Those require a separately reviewed runtime profile.

`FreshSession.run(model)` accepts a stateless provider callback and starts with only its generic instructions, task metadata and approved evidence catalog. It exposes nine source tools, `ancestor_read` for retrieval packets, and five graph tools when a graph packet is attached. It rejects reuse of the session object. The callback must not attach prior conversations or remote session IDs. The driver returns an unpublished draft/transcript; it does not save corpus entries. Tests use explicit fixtures, not fabricated model outputs.

## Remaining work

The five graph tools are attached through the restricted packet bridge. The Codex Astra adapter and editorial v2 candidate are now implemented. Approved ancestor-prose export is also implemented. Independently review the complete boundary before promoting any fresh authoring into the corpus. Only afterward run a real training-example dry run and freeze the schemas. See the [boundary review guide](../docs/teacher-boundary.md).

## Restricted graph bridge

`graph_packet.py` reads the administrative timeline in read-only mode and exports only graph snapshots and symbol events for the packet's strict Git ancestors. It verifies snapshot fingerprints, backend archive checksums and parent identities before publishing the graph manifest. Indexing suggestions, runtime log paths and other administrative diagnostics are removed from exported JSON provenance. The underlying backend databases are commit-specific derived artifacts; they are not the global timeline. Root tasks have an empty graph allowlist.

The worker reuses the existing frozen graph tool implementations through `PacketTimeline`. Every request first checks the explicit ancestor allowlist. Symbol history is further restricted to the requested commit's ancestors. Query execution receives a disposable copy of only the selected backend database, with supplemental edges added there. No host graph store, global timeline or current source checkout is mounted. Verified snapshot JSON is cached only within one invocation; a cross-call cache remains deferred.

Graph calls additionally mount an explicit list of graph modules, the frozen graph schema and the checksum-pinned backend executable. Their bounded runtime allows 4 GiB of virtual address space and 256 MiB per file for disposable databases; source `run` calls retain 768 MiB and 2 MiB limits. The 25-second CPU and 30-second outer wall limits remain. Large future snapshots may require a separately tested budget adjustment; exceeding the budget fails closed. Native graph queries may use threads; the source `run` single-process restriction is unchanged.

The real-packet audit checks all five graph tools for entries 9 and 10, plus mutation, task-result and future-commit denials. These are administrative checks, not training traces or an independent boundary review.

## Codex Astra with task-specific reasoning

The provider is pinned to `gpt-6-astra` and Codex CLI 0.167.0. Root and chapter sessions use high reasoning; ordinary commit sessions retain medium reasoning. The [restricted model profile](../schema/codex-teacher-model.json) keeps that model identity but disables native patching, multi-agent and experimental tools, and uses direct dynamic tools instead of Code Mode. Do not remove that profile and rely only on feature flags. The local wire test caught the extra native tools that would otherwise be exposed.

`codex_transport.py` launches a fresh Bubblewrap-isolated app-server with temporary state. It copies the selected Codex auth file into a private temporary directory and removes the copy on exit. It does not modify the original login or user configuration. The provider process has network access for inference; it has no repository, packet, old thread, review or credential directory mounted. Only the copied auth file is available to the trusted provider. The historical tool workers have separate networkless namespaces and no credentials.

`codex_adapter.py` starts an ephemeral thread, rejects model/effort changes and inherited instruction sources, and routes only the advertised dynamic tools to `Runner`. It never resumes or forks a thread. Unknown native tool events, foreign thread events, duplicate calls and approval requests abort the run. Raw assistant text is saved before editorial validation; malformed outputs stay failed rather than becoming corpus entries.

```sh
# Startup only; starts no authoring/model turn:
python3 -m teacher.codex_preflight --packet .teacher/000009
# Full local fake-provider and sandbox checks, without real inference:
EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests
```

After boundary review and preparation of the first historical packet, the draft command is `python3 -m teacher.author --packet PACKET --output .teacher/runs/NEW_RUN`. It starts real inference and writes only a new unpublished draft directory. Never use an existing output directory or an output inside the packet. It records the packet and implementation hashes, raw transcript, validated draft JSON/Markdown and a separate pending review record. It does not update Encyclopedia entries, the mining database or training data. An initial root-entry invocation produces a separate review candidate; it does not replace or approve the existing root entry.

The startup [report](../reports/codex-preflight.json) and [wire-test report](../reports/codex-wire-validation.json) distinguish real process checks from fake model responses. See the [editorial v2 contract](../docs/editorial-v2.md).

## Earlier explanations

Use the [approved ancestor-context workflow](../docs/ancestor-context.md) to review replacement drafts and attach their content before authoring later commits. The author CLI and session APIs fail before inference if a non-root packet lacks complete approved ancestor prose. Review comments and original conversations are not included. New packets use an 8 KiB opening catalog and on-demand entry/chapter reads and mechanical file/symbol search. The legacy 256 KiB inline cap is unchanged; see the workflow for paging and evidence semantics.

## Tracked review artifacts

Teacher run directories under `.teacher/runs/` are tracked, including rejected attempts, raw transcripts, draft JSON/Markdown, provenance, status and review records. The [root candidate](../.teacher/runs/root-candidate-002/draft.md) and its [transcript](../.teacher/runs/root-candidate-002/raw-transcript.json) can be reviewed directly in GitHub. `published: false` means the run has not been promoted into the canonical corpus; it does not mean the files are private. Prepared source/graph packets, mirrors, databases and downloaded binaries remain ignored because of their size and reproducibility.

## Root subsystem restart

Candidate 002 is rejected. Root authoring without an explicit subsystem assignment is blocked. The tracked `schema/root-chapters-v1.json` assigns every code/doc section exactly once across ten chapters, with explicit exclusions for binary illustrations, calibration corpora and numeric transform tables. Each chapter has its own fresh provider session and an exact chapter ID in its output schema.

Prepare packets only after historical evidence recovery is complete:

```bash
python3 -m teacher.root_tasks --destination .teacher/restart/root-chapters-001
python3 -m teacher.author --packet .teacher/restart/root-chapters-001/quantizer --output .teacher/runs/root-quantizer-001
```

Destinations must be new directories. The prepared manifest carries assigned source-section indices, required external source IDs and the chapter focus. The validator checks complete byte-range coverage, including unread tails and gaps; tensor headers use complete tensor-index pagination. `git_show.truncated` now refers to the current section; `commit_truncated` separately describes the enclosing commit. A validated draft gets a separate `coverage.json` report. Reading evidence is a necessary condition, not proof of a sound explanation: design reasoning and paper mappings still need editorial review.

The quantizer task requires the Python/CUDA quantizers, EXL3 documentation, packing/codebook and transform implementations, both pinned papers and QTIP reference code. All chapters remain components of one future canonical root entry. Chapter synthesis, editorial approval and canonical promotion remain separate unfinished steps. Neither rejected old candidate is supplied as authoring context.

## Fresh chapter batch 002

All ten fresh Astra/high chapters completed sequentially, with the quantizer last. Complete assigned coverage, annotation validation, packet and implementation hashes, and chapter-reference targets were checked. All drafts remain pending editorial review and are not training eligible. See the [batch verification report](../reports/root-chapter-batch-002.json).

| Chapter | Draft | Evidence transcript |
| --- | --- | --- |
| quantized-inference | [Draft](../.teacher/runs/root-quantized-inference-002/draft.md) | [Transcript](../.teacher/runs/root-quantized-inference-002/raw-transcript.json) |
| conversion | [Draft](../.teacher/runs/root-conversion-002/draft.md) | [Transcript](../.teacher/runs/root-conversion-002/raw-transcript.json) |
| models | [Draft](../.teacher/runs/root-models-002/draft.md) | [Transcript](../.teacher/runs/root-models-002/raw-transcript.json) |
| modules | [Draft](../.teacher/runs/root-modules-002/draft.md) | [Transcript](../.teacher/runs/root-modules-002/raw-transcript.json) |
| generation | [Draft](../.teacher/runs/root-generation-002/draft.md) | [Transcript](../.teacher/runs/root-generation-002/raw-transcript.json) |
| sampling | [Draft](../.teacher/runs/root-sampling-002/draft.md) | [Transcript](../.teacher/runs/root-sampling-002/raw-transcript.json) |
| loading-tokenization | [Draft](../.teacher/runs/root-loading-tokenization-002/draft.md) | [Transcript](../.teacher/runs/root-loading-tokenization-002/raw-transcript.json) |
| runtime | [Draft](../.teacher/runs/root-runtime-002/draft.md) | [Transcript](../.teacher/runs/root-runtime-002/raw-transcript.json) |
| usage-evaluation | [Draft](../.teacher/runs/root-usage-evaluation-002/draft.md) | [Transcript](../.teacher/runs/root-usage-evaluation-002/raw-transcript.json) |
| quantizer | [Draft](../.teacher/runs/root-quantizer-002/draft.md) | [Transcript](../.teacher/runs/root-quantizer-002/raw-transcript.json) |

## Structured findings and generation revision

The user-supplied Fable review accepts the batch as chapter material and requests a fresh generation revision. [The review record](../reports/root-chapter-review-002.json) binds that decision to the original draft hashes without changing immutable run artifacts or granting canonical/ancestor approval.

New packet CLI outputs and root chapter packets select editorial v3, adding source-cited `findings`. Legacy packets remain v2 unless explicitly versioned before authoring. See [the findings contract](../docs/defect-retrospectives.md#implemented-authoring-time-findings-editorial-v3). The new generation attempt uses a fresh packet and receives general standing instructions, not the prior draft, review prose, or expected defect answers.

Verification distinguishes source inspection, scalar transcription and repository execution. A successful scalar check supports only its modeled computation; reviewers must verify source claims and execution scope. The run tool description now specifies `python3 -c` and the 1–20 second timeout range.

The [generation 004 draft](../.teacher/runs/root-generation-004/draft.md) and [transcript](../.teacher/runs/root-generation-004/raw-transcript.json) are ready for independent review. It contains seven structured findings and explicitly covers optional output fields, banned-string rollback and multi-sequence capacity. Attempt 003 is preserved; it passed mechanical validation but omitted the optional output contract. See the [revision verification report](../reports/generation-revision-004.json). No replacement is canonically promoted.

Generation 004 is now accepted as the replacement chapter by the user-supplied Fable review. The [accepted chapter selection](../reports/root-chapter-selection-001.json) binds the selected ten chapters to artifact hashes. Authored run review files remain unchanged; this administrative selection does not approve a complete ancestor entry or training sample. The [generation findings inventory](../reports/generation-findings-inventory-001.json) preserves observations from both 003 and 004, including the draft-token cutoff finding unique to 003. Administrative extraction of the other nine v2 chapters is complete; the extracted records await review.

## Administrative extraction of accepted v2 chapters

The [legacy findings inventory](../reports/findings/root-legacy-extraction-001.json) covers all nine selected v2 chapters without editing their prose or starting new teacher sessions. It records 76 observations: 27 potential defects, 23 unchecked contracts, 15 semantic differences, eight diagnostic caveats, two unsupported features and one unverified source warning. These categories are extraction decisions, not independent confirmation.

Each record retains exact prose excerpts and JSON pointers, run/artifact hashes and original transcript evidence. Six observations originally confined to uncited limitations now have source snippets recovered from those same transcripts; their administrative associations are explicitly labeled. Paragraph-level citations are not falsely presented as precise proof of every extracted mechanism. No repository execution is claimed.

| Chapter | Records |
| --- | ---: |
| quantizer | 6 |
| quantized-inference | 5 |
| conversion | 10 |
| models | 3 |
| modules | 8 |
| sampling | 11 |
| loading-tokenization | 14 |
| runtime | 9 |
| usage-evaluation | 10 |

[Provenance validation](../reports/findings/root-legacy-extraction-001-validation.json) passed: 220 prose paragraphs accounted for, 119 exact excerpt checks, 206 evidence-reference checks, six recovered source-quote checks, and unchanged original run hashes. This does not prove exhaustive discovery or confirm each finding. The separate generation inventory is linked from the report; cross-chapter overlap remains available for review rather than silently merged. Findings extraction is complete; extraction review, root-entry assembly and canonical approval remain separate work.

Fable has [accepted the administrative extraction](../reports/findings/root-legacy-extraction-001-review.json) for fidelity and provenance. This supersedes its pending extraction-review state administratively, without rewriting the inventory. [The normalization policy](../schema/finding-taxonomy-v1.json) separates classification, unsupported configurations and coarse impact for future ledger ingestion. Individual finding confirmation and impact assessment remain separate.

## Root assembly ready for review

[The combined root entry](../.teacher/assemblies/root-002/entry.md) preserves the ten selected annotations, including generation 004, and resolves their chapter links. [Assembly verification](../reports/root-assembly-validation-002.json) checks 244 prose/limitation strings, 67 links and unchanged source evidence/artifact hashes. No new model session was used.

Reproduce into a new output directory:

```sh
python3 -m teacher.assembly --selection reports/root-chapter-selection-001.json --packets reports/root-assembly-packets-001.json --output .teacher/assemblies/NEW_ATTEMPT
```

Original local packets are required for replay. Candidate output is retained for review, with a separate pending review record. The user-supplied review now accepts root-002 for ancestor use. Canonical promotion remains pending. Bounded retrieval exports prose without the old evidence ledger and supports file/symbol search; see the ancestor-context workflow.
