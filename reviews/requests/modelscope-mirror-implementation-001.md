# Implementation review: hash-verified ModelScope reference recovery

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements `reviews/verdicts/commit-000098-reference-mirrors.decision.md`.
Requested scope: review the second retrieval source and commit 98 reference
recovery before any teacher run. Canonical and training remain false.
Commit 98 has not been authored. The only new packet is an administrative audit
packet: `.teacher/audits/commit-000098-mirrors-001`.

## Change

`teacher.mirror_evidence` accepts explicitly selected ModelScope mirrors for gated
official repositories. Every reference file records official identity, historical
name, official creation date, both identity hashes, mirror repository, immutable
file commit and its date. Small files are compared by Git blob ID; LFS files by
published SHA-256. Downloaded non-weight bytes also match the mirror SHA-256.
Mismatches, missing roles, masked hashes, post-cutoff files and invalid headers
fail closed. Safetensors receive exactly two bounded range reads, never full
weight downloads; servers that ignore or alter ranges are rejected before the
response body is read by the existing transport.

The official history remains gated. No official historical revision is invented:
the bundle's revision is a digest of the verified file set and provenance.
Official current-revision metadata supplies identity only; per-file mirror commit
dates establish historical availability. The teacher-visible index retains the
official name, historical name and a plain mirror notice. Object metadata contains
the per-file proof. Model source dates use the latest constituent file date.

The architecture recovery CLI dispatches explicit mirror selections to the new
source, and its bundle validator rechecks the proofs and file-set digest. Existing
Hugging Face recovery remains the default. Contract 8 / guidance 5 / salience-v2
and the teacher instructions are unchanged. Old packets and authored runs remain
unchanged. Pre-existing arm64 and absent-reference changes in the worktree are
not new parts of this implementation.

## Real recovery and validation

All ten models in the decision recovered successfully: 220 reference objects,
including 172 safetensors headers. Every used file's mirror commit precedes the
cutoff; dates span 2024-03-13 through 2024-12-14. The identity report crosschecks
every proof against saved official and ModelScope metadata snapshots, with their
paths and hashes. Full weight hashes are compared between services; whole weight
files were not locally downloaded or hashed.

Discovery report 002 retains the original enumeration and separately labels the
five other gated architectures as `not_inspected_at_pin`, with their current
public architecture strings. They are neither absent nor historically inspected.
Other failures were reconciled as post-cutoff repository creation or missing root
config confirmed by the pinned tree. Current metadata stays administrative.

All 231 host-enabled tests passed. New tests cover header-only reads, hash and
byte mismatches, masked hashes, missing files, future dates, proof tampering,
architecture-bundle enforcement and the bound teacher-visible mirror notice.
The general boundary audit passed. The real mirror packet passed 222 sandbox
checks: ten index pages, all twenty required config/tokenizer-config reads,
all 172 header objects, and twenty denials for mutable revisions or weight paths.
No live model was invoked. Linux aarch64, Python 3.14.4.

## SHA256

- teacher/mirror_evidence.py: `e3e85e3149839c6fce0a74f12242f234d01d66600b1a0778820600bd0ed9315c`
- teacher/architecture_evidence.py: `9cfa9eb99f3f032b91104ff173328ef5ea607c44bc380009234b5d236165b2ca`
- teacher/evidence_index.py: `c230636d4ed7237cbcfadb7c6b5c5cc2a002462e8b5b53b2d65be609ec3b4458`
- tests/test_mirror_evidence.py: `bd372240955d58746aed4a667e7cb3a83dd2b1acc0da1c201471967cc6097cae`
- docs/ancestor-context.md: `9a421539bbbe55335e20ab4ba2ee3fb0ef1f1abd248207ea4aff6b8fa94f9649`
- reviews/verdicts/commit-000098-reference-mirrors.decision.md: `d1415f21051a32872ab7b9d9504e5f446f38f8019163c65d7d5c0c315638f26c`
- reports/modelscope-mirror-implementation-001.json: `8f67702fc62fc35883b8b565b820ce40d140da0b5f7a5f79e5918c64f3cd7628`
- reports/modelscope-mirror-tests-001.txt: `f8d9a2434b405ada7f9c009befb1f731ab35ef4da04cb093bfc068eb6f29dcca`
- reports/teacher-boundary.json: `455898d200e8de63f72f48ea206c15e69ee754844636f81a2f3c47572aa828e6`
- reports/modelscope-mirror-boundary-001.json: `e3d7f6348a4748dcbbcc3330c11dc72ade08dbff7face5fa42b52bcee451bae4`
- reports/modelscope-mirror-identity-001.json: `0bc37f9f933285fa05c1ba596e0ae18b4633aa92ffc34a171f558a31906aab3b`
- reports/commit-000098-reference-discovery-002.json: `1d360d0d4456568068abc0318bce0558164d95193ed04cb795a22b6324062687`
- reports/commit-000098-reference-selection-002.json: `2712d59f35fd3c4f36618320be3855d4e6ffccc6c2d593d91eae28e4c46d8381`
- reports/commit-000098-mirror-recovery-001.json: `4947184f716742137d53adc7cc3377ec272153e90034a12b4f2a5e633f3e8f4a`
- data/evidence/github/000098-references.json: `b61388343ce1f030c65ff65a07619dc52f1f8efde55577231d04e03f4ba8ceb2`
- .teacher/audits/commit-000098-mirrors-001/manifest.json: `fb30970e1a3b542bf9dd30f144eeef75f7c9004e0bafee5e0807cfc225f5e183`

Reply in `reviews/verdicts/modelscope-mirror-implementation-001.md`.
