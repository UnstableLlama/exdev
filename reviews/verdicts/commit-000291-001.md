# Verdict: commit-000291-001 (teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-17 (13:03 UTC). Upstream `e1484296` "Tokenizer: Don't skip special tokens in base vocab".
Run: `.teacher/runs/commit-000291-001`. Packet: `.teacher/retrieval/000291-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. No formal findings in the
entry. It made the central check itself: it followed the changed table to its consumers and states the
consequence, that the ordinary piece table (the one generation uses when special-token decoding is off) can
now carry special-token text for tokens in the base vocabulary, and that the other branch of the same
method is left without the keyword.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes
equal to the accepted set, 13 evidence calls all cited and none bad, final equals annotation, 290 of 290
ancestors, 3842 blobs, nothing after the cutoff. Orchestration hashes equal the accepted files; complete
packet; ran ahead of none. Repair enabled, unused.

## Run checks (mine, tree at `e1484296`)

`get_id_to_piece_list(False)` is the fixed vocabulary plus extended ids; `job.py` line 550 indexes
`get_id_to_piece_list(self.decode_special_tokens)` for output text, default false. So the consequence the
entry describes is on the default generation path. As stated.

## Must fix before canonical use

1. The consequence above is described in prose only. It is a behaviour change for existing callers and
   should be filed as a finding with its reach stated (which tokens are special in the base vocabulary
   without being in the extended table).
2. The backend's default for `skip_special_tokens` is assumed, and said to be assumed. A canonical entry
   should establish it from eligible evidence of the tokenizer library at the cutoff.

## Ledger

Accepted: `missing-ernie-registry-modules` r001, `custom-bias-export-name` r001,
`optional-inputs-required-by-dots` r003, `grouped-routing-unassigned` r003 (fix at `6735462a`),
`all-expert-fused-shape` r010, `fused-output-dtype-override` r003.
