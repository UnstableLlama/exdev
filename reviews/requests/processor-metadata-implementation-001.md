# Implementation request: processor-metadata-implementation-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements the nonblocking evidence-gap request in reviews/verdicts/commit-000234-001.md. Commit 235 is filed and awaiting its verdict. No 236 run has started. Changes were applied after 235's validation; its recorded implementation hashes describe the earlier implementation. All original packets and authored runs remain unchanged.

Official Hugging Face reference-only recovery now gathers preprocessor_config.json and processor_config.json from the selected pinned tree, using the same pinned resolve URLs and evidence checksum/selection machinery as other metadata. Architecture bundle validation allows these two metadata filenames. ModelScope recovery includes both roles in its existing reference set, retaining official Git-blob identity, mirror byte checks, immutable file revisions and cutoff checks; no new mirror exception is introduced. Weight payload and executable-file exclusions remain in place. Header budgets, guidance 9 and prompts are unchanged.

Both files are optional when absent from the pinned tree. An existing file whose download fails makes recovery incomplete; it is not represented as an upstream absence. Tests cover pinned collection alongside exclusion of weights/code, failed optional-file retrieval, end-to-end packet attachment and validation with both files, and mirror collection with altered bytes rejected. Existing absence tests still cover repositories that publish neither file.

BACKFILL PROPOSAL: after acceptance, recover these files for the selected 164/225 Gemma3 and 234 Mistral3 references at their original immutable pins, with distinct new recovery reports/bundles for use at later eligible positions only. Verify each original pin, hash and publication cutoff; report actual absence or inaccessible files rather than inventing contents. Do not rewrite bound historical bundles, packets, authored entries or approvals, and do not re-author 164, 225 or 234. This request implements recovery support; backfill has not been performed. Reviewer knowledge is not teacher input: only recovered pinned source bytes can be attached under ordinary evidence policy.

The walk remains at 235's review gate. This request is nonblocking for unrelated walk commits, but acceptance and recovery are needed before the next architecture commit reading either processor file. Requested review is of this implementation, not canonical/training approval of any entry.

Validation: `EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests` — Ran 282 tests in 39.267s; OK, exit 0. Log contains HTTPError cleanup ResourceWarnings; no failures.

## SHA256

- reviews/verdicts/commit-000234-001.md: `3ad8f0580b972b12d9790fb7cd0170f2f731d0a901e819fe189c6cedbfe503a7`
- teacher/root_evidence.py: `ed0add45a6fc6be1d0cc9d9b118d6e7b61c1f8567c31f2198b783fa907fd6182`
- teacher/architecture_evidence.py: `2abf7fa45b3023bdef5c372ce7e1ee0553e8a315bf50e1aa579ebb5708eda2d6`
- teacher/mirror_evidence.py: `f9d81e736816520a8e209a0efd458aa4eab1ca85c3bc069754fd580b323c362e`
- tests/test_architecture_evidence.py: `fda310c8cf4f027904c863c47a9ed624406db3b6d15cc1ab22ad05c65de4e5d9`
- tests/test_mirror_evidence.py: `ce17a4f2fa28d956b4d72c790ca6cd56d0e9702347ce981b26e3a4fe68ffc190`
- reports/processor-metadata-implementation-001.patch: `e5dee66b66e341f4958644e636d2f064afa66abd00004396466a4ffaaee6f7b2`
- reports/processor-metadata-tests-001.log: `22d6f7e2c8a5880062f69a2f53d814c7f1de29436d5f53ee7ad5fcdb7a46dd88`
