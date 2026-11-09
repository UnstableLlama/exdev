# SPDX-License-Identifier: MIT
"""Render the completed four-snapshot validation evidence."""
import json
from .validate import ROOT, OUT


def main():
    report = json.loads((ROOT / 'reports/graph-validation.json').read_text())
    lines = ['# Graph validation checkpoint', '',
             'Pinned EXL3 tip: `bd1f519172406a9560bd5c90e61000691bb69a07`. Backend: codebase-memory-mcp v0.12.1, checksum verified. Four snapshots were indexed in increasing miner position, at one fixed checkout path and project name.', '',
             '**Decision: retain the backend for integration, but do not start the full graph walk yet.** Python structure and stable names look useful; native binding gaps and partial CUDA parsing must remain explicit. This is a feasibility check, not proof of complete call resolution.', '',
             '| Position | Commit | Nodes | Edges | Direct Python candidates found | Resolvable binding sites missing | Unresolved binding sites | Partially parsed files |',
             '|---|---|---:|---:|---:|---:|---:|---:|']
    for s in report['snapshots']:
        lines.append(f"| {s['position']} | `{s['sha'][:12]}` | {s['nodes']} | {s['edges']} | {s['python_direct_found']}/{s['python_direct_calls']} | {s['missing_binding_sites']}/{s['resolved_binding_sites']} | {s['unresolved_binding_sites']} | {s['index'].get('parse_partial_count', 0)} |")
    lines += ['', 'Counts of exported code-graph nodes and edges matched the corresponding project rows in each SQLite database. The separate parsing-miss project is not counted as source-code nodes. Raw diagnostics, exports, trace responses and SQLite backups remain under `data/graph/validation/<sha>/`.', '',
              '## Stable qualified names', '']
    for s in report['stability']:
        lines.append(f"- `{s['before'][:12]}` → `{s['after'][:12]}`: {s['stable']}/{s['comparable']} unchanged, unambiguous matches retained their qualified name; {len(s['drift'])} drifted.")
    lines += ['', 'Matches require the same file, kind, simple name and exact source-range hash. This excludes edited functions and ambiguous duplicates; it does not validate rename/move tracking. One apparent drift between positions 755 and 1509 matches the identical declaration `Graph graph_bsz1;` under different owners (`BC_GatedMLP` and `BC_MLP`). Source inspection shows distinct class scopes, so this is a false identity match by the probe, not evidence of backend name instability. Production identity matching must include enclosing scope. The four later differences are methods moved from `CacheLayer_qsa` into `QSAPlanes`, confirmed in the two source trees; their qualified-name changes reflect real owner changes. No unexplained backend name drift remains in this sample.', '', '## Call traces', '',
              'Five outbound, depth-two traces were requested at each snapshot, with `include_tests=true`. The default excludes test code and initially hid calls from `eval/prequant_test.py`; the checks were rerun with that filter disabled. The following comparison checks same-file bare-name call candidates against hop-one results. These are static diagnostic candidates, not a comprehensive labeled benchmark.', '',
              '| Position | Traced callers | Candidate calls returned at hop one |', '|---|---:|---:|']
    for s in report['snapshots']:
        result = json.loads((OUT / s['sha'] / 'result.json').read_text())
        total = found = 0
        for trace in result['traces']:
            table = trace['result'].get('callees', {})
            targets = set()
            for group in table.get('groups', []):
                for row in group['rows']:
                    if row[1] == 1:
                        targets.add('.'.join(filter(None, [group['qn_prefix'], row[0]])))
            expected = {c['target'] for c in result['analysis']['python_direct_calls'] if c['source'] == trace['source']}
            total += len(expected)
            found += len(expected & targets)
        lines.append(f"| {s['position']} | {len(result['traces'])} | {found}/{total} |")
    lines += ['', 'At the root, source inspection confirms `get_device_context → get_key`, `release_device_context → get_key`, and both evaluation chains `main → get_test_tokens → get_dataset_text` in `eval/model_diff.py` and `eval/ppl.py`. The stored backend traces include those hops. These checks do not validate every edge in those traces.', '',
              '## Boundary coverage and limitations', '',
              'The binding probe uses Python AST call locations and direct `m.def("name", &function)` declarations. It accepts only a unique C++/CUDA function definition and an indexed enclosing Python function. Its missing counts are call sites, not unique edges. Module-level calls, ambiguous targets, class bindings, indirect imports and dynamic dispatch need further work. Proposed binding links are recorded as evidence; no supplemental edges have been inserted yet.', '',
              'Partial parsing grows with the codebase. Zero unusable files would not imply full CUDA coverage: constructs inside partial-parse ranges may still be absent. Consult the machine-readable report and full backend logs for file/range diagnostics. No GPU execution was performed.', '',
              '## Next integration work', '',
              '1. Add evidence-bearing supplemental native binding edges, with unresolved cases kept explicit.',
              '2. Implement and test source-hash diffs and the timeline database against actual parents; gaps between these four samples must never become per-commit events.',
              '3. Implement and freeze the five student tool schemas with enforced historical commit boundaries, then attach Encyclopedia symbol links. Production indexing must also isolate Git metadata to the allowed historical revision: these validation worktrees share the full bare repository and are not safe teacher-facing artifacts.',
              '4. Begin the full graph walk at the root, processing parents before children, after this validation checkpoint has been reported.', '',
              'The first 25 Encyclopedia drafts are unchanged. No training traces or full graph-history walk were generated. Later training should join code, Encyclopedia and graph by commit and symbol, without using later information in earlier tasks.', '',
              'Verification: `python3 -m unittest discover -s tests` passes all 13 tests. Export checks cover every code node and edge count in all four snapshots. No commits or pushes were made.', '',
              'Reproduce with `python3 -m graph.validate` followed by `python3 -m graph.report`. See [setup and probe scope](../graph/README.md) and [machine-readable results](graph-validation.json).', '']
    (ROOT / 'reports/graph-validation.md').write_text('\n'.join(lines))


if __name__ == '__main__':
    main()
