"""Drive examples/chat.py through a real pseudo-terminal, as a user would."""
import os, pty, re, select, subprocess, sys, time
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b[=>]|\r")
def clean(s): return ANSI.sub("", s)
class Chat:
    def __init__(self, argv, env=None):
        self.m, s = pty.openpty()
        e = dict(os.environ, TERM="xterm", PROMPT_TOOLKIT_NO_CPR="1", COLUMNS="160", LINES="50"); e.update(env or {})
        self.p = subprocess.Popen(argv, stdin=s, stdout=s, stderr=s, env=e, close_fds=True, start_new_session=True); os.close(s)
        self.buf = ""
    def pump(self, t=0.2):
        r, _, _ = select.select([self.m], [], [], t)
        if r:
            try: d = os.read(self.m, 65536)
            except OSError: return False
            if not d: return False
            d = d.decode("utf8", "replace"); self.buf += d; sys.stdout.write(d); sys.stdout.flush()
        return True
    def wait(self, pat, timeout, start=0):
        end = time.time() + timeout
        while time.time() < end:
            alive = self.pump()
            m = re.search(pat, clean(self.buf)[start:])
            if m: return m
            if not alive or (self.p.poll() is not None and not select.select([self.m], [], [], 0)[0]): return None
        return None
    def send(self, s): os.write(self.m, s.encode())
    def text(self): return clean(self.buf)
    def close(self):
        try: self.p.terminate(); self.p.wait(10)
        except Exception: self.p.kill()
        return self.p.returncode

def tb_info(text, wt):
    """(exception type, last repository frame) of the last traceback in a transcript."""
    i = text.rfind("Traceback (most recent call last)")
    if i < 0: return None, None
    t = text[i:]; wt = os.path.realpath(wt) + "/"
    fr = re.findall(r'File "([^"]+)", line (\d+)', t)
    site = None
    for f, n in fr:
        if os.path.realpath(f).startswith(wt): site = os.path.realpath(f)[len(wt):] + ":" + n
    e = re.findall(r"^([A-Za-z_][\w.]*(?:Error|Exception|Interrupt|Exit)):?", t, re.M)
    return (e[-1] if e else None), site
