# Trigger: receive_logits completes sampling with return_probs=False and return_top_tokens=0 (the
# constructor defaults), reached through the ordinary Generator.generate path.
import torch
import rt
rt.check_import()
from exllamav3 import Config, Model, Cache, Tokenizer, Generator
M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
c = Config.from_directory(M); m = Model.from_config(c); ca = Cache(m, max_num_tokens=2048); m.load("cuda:0"); t = Tokenizer.from_config(c)
g = Generator(model=m, cache=ca, tokenizer=t)
try:
    out = g.generate("The capital of France is", max_new_tokens=4, completion_only=True)
except UnboundLocalError as e:
    rt.report("stated_behaviour", e, message=str(e))
except Exception as e:
    rt.report("other", e, message=str(e))
else:
    rt.report("expected_behaviour", output=out)
