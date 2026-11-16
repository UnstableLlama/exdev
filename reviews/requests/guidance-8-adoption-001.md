# Implementation request: guidance-8-adoption-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements reviews/verdicts/guidance-8-adoption.decision.md. Commit 177 completed under guidance 7 and is filed at reviews/requests/commit-000177-001.md. No 178 has started. Walk advancement is paused pending acceptance of this implementation; 177 also awaits its own verdict.

The production change is one default: prepare() writes guidance_version 8. The already trialled version-8 text and version gates are unchanged. The patch is relative to the implementation immediately before this adoption, excluding the previously accepted trial gate. The updated fixture test checks default 8 and preserves version 5/6/7 checks, unchanged non-system inputs, exact fourth-paragraph addition, and rejection of altered reference evidence.

Verification checks real historical packets at versions 5, 6, 7 and trialled 8 against pre-edit snapshots: complete opening messages, tools and reasoning effort are identical, and each bundle validates. A freshly prepared fixture packet selects version 8 and validates; its system text is exactly guidance 7 plus the decision's paragraph D, with all other inputs unchanged. No provider was invoked and existing packets/runs were untouched. teacher/session.py was not edited.

Full host-enabled suite: EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests — 280 tests passed in 25.760 seconds. Verification script completed successfully.

Please review adoption for new walk packets after acceptance. Existing approvals stay ancestor retrieval only, trial outputs remain unapproved, and existing entries are not re-authored. After a few guidance-8 commits, cost/effect comparison against 172–176 is owed.

## SHA256

- reviews/verdicts/guidance-8-adoption.decision.md: `4c86a92b200686f892eb3b840e460520e3f82085c51417b4034a7f141bc6e494`

- teacher/walk_inputs.py: `e4fb5302dd5fe776238e8373270126b539e4cce14d30d1798a2d11055afb390d`

- teacher/session.py: `f546b0e0407b47104c32d5e45f3e9951fc0136713d95147f0ce4c1ac42cd9f5f`

- tests/test_walk_inputs.py: `c81740cedf0c5a972ddb175dadf476365125abfba2b5d6223fbdc52649497d47`

- reports/guidance-8-adoption-001.patch: `5e865ff3ad76fd86d0054c838667aa98463b8d7d47810c8bdffa4bb70aef6c2a`

- reports/guidance-8-adoption-before.json: `8d9331eb31319f15e43e752fecaf3928464c9dbdf0ff94fb70d94a7626c9991c`

- reports/guidance-8-adoption-verify-001.py: `ef9f4517095a45391a3a5b7150223511b03566ccc82a068181849d287195624a`

- reports/guidance-8-adoption-verification-001.json: `9e542951bfb018050fb936b28076ebe816f5734bb37736623da94d292e13601d`

- reports/guidance-8-adoption-tests-001.txt: `ff6559864bad48613a910511916d3ff89a9fe6f576045ccff5e14256032193ba`

- reviews/requests/commit-000177-001.md: `cf0216e31b59a871bd26d41079687376aa6d2b49001a7637a0d9d8520eecaf5c`
