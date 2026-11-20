# Trigger: enter /tps in an active chat session.
# examples/chat.py driven through a pseudo-terminal (lib/chatdrv.py), Qwen2.5-0.5B-Instruct, chatml, basic
# console, started without -tps and without -mli. After "/tps", a prompt is sent with Enter; if no reply
# starts within 20 s, Ctrl-D is sent (basic multiline input reads to EOF). After the reply, the tokens/second
# line ("Context: ... t/s") is looked for.
# Classification, fixed before running:
#   stated_behaviour   : "/tps" reports enabling tokens/second output, the prompt needs EOF to submit
#                        (multiline was toggled), and no tokens/second line follows the reply.
#   expected_behaviour : a tokens/second line follows the reply and the prompt submits with Enter.
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
c = start(); n = len(c.text()); c.send("/tps\r")
c.wait(r"tokens/second output", 30, n); msg = re.search(r"(Enabled|Disabled) tokens/second output", c.text()[n:])
c.wait(r"\nUser:", 10, n); n2 = len(c.text()); c.send("Name a colour.\r")
replied = c.wait(r"Assistant:", 20, n2) is not None; needed_eof = False
if not replied:
    needed_eof = True; c.send("\x04"); c.wait(r"Assistant:", 60, n2)
c.wait(r"\nUser:", 120, n2); c.wait(r"$^", 2)
t = c.text()[n2:]; c.close()
notes = dict(tps_message=msg.group(0) if msg else None, submit_needed_eof=needed_eof, reply_seen="Assistant:" in t, tps_line=bool(re.search(r"Context: [\d,]+ new tokens at", t)))
print(notes, flush=True)
if notes["tps_message"] == "Enabled tokens/second output" and needed_eof and not notes["tps_line"]: rt.report("stated_behaviour", **notes)
elif notes["tps_line"] and not needed_eof: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
