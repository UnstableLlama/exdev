# Trigger: supply --strategy q and reach its indexed top-level module.
# A tiny random 1-layer LlamaForCausalLM (Qwen2.5 tokenizer files) is converted with the repository's
# convert_model parser/prepare/main and --strategy q; the first transformer block is module index 1, which the
# one-segment strategy "q" addresses. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : conversion raises IndexError (or ValueError) from mod_strategy in
#                        exllamav3/conversion/convert_model.py when that module is reached.
#   expected_behaviour : the malformed value is rejected with an argument-validation error before modules run.
#   other              : anything else.
import json, os, shutil, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3.conversion.convert_model import parser, prepare, main
QWEN = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
H, IM, V = 128, 256, 151936
torch.manual_seed(0); n = lambda *s: (torch.randn(*s) * 0.05).half()
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     "model.layers.0.input_layernorm.weight": torch.ones(H).half(), "model.layers.0.post_attention_layernorm.weight": torch.ones(H).half(),
     "model.layers.0.mlp.gate_proj.weight": n(IM, H), "model.layers.0.mlp.up_proj.weight": n(IM, H), "model.layers.0.mlp.down_proj.weight": n(H, IM)}
for k in "qkvo": t[f"model.layers.0.self_attn.{k}_proj.weight"] = n(H, H)
root = tempfile.mkdtemp(); src, work, out = (os.path.join(root, x) for x in ("src", "work", "out")); os.makedirs(src)
for f in ("tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt"): shutil.copy(os.path.join(QWEN, f), src)
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=2, num_key_value_heads=2,
               num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=2048,
               bos_token_id=151643, eos_token_id=151645, tie_word_embeddings=False, torch_dtype="float16"), open(os.path.join(src, "config.json"), "w"))
save_file(t, os.path.join(src, "model.safetensors"))
argv = ["-i", src, "-w", work, "-o", out, "-b", "4", "-cr", "4", "-cc", "256", "--strategy", "q"]
if any("--devices" in a.option_strings for a in parser._actions): argv += ["-d", "0"]
try:
    a = parser.parse_args(argv); in_args, job_state, ok, err = prepare(a)
    if not ok: rt.report("expected_behaviour", stage="prepare", message=err); raise SystemExit
    main(in_args, job_state)
except SystemExit:
    raise
except (IndexError, ValueError) as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if site.startswith("exllamav3/conversion/convert_model.py") else "other", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("other", note="conversion completed with --strategy q")
