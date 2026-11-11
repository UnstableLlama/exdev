# 271c92122efa1097cdf48566961938a5521083ab


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/271c92122efa1097cdf48566961938a5521083ab) · [Evidence ledger](draft.json)

Moves the custom sampler’s override import to the already-declared typing_extensions dependency and removes the unused base-sampler import.

- [Use the existing override backport](#sampling)

## Problem

Both sampler modules imported override from typing, although only CustomSampler.forward used the decorator. [source; call_49b0e3d650fd4bdeaab59c0c1ad2d5e5, call_a0bc9a230adb4e72929d161cd1df748a]

## Reasoning

The patch switches the used decorator to typing_extensions and removes the unused base-class import. Both changes matter because custom.py imports sampler.py before importing its own decorator. [source; call_c6cc234449a54aad9271f793713eb977, call_ae3b8afb7af04330bcc71205d8f640f8, call_a0bc9a230adb4e72929d161cd1df748a]

## Impact

This is an import-compatibility change, not a sampling-algorithm change: the forward implementation and its decorators remain in place. [source; call_c6cc234449a54aad9271f793713eb977, call_ae3b8afb7af04330bcc71205d8f640f8]

## Source Notes

typing_extensions was already declared in requirements.txt and setup.py, and other modules already imported override from it. [source; call_5046616694e1430b8ac5c9e3dff00e69]

The available interpreter was Python 3.14.4, where the isolated typing.override import succeeded; this does not reproduce the reported Python 3.11 issue. [execution; call_a9aa1d10fe1540fc94f1a7872b6491c3]

<a id="sampling"></a>

## Use the existing override backport

Sampler.forward declares the abstract interface without using override. CustomSampler.forward implements that interface and retains @override above @torch.inference_mode. Removing the former import while redirecting the latter preserves the implementation annotation without requiring either module to obtain it from typing. [source; call_49b0e3d650fd4bdeaab59c0c1ad2d5e5, call_a0bc9a230adb4e72929d161cd1df748a, call_c6cc234449a54aad9271f793713eb977, call_ae3b8afb7af04330bcc71205d8f640f8]

## Uncertainty and limits

Python 3.11 compatibility and full sampler imports were not executed; the available interpreter differs from the reported target.

No sampling or GPU behavior was tested.
