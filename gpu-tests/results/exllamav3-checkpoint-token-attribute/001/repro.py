# Trigger: a full banned-string match reaches rewind_checkpoint.
# Fixture: Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775 unquantized. A greedy job on
# "The capital of France is" (whose greedy continuation is " Paris") with banned_strings=["paris"] runs through
# the repository's Generator. First, a control job without banned strings confirms the greedy continuation
# contains "Paris". The streamed token_ids and suppressed_tokens of the banned job are collected.
# Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : some token ID reported in suppressed_tokens also appears in the emitted token_ids
#                        (rejected IDs flushed from the unrestored held buffer).
#   expected_behaviour : suppressed tokens are reported and none of them appears in the emitted token_ids.
#   other              : anything else (including no suppression happening).
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
    gen.enqueue(Job(input_ids=ids, max_new_tokens=8, sampler=ArgmaxSampler(), **kw)); text, emitted, supp = "", [], []
    while gen.num_remaining_jobs():
        for r in gen.iterate():
            text += r.get("text", "") or ""
            if r.get("token_ids") is not None: emitted += r["token_ids"].flatten().tolist()
            if r.get("suppressed_tokens") is not None: supp += r["suppressed_tokens"].flatten().tolist()
    return text, emitted, supp
ctl_text, _, _ = run()
print("control:", repr(ctl_text), flush=True)
try:
    text, emitted, supp = run(banned_strings=["paris"])
except Exception as e:
    rt.report("other", e, control_text=ctl_text, message=str(e)); raise SystemExit
overlap = sorted(set(supp) & set(emitted))
notes = dict(control_text=ctl_text, text=text, emitted=emitted, suppressed=supp, overlap=overlap,
             overlap_pieces=[tok.decode(torch.tensor([[t]])) for t in overlap])
print(notes, flush=True)
if "paris" not in ctl_text.lower(): rt.report("other", note="control did not produce the banned string", **notes)
elif overlap: rt.report("stated_behaviour", **notes)
elif supp: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
