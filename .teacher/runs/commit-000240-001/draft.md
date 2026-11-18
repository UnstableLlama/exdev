# 98964cbdae78ddcc85b0eefef2f4b13c6a606fbd


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/98964cbdae78ddcc85b0eefef2f4b13c6a606fbd) · [Evidence ledger](draft.json)

Makes chat mode selection optional for discovery and adds a Phi4/ChatML advisory; a model-directory argument remains required.

- [Discovering chat modes without selecting one](#usage-evaluation)

## Problem

The parser required --mode even when --modes requested only a listing, preventing discovery without supplying a placeholder mode. [source; call_e0658a7797de4952a8d14a971bfacb7c, call_356a09dad5314d58980660ff08757d9d]

## Reasoning

The two control-flow edits work together: defaulting mode to None lets parsing succeed, and treating None as a listing request prevents the subsequent prompt_formats lookup from receiving that sentinel. [source; call_e0658a7797de4952a8d14a971bfacb7c, call_356a09dad5314d58980660ff08757d9d]

## Impact

Listing returns before template construction and model loading. The shared parser still requires -m/--model_dir, although the listing path does not open that directory. [source; call_356a09dad5314d58980660ff08757d9d, call_3fe1c7641a5442cc8d8e1c883256a908, call_e0658a7797de4952a8d14a971bfacb7c]

## Source Notes

The root usage-evaluation entry was read; it establishes the existing manually selected chat templates and their BOS/stop policies, rather than automatic checkpoint-template detection. [ancestor; call_e4ce8a0014f643f2b583215255ec425e]

Issue #12 is titled “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions.” Its initial problem involved using llama3 mode for Qwen; a later comment separately complains that listing requires a mode, and turboderp promises a fix. Its relationship to this change is inferred from that exact CLI complaint, not an explicit commit reference. [inference; call_f4b2a0ac1b6b4b00b501962f449ea278, call_e0658a7797de4952a8d14a971bfacb7c]

Other inspected discussions concern different problems: #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” reports an import/build failure; #39, “Gemma 3 architecture not in list?”, concerns architecture availability and later frontend behavior; #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” concerns invalid conversion states; PR #22, “OpenAI compatible API example,” proposes an API frontend. Their chat.py references do not establish that this CLI change fixes those problems. [inference; call_3a781a7457074101beeefdc87bc0faa5, call_2883923b10f84f04963914265dcbb465, call_e28d84550d634e8a976853f691ec6221, call_a96eb4e082754e1fb0f11965f203570a, call_3d928f30702e43029a61d1c2ce38989d, call_3ff08f12f2ba43ac808c338f313466e3]

<a id="usage-evaluation"></a>

## Discovering chat modes without selecting one

Omitting --mode now lists registered modes and returns, even without --modes. Explicit --modes retains priority over any supplied mode. A supplied mode without --modes still follows the unchanged dictionary lookup; the change does not add mode validation or automatic selection. [source; call_e0658a7797de4952a8d14a971bfacb7c, call_356a09dad5314d58980660ff08757d9d]

A bounded standard-library parser transcription confirmed that providing -m unused with either --modes or no mode changes from parser exit 2 to listing. --modes alone still exits 2 because -m remains required. An arbitrary supplied mode plus --modes already reached listing before this change. [execution; call_8c8e66a3bfdd46978c6f67a2345c108d]

The listing reads class descriptions directly from prompt_formats. Updating the Phi description therefore exposes the warning that some Phi4 models use ChatML without changing either formatter: phi retains its system/user/assistant markers and BOS insertion, while chatml retains im_start/im_end markers and disables added BOS. [source; call_98a87db67e4d418c8cea163d446c6f45, call_0f402c9468a84600aab28567b75c1a16, call_356a09dad5314d58980660ff08757d9d]

## Uncertainty and limits

The execution check transcribed only the relevant argparse declarations and branch predicate; it did not import or execute chat.py, load a model, or test GPU inference.

Listing still follows module-level imports, so this change does not provide dependency-free discovery.

The Phi4 description is advisory; checkpoint-specific template compatibility was not independently verified.
