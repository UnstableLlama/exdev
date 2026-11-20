# Trigger: construct Attention with q_norm=None and a non-null k_norm.
# Fixture: a tiny LlamaForCausalLM config (no weights needed for construction). Attention is constructed with
# the same arguments LlamaModel uses plus q_norm=None, k_norm=RMSNorm(...). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : construction succeeds and the supplied k_norm is discarded (attn.k_norm is None).
#   expected_behaviour : construction is rejected (AssertionError/ValueError), consistent with the
#                        "both Q and K norms, or neither" rule.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import Attention, RMSNorm
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=256, intermediate_size=512, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=1, vocab_size=128, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512,
               bos_token_id=1, eos_token_id=2), open(d + "/config.json", "w"))
save_file({"model.norm.weight": torch.ones(256).half()}, d + "/model.safetensors")
cfg = Config.from_directory(d)
kn = RMSNorm(config=cfg, key="model.layers.0.self_attn.k_norm", rms_norm_eps=1e-6)
try:
    a = Attention(config=cfg, key="model.layers.0.self_attn", layer_idx=0, hidden_size=256, head_dim=64, num_q_heads=4, num_kv_heads=4,
                  rope_settings=cfg.rope_settings, sm_scale=None, key_q="q_proj", key_k="k_proj", key_v="v_proj", key_o="o_proj",
                  qmap="block.attn", q_norm=None, k_norm=kn)
except (AssertionError, ValueError) as e:
    rt.report("expected_behaviour", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
notes = dict(q_norm=repr(a.q_norm), k_norm_is_none=a.k_norm is None, k_norm_registered=any(m is kn for m in a))
print(notes, flush=True)
rt.report("stated_behaviour" if a.k_norm is None else "other", **notes)
