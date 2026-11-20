# Trigger: conversion/compilation traverses enough per-module qtensors files for cached handles to exhaust the
# stream (open-file) limit.
# Fixture: a tiny random 60-layer LlamaForCausalLM (hidden 128) with Qwen2.5-0.5B-Instruct tokenizer files,
# converted by the repository's own convert_model parser/prepare/main in-process (62 modules -> 62 qtensors
# files read during compilation). Before conversion, CUDA is initialised and the process's open descriptors
# are counted; the soft RLIMIT_NOFILE is then set to that count + 30, well below the module count but with
# headroom for ordinary use. The limit is the only change; upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : conversion fails with OSError/RuntimeError "Too many open files" (EMFILE).
#   expected_behaviour : conversion completes and writes the output model.
#   other              : anything else.
import errno, json, os, resource, shutil, tempfile, traceback
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3.conversion.convert_model import parser, prepare, main
QWEN = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
H, HEADS, IM, V, L = 128, 2, 256, 151936, 60
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
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=HEADS, num_key_value_heads=HEADS,
               num_hidden_layers=L, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=2048,
               bos_token_id=151643, eos_token_id=151645, tie_word_embeddings=False, torch_dtype="float16"), open(os.path.join(src, "config.json"), "w"))
save_file(t, os.path.join(src, "model.safetensors")); del t
torch.zeros(1, device="cuda:0"); torch.cuda.synchronize()
base = len(os.listdir("/proc/self/fd")); soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
limit = base + 30
resource.setrlimit(resource.RLIMIT_NOFILE, (limit, hard))
print(f"open fds after CUDA init: {base}; RLIMIT_NOFILE soft {soft} -> {limit}; modules: {L + 2}", flush=True)
notes = dict(baseline_fds=base, soft_limit=limit, original_soft_limit=soft, modules=L + 2)
try:
    a = parser.parse_args(["-i", src, "-w", work, "-o", out, "-b", "4", "-cr", "4", "-cc", "256", "-d", "0"])
    in_args, job_state, ok, err = prepare(a)
    assert ok, err
    main(in_args, job_state)
except Exception as e:
    emfile = "Too many open files" in str(e) or getattr(e, "errno", None) == errno.EMFILE
    qn = len(os.listdir(os.path.join(work, "qtensors"))) if os.path.isdir(os.path.join(work, "qtensors")) else 0
    rt.report("stated_behaviour" if emfile else "other", e, qtensors_files_written=qn, message=str(e).splitlines()[0] if str(e) else "", **notes); raise SystemExit
outs = sorted(os.listdir(out)) if os.path.isdir(out) else []
rt.report("expected_behaviour" if any(f.endswith(".safetensors") for f in outs) else "other", output_files=outs, **notes)
