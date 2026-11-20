# SPDX-License-Identifier: MIT
"""Redact Codex failure diagnostics before they leave the authoring process."""
import json
import re
from urllib.parse import quote, quote_plus

REDACTED = '[REDACTED]'
LIMIT = 64 * 1024
KEY = (
    r'(?:[\w-]*api[_-]?key|[\w-]*access[_-]?token|refresh[_-]?token|id[_-]?token|'
    r'session[_-]?token|auth[_-]?token|token|authorization|proxy[_-]authorization|'
    r'cookie|set[_-]cookie|password|passwd|client[_-]?secret|secret|credential[s]?|private[_-]?key)'
)
CREDENTIAL_KEY = re.compile(KEY, re.IGNORECASE)
LABELED = re.compile(
    rf"""(?P<label>\b{KEY}(?:["'])?\s*[:=]\s*)(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[^\s,;&\]}}]+)""",
    re.IGNORECASE,
)
HEADER = re.compile(r'(?im)(\b(?:proxy-)?authorization|\b(?:set-)?cookie)([ \t]*:[ \t]*)(?!["\']).*')
SENSITIVE_TEXT = re.compile(
    r'(?i)\b(?:Bearer|Basic)[ \t]+[\w.~+/=-]+|'
    r'\bsk-[\w-]+|\beyJ[\w-]+\.[\w-]+\.[\w-]+|'
    r'-----BEGIN [^-\r\n]*PRIVATE KEY-----[\s\S]*?-----END [^-\r\n]*PRIVATE KEY-----'
)
URL_CREDENTIALS = re.compile(r'(://)[^/\s?#]*@')


def auth_secrets(data):
    auth = json.loads(data)
    if not isinstance(auth, dict):
        raise ValueError('Invalid Codex auth document')
    secrets = set()

    def visit(value, sensitive=False):
        if isinstance(value, dict):
            for key, item in value.items():
                visit(item, sensitive or CREDENTIAL_KEY.fullmatch(key) is not None)
        elif isinstance(value, list):
            for item in value:
                visit(item, sensitive)
        elif sensitive and isinstance(value, str) and value:
            secrets.add(value)

    visit(auth)
    return secrets


class Redactor:
    def __init__(self, secrets):
        variants = {variant for secret in secrets for encoded in (secret, quote(secret, safe=''), quote_plus(secret))
                    for variant in (encoded, json.dumps(encoded)[1:-1], json.dumps(encoded, ensure_ascii=False)[1:-1])}
        self.exact = re.compile('|'.join(map(re.escape, sorted(variants, key=len, reverse=True)))) if variants else None

    def text(self, value):
        if self.exact:
            value = self.exact.sub(REDACTED, value)
        value = HEADER.sub(lambda m: m[1] + m[2] + REDACTED, value)
        value = SENSITIVE_TEXT.sub(REDACTED, value)
        value = URL_CREDENTIALS.sub(lambda m: m[1] + REDACTED + '@', value)
        return LABELED.sub(lambda m: m['label'] + REDACTED, value)

    def payload(self, value):
        if isinstance(value, dict):
            return {self.text(key): REDACTED if CREDENTIAL_KEY.fullmatch(key) else self.payload(item)
                    for key, item in value.items()}
        if isinstance(value, list):
            return [self.payload(item) for item in value]
        if isinstance(value, str):
            return self.text(value)
        return value
