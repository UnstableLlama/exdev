# Backfill result: processor-metadata-backfill-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implementation acceptance recorded: reviews/verdicts/processor-metadata-implementation-001.md; all eight implementation-request hashes verified. This is the approved pinned-only backfill, not a new implementation change.

Recovered all 26 files: preprocessor_config.json and processor_config.json for each of eleven selected Gemma 3 references from 164/225 and both selected Mistral 3 references from 234. No absences or inaccessible files. The result JSON lists each repository, original official pin, URL, publication date, SHA256 and status; it also binds all cached proof files.

Gemma 3 recovery uses official metadata queried at each originally recorded official revision, and ModelScope listings at the original mirror revision. Each new file's immutable mirror revision, pre-cutoff commit date, size, SHA256 and official Git-blob identity were checked. The new selection revision is necessarily a new file-set digest after adding the two files; existing source bytes and provenance remain unchanged. Official Mistral 3 files use the original official pins and pinned-tree Git-blob checks. No weight payload was fetched.

New bundles live under data/evidence/processor-metadata-backfill-001/ (ignored large local assets), not reports/. Both pass architecture_evidence.load_bundle at their original tasks/cutoffs. All previous objects are unchanged except the new mirror file-set revision on copies. Both original bundle hashes remain unchanged. Commit 225's evidence index matches all 130 original Gemma 3 objects from 164; no separate reference selection was invented for 225.

No bound bundle, historical packet, entry or approval was rewritten; no re-authoring. These new bundles are retained for later eligible positions only and have not been attached to the running 236 session. Guidance remains 9. Please review the backfill result; no canonical or training approval is requested.

Validation uses the accepted implementation and its existing 282-test passing suite; this backfill adds only an administrative retrieval script and data. Live checks: 26 JSON payloads parsed and hashes verified, mirror proofs validated, two complete bundles validated, original bundles and copied objects compared.

## SHA256

- reviews/verdicts/processor-metadata-implementation-001.md: `71a0a3b40327e44a12b13cc146386473161c9b85c00fdb6d7d4b48dfaf16dcde`
- reports/processor-metadata-backfill-001.py: `6f61808bcb15115c7c5cc094d28b29901ed0294a4ee3c3211f7df6b7bf68a466`
- reports/processor-metadata-backfill-001.json: `7f26a540fb8eb372c94ffd682cd37e75ccb4a4a7e1361aa85a2b2e3706d2fad9`
- reports/processor-metadata-backfill-001.log: `75b865eb431500daa9cfa5bdfb89d4c34c77b23f0d301c7574df98ee5d1434bd`
- data/evidence/processor-metadata-backfill-001/000164-references.json: `8e53123357afe7919f2634cafc6415fb0ad318e9406e15130a5718ceb391a3e4`
- data/evidence/processor-metadata-backfill-001/000234-references.json: `dd8dce1e6cf5f65e075b1fb101775f89ab465778acc035ff004a9c534937319d`
- data/evidence/github/000164-references.json: `13ac612239f96fd9bc4826aebb1a3776156b66144ff75608b87a8194b487d40b`
- data/evidence/github/000234-references.json: `c0ddcc2108d7ad50802b84f64cae19eb34e3c9b3b91904fc2b41688c7ff8dd33`
