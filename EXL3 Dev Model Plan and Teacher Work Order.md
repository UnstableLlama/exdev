# EXL3 Dev Model: Plan and Teacher Work Order

Nov 9, 2026 · @UnstableLlama

## Goal

Build a small open-source model that is a specialist in exl3 development: it knows the exllamav3 codebase, how it got to its current shape, and why each decision was made.

The method is distillation with a twist. A stronger teacher model walks the full commit history of exllamav3 in order, builds a chronological reference called the Exllama Encyclopedia, and turns each commit into tool-use training traces for the student.

The commits are the ground truth. The teacher does not invent exl3 expertise; it explains and enriches work that turboderp and other contributors already did. That keeps the student from being capped at whatever the teacher happens to know about quantization or kernels.

## Ground rules

Five rules hold for every stage of the work.

1. **Start from commit one.** The walk begins at the first exllamav3 commit and moves forward in order. Nothing is skipped ahead to.
2. **No hindsight in historical authoring.** The teacher receives the task diff, repository evidence from its strict ancestors, approved ancestor Encyclopedia entries, and eligible external sources; it never uses later commits to explain an earlier change. Later defect findings belong in a separate, labeled retrospective layer used for sample generation and human retrospective views, subject to the evaluation cutoff and permitted ancestry. They never rewrite historical prose or leak into intervening authoring contexts. See [defect retrospective policy](docs/defect-retrospectives.md).
3. **Pin external material to the commit date.** Papers are read at the version that existed then. HuggingFace repos are read at the revision that existed then. If the dated version cannot be recovered, the entry says so.
4. **The teacher annotates; it does not originate.** Every code change in the dataset is a real change from the history. The teacher supplies the problem statement, the reasoning, and the surrounding research.
5. **Training samples are tool-use traces.** The student learns to inspect before it writes: open the config, read the tensor manifest, check the paper, then produce the change. Traces use only the shared tool set defined below.

## Scope and order

exllamav3 comes first and is done completely before anything else starts.

| Order | Repository | Status |
| --- | --- | --- |
| 1 | exllamav3 | Start now, from the first commit |
| 2 | TabbyAPI | After exllamav3 is complete |
| 3 | ezexl3 | After TabbyAPI |
| 4 | exllamav2 | Probably unnecessary; revisit only if the student lacks design context |
| Later | llama.cpp, vLLM | Possible lateral expansion, not part of this plan |

Two cautions for the later stages. Any evaluation cutoff date has to apply across every repo in training, because a TabbyAPI commit can reveal an exllamav3 change it was written to support. And llama.cpp and vLLM have far larger histories, so they would dominate the mix unless capped or trained as a separate model.

## The Exllama Encyclopedia

The Encyclopedia is the chronological index of the project: one entry per commit, in commit order, plus periodic snapshots of the whole codebase. It is the intermediate product that all training samples are later generated from, and it is useful as a reference in its own right.

Each commit entry holds the following.

| Field | Contents |
| --- | --- |
| Identity | SHA, parent SHA, author, date, position in the walk |
| Raw change | Commit message, full diff, files touched |
| Type | Bugfix, new architecture support, performance, refactor, feature, docs, or noise |
| Problem | What was wrong or missing before this commit, written from the parent state |
| Reasoning | Why this approach, and which alternatives the code or discussion rules out |
| Impact | What the change touches downstream and what it makes possible |
| External sources | Every paper, reference implementation, HF repo, issue, and PR consulted, with version or revision and retrieval date |
| Source notes | The analysis of each external source and how it maps onto the code |
| Links | Earlier Encyclopedia entries this one builds on |
| Confidence | Where the teacher is inferring rather than reading, stated plainly |

Noise commits (formatting, version bumps, merges with no content) still get an identity row so the sequence has no gaps, but no analysis.

**Snapshots.** At regular intervals, and at every major structural change, the teacher writes a snapshot entry: the module layout, the main data flow, the supported architectures, and the open problems as of that commit. Snapshots give the student the structure, where commit entries give it the changes.

## External sources

The teacher follows every outside reference a commit makes, because the commit messages are terse and most of the reasoning lives elsewhere.

**Papers.** When a commit or its discussion references a paper, the teacher fetches the paper at the version current on the commit date and analyzes it. The key output is the mapping from paper to code: which equation or algorithm became which function, and where the implementation departs from the paper and why. The teacher also looks for other analysis of the paper, and prefers the authors' reference implementation over blog posts. A comparison between the reference code and the exllamav3 version belongs in the entry.

**Model additions.** When a commit adds support for a model or architecture, the teacher fetches every file in that model's HuggingFace repo except the weights, at the revision current on the commit date:

- `config.json` and `generation_config.json`
- tokenizer files and the chat template
- `model.safetensors.index.json`, which maps tensor names to shards
- the safetensors headers, read by range request, for tensor names, shapes, and dtypes
- the reference modeling code for that architecture in transformers

The entry records what the teacher read and what it learned from each file, so the training trace can show the student doing the same reads before writing the loader.

**Issue and PR threads.** For each commit, the teacher pulls the linked issue and PR discussion from GitHub. This is where the rejected alternatives and the bug reports live.

**HuggingFace repos, especially turboderp's.** Model cards and repo files from turboderp's own HF account are a priority source. They carry measured results, which give entries numbers to anchor on.

Every external source is logged in the entry with its URL, its version or revision, and the date it was retrieved.

## Shared tool set

The teacher's traces use exactly the tools the student will have at inference, with the same names and argument shapes. A student trained on calls it cannot make learns nothing useful from them, so this list is fixed before any traces are generated.

| Tool | Purpose |
| --- | --- |
| `repo_read` | Read a file from the repo at a given commit |
| `repo_list` | List a directory at a given commit |
| `repo_grep` | Search the repo at a given commit |
| `git_show` | Show a commit's message and diff |
| `git_log` | List history for a path, bounded by date |
| `hf_fetch` | Fetch a non-weight file from a HuggingFace repo at a revision |
| `safetensors_header` | Read tensor names, shapes, and dtypes from a safetensors file header |
| `web_fetch` | Fetch a paper, issue thread, PR thread, or web page |
| `run` | Run a command: tests, an import check, a tiny quantization |

Names and argument shapes are proposals. The teacher may adjust them while writing the miner, but must freeze them before generating the first trace and record the final schema in the Encyclopedia's front matter.

## Training samples

Training samples are generated from Encyclopedia entries, after the entries exist. Each meaningful commit yields several traces of different shapes.

| Shape | Input | Trace ends with |
| --- | --- | --- |
| Reconstruction | Repo at the parent commit plus a task description | The real diff |
| Bug localization | Pre-fix repo plus the reported symptom | The location and the real fix |
| Architecture support | A model's HF repo plus the task of adding support | The real loader and mapping code |
| Paper to code | A paper plus the task of implementing part of it | The real implementation, with departures explained |
| Review | A real diff | A critique grounded in the entry's reasoning |
| Codebase Q&A | A snapshot plus a question about structure or flow | An answer that cites files and functions |

In every shape, the middle of the trace is the inspection work: reading the config, the tensor manifest, the relevant source files, and the external sources logged in the entry. The trace must show those reads as actual tool calls with real results, not describe them.

## Verification, training, and evaluation

**Verification.** Anything in a trace beyond the real diff is checked by running it. Tool calls are replayed against the pinned commit and must return what the trace says they return. Code produced in a trace must apply cleanly and import. Where a tiny model can be quantized at that commit, the result is compared against the reference. Traces that fail are dropped, not repaired by hand.

**Training.** The student is a code-capable open-weight base small enough to train on a dual-3090 workstation, fine-tuned with exl3\_qlora. Repo-level tasks are long, so each trace carries only the files its tool calls actually read.

**Evaluation.** The walk supplies its own test set. Wherever the Encyclopedia currently stands, the next commits are ones the student has not seen, so the student is tested on them before they are folded in. The comparison that matters is the fine-tuned student against the same base model with plain retrieval over the repo and no fine-tune. If the fine-tune does not beat that baseline, the Encyclopedia is still useful as the retrieval corpus.

**A known limit.** Learning from history teaches the codebase's idioms and reasoning. It does not by itself produce a model that writes faster kernels than already exist. For performance work, a later stage could generate candidates, benchmark them, and keep the measurably faster ones as training data.

## Open questions

None of these block the work order below.

- [ ] Which base model does the student start from?
- [ ] Final name: Exllama Encyclopedia, or something else?
- [ ] How often are snapshots written: every N commits, at tagged releases, or both?
- [ ] Storage format for entries: one JSON or Markdown file per commit, or a single database?
- [ ] Does the Encyclopedia get published, and if so where?

## Teacher work order: start now

This section is addressed to the teacher model. Do these three things, in this order, on exllamav3 only. Do not generate training traces yet.

### 1. Write the miner

Write a script that clones exllamav3 and walks its history from the first commit forward. For each commit it emits one record containing:

- SHA, parent SHA, author, date, and position in the walk
- the commit message and the full diff
- the list of files touched
- any issue or PR numbers, paper links, model names, and HuggingFace repo names referenced in the message or diff
- a first-pass type tag and a noise flag for formatting, version bumps, and empty merges

The miner must be resumable, must write one record per commit to disk, and must be able to check out the repo at any commit's parent for the tools to read from.

### 2. Start mining

Run the miner over the full exllamav3 history. Report the total commit count, the count per type tag, the count flagged as noise, and the list of every external reference found. Spot-check the type tags on a sample and correct the tagging rules where they are wrong.

### 3. Start the Exllama Encyclopedia

Beginning at commit one and moving forward in order, write an Encyclopedia entry for each commit using the entry fields defined above. For every entry:

- read the repo only as of the parent commit, plus entries already written
- follow every external reference: fetch the paper, the reference implementation, the HuggingFace files other than weights, and the issue and PR threads, each pinned to the commit date
- log every source with its URL, version or revision, and retrieval date
- mark plainly anything inferred instead of read

Write the first snapshot entry once the codebase has a recognizable structure, and another at each major structural change.

Stop and report after the first 25 entries so the format and depth can be reviewed before the rest of the walk continues.
