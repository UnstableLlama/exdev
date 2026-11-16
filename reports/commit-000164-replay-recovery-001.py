"""Administrative validation only. Never starts or changes a teacher run."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from teacher import cycle
from teacher.runner import Runner

errors = []
class SessionResultRunner(Runner):
    def invoke(self, tool, arguments):
        # Exact exception-to-tool-result semantics from FreshSession.run.
        try:
            return super().invoke(tool, arguments)
        except (ValueError, RuntimeError) as exc:
            errors.append(dict(tool=tool, arguments=arguments, error_type=type(exc).__name__, error=str(exc)))
            return {'ok': False, 'error': str(exc)}

run = Path('.teacher/runs/commit-000164-001')
packet = Path('.teacher/retrieval/000164-001')
before = {str(p): cycle.digest(p) for p in run.iterdir() if p.is_file()}
with patch.object(cycle, 'Runner', SessionResultRunner):
    validation = cycle.validate_run(run, packet, Path('.sources/exllamav3.git'), Path('data/evidence/github'), 164)
assert before == {str(p): cycle.digest(p) for p in run.iterdir() if p.is_file()}
validation['administrative_recovery'] = dict(original_failure='reports/commit-000164-manual-001.result.json', method='Original validate_run with Runner adapter matching FreshSession.run exception serialization; all comparisons and integrity checks retained', recovered_exceptions=errors, immutable_run_hashes=before, script_sha256=cycle.digest(__file__))
cycle.write_new(Path('reports/commit-000164-validation-001.json'), validation)
summary = cycle.make_summary(run, packet, Path('.sources/exllamav3.git'), 164, Path('reports/commit-000164-validation-001.json'), Path('reports/commit-000164-catalog-selection-001.json'), Path('data/evidence/github'))
cycle.write_new(Path('reports/commit-000164-cycle-001.json'), summary)
with Path('reports/commit-000164-001.skeleton.md').open('x') as f:
    f.write(cycle.skeleton(summary, '01a1da07-7653-7b81-8507-f69683828acb'))
print({k:v for k,v in validation.items() if k not in ('administrative_recovery','fully_read_task_sections')})
