# Verdict: commit-000040-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000040-001`
Packet: `.teacher/retrieval/000040-001`
Upstream: `4c7b1e29485c7004a59be08ae8d88ebd239e36d1` "Add Markdown support to example chatbot"
Request: `reviews/requests/commit-000040-001.md`
Reviewed: 2026-11-13, in the local checkout at `dfebc8a` plus Astra's uncommitted records

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

The walk may continue from commit 41.

## Artifacts reviewed (sha256)

If any differ, this verdict does not apply.

- draft.json: `9c73947d0cd3323ce8081d3729788bac719c4acff1a724bd9ca1a1b726107878`
- draft.md: `b3c17c6a78d96bdc004ae2eedaa5176e54daf1f23660614e764a9aff75fa1b3c`
- raw-transcript.json: `8dcac168f97a76465df79efa6822e8f27f4b78c2cb70883e62e014438abd2356`
- provenance.json: `40032d141a26298ab414fd62964259ed125da2e555d7c260b9807c557796416e`
- coverage.json: `07f234ca5889013a18b75306862549b6ba664a514fc19fddfbcf45552308d351`
- packet manifest (on disk): `14fff32892934630ea755c9e7a33a25b986e755b563e34160981ac2f5c811b18`
- unreferenced evidence bundle: `fc136d32c1515802157aaf42b3baeee3d98bacc3158292dcd78a44c75fc6cf96`
- validation report: `7a718b7c1e1e3f1b4ee3145259ed428c7c75e91490ef7efd58d4d468a76a262f`

All eight match the request.

## Run checks

| Check | Result |
|---|---|
| Evidence hashes | 9 of 9 ledger entries match the transcript tool results, with matching tool and arguments. Every call made is in the ledger. |
| Final message | The last assistant message parses to exactly `draft.json`'s annotation. |
| Markdown | `draft.md` equals `teacher.editorial.render(draft.json)`. |
| Policy assessment | Passes; full review (non-mechanical path, finding present, execution claim). |
| Provenance | Packet manifest on disk matches provenance. 34 of 34 implementation hashes match the working tree. Standing instructions are byte-identical to the previous runs. |
| Packet ancestry (on disk) | Exactly 39 entries, equal to the 39 strict ancestors; no duplicates. Nothing outside the ancestors and the task. All 489 blobs hash to their names. Commit 17 is attempt 003 and commit 32 is attempt 002. |
| Hindsight boundary | I searched the whole packet for the later-fix SHA and for the word "hindsight": no matches. The commit 39 review report keeps the reminder administrative. |
| Opening context | Message, author name, parent `75c7366b` (commit 39) and task SHA match Git. Cutoff `2025-04-12T03:26:05+02:00` is the committer date. |
| Catalog | Six rows: 1, 4, 7, 10, 12, 13. Issues 12 and 13 closed at 02:05 and 02:43 UTC, after this cutoff (01:26 UTC). Correct. No snapshot timestamp is later than the cutoff. |
| Reading rule | Followed: issues 7 and 12 read. Issue 12's hint names `examples/chat.py`, the file this task changes. PR 13 not read, consistent with the commit 38 note. |
| Source claims | Verified against the diff and parent file. Three unconditional `rich` imports. Streamer pair selected by `--basic_console`, Rich the default. `--refresh_per_second` defaults to 25 and goes only to `Live`. `Streamer_rich` builds `Live(..., vertical_overflow="visible")` and re-creates `Markdown` from the whole accumulated string on each chunk. Both streamers add the raw chunk to `all_text` and drop one leading space from display only at the start. History gets `s.all_text.strip()`. The max-token warning is set as a flag inside the context and printed after it exits. Default response limit is still 1000. |
| `--mli` finding | Confirmed. `read_input_rich` calls `Prompt.ask` and never reads `args.mli`; only `read_input_console` keeps `sys.stdin.read()`. With the default (Rich) path the option has no effect. Marked suspected, classified as a behaviour change, reach stated, no execution claimed. That is the right strength. |
| Scalar check | Re-ran the recorded command: output identical, 343 sequences (7 choices, 3 chunks). It compares old and new string accumulation only, and the draft says so. |
| Issue notes | Issue 12's title is quoted exactly and its traceback does fail at `Job(` in `examples/chat.py`; the link is labelled inference and says this patch does not touch stop conditions. Issue 7's title is quoted exactly; it is an import failure of the native extension and the reporter's follow-up gives a conda toolchain workaround. |
| Ancestor attribution | The read root chapter (usage-evaluation) describes `chat.py` as the draft says; it is linked. |
| Tests | Full suite: 189 passed with pinned Codex 0.167.0 first on PATH (re-run by me). |
| Commit 39 records | `review.json`, `reports/commit-000039-review-001.json` and the journal bind my verdict by path and the correct SHA-256 and keep canonical and training false. The position 44 reminder and the reference-evidence question are recorded as administrative only, with no guidance change. |

## Not verified here

- Nothing was rendered. Rich's behaviour (how `Markdown` treats the ANSI colour codes in the prefix, whether `Prompt.ask` strips input) was not executed by me or by the teacher.
- That each of the other 37 packet entries is the currently approved attempt for its commit.
- GitHub was not re-queried; I reused the state fetched earlier today.

## Must fix before any canonical use (not blocking ancestor retrieval)

1. "Rich imports are unconditional" should say whether `rich` was already a declared dependency. It was: `requirements.txt` and `setup.py` both list it in the parent, and `exllamav3/util/progress.py` already imports it. Without that, a reader may take the sentence as a new-dependency warning.
2. Two differences on the default input path are not mentioned: the old code called `.strip()` on the input and the new Rich path leaves that to `Prompt.ask`, and the bot-name prefix with raw ANSI codes is now passed through `Markdown`. Both are unexecuted library behaviour; a canonical entry should list them as unestablished.

## Follow-ups

1. Carried and still open: the user's pending question on reference evidence for new-architecture commits; the position 44 ledger check; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

## Next

Record this approval locally with the original packet and continue the walk from commit 41.
