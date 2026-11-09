# SPDX-License-Identifier: MIT
"""Evaluate the conservative binding pass against existing validation snapshots."""
import io
import json
from pathlib import Path
import subprocess
import tarfile
from collections import Counter
from .bindings import supplement
from .validate import ROOT, OUT


def source_files(sha):
    archive=subprocess.check_output(['git','--git-dir='+str(ROOT/'.sources/exllamav3.git'),'archive',sha])
    files={}
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        for member in tar:
            if member.isfile() and member.name.endswith(('.py','.cpp','.cc','.cu')):
                files[member.name]=tar.extractfile(member).read().decode('utf-8',errors='replace')
    return files


def main():
    summary=[]
    for p in sorted(OUT.glob('*/result.json')):
        snapshot=json.loads(p.read_text())
        result=supplement(snapshot,source_files(snapshot['sha']))
        target=p.parent/'bindings-v1.json'
        target.write_text(json.dumps(result,indent=2)+'\n')
        summary.append(dict(sha=snapshot['sha'],position=snapshot['position'],
                            added_edges=len(result['edges']),call_sites=dict(Counter(s['status'] for s in result['sites'])),
                            parse_errors=result['parse_errors']))
        print(snapshot['position'],len(result['edges']),dict(Counter(s['status'] for s in result['sites'])),flush=True)
    (ROOT/'reports/bindings-v1.json').write_text(json.dumps(sorted(summary,key=lambda s:s['position']),indent=2)+'\n')

if __name__=='__main__':main()
