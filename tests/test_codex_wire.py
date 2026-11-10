# SPDX-License-Identifier: MIT
"""Local fake provider only: no real credential, model output or corpus generation."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import base64
import hashlib
import struct
import os
from pathlib import Path
import threading
import unittest
from unittest.mock import patch
from teacher.codex_adapter import CodexTeacher
from teacher.codex_transport import CodexTransport, configuration
from teacher.session import FreshSession
import test_teacher_packet
import test_ancestor_context
from teacher.ancestor_context import approve_run, attach_entries
import test_teacher_graph


@unittest.skipUnless(os.environ.get('EXDEV_SANDBOX_TESTS')=='1','Host namespace and loopback integration test')
class CodexWireTests(unittest.TestCase):
    def setUp(self):
        test_teacher_packet.PacketTests.setUp(self)
        run,source=test_ancestor_context.AncestorContextTests.run_fixture(self)
        approve_run(run,source,'TEST REVIEWER','ADMIN_REVIEW_SECRET')
        attach_entries(self.packet,[run])
    tearDown=test_teacher_packet.PacketTests.tearDown

    def test_actual_codex_request_has_only_approved_tools_and_no_inherited_context(self):
        self.exercise_wire()

    def test_retrieval_wire_has_citable_content_and_fifteen_tools(self):
        self.exercise_wire(retrieval=True)

    def exercise_wire(self, retrieval=False):
        test_teacher_graph.GraphPacketTests.prepare(self)
        if retrieval:
            path=self.packet/'manifest.json';manifest=json.loads(path.read_text())
            manifest.update(ancestor_context_mode='retrieval_v1',editorial_schema_version=4)
            manifest.pop('ancestor_context_complete');manifest['ancestor_entries']=[]
            path.write_text(json.dumps(manifest))
            attach_entries(self.packet,[self.root/('run-'+self.first)])
        captured=[]
        task=self.task
        first=self.first
        expected_tool='ancestor_read' if retrieval else 'git_show'
        class Handler(BaseHTTPRequestHandler):
            protocol_version="HTTP/1.1"
            def log_message(self,*args):pass
            def do_GET(self):
                if self.headers.get('Upgrade','').lower()!='websocket':
                    self.send_error(404);return
                accept=base64.b64encode(hashlib.sha1((self.headers['Sec-WebSocket-Key']+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()).decode()
                self.send_response(101);self.send_header('Upgrade','websocket')
                self.send_header('Connection','Upgrade');self.send_header('Sec-WebSocket-Accept',accept);self.end_headers()
                self.connection.settimeout(5)
                for _ in range(4):
                    head=self.rfile.read(2)
                    if len(head)!=2:return
                    first,second=head
                    if first&15==8:return
                    length=second&127
                    if length==126:length=struct.unpack('!H',self.rfile.read(2))[0]
                    elif length==127:length=struct.unpack('!Q',self.rfile.read(8))[0]
                    mask=self.rfile.read(4) if second&128 else b''
                    body=self.rfile.read(length)
                    if mask:body=bytes(c^mask[i%4] for i,c in enumerate(body))
                    request=json.loads(body)
                    captured.append(request)
                    final=any(i.get('type')=='function_call_output' for i in request.get('input',[]))
                    self.respond(websocket=True, tool_call=request.get('generate') is not False and not final)
                    if final:
                        self.close_connection=True
                        return

            def do_POST(self):
                body=self.rfile.read(int(self.headers['Content-Length']))
                captured.append(json.loads(body))
                self.respond(websocket=False)

            def respond(self,websocket,tool_call=False):
                annotation={'schema_version':2,'type':'noise','problem':[], 'reasoning':[],
                    'impact':[], 'source_notes':[], 'limitations':['TEST FIXTURE ONLY'], 'links':[], 'chapters':[]}
                if retrieval:
                    annotation.update(schema_version=4,summary='TEST FIXTURE ONLY overview',findings=[])
                if not tool_call:
                    annotation['problem']=[{'text':'TEST FIXTURE ONLY','basis':'source','evidence':['read-1']}]
                item={'id':'msg_fixture','type':'message','role':'assistant','phase':'final_answer',
                    'content':[{'type':'output_text','text':json.dumps(annotation),'annotations':[]}]}
                if tool_call:
                    item={'id':'fc_fixture','type':'function_call','call_id':'read-1','name':expected_tool,'arguments':json.dumps({'mode':'content','commit':first} if retrieval else {'commit':task})}
                events=[{'type':'response.created','response':{'id':'resp_fixture','status':'in_progress'}},
                        {'type':'response.output_item.done','output_index':0,'item':item},
                        {'type':'response.completed','response':{'id':'resp_fixture','status':'completed','output':[item],
                          'usage':{'input_tokens':1,'output_tokens':1,'total_tokens':2}}}]
                if not websocket:
                    self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
                for event in events:
                    data=json.dumps(event).encode()
                    if websocket:
                        prefix=bytes([129,len(data)]) if len(data)<126 else bytes([129,126])+struct.pack('!H',len(data))
                        self.wfile.write(prefix+data)
                    else:self.wfile.write(b'data: '+data+b'\n\n')
                self.wfile.flush()
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        auth=self.root/'fixture-auth.json';auth.write_text(json.dumps({'OPENAI_API_KEY':'TEST_FIXTURE_NOT_A_CREDENTIAL'}))
        config=f'openai_base_url="http://127.0.0.1:{server.server_port}/v1"\n'+configuration()
        try:
            with patch('teacher.codex_transport.configuration',return_value=config):
                with CodexTransport(auth,timeout=30) as transport:
                    try:
                        result=CodexTeacher().run(FreshSession(self.packet),transport)
                    except Exception:
                        transport.stderr.seek(0)
                        raise AssertionError(transport.stderr.read(4096).decode(errors="replace"))
            self.assertFalse(result['published'])
            self.assertEqual(result['draft']['evidence']['read-1']['tool'],expected_tool)
            self.assertEqual(len(FreshSession(self.packet).tools),15 if retrieval else 14)
            self.assertTrue(captured)
            requests=[r for r in captured if r.get('generate') is not False]
            self.assertTrue(requests, 'No actual turn request captured')
            catalogs_checked=0
            for request in requests:
                self.assertEqual(request['model'],'gpt-6-astra')
                self.assertEqual(request['reasoning']['effort'],'medium')
                advertised=request.get('tools',[])+[t for item in request['input'] if item.get('type')=='additional_tools' for t in item['tools']]
                names={leaf['name'] for tool in advertised for leaf in (tool['tools'] if tool['type']=='namespace' else [tool])}
                if advertised:
                    self.assertEqual(names,{t['name'] for t in FreshSession(self.packet).tools})
                    catalogs_checked+=1
                serialized=json.dumps(request)
                for forbidden in ['ADMIN_SECRET','ADMIN_REVIEW_SECRET','TEST REVIEWER',self.future,str(self.repo),'astra-review.md','<skills_instructions>','<multi_agent_role>']:
                    self.assertNotIn(forbidden,serialized)
            self.assertGreater(catalogs_checked,0)
        finally:
            server.shutdown();server.server_close();thread.join()
