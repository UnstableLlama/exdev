"""Sparse approved-prose adapter, used only by the opt-in queue driver.

Source ancestry stays complete. The existing worker's ancestor retrieval runs
against the selected subset; every other tool sees the original manifest.
"""
from contextlib import contextmanager
from copy import deepcopy
import importlib.util
import json
from pathlib import Path


def selected_manifest(manifest):
    selection = manifest.get('approved_ancestor_selection')
    if selection is None:
        return manifest
    order = manifest['history_order']
    if len(order) != len(set(order)) or set(order) != set(manifest['commits']):
        raise ValueError('Incomplete source ancestry')
    if selection != [sha for sha in order if sha in set(selection)] or len(selection) != len(set(selection)):
        raise ValueError('Invalid approved ancestor selection')
    if any(sha not in manifest['commits'] for sha in selection):
        raise ValueError('Selection outside strict ancestry')
    if [r['sha'] for r in manifest.get('ancestor_entries', [])] != selection:
        raise ValueError('Prose differs from approved selection')
    result = deepcopy(manifest)
    result['commits'] = {sha:manifest['commits'][sha] for sha in selection}
    result['history_order'] = selection
    return result


def sparse_attach(packet, runs):
    from teacher.ancestor_context import attach_entries
    from teacher.author import write_json
    from teacher.retrieval import attach
    packet = Path(packet)
    manifest = json.loads((packet/'manifest.json').read_text())
    selected = {json.loads((Path(run)/('entry.json' if (Path(run)/'entry.json').exists() else 'draft.json')).read_text())['sha'] for run in runs}
    if selected == set(manifest['commits']):
        return attach_entries(packet, runs)
    if manifest.get('ancestor_context_mode') != 'retrieval_v1':
        raise ValueError('Sparse selection requires retrieval_v1')
    # attach validates approval artifact hashes and strict ancestry for each run.
    subset = deepcopy(manifest)
    subset['commits'] = {k:v for k,v in manifest['commits'].items() if k in selected}
    subset['history_order'] = [sha for sha in manifest['history_order'] if sha in selected]
    attach(packet, runs, subset)
    subset.update(commits=manifest['commits'], history_order=manifest['history_order'],
                  approved_ancestor_selection=subset['history_order'])
    write_json(packet/'manifest.json', subset)


@contextmanager
def installed():
    """Host catalog and isolated tool adapter; sequential calls stay byte-identical."""
    from teacher import worker, runner, cycle
    old_read, old_command, old_attach = worker.ancestor_read, runner.command, cycle.attach_entries
    def read(packet, manifest, args):
        return old_read(packet, selected_manifest(manifest), args)
    def command(packet, graph=False):
        argv = old_command(packet, graph=graph)
        manifest = json.loads((Path(packet)/'manifest.json').read_text())
        if not graph and 'approved_ancestor_selection' in manifest:
            argv[-1] = '/app/run_ahead_worker.py'
            argv[1:1] = ['--ro-bind', str(Path(__file__).resolve()), '/app/run_ahead_worker.py']
        return argv
    worker.ancestor_read, runner.command, cycle.attach_entries = read, command, sparse_attach
    try:
        yield
    finally:
        worker.ancestor_read, runner.command, cycle.attach_entries = old_read, old_command, old_attach


def isolated_main():
    spec = importlib.util.spec_from_file_location('base_worker', '/app/teacher/worker.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original = module.ancestor_read
    module.ancestor_read = lambda packet, manifest, args: original(packet, selected_manifest(manifest), args)
    module.main()


if __name__ == '__main__':
    isolated_main()
