# SPDX-License-Identifier: MIT
"""Narrow historical non-weight exception; later evidence is report-only."""
from datetime import datetime, timezone
import base64
from .evidence import timestamp
from .mirror_evidence import (SCHEME, HISTORICAL, HISTORICAL_NOTICE, ROLES,
    digest, git_blob, checked_hex, checked_repo, file_url, mirror_files, fetch,
    reference_path)


def date(row):
    return datetime.fromtimestamp(row['CommittedDate'], timezone.utc).isoformat()


def blobs(rows):
    return {r['Path']:r for r in rows if r['Type']=='blob'}


def recover_proof(official, primary, copies, cutoff):
    if len(copies)<2 or copies[0]['repo']!=primary or len({c['repo'] for c in copies})!=len(copies):
        raise ValueError('Two distinct mirrors, primary first, required')
    snapshots=[]
    for c in copies:
        checked_repo(c['repo']);checked_hex(c['revision'],40)
        rows,_=mirror_files(c['repo'],c['revision'])
        snapshots.append(dict(repo=c['repo'],revision=c['revision'],files=rows))
    current,_=mirror_files(primary)
    old=blobs(snapshots[0]['files']);now=blobs(current)
    mismatches=[]
    for r in official['siblings']:
        path=r['rfilename']
        if not reference_path(path):continue
        row=old.get(path)
        if row is None:raise ValueError('Missing historical reference')
        if path.endswith('.safetensors'):
            if row['Sha256']!=r.get('lfs',{}).get('sha256'):raise ValueError('Historical weight mismatch')
        else:
            data,_=fetch(file_url(primary,row['Revision'],path))
            if digest(data)!=row['Sha256']:raise ValueError('Historical bytes mismatch')
            if r.get('lfs'):
                if digest(data)!=r['lfs']['sha256']:raise ValueError('Historical LFS companion mismatch')
            elif git_blob(data)!=r.get('blobId'):mismatches.append((path,data))
    if len(mismatches)!=1:raise ValueError('Exactly one historical non-weight mismatch required: '+str([p for p,_ in mismatches]))
    path,data=mismatches[0]
    if path not in ROLES:raise ValueError('Historical exception requires non-weight reference')
    witnesses=[]
    for s in snapshots:
        row=blobs(s['files'])[path]
        other,_=fetch(file_url(s['repo'],row['Revision'],path))
        if other!=data or digest(other)!=row['Sha256']:raise ValueError('Mirrors disagree')
        witnesses.append(dict(repo=s['repo'],revision=row['Revision'],snapshot_revision=s['revision'],committed_at=date(row)))
    latest=now[path];later,_=fetch(file_url(primary,latest['Revision'],path))
    if digest(later)!=latest['Sha256']:raise ValueError('Later matching bytes mismatch')
    admin=dict(path=path,shared_blob_id=git_blob(data),content_sha256=digest(data),
               witnesses=witnesses,official=official,snapshots=snapshots,
               later=dict(repo=primary,row=latest,blob_id=git_blob(later)))
    validate_admin(admin,cutoff)
    return admin


def validate_admin(a,cutoff):
    path=a['path'];w=a['witnesses'];official=a['official']
    if path not in ROLES or len(w)<2 or len({x['repo'] for x in w})!=len(w):raise ValueError('Invalid historical witnesses')
    if not official.get('gated') or timestamp(official['createdAt'])>timestamp(cutoff):raise ValueError('Invalid gated identity')
    refs={r['rfilename']:r for r in official['siblings'] if reference_path(r['rfilename'])}
    if not {'config.json','tokenizer_config.json'}<=refs.keys() or not any(p.endswith('.safetensors') for p in refs):raise ValueError('Incomplete reference set')
    expected=checked_hex(refs[path]['blobId'],40)
    if refs[path].get('lfs') or expected==a['shared_blob_id']:raise ValueError('Exception requires differing non-LFS identity')
    checked_hex(a['shared_blob_id'],40);checked_hex(a['content_sha256'],64)
    later=a['later'];row=later['row']
    if later['repo']!=w[0]['repo'] or row['Path']!=path or later['blob_id']!=expected or timestamp(date(row))<=timestamp(cutoff):raise ValueError('Missing later matching copy')
    checked_hex(row['Revision'],40);checked_hex(row['Sha256'],64)
    if len(a['snapshots'])!=len(w):raise ValueError('Missing mirror snapshot')
    for witness,snapshot in zip(w,a['snapshots']):
        checked_repo(witness['repo']);checked_hex(witness['revision'],40);checked_hex(witness['snapshot_revision'],40)
        rows=blobs(snapshot['files']);r=rows[path]
        if snapshot['repo']!=witness['repo'] or snapshot['revision']!=witness['snapshot_revision'] or r['Revision']!=witness['revision'] or date(r)!=witness['committed_at'] or r['Sha256']!=a['content_sha256'] or timestamp(date(r))>timestamp(cutoff):raise ValueError('Historical witness mismatch')
    # All other files are checked at the same primary historical snapshot.
    rows=blobs(a['snapshots'][0]['files'])
    for name,r in refs.items():
        row=rows.get(name)
        if row is None or timestamp(date(row))>timestamp(cutoff):raise ValueError('Missing cutoff-eligible companion')
        if name!=path and (row['Size']!=r['size'] or (r.get('lfs') and row['Sha256']!=r['lfs']['sha256'])):raise ValueError('Companion identity mismatch')


def public_proof(a,repo,historical_repo,created,row,data):
    return dict(scheme=SCHEME,status=HISTORICAL,notice=HISTORICAL_NOTICE,
                official_repo=repo,historical_repo=historical_repo,official_created_at=created,
                path=a['path'],shared_blob_id=git_blob(data),mirror_file_sha256=digest(data),
                file_size=len(data),witnesses=a['witnesses'],identity_verified=False)


def validate_public(e,data,cutoff):
    p=e['mirror_provenance']
    keys={'scheme','status','notice','official_repo','historical_repo','official_created_at','path','shared_blob_id','mirror_file_sha256','file_size','witnesses','identity_verified'}
    if set(p)!=keys or p['scheme']!=SCHEME or p['notice']!=HISTORICAL_NOTICE or p['status']!=HISTORICAL or p['identity_verified'] is not False:raise ValueError('Invalid historical public proof')
    if e['kind']!='hf_file' or e['artifact_role']!='non_weight' or e['path'] not in ROLES or p['path']!=e['path'] or p['official_repo']!=e['repo_id']:raise ValueError('Historical identity/role mismatch')
    checked_repo(p['official_repo']);checked_repo(p['historical_repo'])
    w=p['witnesses']
    if len(w)<2 or len({x['repo'] for x in w})!=len(w):raise ValueError('Distinct mirrors required')
    for x in w:
        if set(x)!={'repo','revision','snapshot_revision','committed_at'}:raise ValueError('Unexpected witness metadata')
        checked_repo(x['repo']);checked_hex(x['revision'],40);checked_hex(x['snapshot_revision'],40)
        if timestamp(x['committed_at'])>timestamp(cutoff):raise ValueError('Future witness')
    if e['url']!=file_url(w[0]['repo'],w[0]['revision'],e['path']) or e['revision_at']!=w[0]['committed_at'] or e['created_at']!=p['official_created_at'] or timestamp(e['created_at'])>timestamp(cutoff):raise ValueError('Historical availability mismatch')
    if len(data)!=p['file_size'] or digest(data)!=p['mirror_file_sha256'] or digest(data)!=e['content_sha256'] or git_blob(data)!=p['shared_blob_id']:raise ValueError('Historical byte mismatch')


def validate_report(report,entries,cutoff):
    special=[e for e in entries if e.get('mirror_provenance',{}).get('status')==HISTORICAL]
    if not special:
        if report.get('status')==HISTORICAL or report.get('historical_identity'):raise ValueError('Missing historical item')
        return
    if len(special)!=1 or report.get('status')!=HISTORICAL:raise ValueError('Historical selection status required')
    a=report['historical_identity'];validate_admin(a,cutoff)
    e=special[0];p=e['mirror_provenance']
    if a['official']['id']!=e['repo_id'] or a['path']!=e['path'] or a['shared_blob_id']!=p['shared_blob_id'] or a['content_sha256']!=e['content_sha256'] or a['witnesses']!=p['witnesses']:raise ValueError('Historical report mismatch')
    refs={r['rfilename']:r for r in a['official']['siblings'] if reference_path(r['rfilename'])}
    if set(refs)!={e['path'] for e in entries}:raise ValueError('Incomplete historical companions')
    rows=blobs(a['snapshots'][0]['files'])
    for e in entries:
        if e['path']==a['path']:continue
        p=e['mirror_provenance'];r=refs[e['path']];row=rows[e['path']]
        expected=r['lfs']['sha256'] if r.get('lfs') else r['blobId']
        if p['official_hash']!=expected or p['mirror_repo']!=a['witnesses'][0]['repo'] or p['mirror_revision']!=row['Revision'] or p['mirror_file_sha256']!=row['Sha256']:raise ValueError('Companion snapshot mismatch')
