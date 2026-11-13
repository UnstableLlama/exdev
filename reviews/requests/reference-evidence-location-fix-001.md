# Review request: architecture location guard

Reply-to thread: 01a1d636-5761-7593-8e19-f8453a562b16

Prior implementation acceptance is recorded in
`reports/reference-evidence-and-callee-review-001.json`, bound to verdict
`reviews/verdicts/reference-evidence-and-callee-implementation-001.md`
(SHA256 `52fbe55911d0e02e4682d634f38270c8c3a2c663ce00ad6e4d342354fbaafa54`).

This implements required fix 3 only. Inventory scans both known directories.
A non-root task with no model/config classes in either fails closed before
reference loading or packet preparation. Root tasks retain their exemption.

Tests cover successor-directory detection, a new class there, an unknown move
failing at trigger and loader, and root exemption. The common packet fixture
has an opt-in model class used only by architecture/walk tests. Full pinned
host-enabled suite: **197 passed** (sqlite ResourceWarning, no failures).
`git diff --check` passed.

Real-history checks find the moved classes at d9906114 and recognize the
successor location at the pinned tip. The moved files still trigger recovery:
rename/merge classification is the separate required fix 1, still open, along
with identity derivation fix 2. Both remain due before position 100.

Report and exact file hashes: `reports/reference-evidence-location-fix-001.json`, SHA256 `cfee02eb1636cc0f85fa3be651e6365eeb186c70752f1cb4a79380319b4119b4`.
Contract remains v5; guidance remains v2. No new authoring or reference recovery
was performed. The walk stays stopped before 44 pending the user's ordering
decision; this request is not prose approval.

Write only `reviews/verdicts/reference-evidence-location-fix-001.md`.
