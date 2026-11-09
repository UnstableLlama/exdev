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
python3 -m teacher.audit_boundary
```

Recovery requires authenticated `gh` and network access. `--reuse` reprocesses existing raw retrievals. Packet destinations must be new. The runner requires Linux amd64, system Python, libseccomp and Bubblewrap with user namespaces enabled. Nested execution sandboxes may block namespace creation; run integration checks in the host environment. Ordinary test discovery skips eight sandbox tests unless the environment flag is set. The host-enabled suite passed all 73 tests.

`python3 -m teacher.runner --packet .teacher/000009` reads one JSON request from stdin: `{"tool":"repo_list","arguments":{"commit":"ANCESTOR_SHA"}}`. Packet selection and cutoff are trusted configuration, never model arguments. Consult the schema for complete arguments.

## Isolation and tool behavior

Each tool call gets fresh Bubblewrap namespaces, no network, a cleared environment, no capabilities, read-only packet and runtime mounts, and disposable `/work` and `/tmp`. Mounted host runtime paths are the system Python executable, matching standard library, `/usr/lib/x86_64-linux-gnu` and loader; application mounts contain only the worker and tool schema. `/proc` and `/dev` are namespace-local. No host home, credentials, repository or administrative directory is mounted. Errors never fall back to host execution.

Repository reads allow ancestor trees only; `git_show` additionally permits the explicit task change. External fetch tools serve only curator-approved cached objects, with no live retrieval fallback. HF artifacts require immutable revision identifiers and approved non-weight/header roles. Header tools expose bounded tensor-header data rather than weights. Blob hashes, paths, request sizes and output sizes are checked.

`run` materializes the first-parent source tree and applies optional disposable file replacements. It runs isolated standard-library Python only, with time, memory, file-size and output limits. A seccomp filter denies process/thread creation and namespace changes. This profile cannot execute Torch, GPU workloads or threaded tests. Those require a separately reviewed runtime profile.

`FreshSession.run(model)` accepts a stateless provider callback and starts with only its generic instructions, task metadata and approved evidence catalog. It exposes exactly the nine tools and rejects reuse of the session object. The callback must not attach prior conversations or remote session IDs. The driver returns an unpublished draft/transcript; it does not save corpus entries. Tests use explicit fixtures, not fabricated model outputs.

## Remaining work

The five graph tools are not attached to this runner. Do not grant a fresh author access to the host graph tools as a workaround. Add a restricted graph bridge and live model adapter, review the complete boundary, revise the editorial schema, then author entries in fresh per-task contexts. Only afterward run a real training-example dry run and freeze the schemas. See the [boundary review guide](../docs/teacher-boundary.md).
