# Implementation review: closed discussion salience

Reply-to thread: 01a1d636-5761-7593-8e19-f8453a562b16

Requested scope: accept the new packet implementation for ancestor retrieval only.
Canonical and training remain false. Acts on `reviews/verdicts/closed-discussion-salience.decision.md` (SHA256 `e1fd1e90efd0153e2a2da00ae9ace8329a5adea54bea86df7db139a7bd65010f`).

69/002 was already submitted and remains pending its own review under the old
contract. No 70 was authored. No audit entry was re-authored. The new packet at
`.teacher/validation/closed-salience-69` is a validation artifact only: no provider
session ran. After implementation acceptance, author 69 unassisted as directed.

Contract 8 / guidance 5 adds a separate, paged closed catalog. Open selection is
unchanged. Candidates must be closed at the cutoff with established full root,
body and comment text; unknown histories and edit summaries fail closed. No age
window. Task terms use only task message, paths and code-line identifiers.
Minimum length 4, fixed stop list; score is the exact rational sum of 1/df² for
shared terms. Gate 1, top 20, kind/number tie-break. Common words have lower weight.
Rows carry matched terms but no score, excerpt or body. Matched terms explicitly
expose discussion words. Existing web_fetch serves cutoff content on demand;
evidence_index with index_id=closed_discussions pages navigation. The single new
guidance sentence extends the existing reading rule and inference-label rules.
Closed snapshots are kept out of the general ancestor evidence index.

Audit attached: every approved position 2–68, plus 69 as the requested validation
case. Positions 2–68 list 66 rows total: 32 have none, 14 have one, 12 have two, 8 have
three, 1 has four. No cap truncation. At 69 only issue 16 qualifies, on tokenizer
and truncation. The initial looser score over-selected generic prose; the fixed
stop list and squared document-frequency penalty reduce that noise. The final
formula and limitations are documented; this audit is not a relevance verdict.
Please assess the gate and identify any audit entries needing re-authoring.

Validation: 219 host-enabled tests passed with pinned Codex 0.167.0. Tests cover
rare/common terms, future text/title exclusion, reopened/closed-after-cutoff state,
no age limit, unknown content, cap and paging, metadata/object/bundle tampering,
on-demand fetch, task-only terms and legacy context. Recorded initial messages,
bundle validation and replay also pass for 39/005, 69/001 and69/002. A new v8 packet
lists 16 and fetches its cutoff snapshot. No authored artifact was changed.

Please review the lexical extractor, conservative full-body requirement, inverse
frequency score, separate paging, contract binding and legacy boundaries. Required
architecture fixes 1/2 and five older invalid ledger origins remain open.

## SHA256

- reports/closed-discussion-salience-implementation-001.json: `25776badc679cd49acedb688318b32ac46f897f814144813d1e99fa06100f9fe`
- reports/closed-discussion-salience-audit-001.json: `815a3c7f08221cce8e496785a317278e62a896c4ebd117af16c445dc3d2818f1`
- reports/closed-discussion-salience-tests-001.txt: `abcba0d1e0494b0ce82095906583c240f09e7dd49226ab6bc46cf609abd94bf7`
- .teacher/validation/closed-salience-69/manifest.json: `38f8694ebde2acfa809438700f21cda072b7b2f0fa41de5d1ba146a0b1b53ec4`
- data/evidence/github/000069-closed.json: `43b9d25f6bcb857b83309cfa10f4f569231e028965211870a5eb0bc055997742`
- teacher/closed_discussions.py: `54de3686c4ed82714a4f029e96189b83f74f1c8651f87dfdde5f2f29696f420d`
- teacher/evidence.py: `3d7f4fc549daaee0cd28bb9d34a034f99f6d05d56ba253199da978884eb91ac0`
- teacher/recover_github.py: `897a7a85da488866c74b15e807cc52f2fdca5f6c6827ddb5c49433f3167f6be5`
- teacher/walk_inputs.py: `786efe80c45b2ff33477a4dd4423b7fdd3cc5d7f9259a06936f33510e0ba4915`
- teacher/session.py: `6037ee158ab5c2d55775e03727a121bf9a4393d52c5bea5ab953dae6597f4167`
- teacher/worker.py: `820befa7ad5ffd7904f4a6af39be8abda63e45f0fb67fae6d38916de14fd7c96`
- teacher/evidence_index.py: `3526b6d93d6d9b33ca49e9136fcf3505394848f808e538d00da8ceade1205021`
- tests/test_closed_discussions.py: `4181b512db86a3b3b07339eb58e90060fed635be62114c9c90e6be98c03a704e`
- tests/test_walk_inputs.py: `2852334af58332d55e1a93e10aa71f6f714454040e121c1eba1e1a43e662bde3`
- tests/test_architecture_evidence.py: `025e09bcabe17ee8e4cc9caccad8bc3029544a70f01938d4fa6467ad43de1fef`
- docs/ancestor-context.md: `c249f831346a6a54c2f8c6834d747ac82f63ab98978680560afc27033d99146f`

Write only `reviews/verdicts/closed-discussion-salience-implementation-001.md`.
