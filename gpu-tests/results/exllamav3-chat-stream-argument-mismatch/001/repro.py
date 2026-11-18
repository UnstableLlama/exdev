# Trigger: a generator result reaches the chat loop's stream call, in basic and in rich console mode.
import os, re, sys
import rt, chatdrv
rt.check_import()
WT = os.environ["EXL3_WT"]; M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
res = {}
for name, flags in (("basic", ["-basic"]), ("rich", [])):
    c = chatdrv.Chat([sys.executable, WT + "/examples/chat.py", "-m", M, "-mode", "chatml", "-maxr", "8", "-cs", "2048"] + flags)
    if not c.wait(r"(^|\n)User:", 180):
        res[name] = dict(state="no_prompt", tail=c.text()[-400:]); c.close(); continue
    n = len(c.text()); c.send("Name three colours.\r")
    m = c.wait(r"(?s)Traceback \(most recent|Assistant.*\nUser:", 120, n)
    if m and m.group(0).startswith("Traceback"):
        c.wait(r"\Z.", 8)  # let the traceback finish and the process exit
        t = c.text()[n:]; et, site = chatdrv.tb_info(t, WT); msg = re.findall(r"^TypeError: .*$", t, re.M)
        res[name] = dict(state="exception", etype=et, site=site, message=msg[-1].strip() if msg else None)
    elif m: res[name] = dict(state="reply_completed")
    else: res[name] = dict(state="timeout", tail=c.text()[-400:])
    c.close()
st = [r["state"] for r in res.values()]
first = next((r for r in res.values() if r["state"] == "exception"), {})
if all(r["state"] == "exception" and r["etype"] == "TypeError" and "stream" in (r["message"] or "") for r in res.values()):
    rt.report("stated_behaviour", etype="TypeError", esite=first["site"], **res)
elif all(s == "reply_completed" for s in st): rt.report("expected_behaviour", **res)
elif "no_prompt" in st or "timeout" in st: rt.report("did_not_run", **res)
else: rt.report("other", etype=first.get("etype"), esite=first.get("site"), **res)
