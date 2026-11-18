# SPDX-License-Identifier: MIT
"""Author one unpublished draft in a fresh Codex process; never modify the Encyclopedia."""
import argparse
import hashlib
import json
import platform
from pathlib import Path
from .codex_adapter import CodexTeacher, MODEL, TRIAL_MODEL
from .codex_transport import CodexTransport, SUPPORTED_VERSION
from .editorial import render
from .validation_repair import repair_metadata
from .session import FreshSession

ROOT=Path(__file__).resolve().parents[1]


def write_json(path, value):
    pending=path.with_suffix(path.suffix+'.new')
    pending.write_text(json.dumps(value,indent=2)+'\n')
    pending.replace(path)


def author(packet, output, auth_file, transport_factory=CodexTransport, *, validation_repair=True):
    return _author(packet, output, auth_file, transport_factory, validation_repair=validation_repair)


def author_revision(packet, output, auth_file, *, revision, transport_factory=CodexTransport):
    """Supervisor-only entry point for a separately reserved revision."""
    from .revision import prepare
    prepared = prepare(packet, output, revision)
    return _author(packet, output, auth_file, transport_factory, revision=prepared)


def author_trial(packet, output, auth_file, *, model=TRIAL_MODEL, transport_factory=CodexTransport):
    """Supervisor-only unpublished model comparison; no CLI or walk override."""
    base=(ROOT/'.teacher/trials/teacher-model-001').resolve()
    packet,output=Path(packet).resolve(),Path(output).resolve()
    manifest=json.loads((packet/'manifest.json').read_text())
    if (model!=TRIAL_MODEL or not packet.is_relative_to(base) or not output.is_relative_to(base)
            or manifest.get('guidance_version')!=11 or manifest.get('coverage_request')):
        raise ValueError('Model trial requires its isolated root, guidance 11 and unassisted input')
    return _author(packet,output,auth_file,transport_factory,model=model,trial=True)


def _author(packet, output, auth_file, transport_factory, *, model=MODEL, trial=False, validation_repair=True, revision=None):
    packet,output=Path(packet).resolve(),Path(output).resolve()
    if output.is_relative_to(packet):
        raise ValueError('Draft output must be outside the immutable packet')
    session=FreshSession(packet)
    session.require_authoring_context()
    coverage=session.runner.packet/'manifest.json'
    coverage=json.loads(coverage.read_text()).get('coverage_request')
    if coverage and output.name!=Path(coverage['path']).name.removesuffix('.coverage.md'):
        raise ValueError('Coverage request belongs to another attempt')
    if revision:
        revision.extend(session)
    output.mkdir(parents=True,exist_ok=False)
    manifest=(packet/'manifest.json').read_bytes()
    provenance={'model':model,'reasoning_effort':session.reasoning_effort,'codex_version':SUPPORTED_VERSION,
        'packet_manifest_sha256':hashlib.sha256(manifest).hexdigest(),
        'input_mode':'entry_analysis','published':False,
        'python_version':platform.python_version(),'machine_architecture':platform.machine(),'operating_system':platform.system(),
        'implementation_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted([*(ROOT/'teacher').glob('*.py'),*(ROOT/'schema').glob('*.json')])}}
    if trial:
        if session.reasoning_effort!='medium':
            raise ValueError('Model trial requires medium effort')
        provenance['trial_only']=True
    coverage=json.loads(manifest).get('coverage_request')
    if coverage:
        provenance['coverage_request']={k:coverage[k] for k in ('path','sha256')}
        provenance['reviewer_assisted']=True
    if revision:
        from .revision import ID_MAP_VERSION, REVISION_FILES, initial_input
        write_json(output/'prior-evidence.json', revision.records)
        write_json(output/'revision-input.json', initial_input(session))
        (output/'revision.coverage.md').write_bytes(revision.coverage)
        provenance.update(attempt_kind='revision', reviewer_assisted=True,
                          guidance_version=json.loads(manifest).get('guidance_version', 1),
                          revision={'source': revision.binding, 'id_map_version': ID_MAP_VERSION,
                                    'artifacts': {name: hashlib.sha256((output/name).read_bytes()).hexdigest()
                                                  for name in REVISION_FILES}})
    provenance['token_usage'] = None
    provenance['validation_repair_enabled']=validation_repair
    provenance.update(repair_metadata([]))
    write_json(output/'provenance.json',provenance)
    write_json(output/'status.json',{'status':'running','published':False})
    def record(transcript):
        write_json(output/'raw-transcript.json',transcript)
        provenance.update(repair_metadata(transcript), token_usage=transcript[0].get('teacher_token_usage'))
        write_json(output/'provenance.json',provenance)
    try:
        with (transport_factory(auth_file,model=model) if trial else transport_factory(auth_file)) as transport:
            result=CodexTeacher().run(session,transport,
                model=model, record=record, validation_repair=validation_repair)
        if manifest!=(packet/'manifest.json').read_bytes():
            raise ValueError('Packet changed during authoring')
        write_json(output/'draft.json',result['draft'])
        if revision:
            from .revision import restore, selected_annotation
            restore(output, packet, provenance, result['transcript'])
            if selected_annotation(result['transcript'], provenance) != result['draft']['annotation']:
                raise ValueError('Revision final does not match the draft')
            result['review'].update(attempt_kind='revision', revision_of_run=revision.binding['revision_of_run'])
        if coverage or revision:
            result['review']['reviewer_assisted']=True
        write_json(output/'review.json',result['review'])
        from .coverage import run_coverage
        write_json(output/'coverage.json',run_coverage(packet,json.loads(manifest),result['transcript'], prior=revision.prior if revision else ()))
        (output/'draft.md').write_text(render(result['draft']))
        write_json(output/'status.json',{'status':'draft','published':False})
        return output
    except BaseException as error:
        write_json(output/'status.json',{'status':'failed','published':False,'error_type':type(error).__name__})
        raise


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True,help='New draft directory, preferably under tracked .teacher/runs/')
    parser.add_argument('--auth-file',type=Path,default=Path.home()/'.codex/auth.json')
    args=parser.parse_args()
    print(author(args.packet,args.output,args.auth_file))


if __name__=='__main__':main()
