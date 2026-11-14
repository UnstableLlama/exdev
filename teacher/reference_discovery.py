# SPDX-License-Identifier: MIT
"""Administrative reference discovery by pinned architecture, never model name."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from .root_evidence import pages, fetch, choose_revision


def discover(organization, architecture, cutoff, workers=6):
    url='https://huggingface.co/api/models?'+urlencode({'author':organization,'limit':100})
    models=sorted({row['id'] for page in pages(url) for row in page})
    def inspect(repo):
        row={'repo':repo}
        try:
            history=[r for page in pages('https://huggingface.co/api/models/'+repo+'/commits/main') for r in page]
            try: pin=choose_revision(history,cutoff)
            except ValueError:
                return dict(row,status='no_eligible_revision')
            row.update(revision=pin['id'],revision_date=pin['date'])
            config=json.loads(fetch('https://huggingface.co/'+repo+'/resolve/'+pin['id']+'/config.json')[0])
            architectures=config.get('architectures',[])
            if not isinstance(architectures,list) or not all(isinstance(x,str) for x in architectures):
                raise ValueError('Invalid architectures field')
            return dict(row,status='inspected_pinned_config',architectures=architectures,matched=architecture in architectures)
        except HTTPError as error:
            return dict(row,status='unavailable',http_status=error.code,reason=str(error))
        except Exception as error:
            return dict(row,status='unavailable',error_type=type(error).__name__,reason=str(error))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        candidates=list(pool.map(inspect,models))
    unavailable=[r['repo'] for r in candidates if r['status']=='unavailable']
    report=dict(organization=organization,architecture=architecture,cutoff=cutoff,enumeration_url=url,
                enumerated_repositories=models,candidates=candidates,unavailable=unavailable,
                complete=not unavailable,basis='All currently visible official repositories, all history pages, latest pre-cutoff config; no repository-name filter. Deleted/private repositories cannot be enumerated.')
    # Selection metadata is administrative but keep even candidate names cutoff-grounded.
    considered=[r['repo'] for r in candidates if r['status']=='inspected_pinned_config']
    selection=[dict(architecture=architecture,repo=r['repo'],reason='Official repository whose latest pre-cutoff config declares the registered architecture; no name filter.',candidates_considered=considered)
               for r in candidates if r.get('matched')]
    return report,selection


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('organization','architecture','cutoff','report','selection'):p.add_argument('--'+name,required=True)
    a=p.parse_args();report,selection=discover(a.organization,a.architecture,a.cutoff)
    for path,data in ((a.report,report),(a.selection,selection)):
        target=Path(path)
        if target.exists():raise ValueError('Use new discovery output paths')
        target.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(enumerated=len(report['candidates']),selected=len(selection),unavailable=len(report['unavailable']))))


if __name__=='__main__':main()
