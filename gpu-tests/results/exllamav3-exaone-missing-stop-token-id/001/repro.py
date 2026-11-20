# Trigger: select --mode exaone with a tokenizer that has a valid EOS ID but no exact [|endofturn|] entry, and
# submit a prompt that reaches Job construction.
# examples/chat.py is driven through a pseudo-terminal (lib/chatdrv.py) with Qwen2.5-0.5B-Instruct
# @ 7ae557604adf67be50417f59c2c2f167def9a775 (whose vocabulary has no [|endofturn|] token; checked below),
# -mode exaone, basic console. One prompt is submitted. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : ValueError "Unsupported type in stop_conditions" from Job construction.
#   expected_behaviour : a reply is generated, or the mode rejects the tokenizer with a message naming the marker.
#   other              : anything else.
import os, re, sys
import rt, chatdrv
rt.check_import()
WT = os.environ["EXL3_WT"]; M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
from exllamav3 import Config, Tokenizer
tok = Tokenizer.from_config(Config.from_directory(M))
sid = tok.single_id("[|endofturn|]")
print("single_id([|endofturn|]) =", sid, "eos =", tok.eos_token_id, flush=True)
c = chatdrv.Chat([sys.executable, WT + "/examples/chat.py", "-m", M, "-mode", "exaone", "-basic", "-maxr", "12", "-cs", "2048"])
if not c.wait(r"(^|\n)User:", 240):
    rt.report("did_not_run", note="no prompt", tail=c.text()[-600:]); c.close(); sys.exit(0)
n = len(c.text()); c.send("Name a colour.\r")
c.wait(r"Traceback[\s\S]*?\n\w*Error[^\n]*|Assistant:[\s\S]*?\nUser:|endofturn", 120, n); c.wait(r"\$^", 3)
t = c.text()[n:]; c.close()
et, site = chatdrv.tb_info(t, WT)
msg = re.findall(r"^\w*Error: ([^\n]*)", t, re.M)
notes = dict(single_id=sid, exception_type=et, site=site, message=msg[-1] if msg else None, transcript=t[-500:])
if et == "ValueError" and msg and "stop_conditions" in msg[-1]: rt.report("stated_behaviour", etype=et, esite=site, **notes)
elif et is None and ("Assistant:" in t or "endofturn" in t): rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
