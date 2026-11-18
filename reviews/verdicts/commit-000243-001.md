# Verdict: commit-000243-001

Reviewer: Fable. Date: 2026-11-16. Upstream `64ef2a37` "Tokenizer: Faster initialization". **First walk entry
authored by `gpt-6.1-sol`** (medium, guidance 11), and the first request filed with the author session on Sol.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. All three findings are
**accepted as true**: `shared-vocabulary-extension` (new defect), `ordinal-return-removed` (behaviour
change), `inherited-eos-filter` (existing defect, carried over). The ledger revision
`exllamav3-vision-floating-ceiling-overflow` r004 is **accepted**.

## Artifacts

Request hashes match. `check.py` clean: manifest and provenance agree and record `gpt-6.1-sol`, medium; the
transcript's server-confirmed runtime says the same; 44 implementation hashes; 20 evidence calls all cited;
final equals annotation; 242 ancestors; 3316 blobs; nothing after the cutoff (2025-06-05T00:27:20Z).
Instructions identical to 242's run.

## Run checks

- Replay: 20 of 20 identical.
- Diff and the whole task file read. Batched decoding in `get_fixed_vocab`, the cached `raw_vocab_size`, and
  `lru_cache` replacing the attribute checks on the table getters are as the entry describes, including that
  `get_fixed_vocab` and `raw_vocab_size` are not under the lock.
- **`shared-vocabulary-extension`: true, and a good catch.** `get_fixed_vocab` is cached and returns one list
  object. `get_id_to_piece_list()` and `get_id_to_piece_list(False)` are different cache keys, so the
  constructor's `get_id_to_piece_list(True)` (which calls the no-argument form) and the following
  `get_id_to_piece_list(False)` each run the body, and each appends the tokens above the raw vocabulary size
  to that same list. I reproduced it with the real `functools.lru_cache`: ordinary list `['a','b','<x>','<x>']`,
  special copy `['a','b','<x>']`. The no-argument call returns the same doubled list, so the reverse
  dictionary built from it is affected too. It needs a tokenizer whose added or "unspecial" tokens have ids
  at or above the raw vocabulary size.
- `ordinal-return-removed`: true; the function body ends without a return. The entry is right that the only
  caller in the tree discards the value.
- `inherited-eos-filter`: true; the filter removes the EOS id on the line before the test for it. Only the
  size query on that path changed here. Correctly labelled inherited.
- The entry's caution about `range(raw_vocab_size)` assuming dense ids is fair and stated as a limit, not a
  finding.

## On the model

Nothing false, nothing invented, limits stated plainly, and the principal finding is one that needs the
cache-key distinction to be noticed. This entry is at least the standard of the Astra entries around it.

## On the request (author session on Sol)

Accurate where I checked it. It reports that token totals were not kept by the production transport and
does not substitute an estimate, which is the right way to miss a condition. See follow-up 1.

## Reviewer knowledge (hindsight; must not reach a teacher)

At the upstream tip both the doubled append and the missing return are gone: the getters are
`cached_property` based and the ordinal getter returns its list. `41544ae4` (2025-10-10, "Fix @lrucache
memory leaks") is the likely place; confirm when the walk reaches it before recording a fix.

## Ledger

- r004 of the ceiling-overflow record: `17f1ab5e` (242) recorded as the fix, earlier observations kept.
  Accepted, including the decision to keep the 234 table-width consequence under the same identity.
- Owed with the next request: new records for `shared-vocabulary-extension` and `ordinal-return-removed`
  (introduced at 243), and an observation revision on the existing EOS-filter identity.

## Follow-ups

1. Implementation request to keep token-usage totals for production walk runs, as the trial supervisor does
   (`token-usage-retention-001`). Small; not blocking the walk.

## Next

Record the approval. Run the five comparison trials, then 244. Replacements wait for the trial assessment.
