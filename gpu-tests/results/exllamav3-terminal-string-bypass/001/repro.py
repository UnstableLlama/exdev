# Trigger: a non-stop token completes a banned string when new_tokens reaches max_new_tokens (no draft tokens).
# Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775 unquantized; greedy job on
# "The capital of France is" whose first token is " Paris" (checked by a control job), with max_new_tokens=1
# and banned_strings=["paris"], through the repository's Generator. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the banned job's emitted text contains "Paris".
#   expected_behaviour : the emitted text does not contain the banned string.
#   other              : anything else.
import torch
import rt
rt.check_import()
from exllamav3 import Model, Config, Cache, Tokenizer, Generator, Job
from exllamav3.generator.sampler import ArgmaxSampler
M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
try:
    config = Config.from_directory(M); model = Model.from_config(config)
    cache = Cache(model, max_num_tokens=2048); model.load(progressbar=False)
    tok = Tokenizer.from_config(config); gen = Generator(model=model, cache=cache, tokenizer=tok)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
ids = tok.encode("The capital of France is")
def run(**kw):
    gen.enqueue(Job(input_ids=ids, **kw)); res = []
    while gen.num_remaining_jobs():
        for r in gen.iterate(): res.append(r)
    return res
ctl = "".join(r.get("text", "") or "" for r in run(max_new_tokens=1, sampler=ArgmaxSampler()))
txt = "".join(r.get("text", "") or "" for r in run(max_new_tokens=1, sampler=ArgmaxSampler(), banned_strings=["paris"]))
notes = dict(control_text=ctl, banned_job_text=txt)
print(notes, flush=True)
if "paris" not in ctl.lower(): rt.report("other", note="control first token is not Paris", **notes)
elif "paris" in txt.lower(): rt.report("stated_behaviour", **notes)
else: rt.report("expected_behaviour", **notes)
