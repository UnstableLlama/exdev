# SPDX-License-Identifier: MIT
"""Exercise failure diagnostics with a local fake stdio server and synthetic credentials."""
import hashlib
import json
import os
import stat
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from teacher.author import author
from teacher.codex_transport import CodexTransport, SUPPORTED_VERSION
import test_author


SERVER = '''
import json
import pathlib
import sys

settings = json.loads(sys.argv[1])
auth = pathlib.Path(sys.argv[2])
auth.write_text(json.dumps({'tokens': {'refresh_token': 'refreshed/value'}}))
mode = settings['mode']
for line in sys.stdin:
    request = json.loads(line)
    method = request['method']
    if method == 'initialized':
        continue
    key = request['id']
    if (mode == 'rpc' and method == 'initialize') or method == 'turn/start':
        if mode == 'oversize':
            print('x' * 70000, file=sys.stderr, flush=True)
        else:
            print('provider refused: old/value refreshed%2Fvalue', file=sys.stderr)
            print('Authorization: Basic bW9ja19jcmVk', file=sys.stderr)
            print('Set-Cookie: session=unknown_session; Secure', file=sys.stderr)
            print('upstream: https://demo:user-secret@example.test/path', file=sys.stderr)
            print('password="text with spaces"', file=sys.stderr, flush=True)
        if mode == 'rpc':
            print(json.dumps({'id': key, 'error': {'code': -32000, 'message': 'setup failed'}}), flush=True)
            break
    if method == 'initialize':
        result = {}
    elif method == 'thread/start':
        result = {'model': 'gpt-6.2-sol', 'reasoningEffort': 'medium', 'thread': {'id': 'test-thread'}}
    else:
        result = {'turn': {'id': 'test-turn'}}
    print(json.dumps({'id': key, 'result': result}), flush=True)
    if method == 'turn/start':
        payload = {'threadId': 'test-thread', 'turnId': 'test-turn', 'error': {
            'message': 'provider refused old/value',
            'data': {'apiKey': 'fake_unknown_key', 'notes': ['Bearer unknown_bearer', 42]},
        }}
        if mode == 'oversize':
            payload['error']['data']['padding'] = 'x' * 70000
        if mode == 'invalid_auth':
            auth.write_text('malformed with secret')
        print(json.dumps({'method': 'error', 'params': payload}), flush=True)
        break
'''


class CodexFailureTests(unittest.TestCase):
    setUp = test_author.AuthorTests.setUp
    tearDown = test_author.AuthorTests.tearDown

    def run_failure(self, mode, message, error_type):
        auth = self.root/'auth.json'
        auth.write_text(json.dumps({'OPENAI_API_KEY': 'old/value'}))
        packet_hash = hashlib.sha256((self.packet/'manifest.json').read_bytes()).hexdigest()
        output = self.root/'failed'
        created = []

        def fake_server(command, **kwargs):
            state = command[command.index('--bind') + 1]
            return subprocess.Popen([sys.executable, '-c', SERVER, json.dumps({'mode': mode}), state + '/auth.json'],
                                    **kwargs)

        def transport_factory(auth_file):
            transport = CodexTransport(auth_file, timeout=10)
            created.append(transport)
            return transport

        process_api = SimpleNamespace(check_output=lambda *args, **kwargs: SUPPORTED_VERSION + '\n',
                                      DEVNULL=subprocess.DEVNULL, PIPE=subprocess.PIPE, Popen=fake_server)
        with patch('teacher.codex_transport.subprocess', process_api):
            with self.assertRaisesRegex(error_type, message):
                author(self.packet, output, auth, transport_factory=transport_factory)
        self.assertFalse((output/'draft.json').exists())
        self.assertEqual(json.loads((output/'status.json').read_text())['status'], 'failed')
        self.assertEqual(hashlib.sha256((self.packet/'manifest.json').read_bytes()).hexdigest(), packet_hash)
        self.assertFalse(os.path.exists(created[0].temporary.name))
        self.assertTrue(created[0].stderr.closed)
        artifact = output/'codex-failure.json'
        self.assertEqual(stat.S_IMODE(artifact.stat().st_mode), 0o600)
        self.assertEqual(list(output.glob('.codex-failure-*')), [])
        return json.loads(artifact.read_text()), output

    def test_error_event_and_stderr_redacted_in_failed_run_only(self):
        diagnostics, output = self.run_failure('event', 'Codex reported an authoring error', ValueError)
        event, = diagnostics['error_events']
        self.assertEqual(event['method'], 'error')
        self.assertEqual(event['params']['error']['message'], 'provider refused [REDACTED]')
        self.assertEqual(event['params']['error']['data'], {'apiKey': '[REDACTED]', 'notes': ['[REDACTED]', 42]})
        self.assertIn('provider refused: [REDACTED] [REDACTED]', diagnostics['stderr'])
        self.assertIn('https://[REDACTED]@example.test/path', diagnostics['stderr'])
        encoded = json.dumps(diagnostics)
        for secret in ('old/value', 'refreshed%2Fvalue', 'bW9ja19jcmVk', 'unknown_session', 'user-secret',
                       'text with spaces', 'fake_unknown_key', 'unknown_bearer'):
            self.assertNotIn(secret, encoded)
        transcript = json.loads((output/'raw-transcript.json').read_text())
        self.assertEqual([row['role'] for row in transcript], ['system', 'user'])
        self.assertNotIn('provider refused', json.dumps(transcript))

    def test_setup_rpc_error_is_diagnostic_and_keeps_original_exception(self):
        diagnostics, _ = self.run_failure('rpc', 'Codex RPC failed for initialize: -32000', RuntimeError)
        event, = diagnostics['error_events']
        self.assertEqual(event['error'], {'code': -32000, 'message': 'setup failed'})
        self.assertIn('provider refused', diagnostics['stderr'])

    def test_oversized_streams_are_omitted_without_saving_partial_secrets(self):
        diagnostics, _ = self.run_failure('oversize', 'Codex reported an authoring error', ValueError)
        self.assertEqual(diagnostics, {'error_events': [], 'omitted_error_events': 1,
                                       'stderr': None, 'stderr_omitted': 'size_limit'})

    def test_bad_auth_state_fails_closed_without_replacing_original_error(self):
        diagnostics, _ = self.run_failure('invalid_auth', 'Codex reported an authoring error', ValueError)
        self.assertEqual(diagnostics, {'unavailable': 'capture_or_redaction_failed'})
