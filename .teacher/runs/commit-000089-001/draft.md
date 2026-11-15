# b124ceb2d598902e5a084fc06c1b378be1dfb6a3


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b124ceb2d598902e5a084fc06c1b378be1dfb6a3) · [Evidence ledger](draft.json)

Adds an opt-in Tk cache map showing active sequence chains, shared pages and KV occupancy, with synchronous rendering and an unconditional tkinter import requirement.

- [Optional live cache-map visualization](#generation)

## Problem

The change adds a graphical debugging view of paged-cache allocation, sequence chains and valid KV occupancy. [source; call_a813ca57b0b24810bc753066b51d146d, call_6ec92c0c7a8744219e525e9c0364354d]

## Reasoning

The visualizer consumes page-table metadata rather than copying KV tensors: active sequences supply ordered physical page indices, job serial numbers supply colors, and kv_position / PAGE_SIZE supplies occupancy. [source; call_a813ca57b0b24810bc753066b51d146d, call_e593b9da476549ada4bc14f3a5a162ec]

## Impact

Window creation is opt-in through show_visualizer=False, but importing tkinter is unconditional. Enabled rendering runs synchronously before iterate returns, after either regular or speculative generation. [source; call_a813ca57b0b24810bc753066b51d146d, call_6ec92c0c7a8744219e525e9c0364354d, call_117d42054c024c5ba755dd230d214453]

## Source Notes

The inspected discussions concern distinct problems: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure; #15 reports incoherent cogito output at bpw <= 2.5; #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns conversion and tokenizer truncation. None explicitly connects its problem to cache visualization. [source; call_94a125b656c9446fb3443a66b77cccdd, call_713b05ff2cb84a9a9b90b10d1449e17e, call_594df7cbdaec4cb3858bb2b9eae29997]

<a id="generation"></a>

## Optional live cache-map visualization

Generator constructs CacheVisualizer with pagetable.max_pages only when enabled. Each iteration snapshots every active sequence’s allocated_pages and every physical page’s KV occupancy, then calls update. Pending jobs are not drawn. [source; call_a813ca57b0b24810bc753066b51d146d]

Page-table allocation can share matching hashed pages across sequences and reserves unique pages for future tokens. The visualization represents these distinctions with multiple horizontal color bands per shared page and darker unused portions. Gray pages mean no active chain references them, not necessarily erased KV data: releasing a page can retain its cached contents. [source; call_e593b9da476549ada4bc14f3a5a162ec, call_6ec92c0c7a8744219e525e9c0364354d]

The renderer cycles through 14 colors by job serial number, connects adjacent entries in each sequence’s page list with routed arrows, and darkens arrows whose destination has zero occupancy. Colors therefore identify jobs only modulo 14, rather than uniquely identifying every job or sequence. [source; call_6ec92c0c7a8744219e525e9c0364354d]

The default 800×600 canvas uses 25-pixel margins and a gap equal to 0.75 times the square cell width. Grid width follows the square root of page count times usable aspect ratio; height rounds up to fit all pages. Resize events recompute this geometry. Each update deletes and rebuilds overlays and pumps Tk events with root.update. [source; call_6ec92c0c7a8744219e525e9c0364354d]

Rebuilding canvas objects favors a straightforward debug implementation over rendering efficiency. The source itself calls the implementation slow and suggests drawing onto a bitmap instead; no benchmark establishes the overhead. [source; call_6ec92c0c7a8744219e525e9c0364354d]

The demo leaves visualization disabled, forwards its toggle to Generator, halves total_context from 32768 to 16384, changes the hard-coded configuration directory, and revises prompts to include repeated long sequences. [source; call_1002897ae66042e8977e5ebdc1f2ca43]

A scalar calculation using PAGE_SIZE=256 gives 128 pages before the demo change and 64 afterward. For 64 pages, default layout produces 10 columns, 7 rows and approximately 44.776-pixel cells; 128 valid tokens fill half a page. [execution; call_a5b9272c37224eafbb9816064c9fc244, call_9f4daac40feb4997aca312c43ee5e440, call_6ec92c0c7a8744219e525e9c0364354d]

## Authoring-time findings — pending review

### unconditional-tk-import (suspected; new_requirement)

The optional visualization introduces an unconditional tkinter import along the public package import path.

Trigger: Import exllamav3 in an environment where tkinter cannot be imported, even without enabling visualization.

Expected: Disabling the optional debug window would permit nonvisual use without its GUI module.

Actual: generator.py imports visualizer.py at module scope, which imports tkinter before show_visualizer is checked. The package initializers eagerly import Generator, so the failure can reach ordinary exllamav3 imports, assuming earlier imports succeed.

Locations: b124ceb2d598902e5a084fc06c1b378be1dfb6a3:exllamav3/generator/visualizer.py — module import tkinter

Source evidence: call_a813ca57b0b24810bc753066b51d146d, call_6ec92c0c7a8744219e525e9c0364354d, call_cc72d15f360c486f8b5bbe2e84e749a4, call_1b36b890610b4fa3bdde9887ceb9177d, call_fd6f74bdb0e344a299a1b7eeef91d5d4

source_inspection: Searched parent import sites and inspected both public package initializers against the new unconditional import chain. [call_cc72d15f360c486f8b5bbe2e84e749a4, call_1b36b890610b4fa3bdde9887ceb9177d, call_fd6f74bdb0e344a299a1b7eeef91d5d4, call_6ec92c0c7a8744219e525e9c0364354d]. Limits: Conditional source conclusion only; no tkinter-missing environment was executed.

## Uncertainty and limits

No GUI, model generation or GPU execution was performed. Rendering cost, display availability and Tk lifecycle behavior remain unmeasured.

The arithmetic check transcribes layout and occupancy formulas in standard-library Python; it does not execute CacheVisualizer.
