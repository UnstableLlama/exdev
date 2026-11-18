# SPDX-License-Identifier: MIT
import json
from pathlib import Path
import tempfile
import unittest
from teacher.codex_adapter import MODEL, checked_model, require_approval_model
from teacher.codex_transport import configuration


class TeacherModelAdoptionTests(unittest.TestCase):
    def test_approval_model_runtime_and_trial_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            run=Path(tmp)/'run';run.mkdir()
            for model in (MODEL,'gpt-6.1-sol','gpt-6-astra'):
                provenance={'model':model,'reasoning_effort':'medium'}
                runtime={'model':model,'reasoning_effort':'medium'}
                (run/'raw-transcript.json').write_text(json.dumps([{'teacher_runtime':runtime}]))
                require_approval_model(run,provenance)
                for changes in ({'model':'other'}, {'reasoning_effort':'high'}, {'trial_only':True}):
                    with self.assertRaises(ValueError):require_approval_model(run,dict(provenance,**changes))
                for bad in ({'model':'other','reasoning_effort':'medium'}, {'model':model,'reasoning_effort':'high'}):
                    (run/'raw-transcript.json').write_text(json.dumps([{'teacher_runtime':bad}]))
                    with self.assertRaises(ValueError):require_approval_model(run,provenance)
            (run/'raw-transcript.json').write_text('[{}]')
            require_approval_model(run,{'model':'gpt-6-astra','reasoning_effort':'medium'})
            with self.assertRaises(ValueError):require_approval_model(run,{'model':'gpt-6.1-sol','reasoning_effort':'medium'})
            trial=Path(tmp)/'.teacher/trials/run';trial.mkdir(parents=True)
            with self.assertRaises(ValueError):require_approval_model(trial,{'model':MODEL,'reasoning_effort':'medium'})

    def test_default_sol_and_explicit_legacy_configuration(self):
        self.assertEqual(MODEL,'gpt-6.2-sol')
        self.assertIn('model = "gpt-6.2-sol"',configuration())
        self.assertIn('model = "gpt-6-astra"',configuration('gpt-6-astra'))

    def test_prior_model_is_approval_only(self):
        with self.assertRaisesRegex(ValueError, 'Unsupported teacher model'):
            checked_model('gpt-6.1-sol')
        with self.assertRaisesRegex(ValueError, 'Unsupported teacher model'):
            configuration('gpt-6.1-sol')
