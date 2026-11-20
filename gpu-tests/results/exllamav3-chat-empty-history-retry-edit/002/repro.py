# Trigger: enter /r or /e immediately after startup (empty history).
# examples/chat.py is driven through a pseudo-terminal (lib/chatdrv.py) with Qwen2.5-0.5B-Instruct
# @ 7ae557604adf67be50417f59c2c2f167def9a775, chatml mode, basic console. Two fresh sessions: one sends "/r",
# the other "/e", as the first input. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : both commands end the session with IndexError from examples/chat.py.
#   expected_behaviour : both commands are refused with a message and the session returns to the User prompt.
#   other              : anything else.
import os, re, sys
import rt, chatdrv
rt.check_import()
WT = os.environ["EXL3_WT"]; M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
BASE = [sys.executable, WT + "/examples/chat.py", "-m", M, "-mode", "chatml", "-basic", "-maxr", "12", "-cs", "2048"]
def start(extra=()):
    c = chatdrv.Chat(BASE + list(extra))
    if not c.wait(r"(^|\n)User:", 240):
        rt.report("did_not_run", note="no prompt", tail=c.text()[-600:]); c.close(); sys.exit(0)
    return c
res = {}
for cmd in ("/r", "/e"):
    c = start(); n = len(c.text()); c.send(cmd + "\r")
    m = c.wait(r"(Traceback \(most recent call last\)[\s\S]*?\n[A-Za-z_.]*(Error|Exception)[^\n]*)|(\nUser:)", 60, n)
    c.wait(r"$^", 3)  # drain
    et, site = chatdrv.tb_info(c.text()[n:], WT)
    res[cmd] = dict(exception_type=et, site=site, returned_to_prompt=bool(re.search(r"\nUser:", c.text()[n:])), exited=c.p.poll() is not None)
    c.close()
print(res, flush=True)
if all(r["exception_type"] == "IndexError" and (r["site"] or "").startswith("examples/chat.py") for r in res.values()):
    rt.report("stated_behaviour", etype="IndexError", esite=res["/r"]["site"], **{k.strip("/"): v for k, v in res.items()})
elif all(r["exception_type"] is None and r["returned_to_prompt"] for r in res.values()):
    rt.report("expected_behaviour", **{k.strip("/"): v for k, v in res.items()})
else:
    rt.report("other", **{k.strip("/"): v for k, v in res.items()})
