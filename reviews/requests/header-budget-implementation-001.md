# Implementation request: bounded large safetensors headers

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Commit 140 approval and its two ledger acceptances are recorded. Commit 141 is
`a5caa423bbd9d8a61266a88fb237c18fb77ec0b8` — "Add Qwen3MoeForCausalLM" (Git title),
cutoff 2025-05-11T15:35:38+02:00. No 141 teacher run or retrieval packet has started.
Please review this implementation and the three administrative ledger candidates
before authoring resumes. Ancestor retrieval only; canonical and training remain false.

Discovery enumerated all 469 currently visible official Qwen repositories, using
all history pages and latest pre-cutoff configs, without name filtering. Qwen is
the original official publisher; no additional official publisher is identified.
All 37 initial unreadable-config cases resolve to absent root config.json in their
complete pinned file trees. Seven repositories declare Qwen3MoeForCausalLM.
The derived architecture is resolved; no curator_attestation or unresolved file.

Initial recovery failed closed on five GPTQ headers: four 235B shards declare
4,223,256 / 4,427,128 / 4,426,888 / 4,426,888 bytes; the 30B single shard declares
9,080,000 bytes. The latter prefix was c08c8a0000000000 at revision
5b78b1b5f244a39334307aed060c27aa8d21e068. These exceed the existing 4 MiB budget.
Neither matching repository was excluded or relabeled absent.

The proposed implementation raises official HF raw-header recovery and cached-header
runtime bounds to 16 MiB. Recovery also rejects normalized JSON exceeding that
runtime bound, including expansion during JSON encoding. Length-prefix and exact
header-range validation remain in force; no weight payloads are downloaded.
The runtime still returns only the requested tensor page. ModelScope's separate
4 MiB recovery/identity bound is unchanged. No output, provider-request, process,
network, historical-cutoff or teacher-instruction limits changed.

All seven sources now recover completely, yielding 239 objects in a
validated bundle. Successful first-pass sources are retained; only the two failed
sources were recovered into a new cache directory. The incomplete initial report
is preserved. This bundle is prepared but has not been bound to a teacher packet.
Discussion catalogs and the parent snapshot are ready; no partial teacher run exists.

Validation: 247 host-enabled tests passed, no skips, on Linux aarch64 / Python
3.14.4. New tests cover exact upper-bound ranges, rejection before a second fetch
for invalid lengths, normalized expansion, large-header paging and runtime denial
above the limit. The real-packet boundary audit passes all 42 checks. Twelve
sandbox checks on the six recovered GPTQ header contents compare first/last pages
against direct dispatch in administrative fixture packets (synthetic locators,
actual pinned content). No model inference occurred. git diff --check passes.

Ledger candidates from the 140 verdict: BF16 odd-tail r001 is the single approved
119 identity with 140 affected; missing single-load abort r001 is a reviewer
observation introduced at 140; variant-collection loader API r002 adds 140's
explicit-device reach to the existing 119 identity. All remain suspected and carry
no claimed execution or fixes. Evidence hashes validate. The authoring record
passes schema validation; the two reviewer_observation records preserve the
requested origin outside the unchanged validator vocabulary, as with prior
accepted records. All reviewer notes and ledger data remain outside teacher input.
Older ledger revisions and the discussion-history cache request remain tracked.

The walk is paused at 141 pending this implementation verdict. On acceptance,
author 141 unassisted on the complete bundle, file its separate review request,
and wait before 142.

## SHA256

- teacher/root_evidence.py: `3ffa2f330f375ed66ecef08a4a3b6b22f2c9de4cdd368f685f7b709d759c95bd`
- teacher/worker.py: `ceb99e96d5fb46e077ebbf59e219fb620d4e53d0a35946c41fa99da6f2dd60b2`
- teacher/README.md: `bf9c4d419dc076448a85dfd9d2cf94410f8e8b555811c106950b30da6ac474a7`
- tests/test_large_headers.py: `7366f57f93a5dd45f5e2b7973215658ea19a216de029f308d20a70ea90ca4a5e`
- reports/header-budget-implementation-001.patch: `876e1847f1f65ea103cedfddb7cc786dc24336daf3cf629faf33e02b1f9c1ebd`
- reports/header-budget-implementation-001.json: `9c4488724105167f16abd793e1fa85cd1ed3aabf3584db43808700f89da68e18`
- reports/header-budget-tests-001.txt: `d29a3b567217f53ec6523c2409769b0111ee15ba85c4faa39dd2f77b2c35c1f8`
- reports/header-budget-boundary-001.json: `455898d200e8de63f72f48ea206c15e69ee754844636f81a2f3c47572aa828e6`
- reports/header-budget-live-audit-001.json: `82e6537c44745a17d7906481fc42c96cace6ff0cab751fb860cfe9e10423be1c`
- reports/header-budget-live-audit-001.py: `1dcc148dc7e2d07a6df59241b9a19ffb092be5cfad23e3b55c79c67eb05ee405`
- reports/commit-000141-reference-discovery-001.json: `60ad6c83de2b8a9ce5e737526734e441b5af71a33538386959f47c30ab4e0092`
- reports/commit-000141-reference-discovery-002.json: `e9f054beaa8e486f70cc64cfc05af94b0eea6c2a4a29ff69c2f05e4558f65e51`
- reports/commit-000141-reference-selection-001.json: `ced2d8c68aa93019a0b02750a277d46b7de3445f5ce92257e753300ed2136e55`
- reports/commit-000141-reference-recovery-001.json: `a324e58acc2f6202af5884221831e628c1a056d30d083754285975c8d7298340`
- reports/commit-000141-reference-recovery-002.json: `4718354f8f0d72002e1a5200184bd9849281f4473e910dd587ba78b02c281d52`
- reports/commit-000141-header-limit-diagnostic-001.json: `1875e54832638ac718b0d2c44f1bae07c415d4461b82efd953e20635b844496a`
- data/evidence/github/000141-references.json: `4f72a21e0f120cfce9368bb5e9b3797fabdb336dce0d4c2c43f47959c5b99997`
- reviews/verdicts/commit-000140-001.md: `8d2148d666b0bbb2786668cd9f416fc3a9f7b8c257643d172b671922d2de27e7`
- reports/commit-000141-ledger-candidates-001.json: `1ac5b0f4a4a993daf003a966a8845e84a743809d1803a68c9a49aadc43f5aab7`
- reports/defect-ledger/exllamav3-deferred-bf16-odd-tail--r001.json: `eb8ad5ba4b2cc3c6fbb48dd377c337d0a3ae89453ca81bc5e93e87f38853c1bf`
- reports/defect-ledger/exllamav3-single-load-missing-deferred-abort--r001.json: `5286dba1715d68a217eb92612de653d3e89aa0623dc15c4e301d7b4a858b1371`
- reports/defect-ledger/exllamav3-variant-collection-loader-api--r002.json: `a18cbf7b906ef0a499c85d1964a7a1c2de7d8456d6a8b8437bab47f1f7dd0c41`
- reports/defect-ledger/evidence/commit119-draft.json: `792fcc397f23c30698f69ad0f1e7e5284c0b6e2e5bd2e2b7ea8dc8cbb52fd1ed`
- reports/defect-ledger/evidence/commit119-transcript.json: `977cb8f45da70b234b8609a0403f000ee8afd4d8827fabd34fecd43cc1c82e66`
- reports/defect-ledger/evidence/commit119-verdict.md: `c4815cd7a5d1d8f9ca89ed8188b3b51907761616b6927a75c22a9ebd56a9fdf8`
- reports/defect-ledger/evidence/commit140-draft.json: `73c6cfb246e2f136326a7c6a44638aee140731867aa4867cd7c9473fd2088427`
- reports/defect-ledger/evidence/commit140-transcript.json: `442bc674e5b63b37010a48efe55b23b9c49d90471739dd0647968c91e0fc7b3a`
- reports/defect-ledger/evidence/commit140-verdict.md: `8d2148d666b0bbb2786668cd9f416fc3a9f7b8c257643d172b671922d2de27e7`

Reply in `reviews/verdicts/header-budget-implementation-001.md`.
