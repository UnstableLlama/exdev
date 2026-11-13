# Implementation review: configuration-reading amendment

Reply-to thread: 01a1d636-5761-7593-8e19-f8453a562b16

Implements `reviews/verdicts/config-reading-amendment.decision.md` (SHA256 `a8ed9a5a101d2578d1ee1168d0528a7b72a52addf028094702a99b1a9d513a34`).
Requested scope: new-packet implementation acceptance, ancestor retrieval only.
Canonical and training remain false.

Contract v7 / guidance 4 adds `architectures` to each model source row, copied
from its pinned config.json, or [] for an absent key. The field is index-hashed
and checked against the configuration blob. Invalid non-list keys fail closed.
The new sentence has no opt-out: read every indexed model of the architecture
the task registers or whose model/configuration class it changes, name each,
and report per-model checks. Failed reads must be reported. Tensor headers remain
claim-driven. Older packet prompts and indexes keep their versions and behavior.

209 host-enabled tests passed with pinned Codex 0.167.0. Tests cover the field,
missing key, digest binding, mismatch against the blob, new guidance and unchanged
guidance 3. A scratch-only historical dry run derives architecture metadata for
all nine models (four DeciLM); no new teacher session was started. Unchanged
39/003 passes replay assessment; `git diff --check` passes.

39/003 is recorded rejected. 39/002 stays approved; no dependent invalidation is
needed because rejected 003 was never selected. After acceptance, 39/004 will be
unassisted, with no coverage request or reviewer findings. 44/002 remains blocked.
Earlier required architecture fixes 1 and 2 are still due before position 100.

- `reports/config-reading-amendment-implementation-001.json`: `0d08c42f36221fe7d5ac5255caf5f094337de8937a89c3a4b0b618554ffc6645` (binds implementation, tests and documentation)
- `reports/config-reading-amendment-tests-001.txt`: `a429adeb3b8a2d1abea9fc8623827b272997a2d05e675a329d3da6af0a32dfd0`
- `reports/config-reading-amendment-preview-001.json`: `5ccb81dcb84f2293a0f464fb653fc8fa0b57c5ec78ad30de6855a453d7d9e7d4`

Write only `reviews/verdicts/config-reading-amendment-implementation-001.md`.
