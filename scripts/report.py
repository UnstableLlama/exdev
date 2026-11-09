#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 UnstableLlama and exdev contributors
"""Render aggregate mining results without exposing later diffs to the reviewer."""
import json
from collections import Counter
from pathlib import Path
from mine import atomic_json

DATA=Path('data/exllamav3-v5')
report=json.loads((DATA/'report.json').read_text())
manifest=json.loads((DATA/'manifest.json').read_text())
entries=[json.loads(p.read_text()) for p in sorted(Path('encyclopedia/entries').glob('*.json'))]
Path('reports').mkdir(exist_ok=True)
atomic_json(Path('reports/external-references.json'),{'head':report['head'],'retrieved_at':manifest['retrieved_at'],'references':report['references']})
summary={k:v for k,v in report.items() if k!='references'}
summary['reference_counts_by_kind']=dict(Counter(r['kind'] for r in report['references']))
summary['reviewed_positions']=[e['position'] for e in entries]
summary['encyclopedia_statuses']=dict(Counter(e['status'] for e in entries))
atomic_json(Path('reports/mining-summary.json'),summary)
lines=['# Mining and first-25 review report','',f"Pinned upstream tip: `{report['head']}`. Retrieved {manifest['retrieved_at']}.",'',
       f"**{report['total_commits']:,} commits**, one raw record per commit reachable from the pinned default-branch tip; **{report['noise_count']} flagged as noise**. Unmerged branches and unreachable objects are outside this walk.",'',
       '| Type | Count |','| --- | ---: |']
lines += [f'| {k} | {v:,} |' for k,v in report['counts_per_type'].items()]
lines += ['', '## Reference inventory','', '[Every extracted reference and its commit positions](external-references.json) is recorded as JSON. The list includes URLs, paper links, HF repository candidates, issue/PR references and model-name candidates. Embedded calibration-text URLs are listed separately. Candidates are not claims that a model is supported or that a source was consulted.','',
          '| Reference kind | Distinct values |','| --- | ---: |']
lines += [f'| {k} | {v:,} |' for k,v in sorted(summary['reference_counts_by_kind'].items())]
lines += ['', '## Tagging spot-check','', 'All first 25 diffs were reviewed in chronological order. [Reviewed labels](../seeds/type-reviews.json) override automatic guesses and retain a review reason. The final records also retain automatic_type. The sample is concentrated at the start of history, not a statistically representative accuracy estimate.','',
          'Rule corrections: do not classify executable examples as documentation merely by directory name; recognize VRAM, golden-section search and skipped GC as performance clues; identify docstring changes; restrict formatting noise to checked documentation presentation changes; never infer Python semantic equivalence from whitespace-insensitive diffs. Binary patch payloads no longer generate model/issue matches. Calibration references are segregated, Markdown URL endings are parsed more carefully, and HF collection pages are not treated as model repositories.','',
          'Context-sensitive corrections include the JIT manifest fix (000017), the two halves of the capitalization change (000019–000020), and formatting-only entry 000003. The contributor commit and merge at 000009–000010 have the same diff and must not be treated as independent fixes during future sample generation.','',
          '## Encyclopedia checkpoint','', '25 entries and snapshots at 000001, 000018 and 000024 are present. No entry beyond 25 and no training traces were generated. [Index and temporal rules](../encyclopedia/README.md).','',
          'Four entries explicitly carry source gaps: 000001 (root-source research), 000008 (historical HF collection membership), 000009 and 000010 (historical issue body). Other entries are drafts pending review, not certified training examples. Root work still lacks the full historical HF non-weight inventories/safetensors headers, exhaustive architecture-reference comparisons and some paper/kernel details. These requirements are not represented as complete.','',
          '## Validation','', '[Verification results](verification.json) cover all record identities, checksums, DAG ordering, database counts, tag totals and exact tree replay for the first 25 diffs. Eight standard-library tests cover extraction, conservative tagging, roots, resume, parent exports, merges, tamper detection and packaged upstream notice presence. Small CPU checks additionally support entries 000012, 000015, 000022 and 000025.','',
          'No upstream CUDA build, complete model import, tiny-model quantization or multi-GPU correctness benchmark was performed. Patch applicability alone does not establish runtime correctness; observed intermediate defects remain documented.','',
          '## Licensing','', 'Original exdev work uses MIT. Copied upstream notices preserve Turboderp’s copyright. Each mining output includes a NOTICE, ATTRIBUTION.md and LICENSES/exllamav3-MIT.txt; records include the historical LICENSE blob ID or null when absent. External sources retain their own terms. See [attribution](../ATTRIBUTION.md). Raw source caches and full mined diffs remain ignored local artifacts.','']
Path('reports/mining-report.md').write_text('\n'.join(lines))
print(json.dumps(summary,indent=2))
