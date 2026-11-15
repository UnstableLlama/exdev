# Verdict: commit-000098-reference-access-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/commit-000098-reference-access-001.md`
Upstream at walk position 98: `875e503e84ddf27441f551a2c7dc50982c8cd48c` "Add Cohere architecture"
Reviewed: 2026-11-14, machine `exdev-314`

## Decision

**HELD for the user.** Stopping here was right. Do not author commit 98, and do not treat any gated file as absent.

## What I checked

- Commit 98 adds `exllamav3/models/cohere.py` and registers an architecture, so the reference-evidence rule applies.
- `config.json` at `CohereLabs/c4ai-command-r-v01`, `CohereForAI/c4ai-command-r-v01`, `CohereLabs/c4ai-command-r-plus` and
  `CohereLabs/aya-expanse-8b` returns HTTP 401 from this machine without a credential. Confirmed.
- `teacher/root_evidence.py` takes a credential from `HF_TOKEN` or `~/.cache/huggingface/token`. Neither exists here.
- The gates are per repository and of the automatic kind: the account holder has to accept each one on the website. A
  token alone is not enough.

## Which repositories need access

Hugging Face's public listing (no credential needed) gives each repository's creation date and the architecture string
of its current config. This is a pointer for the user's clicking, not reference evidence; the pinned configs still have
to be fetched and checked by the discovery tool.

Gated, created before the cutoff (2025-04-27 15:06 UTC), currently declaring `CohereForCausalLM` (ten):

- `CohereLabs/c4ai-command-r-v01`, `CohereLabs/c4ai-command-r-v01-4bit`
- `CohereLabs/c4ai-command-r-plus`, `CohereLabs/c4ai-command-r-plus-4bit`
- `CohereLabs/aya-23-8B`, `CohereLabs/aya-23-35B`
- `CohereLabs/c4ai-command-r-08-2024`, `CohereLabs/c4ai-command-r-plus-08-2024`
- `CohereLabs/aya-expanse-8b`, `CohereLabs/aya-expanse-32b`

Gated, created before the cutoff, currently declaring something else, which discovery must still be able to open to
confirm what they declared at the cutoff (five):

- `CohereLabs/c4ai-command-r7b-12-2024`, `CohereLabs/c4ai-command-r7b-arabic-02-2025`, `CohereLabs/c4ai-command-a-03-2025`
- `CohereLabs/aya-vision-8b`, `CohereLabs/aya-vision-32b`

Everything else in the organisation is either ungated or was created after the cutoff.

## For the user

1. Accept the gate on each of the fifteen repositories above while signed in to Hugging Face.
2. Put a read token for that account at `~/.cache/huggingface/token` on `exdev-314`.
3. Tell Fable; I will tell Astra to rerun discovery.

## Next (Astra)

1. Wait. Nothing to author.
2. When told access is in place: rerun discovery for `CohereForAI`, `CohereLabs` and `Cohere` at commit 98's cutoff, rebuild
   the reference bundle, and report any repository that is still unreadable by name before authoring.
3. Never print, log or copy the token into any report, packet or bundle.
