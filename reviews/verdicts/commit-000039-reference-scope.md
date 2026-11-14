# Reviewer answer: reference scope for 39/006

From Fable, 2026-11-13. Answers the question in `reports/commit-000039-reference-recovery-006.json` (walk status
`awaiting_reference_scope_answer`). This is my reading of the user's decision in
`commit-000039-deci-references.decision.md`, not a new user decision. The user can overrule it.

Recovery found five complete Deci repositories and one incomplete: `Deci/DeciLM-7B-instruct-GGUF`, whose pinned
`config.json` declares the architecture but which has no safetensors files and no `tokenizer_config.json`.

Answer:

1. Attach the five complete repositories as they are.
2. Attach the GGUF repository's `config.json` too, and record in the bundle that it has no tensor headers and no
   tokenizer config, with the reason (a GGUF conversion; the files do not exist at the pinned revision). "Attach configs
   and headers" means attach what exists and say what does not. A file that was never published is not a recovery
   failure.
3. The validator's "Incomplete reference recovery" should tell apart a file that does not exist at the pin from one that
   could not be fetched. Only the second blocks. If that needs a code change, it goes through an implementation request
   as usual.
4. Nothing else about 39/006 changes: unassisted, no coverage request, 39/005 in force until 006 is reviewed.
