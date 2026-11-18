# 784107df084163af6a13310c4cb07cf7709439ec


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/784107df084163af6a13310c4cb07cf7709439ec) · [Evidence ledger](draft.json)

Adds a utility that asks the OS for an available IPv4 TCP port and returns its number. The socket closes before the caller receives the result, so the helper does not reserve the port.

- [Let the OS choose an IPv4 TCP port](#port-allocation)

## Problem

The parent utility module has no helper for asking the OS to choose an available port. Turboderp’s commit adds `find_free_port()` without wiring it into any workflow. [source; call_2ad720cb68af4c6fa3523b2cd72b913f, call_95bba2e008e94b45b5e9abbcc35df163, call_e1532e3339bb4dd095dd1fbb52aedefc]

## Reasoning

Binding to port `0` delegates port selection to the OS instead of guessing a number or scanning a range. Returning only the number keeps the interface simple, but a caller that needs to keep the port reserved should retain and use the bound socket rather than close it and bind again later. [inference; call_e1532e3339bb4dd095dd1fbb52aedefc]

## Impact

The existing wildcard re-export makes the helper available as `exllamav3.util.find_free_port` as well as in `exllamav3.util.misc`. It also exposes the newly imported `socket` and `contextlib` names through `exllamav3.util`. A whole-parent literal search found no `find_free_port` references, and the complete diff adds no call site. [source; call_9bac1fd727a64cc9a73a458a78931716, call_a8b1fc72ab3045f0a2e0b0711a8b5368, call_e1532e3339bb4dd095dd1fbb52aedefc]

## Source Notes

The initial commit’s runtime chapter describes `util` as a re-export of miscellaneous helpers and documents the original module’s synchronization and timing utilities. The port helper is a sibling utility; it does not depend on the shared lock or the CUDA helpers. [ancestor; call_4e2fbbdbb08343e0b4ebc0c907eca7e2, call_1e28ed4b67cb4a199a3ddf3dd5d17910, call_e1532e3339bb4dd095dd1fbb52aedefc]

<a id="port-allocation"></a>

## Let the OS choose an IPv4 TCP port

`find_free_port()` creates an IPv4 TCP socket and binds it to `("", 0)`: the empty host selects the IPv4 wildcard, and zero requests an OS-assigned port. It reads the port field from `getsockname()` and exits `contextlib.closing` before the caller receives the integer. It never listens, and it does not catch socket or bind errors. [source; call_e1532e3339bb4dd095dd1fbb52aedefc]

The result is a candidate for a later bind, not a reservation. Another socket can take the port between the helper closing its socket and the caller binding its own. The probe is for IPv4 TCP, not IPv6 or UDP. [inference; call_e1532e3339bb4dd095dd1fbb52aedefc]

A standalone standard-library run of the socket sequence observed `0.0.0.0`, an integer port in the range 1–65535, and an open descriptor inside the context that was closed on exit. [execution; call_7a7bf9a221ed41feb39f302f6a336db8]

## Uncertainty and limits

The socket sequence ran in isolation, not through a package import or an application caller. The check did not test concurrent allocation or whether a later bind succeeds.

The literal search cannot rule out dynamic or external consumers. The commit does not identify an intended consumer.
