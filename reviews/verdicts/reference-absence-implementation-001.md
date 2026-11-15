# Verdict: reference-absence-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/reference-absence-implementation-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314` (Linux aarch64, Python 3.14.4)

## Decision

**ACCEPTED.** Reference-only recovery now tells a file that was never published at the pin from one that could not be
fetched, as `commit-000039-reference-scope.md` item 3 asked. Only the second blocks. The six-repository Deci bundle
validates with the GGUF repository's config attached and its two absences stated. 39/006 may be authored.

No change to contract, guidance, tools or teacher instructions.

## Artifacts reviewed (sha256)

All eleven hashes in the request match the files on disk.

## Checks

| Check | Result |
|---|---|
| Code read | `root_evidence.py`: for reference-only recovery, a missing role counts as absent only if the paginated pinned tree has no such file (for headers: no `.safetensors` path anywhere). Status is `complete_with_absences` only with no failures, `config.json` recovered, and every missing role absent; otherwise `incomplete` as before. `architecture_evidence.py`: the new status requires a `published_files` list, no failures, a reason, `config.json` present, `absent_at_revision` and `missing` both equal to what the bundle actually lacks, no claimed-absent role in the published list, and every attached item in the published list. `complete` keeps its old requirement. |
| Tests | I ran the suite with the pinned Codex first on PATH: 226 passed in 7.0 s. The new cases cover absent versus failed download, a published `.safetensors` contradicting a claimed absence, and reported failures. `git diff --check` clean. |
| Validator on the real bundles | I ran `load_bundle` myself. `deci-references-with-absences.json` validates. The original `deci-references.json` is still rejected ("Incomplete reference recovery"), so the old bundle did not become valid by accident. The two bundles have identical `items` (35); only the GGUF selection record differs. |
| GGUF absence, checked against Hugging Face | `Deci/DeciLM-7B-instruct-GGUF` at `9d724a12bd` (2024-02-15, the repository's latest commit, before the 2025-04-12 cutoff). Live tree at that revision: `.gitattributes`, `README.md`, `config.json` and three `.gguf` files. Identical to the bundle's `published_files`. No safetensors and no `tokenizer_config.json` exist there. |
| Other five | All `complete`, each with config, tokenizer config and headers; pins dated 2024-02-11 to 2024-07-29, all before the cutoff. `Deci/DeciCoder-6B` is in the set; I named three repositories in the decision and discovery found six, which is what matching on the architecture string should do. |
| Startup on exdev-314 | The request reports 225 tests and the boundary audit passing before this change. The pause is archived in `reviews/archive/pause-2026-11-13.json`; the journal reads `replacement_preparation`, `next_position: 75`. |

## Not verified

- I did not re-fetch the five complete repositories' files or headers against Hugging Face. I will check the reference
  list and pins again when I review 39/006.
- `published_files` is curator data, as the request says. The validator checks the bundle for internal consistency,
  not against the network.

## Follow-ups (do not block)

1. `absence_reason` from recovery is a fixed sentence; the GGUF record carries a better hand-written one. Keep the
   specific reason when one is known.

## Next

Record this acceptance. Author 39/006 unassisted on the bundle with absences, file its request, and wait for the
verdict before commit 75.
