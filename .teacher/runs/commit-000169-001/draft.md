# 0488385eb0d4ed8066798435469806a8572aeac2


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/0488385eb0d4ed8066798435469806a8572aeac2) · [Evidence ledger](draft.json)

Adds nine manually inspected long-context tasks, but an unsupported cache-default keyword prevents normal command-line startup.

- [Manual long-context evaluation](#usage-evaluation)

## Problem

The change adds a qualitative long-context evaluation script covering summarization, passage identification, question answering and named-character extraction. [source; call_64ae0d108b894751b0c78a02dbaeef55]

## Reasoning

Each task places the story before its instruction in a single user message. A Transformers tokenizer applies the chat template; the resulting token IDs become an ExLlamaV3 Job using greedy sampling, model-configured EOS tokens and a 768-token output limit. [source; call_64ae0d108b894751b0c78a02dbaeef55]

The nine jobs are enqueued together and iterated until none remain. Results are printed alongside selected reference answers rather than scored automatically, making this a manual comparison tool rather than a quantitative benchmark. [source; call_64ae0d108b894751b0c78a02dbaeef55]

## Impact

The intended command-line entry point is blocked before argument parsing: it passes default_cache_size=65536 to a helper that accepts only parser and cache. [source; call_64ae0d108b894751b0c78a02dbaeef55, call_989fcc41178048edaba2ae04a0562d53]

## Source Notes

The script itself acknowledges possible familiarity with the source stories through a TODO requesting unfamiliar original material. [source; call_64ae0d108b894751b0c78a02dbaeef55]

<a id="usage-evaluation"></a>

## Manual long-context evaluation

The script resolves eight fixture files relative to its own eval_texts directory, avoiding dependence on the working directory. Reference summaries and the character list are displayed after inference, not included in the corresponding prompts. [source; call_64ae0d108b894751b0c78a02dbaeef55, call_d87c75714d1a408a83a0bd526c0a3180, call_934b632fb106416f920906efacfb8f66, call_1604377013ae4d9680584f82b05d1d5e]

The requested 65536 value is a cache-token capacity, not a measured story length or accuracy threshold: model_init.init forwards args.cache_size as Cache.max_num_tokens. The existing parser helper instead supplies an 8192-token default and offers no default_cache_size parameter. [source; call_64ae0d108b894751b0c78a02dbaeef55, call_989fcc41178048edaba2ae04a0562d53]

Executing the unchanged parent add_args function extracted by AST, with the new entry point's keyword argument, produced TypeError: add_args() got an unexpected keyword argument 'default_cache_size'. [execution; call_755c9e4e2a0f4323bd0425818a8a36fd]

## Authoring-time findings — pending review

### unsupported-cache-default-argument (suspected; defect)

The new command-line entry point calls model_init.add_args with an unsupported keyword.

Trigger: Run eval/longctx.py as a script, assuming imports succeed.

Expected: Register command-line arguments with a 65536-token cache default, then parse arguments and start evaluation.

Actual: Argument registration raises TypeError before parse_args or main executes. This affects the direct script entry point, not a caller invoking main with an already constructed namespace. Whole-parent search found no longctx references.

Locations: 0488385eb0d4ed8066798435469806a8572aeac2:eval/longctx.py — __main__

Source evidence: call_64ae0d108b894751b0c78a02dbaeef55, call_989fcc41178048edaba2ae04a0562d53, call_cc32da76c2b140a2885dbdbefda8369c, call_c126df3d5c13477b93a2a222feb074c2

repository_execution: Compiled and executed the parent repository's actual add_args AST node with argparse supplied, then called it with the new keyword. [call_755c9e4e2a0f4323bd0425818a8a36fd]. Limits: Isolated helper execution only; the complete script, package imports and model loading were not run.

## Uncertainty and limits

No model inference or GPU execution was performed; tokenizer compatibility, context fit and generated-answer quality remain unverified.

The reference summaries and character list were inspected, but the full story fixtures and their edits were not audited for accuracy.
