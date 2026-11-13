# SPDX-License-Identifier: MIT
"""Recover immutable root paper/HF evidence; weight payloads are never downloaded."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import struct
from urllib.parse import quote, urlsplit
from urllib.error import HTTPError
from urllib.request import Request, build_opener, HTTPRedirectHandler
from .evidence import timestamp

ROOT=Path(__file__).resolve().parents[1]
TASK='543c4b27714c6a677a6e714c452d62532f634cff'
CUTOFF='2025-04-06T12:42:49Z'
MODELS={'llama':'TinyLlama/TinyLlama-1.1B-Chat-v1.0','mistral':'mistralai/Mistral-7B-v0.1',
        'qwen2':'Qwen/Qwen2.5-0.5B','phi3':'microsoft/Phi-3-mini-4k-instruct','gemma2':'unsloth/gemma-2-2b'}
MIRRORS={'gemma2': {'upstream_repo':'google/gemma-2-2b',
                   'reason':'Official repository requires access; user authorized a public mirror.',
                   'equivalence':'Mirror evidence; byte identity with the gated upstream is not verified.'}}
PAPERS={'qtip':('2406.11235v3','2024-10-29T18:55:48Z'),
        'quip-sharp':('2402.04396v2','2024-06-04T04:51:52Z')}
WEIGHTS=('.safetensors','.bin','.pt','.pth','.gguf','.ckpt','.h5','.hdf5','.npz','.npy','.msgpack','.onnx','.ot')


class Redirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        redirected=super().redirect_request(request,fp,code,msg,headers,newurl)
        if redirected and urlsplit(request.full_url).netloc!=urlsplit(newurl).netloc:
            redirected.remove_header('Authorization')
        return redirected


def validate_range(status, content_range, start, end):
    match=re.fullmatch(r'bytes (\d+)-(\d+)/(\d+)',content_range or '')
    if status!=206 or not match or (int(match[1]),int(match[2]))!=(start,end):
        raise ValueError('Server did not honor the exact header-only byte range')


def fetch(url, byte_range=None, limit=32*1024**2, authenticated=False):
    headers={'User-Agent':'exdev-historical-evidence/1','Accept-Encoding':'identity'}
    if authenticated and urlsplit(url).netloc=='huggingface.co':
        token=os.environ.get('HF_TOKEN')
        cached=Path.home()/'.cache/huggingface/token'
        if not token and cached.is_file():token=cached.read_text().strip()
        if token:headers['Authorization']='Bearer '+token
    if byte_range:headers['Range']=f'bytes={byte_range[0]}-{byte_range[1]}'
    try:
        response=build_opener(Redirect()).open(Request(url,headers=headers),timeout=30)
    except HTTPError as error:
        if error.code==401 and not authenticated and urlsplit(url).netloc=='huggingface.co':
            return fetch(url,byte_range,limit,authenticated=True)
        raise
    with response:
        if byte_range:
            validate_range(response.status,response.headers.get('Content-Range'),*byte_range)
            length=byte_range[1]-byte_range[0]+1
            data=response.read(length)
            if len(data)!=length:raise ValueError('Incomplete tensor header range')
        else:
            data=response.read(limit+1)
            if len(data)>limit:raise ValueError('Non-weight evidence exceeds retrieval budget')
        return data,dict(response.headers)


def pages(url):
    while url:
        data,headers=fetch(url)
        yield json.loads(data)
        link=headers.get('Link',headers.get('link',''))
        match=re.search(r'<([^>]+)>;\s*rel="next"',link)
        url=match[1] if match else None
        if url and urlsplit(url).netloc!='huggingface.co':raise ValueError('Unexpected pagination host')


def choose_revision(rows, cutoff=CUTOFF):
    eligible=[row for row in rows if timestamp(row['date'])<=timestamp(cutoff)]
    if not eligible:raise ValueError('No recoverable pre-cutoff revision')
    return max(eligible,key=lambda row:timestamp(row['date']))


class PaperParser(HTMLParser):
    def __init__(self):super().__init__();self.depth=0;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag=='article':self.depth+=1
        if self.depth and tag=='math' and dict(attrs).get('alttext'):
            self.parts.append(dict(attrs)['alttext'])
        if self.depth and tag in ('p','div','section','h1','h2','h3','li'):self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag=='article':self.depth=max(0,self.depth-1)
    def handle_data(self,data):
        if self.depth:self.parts.append(data)


def paper_text(html):
    parser=PaperParser();parser.feed(html)
    return re.sub(r'\n[ \t\n]+','\n',' '.join(parser.parts)).strip()


def item(source_id,url,data,date,**extra):
    entry={'source_id':source_id,'url':url,'kind':'web','created_at':date,'revision_at':date,
           'retrieved_at':datetime.now(timezone.utc).isoformat(),'representation':'pinned_source',
           'content_sha256':hashlib.sha256(data).hexdigest()}
    try:entry['content']=data.decode('utf-8')
    except UnicodeDecodeError:entry['content_base64']=base64.b64encode(data).decode()
    entry.update(extra)
    return entry


def recover_paper(name, cache):
    revision,date=PAPERS[name];url='https://arxiv.org/html/'+revision
    data,_=fetch(url)
    (cache/(name+'.html')).write_bytes(data)
    text=paper_text(data.decode()).encode()
    if len(text)<1000:raise ValueError('Paper article extraction failed')
    return [item('paper:'+name,url,text,date,representation='pinned_html_article_text_with_math_alttext')],{
        'source':name,'revision':revision,'date':date,'raw_sha256':hashlib.sha256(data).hexdigest(),'status':'complete'}


def recover_hf(architecture, cache, repo=None, cutoff=CUTOFF, reference_only=False):
    repo=repo or MODELS[architecture]
    rows=[row for page in pages('https://huggingface.co/api/models/'+repo+'/commits/main') for row in page]
    (cache/(architecture+'-history.json')).write_text(json.dumps(rows,indent=2))
    try:pin=choose_revision(rows,cutoff)
    except ValueError:
        if not reference_only:raise
        return [],{'architecture':architecture,'repo':repo,'status':'no_eligible_revision'}
    sha=pin['id']
    tree=[row for page in pages('https://huggingface.co/api/models/'+repo+'/tree/'+sha+'?recursive=true') for row in page]
    (cache/(architecture+'-tree.json')).write_text(json.dumps(tree,indent=2))
    evidence=[];nonweights=[];headers=[];failures=[]
    for row in tree:
        if row['type']!='file':continue
        path=row['path'];url='https://huggingface.co/'+repo+'/resolve/'+sha+'/'+quote(path)
        try:
            if path.endswith('.safetensors'):
                prefix,_=fetch(url,byte_range=(0,7))
                length=struct.unpack('<Q',prefix)[0]
                if not 2<=length<=4*1024**2:raise ValueError('Tensor header length outside allowed bounds')
                # Distinct query avoids intermediaries incorrectly reusing the first range.
                data,_=fetch(url+'?header=metadata',byte_range=(8,7+length))
                parsed=json.loads(data)
                if not isinstance(parsed,dict):raise ValueError('Invalid tensor header')
                for name,value in parsed.items():
                    if name!='__metadata__' and not {'dtype','shape','data_offsets'}<=set(value):
                        raise ValueError('Invalid tensor metadata')
                data=json.dumps(parsed,sort_keys=True).encode()
                evidence.append(item('hf:'+architecture+':'+path,url,data,pin['date'],kind='safetensors_header',
                                     repo_id=repo,revision=sha,path=path,artifact_role='tensor_header'))
                headers.append(path)
            elif not path.lower().endswith(WEIGHTS) and (not reference_only or Path(path).name in ('config.json','tokenizer_config.json','tokenizer.json','special_tokens_map.json','added_tokens.json','generation_config.json')):
                data,_=fetch(url)
                evidence.append(item('hf:'+architecture+':'+path,url,data,pin['date'],kind='hf_file',
                                     repo_id=repo,revision=sha,path=path,artifact_role='non_weight'))
                nonweights.append(path)
        except Exception as error:
            failures.append({'path':path,'error_type':type(error).__name__,'message':str(error)})
    needed=('config.json','tokenizer_config.json') if reference_only else ('config.json','tokenizer_config.json','tokenizer.json')
    missing=[path for path in needed if path not in nonweights]
    if not headers:missing.append('safetensors headers')
    for entry in evidence:
        if architecture in MIRRORS:entry['mirror_provenance']=MIRRORS[architecture]
    return evidence,{'architecture':architecture,'repo':repo,'revision':sha,'date':pin['date'],
                     **({'mirror_provenance':MIRRORS[architecture]} if architecture in MIRRORS else {}),
                     'non_weight_files':nonweights,'header_files':headers,'failures':failures,'missing':missing,
                     'status':'complete' if not failures and not missing else 'incomplete'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'data/evidence/root')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    jobs=[('paper:'+name,lambda n=name:recover_paper(n,args.output)) for name in PAPERS]
    jobs += [('hf:'+name,lambda n=name:recover_hf(n,args.output)) for name in MODELS]
    items=[];reports=[]
    with ThreadPoolExecutor(max_workers=7) as executor:
        futures=[(name,executor.submit(job)) for name,job in jobs]
        for name,future in futures:
            try:
                evidence,report=future.result();items.extend(evidence)
                (args.output/(name.replace(':','-')+'-evidence.json')).write_text(json.dumps(evidence))
            except Exception as error:
                report={'source':name,'status':'incomplete','error_type':type(error).__name__,'message':str(error)}
            reports.append(report)
            print(json.dumps({'source':name,'status':report['status'],'items':len(items)}),flush=True)
    reference=args.output/'reference-code.json'
    if reference.exists():items.extend(json.loads(reference.read_text())['items'])
    complete=all(report['status']=='complete' for report in reports) and reference.exists()
    bundle={'task_sha':TASK,'cutoff':CUTOFF,'items':items,'complete':complete}
    (args.output/'bundle.json').write_text(json.dumps(bundle))
    summary={'task_sha':TASK,'cutoff':CUTOFF,'status':'complete' if complete else 'incomplete',
             'sources':reports,'evidence_objects':len(items),'reference_code_present':reference.exists(),
             'weight_payload_bytes_downloaded':0}
    (ROOT/'reports/root-evidence-recovery.json').write_text(json.dumps(summary,indent=2)+'\n')


if __name__=='__main__':main()
