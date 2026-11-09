# SPDX-License-Identifier: MIT
"""Author one unpublished draft in a fresh Codex process; never modify the Encyclopedia."""
import argparse
import hashlib
import json
from pathlib import Path
from .codex_adapter import CodexTeacher, MODEL, EFFORT
from .codex_transport import CodexTransport, SUPPORTED_VERSION
from .editorial import render
from .session import FreshSession

ROOT=Path(__file__).resolve().parents[1]


def write_json(path, value):
    pending=path.with_suffix(path.suffix+'.new')
    pending.write_text(json.dumps(value,indent=2)+'\n')
    pending.replace(path)


def author(packet, output, auth_file, transport_factory=CodexTransport):
    packet,output=Path(packet).resolve(),Path(output).resolve()
    if output.is_relative_to(packet):
        raise ValueError('Draft output must be outside the immutable packet')
    session=FreshSession(packet)
    session.require_authoring_context()
    output.mkdir(parents=True,exist_ok=False)
    manifest=(packet/'manifest.json').read_bytes()
    provenance={'model':MODEL,'reasoning_effort':EFFORT,'codex_version':SUPPORTED_VERSION,
        'packet_manifest_sha256':hashlib.sha256(manifest).hexdigest(),
        'input_mode':'entry_analysis','published':False,
        'implementation_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted([*(ROOT/'teacher').glob('*.py'),*(ROOT/'schema').glob('*.json')])}}
    write_json(output/'provenance.json',provenance)
    write_json(output/'status.json',{'status':'running','published':False})
    try:
        with transport_factory(auth_file) as transport:
            result=CodexTeacher().run(session,transport,
                record=lambda transcript:write_json(output/'raw-transcript.json',transcript))
        if manifest!=(packet/'manifest.json').read_bytes():
            raise ValueError('Packet changed during authoring')
        write_json(output/'draft.json',result['draft'])
        write_json(output/'review.json',result['review'])
        (output/'draft.md').write_text(render(result['draft']))
        write_json(output/'status.json',{'status':'draft','published':False})
        return output
    except BaseException as error:
        write_json(output/'status.json',{'status':'failed','published':False,'error_type':type(error).__name__})
        raise


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True,help='New draft directory, preferably under ignored .teacher/runs/')
    parser.add_argument('--auth-file',type=Path,default=Path.home()/'.codex/auth.json')
    args=parser.parse_args()
    print(author(args.packet,args.output,args.auth_file))


if __name__=='__main__':main()
