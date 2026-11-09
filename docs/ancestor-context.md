# Approved ancestor context

A fresh teacher receives earlier explanations only after an administrative reviewer approves the exact replacement draft and its recorded evidence. This does not approve the draft for training or promote it into the canonical Encyclopedia.

`teacher.ancestor_context approve` reassembles the draft from its original packet and raw transcript, checks the packet fingerprint and identity, and records hashes of the draft, transcript and provenance. It requires a named reviewer and rationale. It is an administrative CLI, not a teacher tool; neither the provider process nor a tool worker receives its code or review files. This is a trusted review record, not a cryptographic attestation of model execution or a substitute for checking claim quality.

```sh
python3 -m teacher.ancestor_context approve --run RUN_DIRECTORY --packet ORIGINAL_PACKET --reviewer REVIEWER --note 'Review rationale'
python3 -m teacher.ancestor_context attach --packet NEXT_PACKET --run APPROVED_RUN_1 --run APPROVED_RUN_2
```

Attachment requires exactly one approved replacement for every strict Git ancestor. Pending, edited, duplicated, unrelated and future entries are rejected. Entry identity, parents and cutoff must match Git history. Only explanatory content and evidence references are exported as checksum-verified blobs; reviewer names, notes, raw conversations and provider metadata stay outside the packet. A root packet can attach an empty set.

`FreshSession` reads these verified blobs into its initial task context. Each entry has an `ancestor:<sha>` evidence ID. The editorial validator permits those IDs for source-based claims and inferences, but an execution claim still requires a successful `run` in the current session. Ancestor citations are stored as `approved_ancestor_context`, never fabricated tool calls. Actual code access remains limited to the packet's ancestry.

The current implementation supplies full approved prose inline for the first-25 restart, capped at 256 KiB of serialized context. It fails rather than silently dropping entries if that budget is exceeded. Scalable retrieval for later history remains future work; this cap must not be bypassed by mixing unrelated branch summaries into the prompt.

The author CLI and both model-session entry points reject missing ancestor context before inference. Preparation and startup checks can still inspect an incomplete packet. Graphs, source, evidence and prose must all be attached before authoring, because the recorded manifest fingerprint describes that exact input packet. A review binds that fingerprint even if preparation later creates other packets.

The task diff also has a byte-offset index for each file section. This lets `git_show` read a selected part of the explicit task change without scanning binary payloads. It adds no future files or new tools and is particularly useful for the large initial commit.

Existing first-25 drafts have not been approved or imported. Synthetic test fixtures are used only in tests. The independent boundary review remains outstanding; any initial live output is a separate review candidate, not a replacement corpus entry.
