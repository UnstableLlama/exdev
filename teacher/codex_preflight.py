# SPDX-License-Identifier: MIT
"""Check real Codex startup without creating a model turn or authoring an entry."""
import argparse
import hashlib
import json
from pathlib import Path
from .codex_adapter import MODEL, thread_parameters
from .codex_transport import CodexTransport, SUPPORTED_VERSION
from .session import FreshSession


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',type=Path,required=True)
    parser.add_argument('--auth-file',type=Path,default=Path.home()/'.codex/auth.json')
    parser.add_argument('--report',type=Path,default=Path('reports/codex-preflight.json'))
    args=parser.parse_args();session=FreshSession(args.packet)
    with CodexTransport(args.auth_file,timeout=90) as transport:
        transport.request('initialize',{'clientInfo':{'name':'exdev_teacher','version':'0.1.0'},
                          'capabilities':{'experimentalApi':True}})
        transport.notify('initialized',{})
        started=transport.request('thread/start',thread_parameters(session,transport.cwd))
        if started['model']!=MODEL or started.get('reasoningEffort')!=session.reasoning_effort or started.get('instructionSources'):
            raise ValueError('Provider startup did not preserve the selected boundary')
        report={'status':'passed','codex_version':SUPPORTED_VERSION,'model':MODEL,'reasoning_effort':session.reasoning_effort,
                'ephemeral':True,'instruction_sources':started.get('instructionSources',[]),
                'dynamic_tools':len(session.tools),'model_turn_started':False,
                'packet_manifest_sha256':hashlib.sha256((args.packet/'manifest.json').read_bytes()).hexdigest(),
                'limitations':['This startup check does not invoke a live model; wire inventory is tested separately against a local fixture',
                               'Independent boundary review remains pending']}
    args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
