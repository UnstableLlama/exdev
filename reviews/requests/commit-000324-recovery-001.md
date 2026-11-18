# Failure handoff for commit 324

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Run `.teacher/runs/commit-000324-001`, packet `.teacher/retrieval/000324-001`. Upstream `6171f9af3d4b477ccd43fdf8d7172d40fc770a38` — **Fix default chat prompts for Dots and Ernie**.

The original final and single validator repair final (17,054 bytes each) both failed with `Unknown or unsuccessful evidence call`. Both cite `call_50832e5bd8be469ba24c813982789a2` in the third Source Notes claim, which discusses two VRAM issue reports. That call ID is absent from the transcript. The repair reran a scalar prompt-format check and updated its citations. The refused finals are transcript rows 128 and 133 (zero-based), respectively.

The queue is stopped at 324, with no active cycle or published draft. Please review one fresh unassisted 324/002 attempt via the normal packet builder, with the same cutoff, approved ancestors, pinned evidence, contract 8, guidance 12 and gpt-6.2-sol medium. Preserve 324/001 and keep this handoff out of teacher input.

## Artifact bindings

- reports/run-ahead-detached-000324-806b83c1ca274d53a9d884669b9a5444.json: `5eb37f8414d786aea36ff3eb0e36870f6f57c7e352d4330701b007b2bbd9b4f4`
- reports/run-ahead-detached-000324-806b83c1ca274d53a9d884669b9a5444.log: `d6a0f560a189fac8c444a712fbd2c1b5ee362e74409f934c88f33d270b469f32`
- .teacher/admin/run-ahead/0d8ba71f593d4dbebaed171ca27fd409.log: `ebfb983d81c43b7fd3148887e5f4d5c9b29de0a11a8be958b4c7760b54fef741`
- .teacher/admin/run-ahead/0d8ba71f593d4dbebaed171ca27fd409.json: `009cae46c908caa7828e13ead1cb24cc817ecddce6fb42352766febcdf456e42`
- reports/commit-000324-catalog-selection-001.json: `c1607e0e908f6b61da67dcd5793b8466d01d559ca446949e080bbfb4dbe3fcf8`
- .teacher/retrieval/000324-001/manifest.json: `6e3c26bf4b3df623f11b384afe307cda7f9d2fa89c3228701e55c0e05d8e6523`
- .teacher/runs/commit-000324-001/status.json: `5c9212a8a1ae15548ed79fbbc877ae1904c6dec5e5a3e65ebfa40bd2a195696e`
- .teacher/runs/commit-000324-001/provenance.json: `3c843e67356eecf9bd370604176e8cef9e4f041298288c435bbd9e00de2d85d6`
- .teacher/runs/commit-000324-001/raw-transcript.json: `3e80a40c7a590641cccc02bf769a858a3fed275bcfd48d50dad78bb83aeb9345`
