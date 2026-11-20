# Trigger: enable probability / top-token reporting while using distribution-changing sampling.
# Qwen/Qwen2.5-0.5B-Instruct unquantized; a 1-token job on "The capital of France is" with
# ComboSampler(temperature=0.05) (which sharpens the distribution to nearly one-hot), return_probs=True and
# return_top_tokens=3. The reported probabilities are compared with (a) softmax of the raw model logits for the
# same prompt and (b) softmax(raw logits / 0.05), the distribution the sampler actually draws from.
# Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the reported top probability matches the raw softmax (within 0.02) and differs from
#                        the temperature-scaled one by more than 0.1.
#   expected_behaviour : it matches the temperature-scaled distribution (within 0.02).
#   other              : anything else.
from exllamav3.generator.sampler import ComboSampler
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
res = run(max_new_tokens=1, sampler=ComboSampler(temperature=0.05), return_probs=True, return_top_tokens=3)
tp = [r for r in res if r.get("top_k_probs") is not None]
if not tp: rt.report("did_not_run", note="no top_k_probs reported", keys=sorted({k for r in res for k in r})); raise SystemExit
rep = tp[0]["top_k_probs"].flatten().float().tolist(); rep_tok = tp[0]["top_k_tokens"].flatten().tolist()
with torch.inference_mode(): lg = model.forward(ids).float()[0, -1]
raw = torch.softmax(lg, -1); hot = torch.softmax(lg / 0.05, -1)
notes = dict(reported_top_tokens=rep_tok, reported_top_probs=rep, raw_softmax_top=[float(raw[t]) for t in rep_tok], temp_scaled_top=[float(hot[t]) for t in rep_tok])
print(notes, flush=True)
d_raw, d_hot = abs(rep[0] - notes["raw_softmax_top"][0]), abs(rep[0] - notes["temp_scaled_top"][0])
if d_raw <= 0.02 and d_hot > 0.1: rt.report("stated_behaviour", **notes)
elif d_hot <= 0.02: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
