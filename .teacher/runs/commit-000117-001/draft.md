# 04dc55717c499539504b9a3d8454d631de84f7c2


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/04dc55717c499539504b9a3d8454d631de84f7c2) · [Evidence ledger](draft.json)

Fixes architecture-mismatch assertion formatting by replacing undefined expect_arch with self.arch_string.

- [Preserving the architecture-mismatch diagnostic](#config)

## Problem

Config.__init__ references undefined expect_arch when formatting an architecture-mismatch assertion, masking the intended diagnostic with NameError. [source; call_753a771dd3cb41ebb2440bca6fa0d1ff, call_cf22f1a3251542f3a5028783af0d1547]

## Reasoning

The replacement uses self.arch_string, the same expected architecture already used by the assertion predicate. Only the failure message changes. [source; call_759115a478584bddbe7e1adab935bfdc]

## Impact

An isolated check of the extracted assertion produced NameError before the patch and AssertionError with the actual architecture, config filename and expected architecture afterward. Matching architectures passed both versions. [execution; call_668ac9e2887b4c44b7e737e99f0df113]

## Source Notes

PR #4, “chore: update config.py,” proposes a spelling correction. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure. Their inferred connection here is only the shared config.py filename; neither discussion establishes motivation for this assertion fix. [inference; call_3423991c9dad473581b0481c9e79f8d2, call_043abbabb3a948498bc3888c06522e76, call_759115a478584bddbe7e1adab935bfdc]

<a id="config"></a>

## Preserving the architecture-mismatch diagnostic

The constructor reads config.json, requires exactly one architecture, and compares it with self.arch_string before collecting weight files. The patch restores the diagnostic at this early validation boundary without changing accepted architectures. [source; call_753a771dd3cb41ebb2440bca6fa0d1ff, call_759115a478584bddbe7e1adab935bfdc]

Config.from_directory independently validates the architecture and selects its registered configuration class before construction. This change therefore repairs the constructor's mismatch path, rather than adding support for unknown architectures. [source; call_753a771dd3cb41ebb2440bca6fa0d1ff]

## Uncertainty and limits

The check executed an extracted assertion and its patched equivalent, not full configuration loading or model initialization.
