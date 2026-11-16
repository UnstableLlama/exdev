# SPDX-License-Identifier: MIT
"""Curator-only ModelScope retrieval of hash-identical official reference files."""
from datetime import datetime, timezone
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import struct
from urllib.parse import urlencode
from .evidence import timestamp
from .root_evidence import fetch, item

SCHEME = 'modelscope_hash_verified_v1'
HISTORICAL = 'mirror_historical_unverified_identity'
HISTORICAL_NOTICE = 'Pre-cutoff mirror copy; identity with the official file at that date could not be checked because the official history is gated.'
NOTICE = 'Bytes retrieved from a hash-verified ModelScope mirror. Revision identifies the verified file set, not an official Git commit.'
ROLES = {'config.json', 'tokenizer_config.json', 'tokenizer.json',
         'special_tokens_map.json', 'added_tokens.json', 'generation_config.json','preprocessor_config.json','processor_config.json'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def checked_hex(value, length):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{'+str(length)+'}', value):
        raise ValueError('Missing or invalid immutable hash')
    return value


def checked_repo(repo):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid repository identity')
    return repo


def checked_path(path):
    if not isinstance(path, str) or str(PurePosixPath(path)) != path or path.startswith('/') or '..' in PurePosixPath(path).parts:
        raise ValueError('Invalid reference path')
    return path


def reference_path(path):
    return path in ROLES or path.endswith('.safetensors')


def file_url(repo, revision, path):
    checked_repo(repo); checked_hex(revision, 40); checked_path(path)
    return 'https://modelscope.cn/api/v1/models/'+repo+'/repo?'+urlencode({'Revision':revision, 'FilePath':path})


def json_fetch(url):
    data, _ = fetch(url)
    return json.loads(data), data


def mirror_files(repo, revision='master'):
    url = 'https://modelscope.cn/api/v1/models/'+checked_repo(repo)+'/repo/files?'+urlencode({'Revision':revision,'Recursive':'true'})
    obj, raw = json_fetch(url)
    if obj.get('Code') != 200 or not isinstance(obj.get('Data', {}).get('Files'), list):
        raise ValueError('Incomplete ModelScope file listing')
    return obj['Data']['Files'], raw


def file_set_revision(entries):
    rows = sorted((e['path'], e['content_sha256'], e['mirror_provenance']) for e in entries)
    return digest(json.dumps(rows, sort_keys=True, separators=(',', ':')).encode())


def validate_item(entry, data, cutoff):
    p = entry['mirror_provenance']
    if p.get('status') == HISTORICAL:
        from .historical_mirror import validate_public
        return validate_public(entry, data, cutoff)
    if p.get('scheme') != SCHEME or p.get('notice') != NOTICE:
        raise ValueError('Invalid mirror provenance')
    if p['official_repo'] != entry['repo_id'] or p['path'] != entry['path']:
        raise ValueError('Mirror identity mismatch')
    checked_repo(p['official_repo']); checked_repo(p['historical_repo'])
    checked_hex(p['official_metadata_sha256'], 64); checked_hex(p['mirror_listing_sha256'], 64)
    checked_hex(p['official_revision'], 40)
    if entry['url'] != file_url(p['mirror_repo'], p['mirror_revision'], p['path']):
        raise ValueError('Mirror URL is not pinned')
    for date in (p['official_created_at'], p['mirror_committed_at']):
        if timestamp(date) > timestamp(cutoff):raise ValueError('Mirror evidence exceeds cutoff')
    if entry['created_at'] != p['official_created_at'] or entry['revision_at'] != p['mirror_committed_at']:
        raise ValueError('Mirror availability mismatch')
    if digest(data) != entry['content_sha256']:raise ValueError('Mirror content checksum mismatch')
    if p['identity_verified'] is not True or p['official_hash'] != p['mirror_hash']:
        raise ValueError('Mirror file identity mismatch')
    checked_hex(p['mirror_file_sha256'], 64)
    if p['hash_algorithm'] == 'git_blob_sha1':
        checked_hex(p['official_hash'], 40)
        if entry['kind'] != 'hf_file' or git_blob(data) != p['official_hash']:
            raise ValueError('Git blob identity mismatch')
    elif p['hash_algorithm'] == 'sha256':
        checked_hex(p['official_hash'], 64)
        if p['official_hash'] != p['mirror_file_sha256']:raise ValueError('Whole-file SHA mismatch')
    else:raise ValueError('Unknown identity algorithm')
    if entry['kind'] == 'hf_file':
        if entry['path'] not in ROLES or len(data) != p['file_size'] or digest(data) != p['mirror_file_sha256']:
            raise ValueError('Reference file mismatch')
    elif entry['kind'] == 'safetensors_header':
        if not entry['path'].endswith('.safetensors') or p['hash_algorithm'] != 'sha256':raise ValueError('Invalid header identity')
        if not 2 <= len(data) <= 4*1024**2 or p.get('ranges') != [[0,7],[8,7+len(data)]] or 8+len(data) > p['file_size']:
            raise ValueError('Invalid header ranges')
        header = json.loads(data)
        if not isinstance(header, dict) or not header:raise ValueError('Invalid tensor header')
        for name, value in header.items():
            if name != '__metadata__' and (not isinstance(value, dict) or set(value) != {'dtype','shape','data_offsets'}):
                raise ValueError('Only tensor metadata allowed')
    else:raise ValueError('Invalid mirror artifact role')


def validate_selection(report, entries, cutoff):
    if report.get('retrieval_source') != SCHEME:return
    if not entries or any(e.get('mirror_provenance', {}).get('scheme') != SCHEME for e in entries):
        raise ValueError('Missing mirror file proofs')
    for e in entries:
        data = base64.b64decode(e['content_base64'], validate=True) if 'content_base64' in e else e['content'].encode()
        validate_item(e, data, cutoff)
    from .historical_mirror import validate_report
    validate_report(report, entries, cutoff)
    revision = file_set_revision(entries)
    if report['revision'] != revision or any(e['revision'] != revision for e in entries):
        raise ValueError('Mirror file-set revision mismatch')
    if report['date'] != max((e['revision_at'] for e in entries), key=timestamp):raise ValueError('Mirror selection date mismatch')
    if sorted(e['path'] for e in entries) != report['verified_files'] or len(set(e['path'] for e in entries)) != len(entries):
        raise ValueError('Incomplete mirror selection')


def recover_modelscope(architecture, cache, *, repo, mirror_repo, historical_repo, cutoff, historical_copies=None):
    """Use current official hashes only as identity; date bytes by mirror file commit."""
    checked_repo(repo); checked_repo(mirror_repo); checked_repo(historical_repo)
    cache = Path(cache); cache.mkdir(parents=True, exist_ok=True)
    official, official_raw = json_fetch('https://huggingface.co/api/models/'+repo+'?blobs=true')
    if official.get('id') != repo or not official.get('gated'):
        raise ValueError('Expected an explicitly selected gated official repository')
    checked_hex(official['sha'], 40)
    if timestamp(official['createdAt']) > timestamp(cutoff):raise ValueError('Official repository exceeds cutoff')
    admin = None
    if historical_copies:
        from .historical_mirror import recover_proof
        admin = recover_proof(official, mirror_repo, historical_copies, cutoff)
    rows, mirror_raw = mirror_files(mirror_repo, historical_copies[0]['revision']) if admin else mirror_files(mirror_repo)
    (cache/'official-metadata.json').write_bytes(official_raw)
    (cache/'mirror-files.json').write_bytes(mirror_raw)
    sources = {r['Path']:r for r in rows if r['Type'] == 'blob'}
    wanted = [r for r in official['siblings'] if reference_path(checked_path(r['rfilename']))]
    if not {'config.json','tokenizer_config.json'} <= {r['rfilename'] for r in wanted} or not any(r['rfilename'].endswith('.safetensors') for r in wanted):
        raise ValueError('Official reference roles incomplete')
    entries = []
    for r in wanted:
        path = r['rfilename']
        if path not in sources:raise ValueError('Mirror missing published reference: '+path)
        row = sources[path]
        date = datetime.fromtimestamp(row['CommittedDate'], timezone.utc).isoformat()
        if timestamp(date) > timestamp(cutoff):raise ValueError('Mirror file exceeds cutoff: '+path)
        special = admin is not None and path == admin['path']
        if not special and row['Size'] != r['size']:raise ValueError('Mirror size mismatch: '+path)
        full_sha = checked_hex(row['Sha256'], 64)
        proof = dict(scheme=SCHEME, notice=NOTICE, official_repo=repo, historical_repo=historical_repo,
                     official_created_at=official['createdAt'], official_revision=official['sha'],
                     official_metadata_sha256=digest(official_raw), mirror_listing_sha256=digest(mirror_raw),
                     mirror_repo=mirror_repo, mirror_revision=checked_hex(row['Revision'],40),
                     mirror_committed_at=date, path=path, file_size=row['Size'], mirror_file_sha256=full_sha,
                     identity_verified=True)
        url = file_url(mirror_repo, row['Revision'], path)
        lfs = r.get('lfs')
        if special and lfs:raise ValueError('Historical exception cannot use LFS')
        if lfs:
            proof.update(hash_algorithm='sha256',official_hash=checked_hex(lfs['sha256'],64),mirror_hash=full_sha)
            if proof['official_hash'] != full_sha:raise ValueError('Mirror SHA mismatch: '+path)
        if path.endswith('.safetensors'):
            if not lfs:raise ValueError('No published full-file SHA for tensor file')
            prefix, _ = fetch(url, byte_range=(0,7))
            length = struct.unpack('<Q',prefix)[0]
            if not 2 <= length <= 4*1024**2 or 8+length > row['Size']:raise ValueError('Invalid header length')
            data, _ = fetch(url+'&header=metadata', byte_range=(8,7+length))
            proof['ranges'] = [[0,7],[8,7+length]]
            kind, role = 'safetensors_header','tensor_header'
        else:
            data, _ = fetch(url)
            if digest(data) != full_sha:raise ValueError('Mirror downloaded bytes mismatch: '+path)
            if not lfs:proof.update(hash_algorithm='git_blob_sha1',official_hash=checked_hex(r['blobId'],40),mirror_hash=git_blob(data))
            kind, role = 'hf_file','non_weight'
        if special:
            from .historical_mirror import public_proof
            proof = public_proof(admin, repo, historical_repo, official['createdAt'], row, data)
        e = item('hf:'+architecture+':'+path,url,data,date,kind=kind,artifact_role=role,repo_id=repo,
                 path=path,created_at=official['createdAt'],representation=HISTORICAL if special else 'hash_verified_mirror_file',mirror_provenance=proof)
        validate_item(e,data,cutoff);entries.append(e)
    revision = file_set_revision(entries)
    for e in entries:e['revision'] = revision
    report = dict(architecture=architecture,repo=repo,revision=revision,date=max((e['revision_at'] for e in entries),key=timestamp),
                  status='complete',retrieval_source=SCHEME,verified_files=sorted(e['path'] for e in entries),
                  failures=[],missing=[],weight_payload_bytes_downloaded=0,
                  identity_limit='Full weight SHA equality is from both services metadata; only header bytes were downloaded, not whole weights hashed locally.')
    if admin:
        report.update(status=HISTORICAL, historical_identity=admin)
    validate_selection(report,entries,cutoff)
    return entries,report
