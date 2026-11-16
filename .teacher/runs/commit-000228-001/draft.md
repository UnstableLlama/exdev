# 4f6929dd0c1d18257ada829ec0373237c81f141b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4f6929dd0c1d18257ada829ec0373237c81f141b) · [Evidence ledger](draft.json)

Updates legacy generator docstring names without changing runtime behavior; AsyncJob's new DynamicJob reference still differs from the actual Job class.

- [Updating generator documentation references](#generation)

## Problem

Generator docstrings still used ExLlamaV2-prefixed names. [source; call_b3c6f3a769a0439bad3d911735ef7234, call_7d6720e20ac442a0819ad7c77b38240c]

## Reasoning

The change updates four documentation references without changing executable statements, signatures or defaults. [source; call_b3c6f3a769a0439bad3d911735ef7234, call_7d6720e20ac442a0819ad7c77b38240c]

## Impact

AsyncGenerator now correctly points readers to Generator. The filter wording remains inside a TODO block; it does not enable filtering. [source; call_b3c6f3a769a0439bad3d911735ef7234, call_e962e131a5794ffbb6c93da3bbaaa67a, call_303d1c67fc714dc59a259635fc0e9ba2]

## Source Notes

The root generation entry was read for provenance. It describes the cooperative async wrapper and records a cancellation wakeup concern. [ancestor; call_96ad895782f54d7db8233c496df2d49a, call_532c3ae5d3724fb9b5c5f34522555bae]

<a id="generation"></a>

## Updating generator documentation references

AsyncGenerator constructs Generator directly; AsyncJob constructs Job and enqueues its wrapper. Thus the first replacement matches the implementation, whereas the new DynamicJob reference still does not name the wrapped class. [source; call_7182cef1ed684a88a37d229a763395fd, call_b3c6f3a769a0439bad3d911735ef7234, call_5b4f0a031a8148b498d0a5db96f54c86]

The embedding description loses its ExLlamaV2 prefix, but MMEmbeddings is plural prose rather than the actual MMEmbedding class name. The signature accepts one list or a batch of lists; generate normalizes the single-prompt case and passes each prompt's embeddings to tokenization and Job. [source; call_7d6720e20ac442a0819ad7c77b38240c, call_e962e131a5794ffbb6c93da3bbaaa67a, call_303d1c67fc714dc59a259635fc0e9ba2, call_b17516b834704c9993adb3f68d39d6dd]

The inherited cancellation wakeup concern is carried over unchanged: cancel sets a flag after removing the job, while the iterator checks that flag only before awaiting queue.get. The comment-only diff supplies no wakeup mechanism. [source; call_7182cef1ed684a88a37d229a763395fd, call_b3c6f3a769a0439bad3d911735ef7234]

## Authoring-time findings — pending review

### async-job-doc-reference (suspected; defect)

The replacement AsyncJob documentation reference still names the wrong class.

Trigger: A reader follows AsyncJob's instruction to consult DynamicJob.

Expected: Point to Job, the class instantiated by AsyncJob.

Actual: The docstring points to DynamicJob; the whole-parent-tree search found only the old docstring occurrence, not a corresponding definition.

Locations: 4f6929dd0c1d18257ada829ec0373237c81f141b:exllamav3/generator/async_generator.py — AsyncJob

Source evidence: call_b3c6f3a769a0439bad3d911735ef7234, call_7182cef1ed684a88a37d229a763395fd, call_5b4f0a031a8148b498d0a5db96f54c86

source_inspection: Compared the new docstring with the constructor and searched the parent tree. The example directly constructs AsyncJob; this mismatch affects documentation, not constructor dispatch. [call_1fbf460f3248488f88b593f6067c09a1, call_5237c6bff3bb4c3d94c18474d2f4e218]. Limits: No runtime failure is implied.

## Uncertainty and limits

No repository execution or generation tests were performed. Numerical computation would not usefully validate these documentation-only replacements.

The explanation checks the edited references and their immediate implementation context, not every pre-existing statement in the generate docstring.
