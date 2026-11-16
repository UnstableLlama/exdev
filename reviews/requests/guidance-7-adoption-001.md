# Implementation request: guidance-7-adoption-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements the user adoption decision in reviews/verdicts/guidance-6-adoption.decision.md. Commit 171 finished under guidance 5 and its request is filed at reviews/requests/commit-000171-001.md. No 172 teacher has started; awaiting both verdicts.

FreshSession selects the adopted three paragraphs for guidance 7, replacing the trial additions. Paragraph A uses the parent tree read together with the task diff; B and C are unchanged. Guidance 6 remains exactly as trialled. prepare() now defaults to 7 and contract 8 accepts 5, 6 and 7, retaining the earlier contract requirements and evidence integrity checks. No fourth paragraph is added. The attached patch is relative to the implementation immediately before this change, excluding unrelated existing work.

Verification uses the actual 171 version-5 packet and the 154 version-6 trial packet: system instructions, full opening messages, tools and reasoning effort match pre-edit snapshots exactly; both bundles still validate. A temporary hardlinked copy of 171 (manifest unlinked before rewriting) validates at version 7 and changes only the appended system instructions. Version-7 text equals the decision's three paragraphs including line breaks. Original packets and runs were not edited; no provider was invoked by verification. The verification script and before snapshots are attached. Initial administrative verification attempts stopped for a missing bundle-path argument and a cross-filesystem hardlink; the corrected script uses a temporary directory on the repository filesystem and completes successfully.

Full required host-enabled suite: EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests — 280 tests passed in 22.461 seconds (ResourceWarnings, no failures). The updated fixture test checks default 7, validation of all three versions, unchanged non-system inputs, replacement rather than duplicate guidance, and rejection of altered reference evidence.

Please review this implementation for use from the next walk commit. Existing approvals remain ancestor retrieval only; trial outputs remain unpublished and unapproved. The walk remains stopped pending your verdict.

## SHA256

- reviews/verdicts/guidance-6-adoption.decision.md: `fc6620e760801c060f85975a5fa73558a05dd4129e09119108c7392188454d7b`
- teacher/session.py: `953cfe8d697606fcf06f6212cc65ccdee511c83c5a49f56613d4fe39e5421b92`
- teacher/walk_inputs.py: `f795f4868c3d4adfd98c0b424e9330f2a548be13c494de15f0523df507b4be16`
- tests/test_walk_inputs.py: `a4637688652d5144949f726a30beb52bae911978e7bd43ee32b08ca9e680b41a`
- reports/guidance-7-adoption-001.patch: `9d4876fb8eb6ad1d6567776fe1f8a79a7ce4f2281db4fdb2a0519c014685d546`
- reports/guidance-7-adoption-001.json: `ecb46ea7c9d9e259cccde2f76e317daf3b652927a34a6d36e8bd27294fa0beed`
- reports/guidance-7-verify-001.py: `adbc95ecd238913590465377b3cf4cda9913df79358a1641139d15672e69a9dd`
- reports/guidance-7-v5-before.json: `5f47a3798c37bd85969ff3c278047c00e395cb047cf117e801a02029e50403ec`
- reports/guidance-7-v6-before.json: `48ee32147db63cfb855147c40decdbbbf018e1760ef1294c2431b80ee2013754`
- reports/guidance-7-tests-001.txt: `9b591fdf5f5225b808d1c4e60a295ae722d0b10c71bb5821b3a007b000516f56`
