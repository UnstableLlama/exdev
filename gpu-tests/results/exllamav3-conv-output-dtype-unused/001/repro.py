# Trigger: a direct caller supplies a constructor-level or forward-call out_dtype different from the convolution
# result dtype. exllamav3.modules.Conv (2-D, 3 -> 16 channels, kernel (4, 4)) is built over a tiny checkpoint
# tensor, with out_dtype=torch.float, loaded on GPU and run on an FP16 (1, 3, 8, 8) input; a second call passes
# forward(..., out_dtype=torch.float). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : both calls return FP16 (neither dtype option is applied).
#   expected_behaviour : both calls return float32.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import Conv
d = tempfile.mkdtemp(); json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=256, intermediate_size=512, num_attention_heads=4, num_key_value_heads=4, num_hidden_layers=1, vocab_size=128, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512, bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
save_file({"model.norm.weight": torch.ones(256).half(), "vis.conv.weight": (torch.randn(16, 3, 4, 4) * 0.1).half(), "vis.conv.bias": torch.zeros(16).half()}, d + "/model.safetensors")
cfg = Config.from_directory(d)
c = Conv(config=cfg, key="vis.conv", in_channels=3, out_channels=16, kernel_size=(4, 4), out_dtype=torch.float)
c.load(torch.device("cuda:0"))
x = torch.randn(1, 3, 8, 8, dtype=torch.half, device="cuda:0")
y1 = c.forward(x, {}); y2 = c.forward(x, {}, out_dtype=torch.float)
notes = dict(constructor_out_dtype=str(c.out_dtype), result_dtype_ctor=str(y1.dtype), result_dtype_forward_arg=str(y2.dtype), shape=list(y1.shape))
if y1.dtype == torch.half and y2.dtype == torch.half: rt.report("stated_behaviour", **notes)
elif y1.dtype == torch.float and y2.dtype == torch.float: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
