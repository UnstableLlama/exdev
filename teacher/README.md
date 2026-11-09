# Historical authoring runner

This is a boundary-review candidate, not a completed authoring service. No live model has been invoked, no entries rewritten and no training traces generated. The [nine tool schemas](../schema/repo-tools-v1.json) remain unfrozen.

The trusted curator builds one packet per task. `packet.py` exports strict ancestors of all task parents as content-addressed blobs, ancestor diffs, the explicit task diff and approved external evidence. It does not export `.git`, source mirrors, existing Encyclopedia drafts, `astra-review.md`, administrative reports or conversation history. `entry_analysis` mode deliberately reveals the task diff: it must not be reused as a code-prediction student's input packet.

`evidence.py` uses content-edit timestamps, not general update timestamps. `recover_github.py` paginates GitHub edit histories, comments and reviews. GitHub describes `UserContentEdit.diff` as a summary of changes; eligible historical text is therefore labeled `edit_event_text`, never asserted to be a reconstructed full body. Raw responses and prepared packets remain ignored local artifacts. The committed recovery report contains provenance and hashes rather than source bodies.

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

Recovery requires authenticated `gh` and network access. `--reuse` reprocesses existing raw retrievals. Packet destinations must be new. The runner requires Linux amd64, system Python, libseccomp and Bubblewrap with user namespaces enabled. Nested execution sandboxes may block namespace creation; run integration checks in the host environment. Ordinary test discovery skips eight sandbox tests unless the environment flag is set. The host-enabled suite passed all 92 tests.

`python3 -m teacher.runner --packet .teacher/000009` reads one JSON request from stdin: `{"tool":"repo_list","arguments":{"commit":"ANCESTOR_SHA"}}`. Packet selection and cutoff are trusted configuration, never model arguments. Consult the schema for complete arguments.

## Isolation and tool behavior

Each tool call gets fresh Bubblewrap namespaces, no network, a cleared environment, no capabilities, read-only packet and runtime mounts, and disposable `/work` and `/tmp`. Mounted host runtime paths are the system Python executable, matching standard library, `/usr/lib/x86_64-linux-gnu` and loader; application mounts contain only the worker and tool schema. `/proc` and `/dev` are namespace-local. No host home, credentials, repository or administrative directory is mounted. Errors never fall back to host execution.

Repository reads allow ancestor trees only; `git_show` additionally permits the explicit task change. External fetch tools serve only curator-approved cached objects, with no live retrieval fallback. HF artifacts require immutable revision identifiers and approved non-weight/header roles. Header tools expose bounded tensor-header data rather than weights. Blob hashes, paths, request sizes and output sizes are checked.

`run` materializes the first-parent source tree and applies optional disposable file replacements. It runs isolated standard-library Python only, with time, memory, file-size and output limits. A seccomp filter denies process/thread creation and namespace changes. This profile cannot execute Torch, GPU workloads or threaded tests. Those require a separately reviewed runtime profile.

`FreshSession.run(model)` accepts a stateless provider callback and starts with only its generic instructions, task metadata and approved evidence catalog. It exposes the nine source tools, plus the five graph tools when a graph packet is attached. It rejects reuse of the session object. The callback must not attach prior conversations or remote session IDs. The driver returns an unpublished draft/transcript; it does not save corpus entries. Tests use explicit fixtures, not fabricated model outputs.

## Remaining work

The five graph tools are attached through the restricted packet bridge. The Codex Astra/medium adapter and editorial v2 candidate are now implemented. Independently review the complete boundary and add approved ancestor-prose export, then author entries in fresh per-task contexts. Only afterward run a real training-example dry run and freeze the schemas. See the [boundary review guide](../docs/teacher-boundary.md).

## Restricted graph bridge

`graph_packet.py` reads the administrative timeline in read-only mode and exports only graph snapshots and symbol events for the packet's strict Git ancestors. It verifies snapshot fingerprints, backend archive checksums and parent identities before publishing the graph manifest. Indexing suggestions, runtime log paths and other administrative diagnostics are removed from exported JSON provenance. The underlying backend databases are commit-specific derived artifacts; they are not the global timeline. Root tasks have an empty graph allowlist.

The worker reuses the existing frozen graph tool implementations through `PacketTimeline`. Every request first checks the explicit ancestor allowlist. Symbol history is further restricted to the requested commit's ancestors. Query execution receives a disposable copy of only the selected backend database, with supplemental edges added there. No host graph store, global timeline or current source checkout is mounted. Verified snapshot JSON is cached only within one invocation; a cross-call cache remains deferred.

Graph calls additionally mount an explicit list of graph modules, the frozen graph schema and the checksum-pinned backend executable. Their bounded runtime allows 4 GiB of virtual address space and 256 MiB per file for disposable databases; source `run` calls retain 768 MiB and 2 MiB limits. The 25-second CPU and 30-second outer wall limits remain. Large future snapshots may require a separately tested budget adjustment; exceeding the budget fails closed. Native graph queries may use threads; the source `run` single-process restriction is unchanged.

The real-packet audit checks all five graph tools for entries 9 and 10, plus mutation, task-result and future-commit denials. These are administrative checks, not training traces or an independent boundary review.

## Codex Astra with medium reasoning

The provider is pinned to `gpt-6-astra`, medium reasoning and Codex CLI 0.167.0. The [restricted model profile](../schema/codex-teacher-model.json) keeps that model identity but disables native patching, multi-agent and experimental tools, and uses direct dynamic tools instead of Code Mode. Do not remove that profile and rely only on feature flags. The local wire test caught the extra native tools that would otherwise be exposed.

`codex_transport.py` launches a fresh Bubblewrap-isolated app-server with temporary state. It copies the selected Codex auth file into a private temporary directory and removes the copy on exit. It does not modify the original login or user configuration. The provider process has network access for inference; it has no repository, packet, old thread, review or credential directory mounted. Only the copied auth file is available to the trusted provider. The historical tool workers have separate networkless namespaces and no credentials.

`codex_adapter.py` starts an ephemeral thread, rejects model/effort changes and inherited instruction sources, and routes only the advertised dynamic tools to `Runner`. It never resumes or forks a thread. Unknown native tool events, foreign thread events, duplicate calls and approval requests abort the run. Raw assistant text is saved before editorial validation; malformed outputs stay failed rather than becoming corpus entries.

```sh
# Startup only; starts no authoring/model turn:
python3 -m teacher.codex_preflight --packet .teacher/000009
# Full local fake-provider and sandbox checks, without real inference:
EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests
```

After boundary review and preparation of the first historical packet, the draft command is `python3 -m teacher.author --packet PACKET --output .teacher/runs/NEW_RUN`. It starts real inference and writes only a new unpublished draft directory. Never use an existing output directory or an output inside the packet. It records the packet and implementation hashes, raw transcript, validated draft JSON/Markdown and a separate pending review record. It does not update Encyclopedia entries, the mining database or training data. No real invocation of this command has been performed yet.

The startup [report](../reports/codex-preflight.json) and [wire-test report](../reports/codex-wire-validation.json) distinguish real process checks from fake model responses. See the [editorial v2 contract](../docs/editorial-v2.md).
