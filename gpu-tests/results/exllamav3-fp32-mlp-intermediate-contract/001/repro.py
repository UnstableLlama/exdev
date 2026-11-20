# Trigger: construct GatedMLP with interm_dtype=torch.float32 and run forward with otherwise valid FP16 inputs.
# Fixture: a tiny random LlamaForCausalLM checkpoint (only the config and one layer's MLP tensors are used),
# loaded unquantized, so gate/up/down are dense FP16 linears (the ledger's "dense down projection" case).
# GatedMLP is constructed and called directly through the repository's own classes. Upstream is not modified.
#
# Classification, fixed before running:
#   stated_behaviour   : forward raises from the down projection's FP16 GEMM input check (fp16.py / ext.hgemm),
#                        i.e. the activation silently accepted the FP32 buffers.
#   expected_behaviour : forward returns a finite FP16 result matching a torch reference (rtol/atol 2e-2),
#                        or the setting is rejected before any computation.
#   other              : anything else (e.g. an exception inside the activation's own dtype check, or a
#                        wrong result without an exception); the details are recorded in notes.
import json, os, tempfile, traceback
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import GatedMLP

H, IM, V = 256, 512, 128
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
p = "model.layers.0.mlp"
t = {f"{p}.gate_proj.weight": n(IM, H), f"{p}.up_proj.weight": n(IM, H), f"{p}.down_proj.weight": n(H, IM),
     "model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     "model.layers.0.input_layernorm.weight": torch.ones(H).half(), "model.layers.0.post_attention_layernorm.weight": torch.ones(H).half()}
for k in "qkvo": t[f"model.layers.0.self_attn.{k}_proj.weight"] = n(H, H)
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512,
               bos_token_id=1, eos_token_id=2, tie_word_embeddings=False), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")

x = (torch.randn(1, 16, H) * 0.5).half().cuda()
g32, u32, d32 = (t[f"{p}.{k}_proj.weight"].float().cuda() for k in ("gate", "up", "down"))
xf = x.float().view(-1, H)
ref = ((torch.nn.functional.silu(xf @ g32.T) * (xf @ u32.T)) @ d32.T).view(1, 16, H)

try:
    c = Config.from_directory(d)
    mlp = GatedMLP(config=c, key=p, hidden_size=H, intermediate_size=IM, key_up="up_proj", key_gate="gate_proj",
                   key_down="down_proj", qmap="block.mlp", interm_dtype=torch.float32)
    mlp.load(torch.device("cuda:0"))
    print("loaded; gate inner:", type(mlp.gates[0].inner).__name__, "down inner:", type(mlp.downs[0].inner).__name__, flush=True)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit

try:
    with torch.inference_mode():
        y = mlp.forward(x.clone(), {})
    torch.cuda.synchronize()
except Exception as e:
    tb = traceback.extract_tb(e.__traceback__)
    site = rt._site(e.__traceback__) or ""
    in_act = any(fr.name in ("forward",) and fr.filename.endswith("mlp.py") and "activation_fn_call" in (fr.line or "") for fr in tb) and tb[-1].filename.endswith("mlp.py")
    in_down = "fp16.py" in site
    beh = "stated_behaviour" if in_down else "other"
    rt.report(beh, e, failed_in_activation_call=in_act, failed_in_fp16_linear=in_down, message=str(e).splitlines()[0] if str(e) else ""); raise SystemExit

yf = y.float()
finite = bool(yf.isfinite().all())
maxdiff = (yf - ref).abs().max().item()
close = finite and torch.allclose(yf, ref, rtol=2e-2, atol=2e-2)
rt.report("expected_behaviour" if close and y.dtype == torch.half else "other",
          out_dtype=str(y.dtype), finite=finite, max_abs_diff_vs_reference=maxdiff, ref_max_abs=ref.abs().max().item())
