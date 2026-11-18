# afa7f1e5d04950143681f32f76cfdae06d727493


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/afa7f1e5d04950143681f32f76cfdae06d727493) · [Evidence ledger](draft.json)

Removes eager HF integration imports from both initializers, isolating the adapter but leaving its example on the deleted convenience export.

- [Make HF adapter imports explicit](#transformers-integration)

## Problem

The parent root initializer eagerly imports the HF adapter, whose module-level imports require Transformers even when no integration is requested. Transformers is absent from setup.py's runtime requirements. [source; call_0c390eaf8f6a48beb0fed5a8211f1e2d, call_e4cd33829aa94baba6b196623601f1b0, call_1ef5990835a64ed28806477ddb248c31, call_9f3ea0d9f41744499049e88a5d56e820]

## Reasoning

Removing both initializer imports separates ordinary package loading from adapter loading. This is explicit opt-in isolation, not lazy registration or an exception-handling fallback. [source; call_0c390eaf8f6a48beb0fed5a8211f1e2d, call_e4cd33829aa94baba6b196623601f1b0]

## Impact

The eager integration import path is removed, but the existing integration example still requests the deleted package-level export and therefore needs its import updated. [source; call_e4cd33829aa94baba6b196623601f1b0, call_3dc3d701ac1c4f3d9e6afc37d62e5f09]

## Source Notes

Read the integration-introduction entry bcaa636f66973eac4ac071ad25ef31e8586a02dc. It records the eager undeclared dependency, omitted integration package in setup.py, and missing decoder-multiplier forwarding. [ancestor; call_cb51d1cf44b14d478f579de75631ed1c, call_0e7f691843e3437087ea5ed5e80f5905]

The task removes the recorded eager initializer dependency. The packaging omission remains in setup.py, although ordinary root initialization no longer requests that omitted package. The unchanged adapter still creates no mcg/mul1 buffers and forwards neither argument in finalize; this task does not repair that previously recorded limitation. [source; call_0c390eaf8f6a48beb0fed5a8211f1e2d, call_e4cd33829aa94baba6b196623601f1b0, call_9f3ea0d9f41744499049e88a5d56e820, call_1ef5990835a64ed28806477ddb248c31]

Issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” and #7, “quantizing model: undefined symbol: __cxa_call_terminate,” report native-extension import failures. Their inferred overlap with this task is the traceback through exllamav3/__init__.py, not evidence that removing HF imports fixes either failure. Issue #49, “running the QTIP inference code,” concerns QTIP installation and comparisons; its inferred overlap is only setup.py/requirements terminology. [inference; call_7b049ae0652e4262a56929fc11e64447, call_d89d558bcf3747318d49a0f8d5e4b09f, call_f822cac678564653a1b141035c2cb4ac, call_0c390eaf8f6a48beb0fed5a8211f1e2d]

<a id="transformers-integration"></a>

## Make HF adapter imports explicit

The root initializer loses only `from . import integration`; its model, tokenizer, cache, generator and sampler exports remain. The integration initializer becomes empty by losing its patch_transformers re-export. Together these edits stop both ordinary root import and explicit integration-package import from automatically loading integration.transformers. [source; call_0c390eaf8f6a48beb0fed5a8211f1e2d, call_e4cd33829aa94baba6b196623601f1b0]

The adapter implementation remains available in integration/transformers.py in the source tree. Its module imports Transformers eagerly, while patch_transformers itself performs the registry mutations: it installs the exl3 quantizer/config mappings and assigns QuantizationMethod.EXL3. Importing the module and calling registration are distinct operations; neither initializer previously called registration. [source; call_1ef5990835a64ed28806477ddb248c31, call_e4cd33829aa94baba6b196623601f1b0]

Whole-parent searches found the integration initializer and examples/transformers_integration.py as importers of patch_transformers, with the example its only discovered direct caller. The example imports from the now-empty package before calling registration and loading an AutoModel. An explicit import from exllamav3.integration.transformers would preserve that opt-in sequence, provided the adapter is present and its dependencies import successfully. [source; call_3367a490e81b4069871efa65fe1d464a, call_4621329e93e343ad8c041218b00978a3, call_3dc3d701ac1c4f3d9e6afc37d62e5f09, call_e4cd33829aa94baba6b196623601f1b0]

The tradeoff is a narrower default dependency boundary at the expense of the former convenience export. Retaining the package-level re-export would preserve the example while avoiding ordinary root eager loading, but would still make explicit import of the integration package load Transformers. The task instead removes both conveniences. [inference; call_0c390eaf8f6a48beb0fed5a8211f1e2d, call_e4cd33829aa94baba6b196623601f1b0, call_1ef5990835a64ed28806477ddb248c31]

## Authoring-time findings — pending review

### integration-example-stale-import (suspected; defect)

The unchanged HF integration example imports an export removed by this commit.

Trigger: Run examples/transformers_integration.py in an environment where its preceding imports succeed.

Expected: The example obtains patch_transformers and registers EXL3 before loading the model.

Actual: Its `from exllamav3.integration import patch_transformers` requests a name no longer defined by the empty initializer, preventing the subsequent registration call and main execution.

Locations: afa7f1e5d04950143681f32f76cfdae06d727493:exllamav3/integration/__init__.py — module initialization, afa7f1e5d04950143681f32f76cfdae06d727493:examples/transformers_integration.py — module-level import

Source evidence: call_e4cd33829aa94baba6b196623601f1b0, call_3dc3d701ac1c4f3d9e6afc37d62e5f09, call_4621329e93e343ad8c041218b00978a3

source_inspection: Compared the removed re-export with the example and whole-parent patch_transformers/import searches. The example is the sole discovered direct registration caller. [call_e4cd33829aa94baba6b196623601f1b0, call_3dc3d701ac1c4f3d9e6afc37d62e5f09, call_4621329e93e343ad8c041218b00978a3]. Limits: Not executed. Earlier dependency failures can mask this failure; external callers and dynamic references were not enumerated.

## Uncertainty and limits

No repository import, installed distribution, Transformers registration or generation was executed; other package dependencies and native-extension failures remain possible.

Searches establish literal in-tree references, not dynamic imports or external consumers.

This import-boundary change has no numerical mechanism requiring a useful scalar computation. Third-party Transformers-version compatibility remains unestablished.
