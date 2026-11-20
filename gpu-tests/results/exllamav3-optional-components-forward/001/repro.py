# Trigger: construct a ParallelDecoderBlock without its input norm (and without attention / MLP) and reach the
# corresponding call in forward. Fixture: a tiny Llama config (no weights needed). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : construction succeeds and forward raises AttributeError ('NoneType' ... 'forward') from
#                        exllamav3/modules/transformer.py.
#   expected_behaviour : construction rejects the omission, or forward handles it deliberately.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import ParallelDecoderBlock
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=256, intermediate_size=512, num_attention_heads=4, num_key_value_heads=4, num_hidden_layers=1, vocab_size=128, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512, bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
save_file({"model.norm.weight": torch.ones(256).half()}, d + "/model.safetensors")
cfg = Config.from_directory(d)
try:
    b = ParallelDecoderBlock(config=cfg, key="model.layers.0", input_norm=None, attn=None, mlp=None)
except Exception as e:
    rt.report("expected_behaviour", e, stage="construction", message=str(e)); raise SystemExit
try:
    b.forward(torch.randn(1, 4, 256, dtype=torch.half, device="cuda:0"), {})
except AttributeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if "NoneType" in str(e) and site.startswith("exllamav3/modules/transformer.py") else "other", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("expected_behaviour", note="forward returned")
