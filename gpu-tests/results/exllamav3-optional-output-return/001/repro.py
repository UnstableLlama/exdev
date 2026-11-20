# Trigger: Job.receive_logits reaches its return with return_probs=True or return_top_tokens > 0.
# Fixture: Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775, loaded unquantized.
# Two jobs, run one at a time through the repository's Generator (enqueue + iterate), greedy sampling,
# 4 new tokens: (a) return_probs=True, (b) return_top_tokens=3. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : both cases raise UnboundLocalError from exllamav3/generator/job.py.
#   expected_behaviour : both cases complete and the streamed results carry the requested extra outputs
#                        (any result key mentioning prob / top for (a) / (b)).
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
def case(**kw):
    job = Job(input_ids=ids, max_new_tokens=4, sampler=ArgmaxSampler(), **kw)
    gen.enqueue(job); keys = set(); n = 0
    try:
        while gen.num_remaining_jobs():
            for r in gen.iterate():
                keys |= set(r.keys()); n += 1
        return dict(ok=True, result_keys=sorted(keys), results=n), None
    except Exception as e:
        try: gen.clear_queue()
        except Exception: pass
        return dict(ok=False, exception_type=type(e).__name__, site=rt._site(e.__traceback__), message=str(e).splitlines()[0] if str(e) else ""), e
a, ea = case(return_probs=True)
print("return_probs:", a, flush=True)
b, eb = case(return_top_tokens=3)
print("return_top_tokens:", b, flush=True)
notes = dict(return_probs=a, return_top_tokens=b)
unb = lambda r: (not r["ok"]) and r["exception_type"] == "UnboundLocalError" and (r["site"] or "").startswith("exllamav3/generator/job.py")
has = lambda r, w: r["ok"] and any(w in k for k in r["result_keys"])
if unb(a) and unb(b): rt.report("stated_behaviour", ea, **notes)
elif has(a, "prob") and has(b, "top"): rt.report("expected_behaviour", **notes)
else: rt.report("other", ea or eb, **notes)
