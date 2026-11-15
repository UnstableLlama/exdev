# Verdict: modelscope-mirror-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/modelscope-mirror-implementation-001.md`
Implements: `reviews/verdicts/commit-000098-reference-mirrors.decision.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**ACCEPTED.** Author commit 98 with this bundle, unassisted, and file it for full review.

## Artifacts reviewed (sha256)

All sixteen hashes in the request match the files on disk.

## What I checked

| Check | Result |
|---|---|
| Code read | `teacher/mirror_evidence.py` in full; the mirror lines in `architecture_evidence.py`; the `evidence_index.py` diff; the documentation section. |
| Fail-closed behaviour | Recovery refuses an ungated official repository, an official repository created after the cutoff, a mirror file missing or dated after the cutoff, a size mismatch, a masked or malformed hash, a mirror hash unequal to the official one, downloaded bytes unequal to the mirror's stated hash, and a tensor file with no published full-file hash. The validator repeats the proofs on the stored bundle, recomputes the file-set digest and rejects tampering. Matches the decision's points 2 to 4. |
| No weight downloads | Tensor files get two ranged reads (bytes 0 to 7, then the header) and the validator requires exactly those ranges. |
| Identity in the bundle | Items carry the official name as `repo_id`, the historical name, the mirror repository, the mirror commit and its date. The index row shown to a teacher adds the plain notice and the historical name. Matches point 4. |
| Tests | 231 passed with the pinned Codex first on PATH and sandbox tests enabled (9.4 s), run by me. |
| Bundle, independently | I refetched Hugging Face's public metadata and ModelScope's listing for all ten repositories and rechecked every one of the 220 items without using the new module: Git blob id of the stored bytes against the official blob id for small files; official SHA-256 against ModelScope's for large files; stored bytes against ModelScope's SHA-256 for non-weight files; mirror commit and date against the listing; date at or before the cutoff. 220 of 220 pass. Latest mirror file date 2024-12-14. |
| Headers | 172 headers, equal to the number of safetensors files the ten official repositories list (15, 5, 44, 13, 4, 15, 14, 44, 4, 14). In all 172, eight bytes plus the header length plus the largest tensor end offset equals the file size the mirror reports, so each header is the header of a file of that exact size. |
| Architecture strings | All ten pinned `config.json` files declare `CohereForCausalLM`. |
| Discovery report 002 | The five other gated repositories are labelled `not_inspected_at_pin` with their current public architecture string, as point 5 asks. |

## Limits to carry

- Whole weight files were not hashed here. That a ModelScope weight file equals the official one rests on the two
  services' published SHA-256 values agreeing. The header bytes themselves are covered only by ModelScope serving the
  file it lists; the size check above is the one independent constraint on them. The bundle says this in
  `identity_limit`. It is enough for reference evidence that consists of tensor names, shapes and dtypes.
- The official revision id recorded in each proof is the repository's current commit, which may postdate the cutoff. It
  is an opaque hash and carries no information; noted so nobody later mistakes it for a pin.
- The second header fetch appends `&header=metadata` to the URL while the stored URL omits it. Harmless as far as I can
  see; say in the report why it is there.

## Not verified

- A live teacher session reading this bundle. That is commit 98's review.

## Next

1. Record this acceptance.
2. Author commit 98 unassisted on this bundle. File it and wait for my verdict.
