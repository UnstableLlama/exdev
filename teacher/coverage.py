# SPDX-License-Identifier: MIT
"""Enforce full byte-range reads of assigned source sections and external evidence."""
import base64
import json


def covered(ranges, start, end):
    cursor=start
    for left,right in sorted(ranges):
        if right<=cursor:continue
        if left>cursor:return False
        cursor=max(cursor,right)
        if cursor>=end:return True
    return cursor>=end


def observed_reads(transcript):
    calls={};reads=[]
    for message in transcript:
        if message['role']=='assistant':
            for call in message.get('calls',[]):calls[call['id']]=call
        if message['role']!='tool':continue
        call=calls.get(message['call_id']);response=json.loads(message['content'])
        if not call or call['tool']!=message['name'] or not response.get('ok'):continue
        result=response.get('result',{})
        if call['tool'] not in ('git_show','web_fetch','hf_fetch'):continue
        if result.get('encoding')=='base64':
            data=base64.b64decode(result['base64'],validate=True)
        elif result.get('encoding')=='utf-8':
            data=result['text'].encode()
        else:continue
        start=call['arguments'].get('offset',0)
        if result.get('offset')!=start or result.get('next_offset')!=start+len(data):
            raise ValueError('Read metadata does not match returned bytes')
        reads.append((call['tool'],call['arguments'],start,start+len(data)))
    return reads


def require_coverage(manifest, transcript):
    task=manifest.get('authoring_task')
    if not task:return None  # Old drafts remain inspectable, never silently upgraded.
    reads=observed_reads(transcript)
    code_ranges=[(start,end) for tool,args,start,end in reads if tool=='git_show' and args['commit']==manifest['task_sha']]
    complete=[];missing=[]
    for index in task['required_sections']:
        section=manifest['task_change_sections'][index]
        if covered(code_ranges,section['offset'],section['offset']+section['bytes']):complete.append(index)
        else:missing.append(section['header'])
    evidence_complete=[]
    for source_id in task['required_evidence']:
        item=next((e for e in manifest['evidence'] if e['source_id']==source_id),None)
        if item is None:raise ValueError('Assigned external evidence missing from packet: '+source_id)
        ranges=[]
        for tool,args,start,end in reads:
            if item['kind']=='web' and tool=='web_fetch' and args['url']==item['url']:
                ranges.append((start,end))
            elif item['kind']=='hf_file' and tool=='hf_fetch' and all(args[k]==item[k] for k in ('repo_id','revision','path')):
                ranges.append((start,end))
        if item['kind']=='safetensors_header':
            # Header results are paginated by tensor names, rather than raw byte ranges.
            calls={c['id']:c for m in transcript if m['role']=='assistant' for c in m.get('calls',[])}
            for m in transcript:
                if m['role']!='tool' or m['name']!='safetensors_header':continue
                call=calls.get(m['call_id']);r=json.loads(m['content'])
                if call and r.get('ok') and all(call['arguments'].get(k)==item[k] for k in ('repo_id','revision','path')):
                    offset=call['arguments'].get('offset',0)
                    ranges.append((offset,offset+len(r['result']['header'])))
            length=item['tensor_count']
        else:length=item['content_bytes']
        if covered(ranges,0,length):evidence_complete.append(source_id)
        else:missing.append(source_id)
    if missing:raise ValueError('Required evidence not fully read: '+', '.join(missing))
    report={'fully_read_sections':complete,'fully_read_evidence':evidence_complete,'policy':'complete_assigned_ranges'}
    if task.get('execution_required'):
        calls={c['id']:c for m in transcript if m['role']=='assistant' for c in m.get('calls',[])}
        successful=[]
        for m in transcript:
            if m['role']!='tool' or m['name']!='run' or calls.get(m['call_id'],{}).get('tool')!='run':continue
            result=json.loads(m['content'])
            if result.get('ok') and result.get('result',{}).get('returncode')==0 and not result['result'].get('timed_out',False):
                successful.append(m['call_id'])
        if not successful:raise ValueError('Assigned computation requires a successful run')
        report['successful_required_runs']=successful
    return report
