# 6c15b8c40f0d28807006ad65d2c9e31382a352b4


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6c15b8c40f0d28807006ad65d2c9e31382a352b4) · [Evidence ledger](draft.json)

Moves final memory cleanup after shared loader closure and makes dictionary scanning in the tensor diagnostic tolerate exceptions.

- [Loading cleanup and best-effort tensor inspection](#runtime)

## Problem

Successful autosplit loading cleaned up memory before returning to load_gen and closing the safetensors collection; explicit-device loading lacked that final cleanup call. [source; call_69efe3c062e64b0a8ecbb710d2a99ead, call_6a7cbc55450c417b8a916d70448f83f5]

## Reasoning

Moving free_mem to the shared successful completion path places garbage collection and CUDA cache emptying after loader closure and after the autosplit generator has finished. This plausibly makes more temporary allocations eligible for reclamation, without changing placement or OOM retry policy. [inference; call_6a7cbc55450c417b8a916d70448f83f5, call_69efe3c062e64b0a8ecbb710d2a99ead, call_c2d17ac3a7364299988f3fb518803d31]

## Impact

Both successful single-device and autosplit loads now invoke final cleanup. Dictionary traversal in the tensor diagnostic becomes best-effort, suppressing exceptions within that traversal block. [source; call_6a7cbc55450c417b8a916d70448f83f5, call_86ccd02572e84c4eb078ee7a8f8711d8]

## Source Notes

The earlier loader entry identifies iterator exhaustion as necessary for cleanup and records missing explicit-device progress notifications. [ancestor; call_ecc9c89d10214c908a919dab84f3baa5]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension import failure; its inferred connection is only a traceback through model.py. Issue #15 reports incoherent low-bpw cogito output, and #21 reports Windows build failure. None establishes motivation for this memory-management change. [inference; call_eb9e55bfbf81426ba2747b35271bf569, call_597c7fd41c144cc8a0253eb9714633a8, call_f8e9cc885d464a539a3e812a80e00cb6, call_6a7cbc55450c417b8a916d70448f83f5]

<a id="runtime"></a>

## Loading cleanup and best-effort tensor inspection

free_mem calls gc.collect followed by torch.cuda.empty_cache. The patch removes its successful-completion call from _load_autosplit and adds it immediately after self.config.stc.close in load_gen. Initial cleanup and cleanup during OOM retry remain unchanged. [source; call_c2d17ac3a7364299988f3fb518803d31, call_69efe3c062e64b0a8ecbb710d2a99ead, call_6a7cbc55450c417b8a916d70448f83f5]

Autosplit creates extra_dummy_states for output-memory estimation when max_output_factor exceeds one. Moving cleanup outside the exhausted helper places it after the helper's local lifetime rather than while those locals remain in its active frame. SafetensorsCollection.close closes native file handles and clears their entries; variant collections delegate closure to their constituent collections. [source; call_69efe3c062e64b0a8ecbb710d2a99ead, call_6a7cbc55450c417b8a916d70448f83f5, call_2263833604894e5891de9ea81d5d3a0a, call_65e619079b6a4e668d4939e703eb1aee]

Cleanup still requires successful completion: it is not protected by finally. The terminal autosplit progress tuple precedes dummy-state release and memory-limit reset; callers must resume to exhaustion to reach collection closure and the relocated free_mem. Model.load and the inspected loading examples exhaust the iterator. [source; call_69efe3c062e64b0a8ecbb710d2a99ead, call_6a7cbc55450c417b8a916d70448f83f5, call_c949deb9b1bd46aba64f47bdd8690788]

list_gpu_tensors walks reachable objects, recording tensor paths and queueing unvisited values. Only its dictionary-items block gains a bare except/pass. If iteration, path formatting, collection, or queue maintenance raises, traversal abandons the remainder of that dictionary without reporting the error; already collected results remain. Attribute and sequence traversal are not covered by this guard. [source; call_c2d17ac3a7364299988f3fb518803d31, call_86ccd02572e84c4eb078ee7a8f8711d8]

The diagnostic trades completeness and visibility of failures for continued scanning. It does not itself free tensors or participate in the inspected model-loading path. [inference; call_c2d17ac3a7364299988f3fb518803d31, call_86ccd02572e84c4eb078ee7a8f8711d8, call_69efe3c062e64b0a8ecbb710d2a99ead]

## Authoring-time findings — pending review

### inherited-single-device-progress (suspected; behavior_change)

The previously recorded explicit-device progress omission is carried over unchanged.

Trigger: Use load_gen(device=...) expecting yielded progress, or load(device=..., callback=...) expecting callback notifications.

Expected: Receive loading progress through the requested interface.

Actual: The explicit-device branch calls _load_single, which only updates its progress bar. Loading can finish and reach the new cleanup without yielding progress or calling the callback.

Locations: 6c15b8c40f0d28807006ad65d2c9e31382a352b4:exllamav3/models/model.py — Model.load_gen

Source evidence: call_69efe3c062e64b0a8ecbb710d2a99ead, call_6a7cbc55450c417b8a916d70448f83f5

source_inspection: Compared the parent explicit-device branch and _load_single with the task diff. Whole-tree load_gen search found Model.load and two loading-example callers; the examples use autosplit and exhaust their iterators. The omission reaches direct explicit-device iterator consumers and explicit-device callback users through Model.load, not the inspected example calls. [call_02a57f63db2446d8ab9d122022aa6f1d, call_c949deb9b1bd46aba64f47bdd8690788, call_69efe3c062e64b0a8ecbb710d2a99ead, call_6a7cbc55450c417b8a916d70448f83f5]. Limits: No runtime reproduction; literal caller searches do not establish external or dynamically dispatched usage.

## Uncertainty and limits

No model loading, CUDA allocation, reclamation timing, or performance measurement was executed. Source ordering does not establish a reduction in peak or retained VRAM.

A scalar arithmetic check would not validate these lifecycle changes; meaningful validation requires generator lifecycle and allocator behavior with real model loads.

The exception motivating the diagnostic guard is not established by the supplied evidence.
