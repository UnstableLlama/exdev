# Trigger: enter "/load saved.json" in the interactive chat loop.
# examples/chat.py driven through a pseudo-terminal (lib/chatdrv.py), Qwen2.5-0.5B-Instruct, chatml, basic
# console, max 12 response tokens. The command names a file that does not exist, so a working /load prints
# "Error loading ..."; a fall-through instead sends the command text to the model as a prompt.
# Classification, fixed before running:
#   stated_behaviour   : no "Loaded session"/"Error loading" message, and an Assistant reply is generated.
#   expected_behaviour : a "Loaded session" or "Error loading" message and no Assistant reply.
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
c = start(); n = len(c.text()); c.send("/load /tmp/does_not_exist_saved.json\r")
c.wait(r"Assistant:[\s\S]*?\nUser:|Error loading|Loaded session", 120, n); c.wait(r"$^", 2)
t = c.text()[n:]; c.close()
notes = dict(load_message=bool(re.search(r"Error loading|Loaded session", t)), assistant_reply=bool(re.search(r"Assistant:", t)), transcript=t[-400:])
print(notes, flush=True)
if not notes["load_message"] and notes["assistant_reply"]: rt.report("stated_behaviour", **notes)
elif notes["load_message"] and not notes["assistant_reply"]: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
