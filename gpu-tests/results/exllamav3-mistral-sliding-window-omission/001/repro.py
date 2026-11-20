# Trigger: construct MistralModel with a Mistral-7B-v0.1-style config declaring sliding_window=4096.
# Fixture: a tiny MistralForCausalLM config.json (sliding_window 4096, 1 layer; Mistral-7B-v0.1's other dims
# scaled down) plus one tensor; Config.from_directory / Model.from_config only (no load). The Attention module's
# sliding_window attribute is read. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : Attention.sliding_window is -1 while the config declares 4096.
#   expected_behaviour : Attention.sliding_window is 4096.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config, Model
from exllamav3.modules import Attention
d = tempfile.mkdtemp()
json.dump(dict(architectures=["MistralForCausalLM"], hidden_size=256, intermediate_size=512, num_attention_heads=4, num_key_value_heads=1,
               num_hidden_layers=1, vocab_size=128, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=32768,
               sliding_window=4096, bos_token_id=1, eos_token_id=2, tie_word_embeddings=False), open(d + "/config.json", "w"))
save_file({"model.norm.weight": torch.ones(256).half()}, d + "/model.safetensors")
cfg = Config.from_directory(d); m = Model.from_config(cfg)
a = [x for x in m if isinstance(x, Attention)][0]
notes = dict(model=type(m).__name__, config_sliding_window=4096, attention_sliding_window=a.sliding_window)
print(notes, flush=True)
if a.sliding_window == -1: rt.report("stated_behaviour", **notes)
elif a.sliding_window == 4096: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
