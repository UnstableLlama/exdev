# 6565dee474d3f9b247673e24dbfe3b9a72ed278c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6565dee474d3f9b247673e24dbfe3b9a72ed278c) · [Evidence ledger](draft.json)

Adds an opt-in cleanup callback helper without wiring it into an entry point. In a standalone CPython check, its bound finalizer retained the instance until interpreter exit, and a callback exception skipped the remaining callbacks on that instance.

- [Add a cleanup callback list backed by weakref.finalize](#cleanup)

## Problem

Turboderp's commit, “Add custom atexit handler,” adds a utility intended to run cleanup callbacks when the main scope ends, before interpreter teardown. The diff adds the utility but does not install it in any entry point. [source; call_a4347946c5db4f979d59f4ad3e78f7a0]

## Reasoning

Each Cleanupper instance owns a list of zero-argument callbacks. Registration appends to the list; unregistration removes the first matching entry if present. The constructor passes its bound _shutdown method to weakref.finalize. When invoked, _shutdown walks the list in registration order and clears it only if the loop finishes. [source; call_a4347946c5db4f979d59f4ad3e78f7a0]

The bound method retains the same object the finalizer watches. A standalone transcription on CPython 3.14.4 showed that a function-local Cleanupper survived return and an explicit garbage collection. Its callbacks ran at interpreter exit, between ordinary atexit handlers registered before and after the Cleanupper was constructed. [execution; call_772c3ea1a1e8411bb4bf3bbb9c6d175e]

## Impact

The existing wildcard import in exllamav3.util exposes Cleanupper through that package, but importing the class does not construct it or register a finalizer. Whole-parent literal searches found no Cleanupper, register_atexit, _shutdown, atexit, or weakref references, and the diff adds no caller outside the class. No existing repository workflow is shown to use the new hook. [source; call_bb3d1649e73c4fb9badd97eaae6107b1, call_60f20b35995d49e6beeba98225cdc13f, call_b012c87ea2014beb9fbf9d0dd65598ab, call_8f29b46ab44c4ce38d139c1c1ed1cde6, call_bd109d062d3d435ab40b3d517a4b63df, call_bdd782f2bba44501ae14ab04ac11a13e, call_a4347946c5db4f979d59f4ad3e78f7a0]

## Source Notes

The initial commit's runtime chapter describes misc.py as a home for shared utilities and notes that util re-exports its helpers. It does not describe a shutdown callback mechanism. [ancestor; call_1719012b8e434d90ac1aa979286dc74a]

The immediate parent added find_free_port, which binds a temporary TCP socket to port zero, reads the assigned port, and closes the socket via contextlib.closing. This task leaves that behavior unchanged; the addition begins after its return statement. [source; call_46fdd5a93588487d892cce0f02a48305, call_a926a7dbebb4464290cf24bd9eb86c37, call_a4347946c5db4f979d59f4ad3e78f7a0]

PR #22, “OpenAI compatible API example,” proposes an endpoint for testing with web UIs. A posted server example catches KeyboardInterrupt and calls server_close() in a finally block. [source; call_cacbb3635b764d03994228c8328d543a, call_1c56df710c924598919f613be3e0f67d]

The concrete overlap with PR #22 is cleanup at a Python entry point. Its posted example uses explicit server cleanup, not Cleanupper, and this diff does not touch the server or chat example. The discussion does not establish the motivation for this commit. [inference; call_1c56df710c924598919f613be3e0f67d, call_a4347946c5db4f979d59f4ad3e78f7a0]

<a id="cleanup"></a>

## Add a cleanup callback list backed by weakref.finalize

The helper groups several callbacks behind a single finalizer. The diff does not attach cleanup to a lexical scope: it adds no context-manager protocol, no explicit close method, and no try/finally at an entry point. [source; call_a4347946c5db4f979d59f4ad3e78f7a0]

If cleanup must happen when a specific operation ends, an explicit try/finally or a context manager would tie it to that boundary rather than to object collection or interpreter exit. A weakref-based design would need a callback and callback state that do not retain the watched instance. [inference; call_a4347946c5db4f979d59f4ad3e78f7a0, call_772c3ea1a1e8411bb4bf3bbb9c6d175e]

## Authoring-time findings — pending review

### bound-finalizer-retains-owner (suspected; defect)

The finalizer holds a bound method that retains the instance it is supposed to watch, preventing cleanup from being triggered by loss of the caller's last reference.

Trigger: Create a Cleanupper in a main function, register a callback, and return without keeping a strong reference in the caller.

Expected: The callbacks run as the main scope ends, as the class docstring describes.

Actual: In the transcription, the instance remained reachable after main returned and gc.collect() ran. The cleanup callbacks ran during weakref's interpreter-exit processing instead.

Locations: 6565dee474d3f9b247673e24dbfe3b9a72ed278c:exllamav3/util/misc.py — Cleanupper.__init__

Source evidence: call_a4347946c5db4f979d59f4ad3e78f7a0, call_60f20b35995d49e6beeba98225cdc13f

scalar_transcription: Transcribed the class and observed the instance through a weak reference after main returned, then observed callback order at normal process exit. [call_772c3ea1a1e8411bb4bf3bbb9c6d175e]. Limits: No in-tree instantiation was found. This exercises the helper in isolation on CPython 3.14.4 and does not establish timing relative to worker teardown.

### callback-error-skips-remaining-cleanup (suspected; defect)

One failing callback skips later callbacks registered on the same instance and bypasses the list reset.

Trigger: Register at least two callbacks on one Cleanupper and let an earlier callback raise during _shutdown.

Expected: Other registered cleanup callbacks still get an attempt when one fails.

Actual: The exception escapes the unguarded loop before it reaches the later callbacks or the reset. In the standalone exit check, weakref reported the exception and continued processing a separate Cleanupper, but the later callback on the failing instance did not run.

Locations: 6565dee474d3f9b247673e24dbfe3b9a72ed278c:exllamav3/util/misc.py — Cleanupper._shutdown

Source evidence: call_a4347946c5db4f979d59f4ad3e78f7a0, call_8f29b46ab44c4ce38d139c1c1ed1cde6, call_b012c87ea2014beb9fbf9d0dd65598ab

scalar_transcription: Registered a raising callback before a marker callback on one transcribed instance and successfully ran the process through normal interpreter exit. The exception appeared, the marker did not, and callbacks on the separate instance ran. [call_772c3ea1a1e8411bb4bf3bbb9c6d175e]. Limits: The direct trigger is the new finalizer's call to _shutdown. No repository application callback or entry point was shown to reach it.

## Uncertainty and limits

The successful check ran a standalone class transcription, not an ExLlamaV3 import or application. The sandbox could not start a test thread, so ordering relative to worker shutdown was not measured. Behavior on other Python versions and implementations is unestablished.

Literal searches do not establish whether external code or dynamic lookup uses the new helper.
