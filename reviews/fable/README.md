# Fable's reviewer notes

Fable is the independent reviewer of the exdev teacher walk. These files let the role be picked up from a clone of this
repository on another machine. They are reviewer working notes, not teacher input: nothing here may be given to a teacher.

- `STATE.md`: where the walk stands, the rules in force, how a run is reviewed, open threads, and what Git does not carry.
- `check.py`: the mechanical part of a run review. From the repo root: `python3 reviews/fable/check.py 000070 001`.
- `MAILBOX.md`: how Fable and Astra exchange reviews through files and `codex queue`.
- `../FABLE-HANDOFF.md`: a block to paste as the first message of a fresh reviewer session.
- `../verdicts/`: every verdict, user decision (`*.decision.md`) and coverage request (`*.coverage.md`).
- `../AUTHOR-INSTRUCTIONS.md`: Astra's side of the handoff.

## Continuing on another machine

Git carries the code, every run's draft and transcript, the reports, verdicts and decisions. It does not carry the
ignored directories, and the walk cannot build or validate packets without them:

| Path | Size | What it is |
|---|---|---|
| `data/` | about 850 MB | mined records, graphs and the evidence bundles. The bundles are bound into packets by hash and carry retrieval timestamps, so copy them; do not re-fetch. |
| `.sources/` | about 15 MB | the pinned upstream mirror |
| `.teacher/retrieval/`, `.teacher/validation/` | about 9.5 GB | prepared packets |

To continue the walk elsewhere, copy those three from the machine that has them, for example:

```bash
rsync -a --info=progress2 WORK_HOST:git/exdev/{data,.sources,.teacher} ~/git/exdev/
```

Reading and discussing the existing entries and verdicts needs none of that.

The pinned Codex CLI (0.167.0) is also needed on the PATH for the tests and the teacher runs, and Astra's Codex thread id
is per machine: a new Astra session gets a new id, which each request file states as `Reply-to thread:`.
