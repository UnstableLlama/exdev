# SPDX-License-Identifier: MIT
"""Validator-only, one-turn repair audit shared by publication and approval."""
import hashlib
import json
from .editorial import assemble_draft

POLICY = 'validator-only-v1'

# Explicit annotation refusals only; internal integrity failures are terminal.
ANNOTATION_ERRORS = frozenset(['Duplicate ancestor link', 'Links require approved, supplied ancestor prose', 'Chapter output does not match assigned subsystem', 'Duplicate chapter ID', 'Duplicate chapter reference', 'Claims, including inferences, need evidence anchors', 'Duplicate evidence anchor', 'Duplicate finding evidence', 'Findings require successful current-session evidence', 'Duplicate finding ID', 'Findings require inspected source evidence', 'Ancestor links require a successful nonempty prose read in this session', 'Unknown or unsuccessful evidence call', 'Ancestor-only claims require basis ancestor', 'Ancestor basis requires ancestor prose evidence', 'Execution claims require successful run evidence', 'Finding locations require repository-relative paths', 'Source inspection requires source evidence', 'Computational verification requires successful run evidence'])
SHAPE_ERRORS = (': wrong type', ': incorrect version', ': unknown value',
                ': missing or protected fields', ': invalid number of items',
                ': invalid length', ': invalid format')

def eligible(error):
    message=str(error)
    return (type(error) is json.JSONDecodeError or type(error) is ValueError and (
        message in ANNOTATION_ERRORS or
        (message.startswith('Exceeds the limit (') and
         ' digits) for integer string conversion: value has ' in message and
         message.endswith(' digits; use sys.set_int_max_str_digits() to increase the limit')) or
        message == 'Assigned computation requires a successful run' or
        message.startswith('Required evidence not fully read: ') or
        message.startswith('annotation') and message.endswith(SHAPE_ERRORS)))



def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def repair_metadata(transcript):
    events=[m for m in transcript if m.get('role')=='validation']
    if not events:
        return {'validation_repair_policy':POLICY, 'validation_repair':False}
    if len(events)!=1:
        raise ValueError('Exactly one validation refusal is permitted')
    event=events[0]
    return {'validation_repair_policy':POLICY, 'validation_repair':event['feedback_sent'],
            'validation_repair_refused_sha256':event['refused_sha256'],
            'validation_repair_input_sha256':digest(event['error']),
            'validation_repair_selected_final_index':event['selected_final_index']}


def verify_final(annotation, manifest, transcript, provenance):
    """Historical unmarked runs retain their path; marked repairs fail closed."""
    events=[(i,m) for i,m in enumerate(transcript) if m.get('role')=='validation']
    marked='validation_repair_policy' in provenance or 'validation_repair' in provenance
    if not events:
        if marked and type(provenance.get('validation_repair')) is not bool:
            raise ValueError('Validation repair must be a boolean')
        if marked and provenance != {**provenance, **repair_metadata(transcript)}:
            raise ValueError('Validation repair provenance mismatch')
        if marked and (('validation_repair_enabled' in provenance and
                        type(provenance['validation_repair_enabled']) is not bool) or
                       any(k.startswith('validation_repair_') and k not in
                           ('validation_repair_policy', 'validation_repair_enabled')
                           for k in provenance)):
            raise ValueError('Unexpected repair provenance on unrepaired run')
        return assemble_draft(annotation, manifest, transcript)
    if not marked or type(provenance.get('validation_repair')) is not bool or len(events)!=1:
        raise ValueError('Missing or ambiguous validation repair provenance')
    if provenance.get('validation_repair_enabled') is False:
        raise ValueError('Validation repair was disabled for this run')
    i,event=events[0]
    keys={'role','policy','refused_index','prefix_end','refused_sha256','error_type','error',
          'thread_id','first_turn_id','repair_turn_id','selected_final_index','feedback_sent'}
    if set(event)!=keys or event['policy']!=POLICY or event['feedback_sent'] is not True:
        raise ValueError('Invalid validation repair event')
    refused=event['refused_index']; chosen=event['selected_final_index']
    if (type(refused) is not int or type(chosen) is not int or event['prefix_end']!=i
            or not 0<=refused<i<i+1<chosen<len(transcript)
            or any(not isinstance(event[k],str) or not event[k] for k in
                   ('thread_id','first_turn_id','repair_turn_id'))
            or event['first_turn_id']==event['repair_turn_id']
            or any(m.get('role')=='assistant' and 'content' in m for m in transcript[refused+1:i])):
        raise ValueError('Invalid repair ordering or turn identity')
    original=transcript[refused]
    if (set(original)!={'role','content'} or original['role']!='assistant'
            or digest(original['content'])!=event['refused_sha256']):
        raise ValueError('Refused annotation fingerprint mismatch')
    if transcript[i+1]!={'role':'user','content':event['error']}:
        raise ValueError('Repair feedback must equal the verbatim validator error')
    for message in transcript[i+2:]:
        if message.get('turn_id')!=event['repair_turn_id'] or message.get('role') not in ('assistant','tool'):
            raise ValueError('Unexpected message or turn in repair transcript')
        allowed=({'role','turn_id','calls'} if 'calls' in message else
                 {'role','turn_id','content'} if message['role']=='assistant' else
                 {'role','turn_id','name','call_id','content'})
        if set(message)!=allowed:
            raise ValueError('Unexpected repair message fields')
    selected=transcript[chosen]
    if (selected.get('role')!='assistant' or 'content' not in selected
            or chosen!=len(transcript)-1):
        raise ValueError('Ambiguous repaired final selection')
    metadata=repair_metadata(transcript)
    if any(provenance.get(k)!=v for k,v in metadata.items()):
        raise ValueError('Validation repair provenance mismatch')
    # Reproduce the refusal against ONLY evidence available at that first final.
    try:
        assemble_draft(json.loads(original['content']),manifest,transcript[:i])
    except ValueError as error:
        if not eligible(error) or type(error).__name__!=event['error_type'] or str(error)!=event['error']:
            raise ValueError('Recorded validation refusal does not reproduce') from error
    else:
        raise ValueError('Recorded refused annotation was valid')
    final=json.loads(selected['content'])
    if final!=annotation:
        raise ValueError('Published annotation differs from selected repaired final')
    return assemble_draft(final,manifest,transcript)


def disclosure(transcript):
    """Administrative request/report fields; never supplied as historical evidence."""
    result=repair_metadata(transcript)
    if result['validation_repair']:
        event=next(m for m in transcript if m.get('role')=='validation')
        boundary=event['prefix_end']
        counts=[sum(len(m.get('calls',[])) for m in part if m.get('role')=='assistant')
                for part in (transcript[:boundary],transcript[boundary+2:])]
        result.update(validator_message=event['error'],repair_count=1,
                      tool_calls_by_turn=counts,tool_calls_total=sum(counts))
    return result
