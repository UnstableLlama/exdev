# Verdict: commit-000169-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000169-001`
Packet: `.teacher/retrieval/000169-001`
Upstream: `0488385eb0d4ed8066798435469806a8572aeac2` "Add simple long-context evaluation script"
Request: `reviews/requests/commit-000169-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only**, with canonical-use notes. Canonical and training remain false.

Every statement I checked is true and the finding is correct and important: as committed, the script cannot
start. The entry is short for a commit that adds a whole evaluation tool, and it leaves out what makes that tool
interesting (below). Nothing in it is wrong.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review, with `validation_incomplete` correctly raised; 44 of 44 implementation hashes; exactly 168 strict-ancestor entries; 2,607 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 168/001's. Guidance 5. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path or the tracking files. |
| Catalog | Twelve open rows at 2025-05-17T14:58:12Z; my query agrees. One closed row by terms, selected. |
| Sections | Four of nine read: the script, the two reference summaries and the character list. The five unread are the story texts, about 79,000 words. Disclosed, and the entry claims nothing about their content. |
| The script | Loads the model through `model_init.init`, prints the bitrates from `get_storage_info`, builds each prompt with a Transformers tokenizer's chat template, makes nine jobs with `GreedySampler`, a 768-token limit and the model's EOS list, enqueues them together, and prints each completion beside a reference where one exists. No scoring. Correct. |
| Finding `unsupported-cache-default-argument` | Correct. The entry point calls `model_init.add_args(parser, default_cache_size = 65536)`; at this commit `add_args` takes `parser` and `cache` only. The teacher extracted the real function from the parent tree and called it; the recorded result is the `TypeError`. The imports the script needs do exist (`GreedySampler` is exported), so this is the first thing that fails. Suspected is conservative; the helper itself was executed. |
| The 65,536 | A cache size in tokens passed on as the default, not a measured text length. Correct. |

## Reviewer-only notes (never to a teacher)

- **What the tool actually tests is in the script the teacher read, and the entry does not say it.** Three of
  the nine tasks use altered copies of a story: one with a paragraph translated into another language to be
  translated back, one with two paragraphs rewritten in slang to be identified, and one with an unrelated
  passage inserted to be found. The fourth story has its names replaced, with reference answers using the new
  names, which is the script's answer to the memorisation worry it states in its own TODO. The entry reduces all
  this to "passage identification". I confirmed the three alterations by comparing the text files: a replaced
  paragraph at one place in the first copy, rewritten paragraphs in the second, and fifteen inserted lines in the
  third.
- The story files are opened without an encoding argument and contain non-ASCII punctuation; on a platform whose
  default is not UTF-8 the read would differ. Not raised by the entry; minor.
- 168's fix an hour earlier is what makes the bitrate line at the top of this script right for Gemma 3.
- Hindsight to watch: the missing `default_cache_size` parameter suggests a change to `model_init.py` that was
  not committed with this script. Expect it soon.

## Not verified

- Any run of the script. The content of the story files beyond the differences above.

## Must fix before canonical use

- Describe the nine tasks as they are, including the three altered-text tasks and the name replacement.
- Five text sections were not read; either read them or keep saying so.

## Follow-ups

1. Ledger: file `unsupported-cache-default-argument`, introduced at `0488385e`, with verification by isolated
   execution of the parent helper.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval with `--approve`.
2. Continue at 170 on guidance 5.
