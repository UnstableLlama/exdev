# Implementation request: tool-replay-errors-implementation-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

The completed 164 teacher recorded an evidence_index argument error (max_bytes=24000), recovered with 16384, and saved its draft. Its supervisor then failed because validate_run did not reproduce FreshSession's exception-to-tool-result conversion. Original failure artifacts and authored run remain unchanged; 164's separate request documents the manual exact replay recovery performed before implementation edits.

The administrative replay now catches exactly ValueError and RuntimeError, forms the same {ok:false,error:str(exc)} envelope as FreshSession, and compares the complete result. It neither skips failed calls nor accepts a different error or success/error substitution. Other exceptions still propagate. Manifest/provenance/implementation/assistance/blob checks and failed-run stop behavior remain intact. No teacher-visible input, argument limits, worker or provider behavior changes.

Regression tests cover matching ValueError/RuntimeError, differing error messages, success/error substitutions in both directions, matching success and an uncaught OSError. All 35 actual 164 results replay identically with the permanent function on the host-enabled sandbox. The earlier recovery report separately records the complete pre-edit implementation fingerprint checks; this new report does not claim current source files match the older provenance.

Full host-enabled suite with the separately submitted guidance-6 patch installed: **280 tests passed** in 22.344 seconds. No new teacher session was started. Please accept this administrative fix before the next cycle; 164 remains awaiting its ancestor-retrieval verdict. The failure result is retained and the journal records supervisory failure plus successful validation recovery, rather than presenting the original supervisor as successful.
## SHA256

- teacher/cycle.py: `dd093552f9d46c3dfa5ac3eb7156f48c56dfb56a6dc4edc502c05d175dd03b80`
- tests/test_cycle.py: `f636725f4ec4b636da3405edb1a2caa6f0507ddd9c83685ce2cf805c6c69bfca`
- reports/tool-replay-errors-implementation-001.patch: `e325fcf5177db329d14a040900290423634a6312e5ef157c5014ca0873267811`
- reports/tool-replay-errors-implementation-001.json: `9a2d9fbacd732b0e3e351aa2fc4014f5a23f0e6c156639ca9c045a632542ac27`
- reports/guidance-6-tests-001.txt: `a46bbc93b31520018ac48a1e42778ed3c0d4838cdfd8c8402953e0070cab7598`
- reports/commit-000164-validation-001.json: `c3a00d9292612304935f148696e2d7f2286b92c49cd3ffac0dc01cac29ecf7ce`
- reports/commit-000164-replay-recovery-001.py: `fe1cd1e175e3368c88dd1df06e0cb721eb87a18d40483047a27d23ffc456ebcc`
- reports/commit-000164-manual-001.result.json: `fe3e8b1e1bf4f2d3867b61ae0e9c6ff1530828d9522775b959a1908711bfe7c9`
