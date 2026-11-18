# Implementation request: guidance-11-adoption-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements the user's guidance-11 adoption decision. Commit237 finished under guidance9 and its review request is filed; its verdict is pending. An explicit advancement pause prevents238 until both that verdict and this adoption request are accepted. No238 or replacement run has started.

The only production change is prepare() writing guidance_version11 for new packets. teacher/session.py matches the accepted guidance11 gate hash exactly, including the version11 branch and paragraph F; versions5–10 are unchanged. The attached patch is relative to the working tree before adoption, excluding already accepted trial-gate changes. The existing compatibility test now checks default11 against its version11 branch while preserving all older-version checks.

Verification: complete opening messages, tools and reasoning effort reproduce identically for19 historical packets: the12 packets from the version9 adoption check (versions5–10), all six version11 trial packets, and237. All19 bound bundles validate. A freshly prepared fixture selects11 and validates; its instructions equal guidance9 plus the adoption decision's exact paragraph F, with identical non-system inputs, tools and reasoning effort. No provider/teacher was invoked, and no historical packet/run was edited. The full before-input snapshot and verification script/report are attached.

Full host-enabled suite: EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests — Ran 282 tests in 42.066s, OK, exit0. The initial suite failed one stale assertion comparing default inputs to version9; its log is preserved. That assertion now compares default inputs to version11, and the complete suite passed on rerun. ResourceWarnings concerning cleanup of HTTPError401 objects remain non-failing.

Please accept guidance11 as the default from238. Existing approvals remain ancestor retrieval only; canonical/training false. After acceptance I will file guidance-11-reauthoring-plan-001 for the eleven decision-listed entries; no replacement run before plan acceptance. The forward walk may resume while that plan is reviewed, subject to237 approval. Trial outputs remain excluded from ancestor retrieval.

## SHA256

- reviews/verdicts/guidance-11-adoption.decision.md: `8845a6711d39b1f7590bf489d591e1a184163bcd46826acc3ddba1e9d7cad458`
- reviews/verdicts/guidance-11-reauthoring.decision.md: `b821adb64f71e086b9a60f3a2243cc45bf1b88d2634e2ac8a38e7924512df70e`
- teacher/walk_inputs.py: `35327960008029745460ab3a6fb550f92672bf783f764b22505f6103e86809f2`
- teacher/session.py: `780404d28779bfaee28fea23f2bb2807859fc62fd558b6eff6506a6b23ad074c`
- tests/test_walk_inputs.py: `766c75074200f44bf768bfadc757d3e6467d587b99ff2c6193babca8db8265e9`
- reports/guidance-11-adoption-001.patch: `b020d6f6d3df7024749af14ccb67ba8043cee22d542d8db7d253b6e3c1705b5b`
- reports/guidance-11-adoption-before.json: `b69cc005cced14c206fd2408213c3017816eab9706efa259b8c4f72aa390b442`
- reports/guidance-11-adoption-verify-001.py: `e9f66f1aca9501d8de4ca887e533dd89e6542324675c00b2153b4e1485243ca7`
- reports/guidance-11-adoption-verification-001.json: `ba6c998971b7945c274728196bfeaed30de25d233349785b50c9e223f61f5976`
- reports/guidance-11-adoption-tests-initial-001.txt: `2e5b36271bb6c2829cb7a05b983788448b80987b68c69ce09b4b798d59766881`
- reports/guidance-11-adoption-tests-001.txt: `9cbae21f31b093f0cbdbee5e585fcb93ac30bc155287b173e9a0dfaa44f4b7de`
- reviews/requests/commit-000237-001.md: `0dbad1448739429f3501f35b6b943f7e2f436740acf96eef0cca143a3c9dfbeb`
