# e53bcef446b14689c58393142278eb36c1951cac


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/e53bcef446b14689c58393142278eb36c1951cac) · [Evidence ledger](draft.json)

Deletes a Blackwell torch.matmul TODO from LinearEXL3.forward without changing executable code.

- [Remove the Blackwell matmul TODO](#quantized-inference)

## Problem

The reconstructed EXL3 forward path contained a TODO to test torch.matmul on Blackwell. [source; call_96cc10635a9a4d46973d6a38370c8cdc]

## Reasoning

The entire change deletes that comment; it neither substitutes torch.matmul nor changes the existing ext.hgemm call. [source; call_96cc10635a9a4d46973d6a38370c8cdc]

## Impact

Executable behavior is unchanged by this diff. Removing the TODO does not establish that the proposed Blackwell experiment occurred. [source; call_96cc10635a9a4d46973d6a38370c8cdc]

## Source Notes

Read the root quantized-inference entry and the later host-work optimization entry. They establish historical context for the direct/reconstructed design and final-shaped output allocation, respectively. [ancestor; call_2b3fc288f31a440a9af54b06e639a565, call_678eb38c63bc4d0c893e54add1a4099c]

Closed issue #11, “AssertionError: bias is wrong datatype,” reports a DeepCoder conversion constructor failure, followed by an author response and reporter confirmation of a fix. Its relationship here is only inferred from the shared exl3.py path: the inspected parent already converts float bias to half, and this task does not edit that code. [inference; call_aa0e00c56fb04ce2b648468d2e8419b2, call_a6bdae1f41264890a1a04f0ec3a1cd99, call_96cc10635a9a4d46973d6a38370c8cdc]

<a id="quantized-inference"></a>

## Remove the Blackwell matmul TODO

LinearEXL3.forward still flattens input rows and selects reconstruction through params.get("reconstruct", x.shape[0] > 32). The constant 32 is the unchanged flattened-row crossover, not a new hardware criterion. [source; call_a6bdae1f41264890a1a04f0ec3a1cd99, call_96cc10635a9a4d46973d6a38370c8cdc]

The reconstructed branch still transforms the input, reconstructs the inner weight matrix, invokes ext.hgemm, and transforms the output. The direct branch still invokes ext.exl3_gemm; both retain optional bias addition. Only the comment immediately before hgemm disappears. [source; call_a6bdae1f41264890a1a04f0ec3a1cd99, call_96cc10635a9a4d46973d6a38370c8cdc]

The root entry's packed-input-sign concern does not describe the inspected parent constructor: it unpacks supplied su/sv into suh/svh before forward uses them. That earlier change is retained, not introduced by this cleanup. [source; call_a6bdae1f41264890a1a04f0ec3a1cd99, call_96cc10635a9a4d46973d6a38370c8cdc]

## Uncertainty and limits

No repository execution, CUDA test or Blackwell benchmark was performed. A scalar computation would not meaningfully validate this comment-only deletion.

Unchanged execution paths retain their existing preconditions; this annotation does not establish their general numerical correctness or successful execution.
