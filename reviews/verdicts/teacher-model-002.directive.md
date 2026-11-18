# Directive: switch teacher and author to gpt-6.2-sol

Reviewer: Fable, relaying the user. Date: 2026-11-17 20:48 UTC.

The user's words: "it looks like openai just came out with 6.2 sol, can we switch to that for the author and
teacher?" `gpt-6.2-sol` is in the Codex 0.167.0 model catalogue on this machine (fetched 20:46 UTC).

## What to do

1. Finish and submit whatever run is complete now (309) on `gpt-6.1-sol`. Do not start a new teacher run on
   6.1 after reading this. Let run-ahead drain; do not discard a finished run.
2. Implementation change `teacher-model-implementation-002`: in `teacher/codex_adapter.py` set `MODEL` and
   `TRIAL_MODEL` to `gpt-6.2-sol`, effort stays medium, contract 8 and guidance 12 unchanged. Nothing else.
   Run the focused and full tests, submit the request with the diff and new implementation hashes.
3. Stop there and wait. After I accept it I will restart your window on `gpt-6.2-sol` (same thread, same
   rules); you re-read `reviews/AUTHOR-INSTRUCTIONS.md` and `reviews/AUTHOR-STATE.md` and continue.
4. No separate trial. The first three entries on 6.2 are the test: I review them at full depth, and the
   user is told the result. Requests must keep reporting the model read from provenance.
