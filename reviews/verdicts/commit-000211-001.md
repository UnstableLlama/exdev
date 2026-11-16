# Verdict: commit-000211-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000211-001`
Packet: `.teacher/retrieval/000211-001`
Upstream: `00ad26e86660724a794c09bb808741493703ad47` "convert.py: Experimental args bitrate tweaking"
Request: `reviews/requests/commit-000211-001.md` (sha256 `8c0ac37c041c8743cac5592f4ec712cc823d54840f591f246f8c8820be5d0c6f`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement about this commit that I checked is true, and the new finding is true as stated. The inherited
budget finding is repeated without the qualification recorded at 181 and 182; that condition stands (below).
The ledger item filed with this request is accepted.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 35 of 35 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 210 strict-ancestor entries; 3,005 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 35 of 35 recorded tool calls identical, including the three `run` calls. |
| Unassisted | Standing instructions byte-identical to 210/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fifteen open rows at 2025-05-31T14:59:05Z; my query agrees. Six closed rows, five by path alone, none cut; discussion links are called inferences. |
| The option | `-strat/--strategy`, string, parser default `None`, stored default `""`, registered as not overridable. In `override`, a resumed job whose stored value differs from a new non-empty one raises unless `--override_anyway`. Correct. |
| `mod_strategy` | Prepends an empty segment and indexes by the position in `model.modules`, so the first segment addresses index 1; each segment is read as letter-digit pairs, later pairs overwriting earlier; each strategy key is looked up in the block and its bits become `min(bits + increment, 8)`. Called after allocation; the surplus kept is the allocator's. Correct. |
| Labels | Attention q/k/v/o; MLP u/d; GatedMLP g/u/d on every slice; default empty elsewhere. `Module.find_module` returns the first module with the key, else `None`. Correct. |
| Lookup always succeeds here | Strategy keys are the projections' own keys (the allocator maps pattern keys back to each module's key), and attention, MLP, sliced and block-sparse projections are all registered submodules. Block-sparse experts and heads are found but unlabelled, so they get no increment. Correct. |
| New `Linear` parameter | Inserted before `fkey`; the AST scan of call sites found no positional use of the shifted arguments. Correct, with the stated limit on external callers. |
| Finding: malformed strategy | `"q"` leaves one character, so `s[1]` raises `IndexError`; `"q-1"` gives `int("-")`, a `ValueError`; a two-digit increment such as `q10` fails the same way. Raised when the loop reaches that module's index, with earlier modules already converted. True. |
| Execution | An AST scan and a line printer over the parent tree, and a standard-library transcription of the parser; all labelled. |

## Not verified

- Any conversion run; what the increments do to quality or size.

## Must fix before canonical use

1. `inherited-exact-budget-boundary` is stated as at the root entry, without the qualification from the 181 and
   182 verdicts: the callers' budget already includes `+1`, so the practical effect is not an excluded exact
   match. The identity remains held; no ledger record follows from this entry.
2. Minor: say that a malformed segment is only reached when the loop arrives at that module, so a long
   conversion can fail part-way instead of at start-up. The entry's "before processing modules" is the expected
   behaviour, not the actual one, and could say so more plainly.

## Ledger items filed with this request

- `exllamav3-reconstruction-width--r001`: **accepted.** One identity, suspected; introduction at the root for
  the missing width check and truncated stride; 210 recorded as the commit that changes the consequence; no
  fix; not eligible for teacher context.

## Follow-ups

1. Ledger, with 212's request: the malformed-strategy finding as suspected, introduced at `00ad26e8`.

## Next

1. Record this approval with `--approve`.
2. Proceed to 212.
