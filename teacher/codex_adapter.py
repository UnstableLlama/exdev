# SPDX-License-Identifier: MIT
"""Fresh Codex app-server authoring session, pinned to Astra with medium reasoning."""
from copy import deepcopy
import json
from .editorial import SCHEMA, assemble_draft

MODEL = 'gpt-6-astra'
EFFORT = 'medium'
DISABLED_FEATURES = (
    'apps','plugins','hooks','shell_tool','unified_exec','shell_snapshot','shell_snapshot_v2',
    'browser_use','browser_use_external','computer_use','in_app_browser','view_image',
    'multi_agent','multi_agent_v2','goals','sleep_tool','skill_search','skill_mcp_dependency_install',
    'external_agent_memory_import','code_mode','code_mode_host','js_repl','tool_suggest',
)
INSTRUCTIONS = '''Return one JSON annotation matching the supplied editorial schema.
Use only the provided historical tools. Cite each claim using evidence_id values
returned by tools. Use basis source for inspection, execution only for a measured
result supported by a successful run, and inference for interpretations. Keep
substantive uncertainty in limitations; do not repeat pipeline bookkeeping.
The canonical root entry may contain linked subsystem chapters. Do not invent
ancestor entries or mark an annotation reviewed or training eligible.'''


def thread_parameters(session, cwd):
    return {'model':MODEL,'modelProvider':'openai','allowProviderModelFallback':False,
            'ephemeral':True,'cwd':str(cwd),'runtimeWorkspaceRoots':[],
            'environments':[],'selectedCapabilityRoots':[], 'approvalPolicy':'never',
            'sandbox':'read-only','baseInstructions':session.initial[0]['content'],
            'developerInstructions':INSTRUCTIONS,
            'config':{'model_reasoning_effort':EFFORT, 'web_search':'disabled',
                      'project_doc_max_bytes':0,
                      'features':{**{name:False for name in DISABLED_FEATURES},
                                  'skip_host_skill_discovery':True,'omit_skill_descriptions':True}},
            'dynamicTools':[{'type':'function','name':tool['name'],
                             'description':tool['description'],'inputSchema':tool['parameters']}
                            for tool in session.tools]}


class CodexTeacher:
    def run(self, session, transport, record=None, max_calls=256):
        if session.used:
            raise ValueError('A fresh authoring session cannot be reused')
        session.used=True
        transcript=deepcopy(session.initial)
        def save():
            if record is not None:
                record(deepcopy(transcript))
        transport.request('initialize',{'clientInfo':{'name':'exdev_teacher','version':'0.1.0'},
                                       'capabilities':{'experimentalApi':True}})
        transport.notify('initialized',{})
        started=transport.request('thread/start',thread_parameters(session,transport.cwd))
        if started['model']!=MODEL or started.get('reasoningEffort')!=EFFORT:
            raise ValueError('Codex changed the selected model or reasoning effort')
        if started.get('instructionSources'):
            raise ValueError('Unexpected inherited instruction sources')
        thread=started['thread']['id']
        turn=transport.request('turn/start',{'threadId':thread,'model':MODEL,'effort':EFFORT,
            'environments':[],'runtimeWorkspaceRoots':[], 'outputSchema':SCHEMA,
            'input':[{'type':'text','text':session.initial[1]['content']}]})['turn']['id']
        allowed={tool['name'] for tool in session.tools}
        seen=set(); final=None
        save()
        while True:
            event=transport.receive()
            method=event.get('method','')
            params=event.get('params',{})
            if params.get('threadId',thread)!=thread or params.get('turnId',turn)!=turn:
                raise ValueError('Foreign thread or turn event')
            if 'id' in event:
                if method!='item/tool/call':
                    raise ValueError('Unexpected server request; approvals are not permitted')
                name=params['tool']; identity=params['callId']
                if name not in allowed or params.get('namespace') not in (None,''):
                    raise ValueError('Unapproved model tool')
                if identity in seen or len(seen)>=max_calls:
                    raise ValueError('Duplicate tool call or tool budget exceeded')
                seen.add(identity)
                call={'id':identity,'tool':name,'arguments':params['arguments']}
                transcript.append({'role':'assistant','calls':[call]})
                try:
                    result=session.runner.invoke(name,params['arguments'])
                except (ValueError,RuntimeError) as exc:
                    result={'ok':False,'error':str(exc)}
                transcript.append({'role':'tool','name':name,'call_id':identity,'content':json.dumps(result)})
                save()
                transport.reply(event['id'],{'success':result['ok'], 'contentItems':[
                    {'type':'inputText','text':json.dumps(dict(result,evidence_id=identity))}]})
            elif method in ('item/started','item/completed'):
                item=params['item']; kind=item['type']
                if kind not in ('userMessage','agentMessage','reasoning','dynamicToolCall'):
                    raise ValueError('Unexpected native tool or context event: '+kind)
                if kind=='dynamicToolCall' and item.get('tool') not in allowed:
                    raise ValueError('Unapproved tool event')
                if method=='item/completed' and kind=='agentMessage':
                    transcript.append({'role':'assistant','content':item['text']})
                    save()  # Preserve raw model text even if JSON/schema validation later fails.
                    if item.get('phase') in (None,'final_answer'):
                        final=item['text']
            elif method=='turn/completed':
                if params['turn']['id']!=turn or params['turn']['status']!='completed' or final is None:
                    raise ValueError('Authoring turn did not complete successfully')
                break
            elif method=='error':
                raise ValueError('Codex reported an authoring error')
        manifest=json.loads((session.runner.packet/'manifest.json').read_text())
        annotation=json.loads(final)
        entry, review=assemble_draft(annotation,manifest,transcript)
        return {'draft':entry,'review':review,'transcript':transcript,'published':False,
                'model':MODEL,'reasoning_effort':EFFORT}
