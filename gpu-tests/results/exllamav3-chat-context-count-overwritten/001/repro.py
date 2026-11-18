# Trigger: run examples/chat.py with --show_tps, complete one reply whose generated-token
# count differs from prompt_tokens - cached_tokens, and read the printed Context count.
import os, re, sys
import rt, chatdrv
rt.check_import()
WT = os.environ["EXL3_WT"]; M = "/home/unstable/exdev-gpu-work/models/SmolLM2-135M-Instruct"
sys.path.insert(0, WT + "/examples")
USER = "Name three colours."; MAXR = 12
from exllamav3 import Config, Tokenizer
from chat_templates import prompt_formats
pf = prompt_formats["chatml"]("User", "Assistant")
tok = Tokenizer.from_config(Config.from_directory(M))
prompt_tokens = tok.encode(pf.format(pf.default_system_prompt(), [(USER, None)]), add_bos=pf.add_bos(), encode_special_tokens=True).shape[-1]
c = chatdrv.Chat([sys.executable, WT + "/examples/chat.py", "-m", M, "-mode", "chatml", "-basic", "-tps", "-maxr", str(MAXR), "-cs", "2048"])
if not c.wait(r"User: ", 180):
    rt.report("did_not_run", note="no prompt", tail=c.text()[-600:]); c.close(); sys.exit(0)
n = len(c.text()); c.send(USER + "\r")
m = c.wait(r"Context: ([\d,]+) new tokens at ([\d.]+) t/s - ([\d,]+) tokens cached - Generate: ([\d,]+) tokens", 180, n)
if not m:
    rt.report("did_not_run", note="no Context line", tail=c.text()[-800:]); c.close(); sys.exit(0)
ctx, cached, gen = [int(m.group(i).replace(",", "")) for i in (1, 3, 4)]
c.close(); want = prompt_tokens - cached
notes = dict(prompt_tokens=prompt_tokens, cached=cached, uncached_expected=want, context_printed=ctx, generate_printed=gen)
if gen == want: rt.report("other", note="counts coincide, cannot discriminate", **notes)
elif ctx == gen: rt.report("stated_behaviour", **notes)
elif ctx == want: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
