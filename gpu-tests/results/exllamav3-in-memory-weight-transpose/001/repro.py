# Trigger: conversion reloads an unquantized linear weight from the in-memory tensor override through
# Linear.load_fp16 with transpose=True.
# No built-in model at these commits was found whose conversion leaves a linear unquantized inside a quantized
# module, so the reload is performed directly with the same calls convert_model.main makes after a module:
# collect m.get_tensors(), config.stc.set_new_tensors(tensors), module.load(device, source=tensors),
# config.stc.set_new_tensors(None). Fixture: a tiny random LlamaForCausalLM checkpoint; two Linear modules are
# built over its tensors, one rectangular (q_proj-shaped 256 -> 512) and one square nonsymmetric (256 -> 256).
# Upstream is not modified.
#
# Classification, fixed before running (decided by both cases together):
#   stated_behaviour   : the rectangular reload fails with a shape error, or loads in the stored (out, in)
#                        orientation, AND the square reload loads the stored orientation (its forward differs
#                        from the file-backed load).
#   expected_behaviour : both reloads give the same weight and forward as the file-backed load.
#   other              : anything else.
import json, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3 import Config
from exllamav3.modules import Linear

H, V = 256, 128
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     "model.layers.0.input_layernorm.weight": torch.ones(H).half(), "model.layers.0.post_attention_layernorm.weight": torch.ones(H).half(),
     "model.layers.0.mlp.gate_proj.weight": n(512, H), "model.layers.0.mlp.up_proj.weight": n(512, H), "model.layers.0.mlp.down_proj.weight": n(H, 512),
     "model.layers.0.self_attn.k_proj.weight": n(H, H), "model.layers.0.self_attn.v_proj.weight": n(H, H)}
t["model.layers.0.self_attn.q_proj.weight"] = n(512, H)   # rectangular: out 512, in 256
t["model.layers.0.self_attn.o_proj.weight"] = n(H, H)     # square, random so nonsymmetric
d = tempfile.mkdtemp()
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=H, intermediate_size=512, num_attention_heads=4, num_key_value_heads=4,
               num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512,
               bos_token_id=1, eos_token_id=2, tie_word_embeddings=False), open(d + "/config.json", "w"))
save_file(t, d + "/model.safetensors")
cfg = Config.from_directory(d); dev = torch.device("cuda:0")
x = (torch.randn(1, 8, H) * 0.5).half().cuda()

def case(key, fin, fout):
    lin = Linear(config=cfg, key=key, in_features=fin, out_features=fout, qmap=None)
    lin.load(dev)
    w_file = lin.inner.get_weight_tensor().clone()
    with torch.inference_mode(): y_file = lin.forward(x.clone(), {}).float()
    tensors = {}
    for m in lin: tensors.update(m.get_tensors())
    lin.unload()
    r = dict(file_weight_shape=list(w_file.shape), exported_shape=list(tensors[key + ".weight"].shape))
    cfg.stc.set_new_tensors(tensors)
    try:
        lin.load(dev, source=tensors)
        w_mem = lin.inner.get_weight_tensor()
        r["memory_weight_shape"] = list(w_mem.shape)
        r["memory_equals_file"] = bool(w_mem.shape == w_file.shape and torch.equal(w_mem, w_file))
        r["memory_equals_file_transposed"] = bool(w_mem.shape == w_file.T.shape and torch.equal(w_mem, w_file.T))
        with torch.inference_mode(): y_mem = lin.forward(x.clone(), {}).float()
        r["forward_max_abs_diff_vs_file"] = (y_mem - y_file).abs().max().item() if y_mem.shape == y_file.shape else None
        r["forward_shape"] = list(y_mem.shape)
    except Exception as e:
        r.update(exception_type=type(e).__name__, site=rt._site(e.__traceback__), message=str(e).splitlines()[0] if str(e) else "")
    finally:
        cfg.stc.set_new_tensors(None)
    print(key, r, flush=True)
    return r

try:
    rect = case("model.layers.0.self_attn.q_proj", H, 512)
    sq = case("model.layers.0.self_attn.o_proj", H, H)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit

notes = dict(rectangular=rect, square=sq)
rect_bad = "exception_type" in rect or rect.get("memory_equals_file_transposed")
sq_bad = sq.get("memory_equals_file_transposed") and (sq.get("forward_max_abs_diff_vs_file") or 0) > 1e-3
good = lambda r: r.get("memory_equals_file") and (r.get("forward_max_abs_diff_vs_file") or 0) == 0
if rect_bad and sq_bad: rt.report("stated_behaviour", etype=rect.get("exception_type"), esite=rect.get("site"), **notes)
elif good(rect) and good(sq): rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
