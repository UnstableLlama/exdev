# Decision: use mirrors for commit 98's gated Cohere reference models

Recorded by Fable (reviewer) on 2026-11-14.

## The user's words

Told that commit 98's reference models are gated on Hugging Face and that the alternative was to accept fifteen gates
and install a token (`commit-000098-reference-access-001.md`), the user answered:

> look for unsloth mirrors and if they dont have them modelscope.cn will

## What I found (checked from `exdev-314`, no credential)

Hugging Face publishes, without a credential, the current file list of each gated repository with every file's Git blob
id and, for large files, its SHA-256. Its commit history stays gated.

**unsloth** has `unsloth/c4ai-command-r-08-2024` and `unsloth/c4ai-command-r-plus-08-2024` (plus `bnb-4bit` variants) and
nothing for the other eight. Neither is a copy: `config.json`, `tokenizer_config.json` and all weight files differ from
the originals (0 of 14 and 0 of 44 weight hashes match). They are re-saved uploads.

**ModelScope** has all ten, and each is byte-identical to the gated original's current files: the `config.json` blob id
matches and every safetensors SHA-256 matches.

| Original (`CohereLabs/…`) | ModelScope repository | Created (UTC) | config | weights |
|---|---|---|---|---|
| `c4ai-command-r-v01` | `AI-ModelScope/c4ai-command-r-v01` | 2024-03-13 | match | 15 / 15 |
| `c4ai-command-r-v01-4bit` | `CohereForAI/c4ai-command-r-v01-4bit` | 2024-12-14 | match | 5 / 5 |
| `c4ai-command-r-plus` | `AI-ModelScope/c4ai-command-r-plus` | 2024-04-09 | match | 44 / 44 |
| `c4ai-command-r-plus-4bit` | `CohereForAI/c4ai-command-r-plus-4bit` | 2024-12-14 | match | 13 / 13 |
| `aya-23-8B` | `CohereForAI/aya-23-8B` | 2024-12-14 | match | 4 / 4 |
| `aya-23-35B` | `CohereForAI/aya-23-35B` | 2024-12-14 | match | 15 / 15 |
| `c4ai-command-r-08-2024` | `AI-ModelScope/c4ai-command-r-08-2024` | 2024-09-03 | match | 14 / 14 |
| `c4ai-command-r-plus-08-2024` | `CohereForAI/c4ai-command-r-plus-08-2024` | 2024-12-14 | match | 44 / 44 |
| `aya-expanse-8b` | `AI-ModelScope/aya-expanse-8b` | 2024-10-25 | match | 4 / 4 |
| `aya-expanse-32b` | `AI-ModelScope/aya-expanse-32b` | 2024-10-25 | match | 14 / 14 |

All ten ModelScope repositories were created before commit 98's cutoff (2025-04-27 15:06 UTC).

## What follows from it (my interpretation, not the user's words)

1. **Use ModelScope for all ten, not unsloth for two.** The user's order was unsloth first. I am departing from it for
   the two models unsloth has, because those uploads are altered and the ModelScope ones are provably the same files.
   The user's aim (no gates, no token) is met either way. The user can overrule this.
2. A mirror file counts as the official file only when identity is shown: its Git blob id (small files) or SHA-256
   (large files) equals the value Hugging Face publishes for the official repository. Record both values and the
   comparison in the bundle for every file used. A file that does not match is not attached under the official name.
3. Cutoff: the official history is gated, so the pin cannot be taken from it. Use the ModelScope file's own commit date
   as the availability date; it must be at or before the cutoff. A file identical to the official one that existed on
   a mirror before the cutoff existed before the cutoff. Record the official repository's public creation date too.
4. The official repository stays the identity in the bundle (`CohereLabs/<name>`, with `CohereForAI/<name>` noted as the
   name at the time); the ModelScope repository is recorded as the retrieval source. The teacher sees the official
   name and a plain statement that the bytes were retrieved from a hash-verified mirror.
5. Gated repositories created before the cutoff whose public metadata shows another architecture string
   (`c4ai-command-r7b-12-2024`, `c4ai-command-r7b-arabic-02-2025`, `c4ai-command-a-03-2025`, `aya-vision-8b`,
   `aya-vision-32b`): record them in the discovery report as "not inspected at the pin; current public metadata declares
   <string>", not as absent and not as inspected.
6. This needs tooling for a second source. That is an implementation change: file an implementation request as usual
   before authoring 98. Safetensors headers must be read by range request, not by downloading weights.
7. General rule from now on: when an official repository is gated and no credential is configured, a hash-verified
   mirror may stand in, under points 2 to 4. An unverifiable mirror may not.

## Addendum, 2026-11-14 (reviewer's interpretation, not the user's words)

Point 7's last sentence ("An unverifiable mirror may not") is refined by
`reviews/verdicts/commit-000103-reference-access-001.md`: a non-weight file whose official copy was edited after the cutoff
may be taken from a pre-cutoff mirror revision under a separate labelled status, when two distinct mirrors hold the
same bytes before the cutoff and every other file of the model verifies against the official hashes. First case:
`c4ai-command-r7b-12-2024/config.json` at commit 103.
