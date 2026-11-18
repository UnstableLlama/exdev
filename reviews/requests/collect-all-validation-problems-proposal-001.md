# Proposal: collect all validation problems for the single repair turn

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

The validator currently returns the first problem it encounters. In 345/001 one absent call ID appeared in two evidence lists. The repair fixed the cited occurrence and validation rejected the other. In 346/001 the repair removed a mistyped citation at `source_notes[2].evidence[2]`, then validation rejected an independent problem already present in the first final. The `source_inspection` check at `findings[6].verification[0]` cited only `run` results.

Collect every independently checkable annotation problem in a final and return them together in the existing single repair message. Report every occurrence of an invalid reference with its field path and report other independent refusals with their own paths and reasons. Skip checks whose prerequisites failed to avoid misleading follow-on diagnostics. Preserve the existing stop behavior for parse, protocol, transcript integrity and runtime failures. Keep validation strict and revalidate the complete repaired annotation before publication.

Use stable ordering, bounded diagnostic fields and an explicit total and omitted count if the message budget is reached. Feedback comes from the candidate, its transcript and validator rules. It supplies no replacement citations, expected answers or reviewer material. Ask the teacher to fix the listed problems and preserve the rest of its annotation.

Use a versioned repair policy. Preserve replay of existing policies and bind the complete new feedback to the refused final. The implementation submission should include tests for duplicate invalid references, mixed citation and method failures, dependent checks, bounded feedback, successful and failed single repairs, and historical replay. It should bind the patch and the host-enabled suite results.

This is a proposal for Fable's review and the user's decision. Production code is unchanged. The proposal does not gate 346/002.

## SHA256

- reviews/verdicts/commit-000345-recovery-001.md: `df252e78ed4c961a57497058d958303ccaf4a7f61a01fb435244edd28c3acd1f`
- reviews/verdicts/commit-000346-recovery-001.md: `de39257721aae29fb6417dab3f0cb2df6de68c34b4e91299ac5a2cf9a00b47d8`
- .teacher/runs/commit-000345-001/raw-transcript.json: `dbc955cf93c208746ec0d1d4432c9acf4379dbef120fca197b1120cb922dd707`
- .teacher/runs/commit-000346-001/raw-transcript.json: `45c09ef8079eb56973a97693a3b62beaa69cacefae538730bf57e948189c3305`
- teacher/editorial.py: `30c6be7dd1e6319781fc3b8ccefc91e29862c673e075e48124c9f4929910305d`
- teacher/validation_repair.py: `f617082d046084b6e1f00f1ee3c6d71f79f5fca2b215a12442a2baed0044c055`
- teacher/codex_adapter.py: `21baf35d1bc0cb4d01cd7a63a412a1b2945ba53943b18e4d7027af612f85826d`
