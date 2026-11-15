# Implementation review: shared read-only packet blobs

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements disk request 1 from `reviews/fable/DISK-AND-CACHE-PROPOSAL.md`, as authorized by the user. Commit 127 was completed and filed before this change; it remains awaiting its own verdict. No teacher session started during this work. The journal has an advancement pause pending this implementation review. Requested scope: implementation for ancestor retrieval only; canonical and training remain false.

All six packet blob writers now use `teacher.blob_store.put`. Packets under `.teacher/` share `.teacher/blob-store/`; standalone packets use a sibling store, keeping temporary fixtures isolated. Each object and packet hard link has mode 0444. Writes use a store lock, a new temporary inode and atomic replacement; existing object and packet bytes are verified before reuse. Symlinks and corrupt hashes fail closed. Cross-filesystem links fail without replacing the original packet copy. Interrupted migration is restartable. No garbage collection or historical artifact deletion was introduced.

The store directory stays writable for trusted publication; its objects are read-only. This protects against accidental host writes, not a host owner deliberately changing permissions. The teacher sees only its selected packet through a read-only mount, never the global store or other packets. Both the unit test and a real migrated packet deny write, chmod and unlink attempts. Hard links preserve the worker's regular-file requirement; no symlink exception was added.

Migration covered all 199 packet directories under `.teacher/`, including retrieval, old administrative packets and audits. Every one of 136,560 entries was hash-verified before replacement and fully re-hashed afterward; every final entry shares its store inode and has no write permission. All 199 manifest hashes are unchanged, including all approved-run packets. All 1,118 files under `.teacher/runs/` are byte-identical to the before snapshot. Original implementation provenance remains historical; new runs automatically hash the new module.

Independent `du -s -B1` measurements (hard links counted once per invocation): retrieval 35,541,733,376 → 993,390,592 bytes; all `.teacher` 38,290,997,248 → 1,041,518,592 bytes. Shared blob store: 623,890,432 bytes. Filesystem available space rose from 14,350,028,800 to 50,068,549,632 bytes. These are filesystem observations, not apparent-size estimates; detailed snapshots are attached.

Validation: all 244 host-enabled tests passed on Linux aarch64, Python 3.14.4. Tests cover migration/idempotence, sharing, corruption/symlink rejection, failed-link preservation and sandbox mutation denial. Two existing corruption fixtures now replace their link instead of trying to overwrite a read-only shared inode. Historical runs 75/001, 98/001, 103/001, 126/001 and 127/001 replay all 87 recorded tool calls identically; draft rendering and coverage recompute identically. The replay script and boundary report are attached. `git diff --check` passes. No model inference occurred.

Discussion-history caching (request 2) is still outstanding and will be filed separately after disk review; this change does not alter retrieval timestamps, cutoff selection, catalogs, manifests, teacher instructions or review gates. The proposal and this report are administrative only and never teacher input.

## SHA256

- teacher/blob_store.py: `0552562b4ccfccd3ab25808b7413b25e3f45da6f861f3f50a2d863ba6df81bda`
- teacher/packet.py: `dc391fe04f9e453f5113695ccf6b278733af6816ee15790402ecfb568c8d8d8c`
- teacher/ancestor_context.py: `8b71b3c46a92420f2a12950269ac91364629e63007b4de9a699f27f87e6bf28e`
- teacher/retrieval.py: `e6fb5753b1f5b173507c154cb79b27a0f8e99f1d5137b5b5e4b28bc4efccd711`
- teacher/graph_packet.py: `50b7690bbd7cf8fda27581479be22327f121e7ebaced92009a86ca12defb82b7`
- teacher/evidence_index.py: `d93b5e5e86e2cb34ff6749f6f4ed9901aeaf19b157276d4f6e43bb0491deb14c`
- teacher/closed_discussions.py: `bdd88ca4a4d2112f893a58235429101f808c046986d1e1497e3c6c999ea8857f`
- tests/test_blob_store.py: `c1a6a204fb835c25067d7bd43fbe5acb9713f97811fb9f4fee38895979e5ff31`
- tests/test_ancestor_context.py: `9b37eca633020983ac75f661c3d8b3298b1e98f3fb083f30ad7500832f5196b4`
- tests/test_teacher_graph.py: `02622ed799cc75939a109bf6e8cbda176984db5221380a465f2365d0bfecd72b`
- docs/ancestor-context.md: `f9173512d44e33063d532eb72c7e3b219975147f91982b3fdb6a31d20e081631`
- reviews/fable/DISK-AND-CACHE-PROPOSAL.md: `9963368f85616959e0debbb972464136096178872514ad7ebbfc915c78fb318d`
- reports/blob-store-implementation-001.json: `fdfa8a9d7c9fe3c90b07cd3b0ffc4554a760450a04611e874bd4e009a5593f5c`
- reports/blob-store-before-001.json: `d4a37aaea587ac9485b89df1b89e78367e1a32479c859c6e7ac05faa6b0e95eb`
- reports/blob-store-after-001.json: `49a9b4b7154b0b62d8bb000ea1877be636775d0b8de22fc761c25d841f06e63a`
- reports/blob-store-migration-001.json: `c525e1dc3fab96c4e1219859c4b8c21d11e5b0346bd0df869a37484f2512ae4f`
- reports/blob-store-boundary-001.json: `fa12fe42f606cdb457619a3eb83e04b10f2b757d19188b82e712b8a33ebf4b6d`
- reports/blob-store-replay-001.py: `d918dcc98245d9b9048c7ee8ec82cc449c7270cdfabd9dde0351516991c9d212`
- reports/blob-store-tests-001.txt: `62dfafe7514af0e367826d4e7b52ee49cb110e42b449a90717926ffc873baeaa`

Reply in `reviews/verdicts/blob-store-implementation-001.md`.
