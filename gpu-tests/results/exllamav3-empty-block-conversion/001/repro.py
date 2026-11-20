# Trigger: conversion reaches a fully disabled DeciLM (Nemotron NAS / "Ultra") block, i.e. a block whose
# attention and ffn are both no_op, and saving its empty tensor dictionary returns normally.
# No small public DeciLM checkpoint with no_op blocks exists, so a tiny random 3-layer checkpoint is
# generated here; layer 1 is fully disabled. (The Ultra configs first do this at block 9; the position
# does not matter to the code path, which is per-module.) Tokenizer files are copied from
# Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775 so calibration can run.
# Conversion runs through the repository's own CLI entry points (convert.py: parser, prepare, main),
# in-process so the exception site can be recorded. Upstream code is not modified.
import json, os, shutil, sys, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3.conversion.convert_model import parser, prepare, main

QWEN = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
H, HEADS, V, L, DISABLED = 256, 4, 151936, 3, 1
FFN_MULT = 3.0  # int(2 * 3.0 * 256 / 3) = 512, already a multiple of 256
IM = 512
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H)}
blocks = []
for i in range(L):
    p = f"model.layers.{i}"
    if i == DISABLED:
        blocks.append({"attention": {"no_op": True, "n_heads_in_group": None}, "ffn": {"no_op": True, "ffn_mult": None}})
        continue
    blocks.append({"attention": {"no_op": False, "n_heads_in_group": 1}, "ffn": {"no_op": False, "ffn_mult": FFN_MULT}})
    t[f"{p}.input_layernorm.weight"] = torch.ones(H).half()
    t[f"{p}.post_attention_layernorm.weight"] = torch.ones(H).half()
    for k in "qkv": t[f"{p}.self_attn.{k}_proj.weight"] = n(H, H)
    t[f"{p}.self_attn.o_proj.weight"] = n(H, H)
    t[f"{p}.mlp.up_proj.weight"] = n(IM, H); t[f"{p}.mlp.gate_proj.weight"] = n(IM, H); t[f"{p}.mlp.down_proj.weight"] = n(H, IM)

root = tempfile.mkdtemp()
src, work, out = (os.path.join(root, x) for x in ("src", "work", "out"))
os.makedirs(src)
for f in ("tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt"): shutil.copy(os.path.join(QWEN, f), src)
cfg = dict(architectures=["DeciLMForCausalLM"], model_type="nemotron-nas", hidden_size=H, num_attention_heads=HEADS,
           num_hidden_layers=L, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0,
           max_position_embeddings=2048, bos_token_id=151643, eos_token_id=151645, tie_word_embeddings=False,
           torch_dtype="float16", block_configs=blocks)
json.dump(cfg, open(os.path.join(src, "config.json"), "w"), indent=1)
save_file(t, os.path.join(src, "model.safetensors"))

argv = ["-i", src, "-w", work, "-o", out, "-b", "4", "-cr", "4", "-cc", "256", "-d", "0"]
print("convert.py", " ".join(argv), flush=True)
reached = False
try:
    a = parser.parse_args(argv)
    in_args, job_state, ok, err = prepare(a)
    if not ok:
        rt.report("did_not_run", message=f"prepare failed: {err}"); raise SystemExit
    main(in_args, job_state)
except ZeroDivisionError as e:
    saved = os.path.exists(os.path.join(work, "qtensors", f"model.layers.{DISABLED}.safetensors"))
    site = rt._site(e.__traceback__) or ""
    beh = "stated_behaviour" if site.startswith("exllamav3/conversion/convert_model.py") and saved else "other"
    rt.report(beh, e, empty_block_tensors_saved=saved, message=str(e)); raise SystemExit
except SystemExit:
    raise
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit

# Conversion finished: the disabled block was passed without division by zero.
saved = os.path.exists(os.path.join(work, "qtensors", f"model.layers.{DISABLED}.safetensors"))
outputs = sorted(os.listdir(out)) if os.path.isdir(out) else []
done = any(f.endswith(".safetensors") for f in outputs) and "config.json" in outputs
rt.report("expected_behaviour" if saved and done else "other", empty_block_tensors_saved=saved, output_files=outputs)
