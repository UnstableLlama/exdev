# d90e706a406d15b57a72fca39ea908d6ea12e541


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d90e706a406d15b57a72fca39ea908d6ea12e541) · [Evidence ledger](draft.json)

Switches MiMo, Mistral and Qwen2 override imports to the already declared typing_extensions dependency, repairing a shared architecture-registry import boundary without changing model logic.

- [Use the existing override backport consistently](#imports)

## Problem

MiMo, Mistral and Qwen2 imported override from typing, unlike the existing typing_extensions convention elsewhere in the package. [source; call_997071d2985a45e2b7185fc76f835414]

## Reasoning

The three replacements align these modules with an already declared dependency rather than adding a dependency or changing model behavior. [source; call_933a0b0e27934d308410e89df78040c8, call_24439aea84224d2f97c8c82e9796ecca, call_3e652c8cda82403d9882b0136fb6c294, call_997071d2985a45e2b7185fc76f835414]

## Impact

The repair matters beyond selecting these three architectures: the architecture registry eagerly imports all three before Config.from_directory reads and dispatches the requested architecture. [source; call_4018ddc49fcf4eb8bd7e0d532e43f370, call_5c6051b5884148f2917bc0b10e7c374d]

## Source Notes

The earlier chat-formatting entry establishes the introduction of these default_chat_prompt overrides; the MiMo entry establishes its thin Llama-derived adapter and deliberate omission of MTP support. Neither supplies fresh runtime validation of this import repair. [ancestor; call_7314afaa3af94f168f5b02234ee8bcfc, call_e9a357b4443a40ff9f90a5fa24f86cc5]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns native-extension loading; issue #17, “ModuleNotFoundError: No module named 'torch' when installing requirements.txt,” concerns installation; PR #4, “chore: update config.py,” proposes a spelling correction. Their relevance is inferred only from overlapping inspected paths or dependency terms, not an upstream association with this fix. [inference; call_c2476348b11645b1bc91f554206b43df, call_4a3ca5ba70174e8b8c0c1ec9da4d9034, call_3881f710e71440febb6c1f7c0e8b4b90]

<a id="imports"></a>

## Use the existing override backport consistently

Each changed file replaces only its first-line import with from typing_extensions import override. The decorator remains on default_chat_prompt; constructors, Llama inheritance, architecture identifiers and prompt strings are unchanged. [source; call_933a0b0e27934d308410e89df78040c8, call_24439aea84224d2f97c8c82e9796ecca, call_3e652c8cda82403d9882b0136fb6c294, call_54fb326afb014510bc5fed4b275f3182, call_5e0e886616e04a12b31c2f33a527276b, call_781f612ed1ab487982af0cef96a0cb6b]

Whole-parent searches locate the affected modules' direct imports in architectures.py. Its imports are unconditional, whereas the inspected package initializers export Config and Model without directly importing that registry. Thus the demonstrated shared failure boundary is registry loading, including Config.from_directory, rather than necessarily the initial root-package import. [source; call_a8902d06a32c4af7a811bc2be672e220, call_51b1436909bd42daa712ba15eb09d09d, call_fa850b3d1f5a4848bd861aa951167abc, call_4018ddc49fcf4eb8bd7e0d532e43f370, call_5c6051b5884148f2917bc0b10e7c374d, call_c1b82199e6134116ae5cab56f517c6ec, call_6ff0a96b805c43358d353f5487a5b706]

Using the backport unconditionally avoids a version-dependent import branch and follows the surrounding models' convention. This is a compatibility interpretation of the narrow diff, not measured proof that every supported interpreter can load the package. [inference; call_997071d2985a45e2b7185fc76f835414, call_933a0b0e27934d308410e89df78040c8, call_24439aea84224d2f97c8c82e9796ecca, call_3e652c8cda82403d9882b0136fb6c294]

## Uncertainty and limits

The author's stated Python <3.13 boundary is not established by eligible language-version documentation or interpreter testing here.

No package import or model execution was performed. This import-only change offers no useful numerical identity for a scalar computation.

Successful imports still require an installed typing_extensions version providing override; the inspected dependency declarations do not specify a minimum version.
