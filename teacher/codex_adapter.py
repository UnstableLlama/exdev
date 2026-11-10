# SPDX-License-Identifier: MIT
"""Fresh Codex app-server authoring session, pinned to Astra with task-specific reasoning."""
from copy import deepcopy
import json
from .editorial import output_schema, assemble_draft

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
returned by tools, or ancestor:<sha> for supplied approved ancestor prose. Use basis source for inspection, execution only for a measured
result supported by a successful run, and inference for interpretations. Keep
substantive uncertainty in limitations; do not repeat pipeline bookkeeping.
Use the supplied task_change_sections offsets with git_show to inspect individual
files without paging through binary payloads. For an authoring_task, write exactly one chapter with its assigned id. Fully read
EVERY required_sections byte range and EVERY required_evidence item before writing.
Page until each assigned section or evidence item is complete; repeated prefixes do
not count. git_show.truncated is relative to its section, commit_truncated to the
whole change. Source offsets are bytes; tensor-header offsets are tensor counts.
Coverage validation rejects unread tails. Follow the task focus. Explain mechanisms,
data flow, design tradeoffs and supported alternatives, not just the file layout.
Function-level paper mappings must identify actual functions and distinguish exact
correspondence from analogy. Do not claim source inspection proves measured behavior.
The chapter is a component of one eventual canonical root entry, not the whole root.
State substantive gaps honestly; do not summarize uninspected files as inspected.
Explain the meaning of numerical constants and thresholds, deriving them from
permitted sources where possible. When a claim can be checked with a small bounded
standard-library Python computation, use run and cite the result as execution.
Examples include decoder statistics, indexing/permutation inverses, packing identities,
and shape arithmetic. Inspect the source first; do not manufacture a passing check.
A CPU scalar emulation is not a GPU kernel test. State any material mismatch in
integer overflow, precision or execution environment. If no useful computation is
feasible for the chapter, explain that limitation rather than adding a trivial run.
When chapter_catalog is supplied, use related_chapters for useful cross-references
from that catalog. It is a navigation plan, not evidence about another chapter's prose.
Explain the local side of each interface from source; do not claim to have read
other chapter drafts. Do not use position-dependent wording such as "described below"
in limitations; name the relevant function or mechanism instead.
Every defect observation must state the concrete trigger, expected versus actual
behavior, source location and source evidence. Do not hide unsupported bug claims
in limitations or say features have defects without explaining each one. Keep
limitations for uncertainty and execution scope. In schema v3 put each observation
in findings, as suspected authoring_observation; do not invent a later fix or
introduction. Use source_inspection for source reasoning, scalar_transcription for
checks that reimplement or model inspected code, and repository_execution only
when the repository implementation itself actually ran. A buffer-swap model does
not execute the kernel. Cite inspected source separately from the computation,
describe what ran and its limits, and keep confirmation for administrative review.
The run tool accepts argv ["python3", "-c", "CODE"] and an integer timeout_seconds
from 1 through 20 (default 10). A root task's first-parent checkout is empty.
The links field contains ONLY supplied ancestor commit SHAs, never chapter IDs.
For a root commit links must be []. Chapters are local sections linked by the renderer. Do not invent
ancestor entries or mark an annotation reviewed or training eligible.'''


def thread_parameters(session, cwd):
    return {'model':MODEL,'modelProvider':'openai','allowProviderModelFallback':False,
            'ephemeral':True,'cwd':str(cwd),'runtimeWorkspaceRoots':[],
            'environments':[],'selectedCapabilityRoots':[], 'approvalPolicy':'never',
            'sandbox':'read-only','baseInstructions':session.initial[0]['content'],
            'developerInstructions':INSTRUCTIONS + (RETRIEVAL_INSTRUCTIONS if any(t['name']=='ancestor_read' for t in session.tools) else ''),
            'config':{'model_reasoning_effort':session.reasoning_effort, 'web_search':'disabled',
                      'project_doc_max_bytes':0,
                      'features':{**{name:False for name in DISABLED_FEATURES},
                                  'skip_host_skill_discovery':True,'omit_skill_descriptions':True}},
            'dynamicTools':[{'type':'function','name':tool['name'],
                             'description':tool['description'],'inputSchema':tool['parameters']}
                            for tool in session.tools]}


class CodexTeacher:
    def run(self, session, transport, record=None, max_calls=256):
        session.require_authoring_context()
        if session.used:
            raise ValueError('A fresh authoring session cannot be reused')
        session.used=True
        manifest=json.loads((session.runner.packet/'manifest.json').read_text())
        transcript=deepcopy(session.initial)
        def save():
            if record is not None:
                record(deepcopy(transcript))
        transport.request('initialize',{'clientInfo':{'name':'exdev_teacher','version':'0.1.0'},
                                       'capabilities':{'experimentalApi':True}})
        transport.notify('initialized',{})
        started=transport.request('thread/start',thread_parameters(session,transport.cwd))
        if started['model']!=MODEL or started.get('reasoningEffort')!=session.reasoning_effort:
            raise ValueError('Codex changed the selected model or reasoning effort')
        if started.get('instructionSources'):
            raise ValueError('Unexpected inherited instruction sources')
        thread=started['thread']['id']
        turn=transport.request('turn/start',{'threadId':thread,'model':MODEL,'effort':session.reasoning_effort,
            'environments':[],'runtimeWorkspaceRoots':[], 'outputSchema':output_schema(manifest),
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
                'model':MODEL,'reasoning_effort':session.reasoning_effort}

# Retrieval instructions are appended without changing historical saved prompts.
RETRIEVAL_INSTRUCTIONS = "\nWhen ancestor_read is available, the initial ancestor catalog is navigation only. Page it with mode=catalog and next_offset (byte offsets). Use mode=search with file and/or symbol substrings to find entry and chapter targets; search offsets count grouped entry/chapter targets, newest first. Each target gives match_count and up to three examples. Search results are navigation only. Empty search results do not prove absence of discussion; graph coverage is reported. Read relevant entries or chapters with mode=content; cite that current tool call ID. Old session evidence IDs and catalog pages are not evidence. Follow truncated/next_offset for complete reads. The links field may name only ancestors whose prose you successfully read in this session. For schema 4 include a concise entry-level summary.\n"
