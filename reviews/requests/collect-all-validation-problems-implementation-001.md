# Review request for collect-all validation problems implementation 001

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Please review the staged `validator-collect-all-v4` patch. The live walk uses v3. Applying the patch requires the user's authorization and a queue boundary compatible with pending approvals.

- The adapter still allows one repair turn, then fully revalidates the final annotation. Rejected-reference diagnostics give the indexed path and rejected value, with v3-style masking for malformed values. Method diagnostics give the verification path, finding ID and supported tool kinds. Feedback uses only the candidate, the recorded transcript and validator rules.
- Checks require the relevant shape and identifiers. For a broken evidence list, derivation, deduplication and method checks that require its resolved calls are skipped. A missing or invalid finding ID or method skips method checks for that verification record. Other fields and records continue. Coverage and successful-run requirements are checked independently, and integrity failures still abort validation.
- Feedback is capped at 4,096 UTF-8 bytes including the instruction to leave other text unchanged. It keeps an ordered prefix of complete diagnostics and gives exact total and omitted counts when capped.
- The validator replay uses each archived run's original transcript and packet. It reproduced the v3 feedback byte for byte and verified the second-final refusals. On the same original candidates, v4 reports both absent citation positions for 345/001, and both the absent source-note citation and the unsupported verification evidence kind for 346/001. The replay records the exact messages. It did not call the teacher.
- The isolated candidate passed all 358 tests with `EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests`. The patch passes `git apply --check` against the live baseline. The hash manifest binds both 50-file production sets and each changed file. All live production hashes still match the baseline.

## Artifact bindings

- reviews/requests/collect-all-validation-problems-proposal-001.md: `48055f664a7e84c52562ebbb55848a67ba64d0b27ae80501f6807ce5d413108d`
- reviews/verdicts/collect-all-validation-problems-proposal-001.md: `5087d40199ccc58a13d731b6f9733f58fea1a16850fcf0c9ca7d73f40b71f709`
- reports/collect-all-validation-problems-implementation-001.patch: `c98ee67a70696a4464b78cc6cea3034b88df85710efe3cb7bf76b27c608e9d27`
- reports/collect-all-validation-problems-implementation-001.hashes.json: `ac9eb1c7ec4030760c7c64b72f74061f4372db308597c8a09b081da803571bad`
- reports/collect-all-validation-problems-implementation-001-suite.log: `9cc378b031feae7f9b36431da03d633f598ce71c0bfc3c02d2132eb9346f8379`
- reports/collect-all-validation-problems-implementation-001-replay.py: `2cebb2d68e94ce3bd171604ed7d0ec3abf3d023b4b08a7bf501b36d48c5f42ca`
- reports/collect-all-validation-problems-implementation-001-replay.json: `c027dad4191b30223ab031ed5f96f8c2886e0e0f3175b06fd324d21a318f2782`
