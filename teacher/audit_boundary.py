# SPDX-License-Identifier: MIT
"""Administrative end-to-end checks on prepared real historical packets; no model authoring."""
import hashlib
import json
from pathlib import Path
from .runner import Runner

ROOT=Path(__file__).resolve().parents[1]


def main():
    checks=[]
    for position in (9,10):
        packet=ROOT/f'.teacher/{position:06d}'
        manifest=json.loads((packet/'manifest.json').read_text())
        runner=Runner(packet)
        parent=manifest['base_commit'];task=manifest['task_sha']
        calls=[('repo_read',dict(commit=parent,path='setup.py')),
               ('repo_list',dict(commit=parent,path='exllamav3')),
               ('repo_grep',dict(commit=parent,path='setup.py',query='path')),
               ('git_show',dict(commit=task)),('git_log',dict(path='setup.py')),
               ('web_fetch',dict(url='https://github.com/turboderp-org/exllamav3/issues/2')),
               ('run',dict(argv=['python3','-c','import ast; ast.parse(open("setup.py").read()); print("parent setup.py parsed")']))]
        for name,args in calls:
            result=runner.invoke(name,args)
            if not result['ok']:raise ValueError((position,name,result))
            if name=='run' and result['result']['returncode']!=0:raise ValueError(result)
            checks.append(dict(position=position,tool=name,passed=True,
                               result_sha256=hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest()))
        for name,args in [('repo_read',dict(commit=parent,path='../../astra-review.md')),
                          ('repo_read',dict(commit=task,path='setup.py')),
                          ('repo_list',dict(commit='bd1f519172406a9560bd5c90e61000691bb69a07')),
                          ('web_fetch',dict(url='https://example.com/not-approved')),
                          ('hf_fetch',dict(repo_id='org/not-approved',revision='a'*40,path='config.json')),
                          ('safetensors_header',dict(repo_id='org/not-approved',revision='a'*40,path='model.safetensors'))]:
            result=runner.invoke(name,args)
            if result['ok']:raise ValueError('Boundary unexpectedly allowed request: '+name)
            checks.append(dict(position=position,tool=name,denial_verified=True))
    report=dict(status='passed',purpose='administrative_boundary_validation',checks=checks,
                live_model_invoked=False,entries_rewritten=0,training_trace_dry_run=False,
                runtime='Linux amd64 Bubblewrap; Python stdlib only; no network; single-process run',
                limitations=['Provider-neutral driver has no live model adapter yet',
                             'No GPU or third-party Python dependency profile',
                             'HF and header tools require curator-approved pinned cache objects',
                             'Graph tools are not attached to this authoring runner yet',
                             'Independent boundary review and editorial schema revision remain required'])
    (ROOT/'reports/teacher-boundary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))


if __name__=='__main__':main()
