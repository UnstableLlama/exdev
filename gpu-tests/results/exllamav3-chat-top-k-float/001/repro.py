# Trigger: pass an explicit integer top-k on the command line of the caller each fix covers.
#   a027848ddc37 and its parent, and the latest affected commit: examples/chat.py --top_k 40
#   beb7bcd96d0d and its parent: eval/humaneval.py --top_k 40 (the "HumanEval caller" scope of that fix)
import os, re, subprocess, sys, tempfile
import rt, chatdrv
rt.check_import()
WT = os.environ["EXL3_WT"]; M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
sha = os.path.basename(WT)
def classify(text, done, **extra):
    et, site = chatdrv.tb_info(text, WT)
    msg = re.findall(r"^TypeError: .*$", text, re.M)
    if et == "TypeError" and msg and "slice indices" in msg[-1]:
        rt.report("stated_behaviour", etype=et, esite=site, message=msg[-1].strip(), **extra)
    elif et: rt.report("other", etype=et, esite=site, tail=text[-500:], **extra)
    elif done: rt.report("expected_behaviour", **extra)
    else: rt.report("did_not_run", tail=text[-500:], **extra)
if sha in ("3c9ede55404c", "beb7bcd96d0d"):
    out = os.path.join(tempfile.mkdtemp(), "o", "s.jsonl")
    r = subprocess.run([sys.executable, WT + "/eval/humaneval.py", "-m", M, "-o", out, "-spt", "1", "-pf", "chatml", "-cs", "4096",
                        "--top_k", "40", "--max_tokens", "8"], capture_output=True, text=True, timeout=500)
    t = r.stdout + r.stderr; sys.stdout.write(t[-3000:])
    n = sum(1 for _ in open(out)) if os.path.exists(out) else 0
    classify(t, r.returncode == 0 and n > 0, caller="humaneval", returncode=r.returncode, samples_written=n)
else:
    c = chatdrv.Chat([sys.executable, WT + "/examples/chat.py", "-m", M, "-mode", "chatml", "-basic", "-maxr", "8", "-cs", "2048", "--top_k", "40"])
    if not c.wait(r"(^|\n)User:", 180): rt.report("did_not_run", tail=c.text()[-500:]); c.close(); sys.exit(0)
    n = len(c.text()); c.send("Name three colours.\r")
    m = c.wait(r"(?s)Traceback \(most recent|Assistant.*\nUser:", 120, n)
    if m and m.group(0).startswith("Traceback"): c.wait(r"\Z.", 8)
    t = c.text()[n:]; c.close()
    classify(t, bool(m) and not m.group(0).startswith("Traceback"), caller="chat")
