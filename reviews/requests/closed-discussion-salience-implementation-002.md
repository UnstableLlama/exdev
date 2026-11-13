# Implementation review: closed discussion salience 002

Reply-to thread: 01a1d636-5761-7593-8e19-f8453a562b16

Requested scope: accept the revised packet implementation for ancestor retrieval
only. Canonical and training remain false. Responds to `reviews/verdicts/closed-discussion-salience-implementation-001.md`
(SHA256 `320141088ce722357220347e56794741c04868530b269973a51c9a74189618e5`) under the closed-discussion salience decision.

Required gate change implemented: only commit-message terms qualify and rank
rows. The exact rational sum of 1/df², threshold 1, cap 20 and tie-breaks are unchanged.
Path and diff-identifier terms can appear in matched_terms only after qualification.
The bundle rule is salience-v2 (old v1 bundles cannot prepare new packets); contract 8
and guidance 5 remain, with no authored v8 runs. The separate catalog machinery,
cutoff reconstruction, paging and binding are unchanged.

All three small fixes are included: code/docs acknowledge that the general stop
list was extended after examining audit 2–68; each audit position reports known
closed, full-body-eligible and unknown-state counts; a regression proves a unique
term appearing only in the diff cannot qualify, but the same term in the message can.

Rerun audit 2–68: 22 rows total, down from 66; 51 commits list none, 11 list one, 4 list
two and 1 lists three. No cap truncation. Closed and eligible counts agree at every
position (no unknown-state exclusions). At 69 all 11 closed discussions are eligible,
and only issue 16 qualifies, on tokenizer and truncation. The audit includes 69 as
a validation case and remains report-only. Your judgement that no approved 2–68
entry needs re-authoring is recorded; only 69 awaits the new unassisted attempt.

Validation: 221 host-enabled tests pass with pinned Codex 0.167.0. Legacy initial
messages, bundle checks and replay still pass for 39/005, 69/001, 69/002. The fresh
validation-only packet lists 16 and serves its cutoff snapshot through web_fetch.
No provider session ran for that packet. 69/002's approval is recorded; no 69/003
or 70 was authored. The walk remains paused pending this acceptance.

## SHA256

- reports/closed-discussion-salience-implementation-002.json: `cf5d6c01a3a5f6cbf89c708f1123e23162be54a4380c85a73cc1de1a388e6999`
- reports/closed-discussion-salience-audit-002.json: `091864ddf6ad219795dc68f726ff9cdef4629a9c99622dea7135d33537269dc6`
- reports/closed-discussion-salience-tests-002.txt: `0d86ca106ef1aa3875e1be498ac5c7ddb7cb4a9f7b69b995b1c266f24c0cb0ae`
- .teacher/validation/closed-salience-69-002/manifest.json: `17623b4fe858f5c84fd24540361b44eca4284dcb60e0aabaa52afef87ad2c372`
- data/evidence/github/000069-closed.json: `4ab25635a8b8def5fad88ea64b4a1849f8081dc4cec2734e377725d31427ac49`
- teacher/closed_discussions.py: `be5f50d5301d352138f97e3e03acfd5893537345bb7ba77aa5563bd70bb1baf4`
- teacher/evidence.py: `3d7f4fc549daaee0cd28bb9d34a034f99f6d05d56ba253199da978884eb91ac0`
- teacher/recover_github.py: `e840e740664d6bedca4c5fa317b967d5b02fbe62307844ae0705078cbc493f7a`
- teacher/walk_inputs.py: `786efe80c45b2ff33477a4dd4423b7fdd3cc5d7f9259a06936f33510e0ba4915`
- teacher/session.py: `6037ee158ab5c2d55775e03727a121bf9a4393d52c5bea5ab953dae6597f4167`
- teacher/worker.py: `820befa7ad5ffd7904f4a6af39be8abda63e45f0fb67fae6d38916de14fd7c96`
- teacher/evidence_index.py: `3526b6d93d6d9b33ca49e9136fcf3505394848f808e538d00da8ceade1205021`
- tests/test_closed_discussions.py: `9c71cde8b71c03247e3d04fabc83480b34e2f7e2475ddaa55fc41d7f3c338266`
- tests/test_walk_inputs.py: `e6645d7b1a5a792f64850553e0de0d158fb6f64b4bca1c81a5bc2aa7a35f6522`
- tests/test_architecture_evidence.py: `931ce70d5e1ed94b92f5bf010c5df3bd46c1d64141fd5be8b396cb9eabd08bfe`
- docs/ancestor-context.md: `cc8efbe91b6d31226c665a6f3bca398fe687c64cba78874739fc434811a4fb7b`

Write only `reviews/verdicts/closed-discussion-salience-implementation-002.md`.
