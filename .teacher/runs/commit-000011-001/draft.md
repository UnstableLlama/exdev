# 2f12246ec32a231a5f9bde18db1a69ed6e40c29e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2f12246ec32a231a5f9bde18db1a69ed6e40c29e) · [Evidence ledger](draft.json)

Aligns setup.py and requirements.txt on eight dependencies, updates minimum versions, and removes divergent declarations.

- [Consistent installation dependencies](#packaging)

## Problem

The two dependency declarations disagreed: setup.py specified older Torch and unbounded NumPy, omitted several requirements.txt dependencies, and retained a different package set. [source; call_a0d4c0e650284540b4c187816b1ec69c, call_98a23a98d37c4ae8af69c8675f0350da]

## Reasoning

The change aligns package metadata with requirements.txt while adding safetensors and ninja to the latter and removing tabulate. [source; call_1f7933083ef047a9aec5d43a9c204d96, call_bd2830ecdd734e55bb07925f194434ee]

## Impact

A standard-library check applying the inspected dependency edits found identical sets of eight declarations in the two installation interfaces. [execution; call_44ad4f762ba041478fa2335520414d67]

## Source Notes

The parent entry describes a separate fix to native source-path representation; this change instead updates dependency declarations. [ancestor; call_20d09af0d4fb4dcaabf3ac0e19dfea91]

<a id="packaging"></a>

## Consistent installation dependencies

setup.py passes install_requires directly to setuptools.setup. Its replacement list requires torch>=2.6.0, flash_attn>=2.7.4.post1, tokenizers>=0.21.1, numpy>=2.1.0, rich, typing_extensions, ninja and safetensors>=0.3.2. The version numbers are lower bounds rather than exact pins. [source; call_98a23a98d37c4ae8af69c8675f0350da, call_bd2830ecdd734e55bb07925f194434ee]

Package metadata drops pandas, fastparquet, sentencepiece, pygments, websockets, regex and pillow. Ninja, safetensors and rich remain; Torch's lower bound rises from 2.2.0 to 2.6.0 and NumPy gains the 2.1.0 bound already present in requirements.txt. [source; call_bd2830ecdd734e55bb07925f194434ee, call_a0d4c0e650284540b4c187816b1ec69c]

Alignment removes a dependency-set difference between the two installation routes, but the lists remain independently maintained, so future edits can diverge again. [inference; call_1f7933083ef047a9aec5d43a9c204d96, call_bd2830ecdd734e55bb07925f194434ee]

This is not a build-bootstrap redesign: setup.py still checks whether Torch is already available before configuring CUDAExtension and BuildExtension, and EXLLAMA_NOCOMPILE still disables precompilation. [source; call_98a23a98d37c4ae8af69c8675f0350da, call_bd2830ecdd734e55bb07925f194434ee]

## Uncertainty and limits

The check models the dependency edits; it does not run setuptools, pip resolution, native compilation, or application tests.

The inspected evidence does not establish why each minimum version is necessary or whether the resulting dependencies suffice for every optional workflow.
