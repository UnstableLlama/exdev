# Teacher boundary review candidate

The implementation separates trusted preparation from restricted authoring. The curator, packet builder, model adapter, supervisor, Python runtime and operating-system isolation are trusted components. Repository content, external evidence and model tool arguments are untrusted. This is a tested boundary candidate, not an independent security certification.

Review [packet.py](../teacher/packet.py), [worker.py](../teacher/worker.py), [runner.py](../teacher/runner.py), [session.py](../teacher/session.py) and the [schemas](../schema/repo-tools-v1.json) together. Packet ancestry and evidence eligibility are as important as process isolation. In particular, confirm that neither the root review nor administrative reports can enter model context, and that a future provider adapter starts a stateless conversation for every task.

The host-enabled suite passed 78 tests. Sandbox checks cover a host secret canary, credentials/review/report paths, inherited environment, network access, read-only packets, disposable writes, traversal, timeouts, process creation, output bounds and `/proc` root aliases. Actual packets for entries 9 and 10 passed twelve tool calls and nine denial checks each; [results](../reports/teacher-boundary.json) contain result hashes. HF/header success paths currently use synthetic fixtures; real artifacts are not yet recovered for these tasks.

The test results do not establish kernel exploit resistance, support for arbitrary Python dependency environments, or correctness of a live model adapter. The graph bridge is implemented; the live model adapter is absent. Existing drafts and ancestor prose are not supplied by current packets. `entry_analysis` exposes the task diff and is unsuitable for student code-prediction inputs without a separate packet policy.

Next review gates are independent review of the restricted graph bridge, a stateless live model adapter, revised editorial schema and a real trace dry run. No replacement entries should be authored in the administrative conversation that prepared or reviewed this infrastructure.

Graph-specific review should include [export preparation](../teacher/graph_packet.py) and [packet-backed timeline](../teacher/graph_worker.py). Check ancestor-only membership, per-request ancestry for symbol history, checksum verification, and the absence of host timeline/store mounts. The native query backend has a larger bounded runtime profile, still inside fresh networkless namespaces. Successful integration checks are not an independent adversarial audit.
