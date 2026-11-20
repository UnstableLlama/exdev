# Trigger: conversion is interrupted after ckpt is renamed to ckpt_old but before ckpt_new is renamed to ckpt,
# then resume is requested.
# The interruption point lies between two os.rename calls and cannot be hit without patching, so the directory
# state is produced from a real run (disclosed): a tiny random 4-layer LlamaForCausalLM (Qwen2.5 tokenizer
# files) is converted with the repository's convert_model parser/prepare/main, checkpointing after every module
# (-cpi 0) up to module index 3 (-lcpi 3). That leaves work/ckpt (latest) and work/ckpt_old (previous). Renaming
# work/ckpt to work/ckpt_new gives exactly the state after `rename(ckpt, ckpt_old)` and before
# `rename(ckpt_new, ckpt)`. Then the CLI path is run with -w work -resume.
# Classification, fixed before running:
#   stated_behaviour   : resume fails reading ckpt/job.json (missing file), with ckpt recreated empty.
#   expected_behaviour : resume locates ckpt_new/ckpt_old and continues (completes the conversion).
#   other              : anything else.
import json, os, shutil, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3.conversion.convert_model import parser, prepare, main
QWEN = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
H, IM, V, L = 128, 256, 151936, 4
torch.manual_seed(0)
n = lambda *s: (torch.randn(*s) * 0.05).half()
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H)}
for i in range(L):
    p = f"model.layers.{i}"
    t[f"{p}.input_layernorm.weight"] = torch.ones(H).half(); t[f"{p}.post_attention_layernorm.weight"] = torch.ones(H).half()
    for k in "qkvo": t[f"{p}.self_attn.{k}_proj.weight"] = n(H, H)
    t[f"{p}.mlp.gate_proj.weight"] = n(IM, H); t[f"{p}.mlp.up_proj.weight"] = n(IM, H); t[f"{p}.mlp.down_proj.weight"] = n(H, IM)
root = tempfile.mkdtemp(); src, work, out = (os.path.join(root, x) for x in ("src", "work", "out")); os.makedirs(src)
for f in ("tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt"): shutil.copy(os.path.join(QWEN, f), src)
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=2, num_key_value_heads=2,
               num_hidden_layers=L, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=2048,
               bos_token_id=151643, eos_token_id=151645, tie_word_embeddings=False, torch_dtype="float16"), open(os.path.join(src, "config.json"), "w"))
save_file(t, os.path.join(src, "model.safetensors"))
def run(argv):
    a = parser.parse_args(argv); in_args, job_state, ok, err = prepare(a)
    if not ok: raise RuntimeError(f"prepare: {err}")
    main(in_args, job_state)
try:
    run(["-i", src, "-w", work, "-o", out, "-b", "4", "-cr", "4", "-cc", "256", "-cpi", "0", "-lcpi", "3"])
except Exception as e:
    rt.report("did_not_run", e, stage="first conversion", message=str(e)); raise SystemExit
before = {d: sorted(os.listdir(os.path.join(work, d))) for d in ("ckpt", "ckpt_old", "ckpt_new") if os.path.isdir(os.path.join(work, d))}
print("after first run:", before, flush=True)
if "ckpt" not in before or "ckpt_old" not in before:
    rt.report("did_not_run", note="first run did not leave ckpt and ckpt_old", dirs=before); raise SystemExit
os.rename(os.path.join(work, "ckpt"), os.path.join(work, "ckpt_new"))
gap = {d: sorted(os.listdir(os.path.join(work, d))) for d in ("ckpt", "ckpt_old", "ckpt_new") if os.path.isdir(os.path.join(work, d))}
print("gap state:", gap, flush=True)
shutil.rmtree(out, ignore_errors=True)
try:
    run(["-w", work, "-resume"])
except (FileNotFoundError, OSError) as e:
    ck = os.path.join(work, "ckpt")
    rt.report("stated_behaviour" if "job.json" in str(e) else "other", e, gap_state=gap,
              ckpt_recreated=os.path.isdir(ck), ckpt_contents=sorted(os.listdir(ck)) if os.path.isdir(ck) else None, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, gap_state=gap, message=str(e)); raise SystemExit
outs = sorted(os.listdir(out)) if os.path.isdir(out) else []
rt.report("expected_behaviour" if any(f.endswith(".safetensors") for f in outs) else "other", gap_state=gap, output_files=outs)
