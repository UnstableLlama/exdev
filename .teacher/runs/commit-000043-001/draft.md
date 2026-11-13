# df30645b725b113599d60496a8f94d6f649119ea


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/df30645b725b113599d60496a8f94d6f649119ea) · [Evidence ledger](draft.json)

Merge PR #13's BOS/EOS None guards, preventing absent control-token IDs from reaching backend string lookup.

- [Merge absence-safe control-token lookup](#loading-tokenization)

## Problem

PR #13 reports conversion of arcee-ai/Virtuoso-Small failing when tokenizer_config.json contains "bos_token": null: Tokenizer.__init__ passes None to id_to_token, producing a TypeError. [source; call_722682e9709f45e99ab0cca44d00ecc0]

## Reasoning

An unspecified model BOS ID alone does not guarantee failure. Resolution first consults tokenizer configuration and otherwise defaults to ID 1; EOS similarly defaults to ID 2. Explicit null or an unresolved token can leave the resolved ID None. [source; call_1bba5338791246268a4954412c565e0b]

## Impact

The merge's first-parent diff incorporates the same two lookup guards as the PR branch commit, covering both BOS and EOS rather than only the reported BOS case. [source; call_173cd4f60b534f19a5e852807ee15434, call_51f29eefbbd74782ac2d3728b1fab308]

async0x42 separately reports that the change fixed the same error while converting ArliAI/QwQ-32B-ArliAI-RpR-v1; this is contributor-reported success, not a locally reproduced conversion. [source; call_aa0115e16a35417f96421c9029fe2eca]

## Source Notes

PR author oobabooga reports the original failure and presents the change; turboderp's discussion response is an acknowledgment, not a test report. [source; call_722682e9709f45e99ab0cca44d00ecc0, call_246b27e031574b809a294d28b52d00ab]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and an environment workaround. Its traceback does not describe the tokenizer None-ID lookup addressed here. [source; call_3e09f84dd066472399b564776bd1ccca, call_173cd4f60b534f19a5e852807ee15434]

The earlier PR-branch annotation describes the same absence-preserving lookup change and notes that tokenizer construction is shared beyond conversion. [ancestor; call_d9df318837d84a27bd431fbb12f84983]

<a id="loading-tokenization"></a>

## Merge absence-safe control-token lookup

Tokenizer.__init__ now assigns None directly to bos_token or eos_token when its resolved ID is None. Defined IDs retain the existing extended-vocabulary lookup followed by backend fallback for a missing or falsey mapping. The identity check preserves valid ID zero. [source; call_173cd4f60b534f19a5e852807ee15434]

The change preserves absence rather than substituting an arbitrary token. Existing truthiness guards omit absent control-token strings from the extended vocabulary, and encode already checks that BOS/EOS IDs are not None before inserting them. ID resolution and padding fallback remain unchanged. [source; call_1bba5338791246268a4954412c565e0b, call_ed5f40acfbd14c87b35ae627eb76ef18, call_339a75fc74db448882b53b8524ac4c3c, call_173cd4f60b534f19a5e852807ee15434]

A standard-library transcription checked 12 combinations of resolved IDs and extended mappings: three None-ID cases avoided lookup, while nine defined-ID cases preserved results and backend-call selection. The backend was a recording stub, not the tokenizers library. [execution; call_868196921e194bd1b117954ddd5a2b06, call_173cd4f60b534f19a5e852807ee15434]

## Uncertainty and limits

No real tokenizers backend, complete tokenizer initialization, model conversion or GPU workload was executed.

The scalar check covers only lookup selection; it does not establish downstream padding or generation behavior when control-token IDs are absent.
