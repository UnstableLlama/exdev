# Verdict: commit-000150-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000150-001`
Packet: `.teacher/retrieval/000150-001`
Upstream: `1e1754787e52f416252a36ea3ebf7177d2e11f2a` "HumanEval: Move BOS token to individual prompt template, don't prepend by default when tokenizing"
Request: `reviews/requests/commit-000150-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry notices two things the diff does not announce: Gemma's template
already began with `<bos>`, so it had been getting two; and the new condition keeps automatic BOS for an explicit
`raw` format only, while leaving the option out (the documented default, which is a different code path) now gets
none. It is careful to say that the six added markers keep the old token sequence only if each tokenizer maps the
literal to its BOS id. No findings.

The entry's reason for the change is labelled inference, and it had no better source: the most relevant discussion
was not in its packet. That is a gap in the catalog rule, not in the entry; see "Catalog gap" below.

The ledger revision `exllamav3-top-k-int-is-integer-compatibility--r003` is **accepted**.

## Artifacts reviewed (sha256)

All twenty-two hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 149 strict-ancestor entries; 2,264 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions differ from 149/001's only by the merge paragraph that 149, a merge, carried. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Eleven open rows at 2025-05-11T21:02:07Z (33 closed then). Two closed rows of 25 candidates: pull request 25 and issue 16. The session read issue 16 and claims no connection. Correct as far as the catalog goes. |
| Architecture trigger | Does not fire. |
| The change | Six templates gain a leading marker: `granite` and `reka` `<|endoftext|>`, `llama` and `mistral` `<s>`, `llama3` `<|begin_of_text|>`, `deepseek` `<｜begin▁of▁sentence｜>`. `gemma` (already `<bos>`), `chatml`, `qwen3` and `raw` are untouched. The encode call's `add_bos = True` becomes `add_bos = (args.prompt_format == "raw")`. Nothing else. Correct. |
| Prompt selection | `args.prompt_format is None` selects the bare `"{{problem}}"` template, separately from the dictionary's `raw` entry, so the default invocation now encodes without BOS. The help text calls that default "raw completion (for base models)". As the entry says. |
| Tokenizer | `encode` prepends `bos_token_id` only when `add_bos` is true and the id is not `None`; with `encode_special_tokens` the text goes through `encode_special`, which calls the underlying tokenizer with `add_special_tokens = False`. Correct. |
| Execution | Recorded output: every format had automatic BOS before; afterwards only `raw`; the added text per format as listed; placeholder counts preserved. Matches the prose. |
| Ledger `top-k-int-is-integer-compatibility--r003` | Accepted. Adds 149 as affected with the HumanEval default reach and says that neither parent had the failure in that script. No execution claimed. |

## Catalog gap (for Astra; implementation matter, not a fault of this entry)

Pull request 35 was closed at this cutoff, changes the very file this commit changes, and received a comment at
2025-05-11T20:41:37Z, twenty minutes before this commit, reporting much higher scores with a configuration that
defines no BOS token. It was eligible. It did not qualify for the closed catalog, which offered pull request 25 and
issue 16 instead, neither of which has anything to do with this change. The rule scores a closed discussion only
by rare words shared with the commit message; a discussion that touches the same paths gets no credit for that.

Please look at whether path overlap (the task's changed files against a pull request's changed files, or against
paths named in a discussion) should qualify a closed row on its own. This is a request to investigate and, if you
agree, to file an implementation request; it does not block the walk, and 150 does not need a new attempt for
ancestor retrieval.

## Reviewer-only notes (never to a teacher)

- **Hindsight confirmed.** The BOS discussion I noted at 147 is this commit's motivation. The maintainer's own
  explanation follows at 21:08:59Z, seven minutes after this cutoff, and is not eligible here.
- **Possibly unintended (mine, low confidence).** The condition tests for the string `"raw"`, but the default
  "raw completion" is `None`. If the intent was "keep BOS for raw completion", the default path lost it by
  accident. I am not asking for a record on intent alone; watch for a later change to this line.
- **What was wrong before.** Gemma received two BOS tokens and ChatML/Qwen3 one they should not have, since the
  script's first commit (`543c4b27` has both the `<bos>` template and `add_bos = True`).
- The `raw` entry's second element is two adjacent string literals, so its prefix is eight spaces, not four. Old,
  and outside this change.

## Not verified

- Any tokenizer run: whether each literal marker encodes to that model's BOS id.

## Must fix before canonical use

1. A canonical entry should have the pull request 35 comment available. That depends on the catalog question above.

## Follow-ups

1. Catalog rule: as described above.
2. Ledger: a fix-derived record for the script's unconditional BOS (double for Gemma, unwanted for ChatML/Qwen3):
   introduced `543c4b27`, fixed `1e175478`, with the limit that marker recognition was not run.
3. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the ledger acceptance.
2. Continue the walk at commit 151.
