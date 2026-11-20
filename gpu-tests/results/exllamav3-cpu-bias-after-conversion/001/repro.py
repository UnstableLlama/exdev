# Trigger: convert a GPU-resident LinearFP16 with a non-None bias through the converter's swap_cpu path, then
# execute the converted layer on GPU.
# Fixture: a tiny random 1-layer Qwen2ForCausalLM (q/k/v projections carry biases, as in real Qwen2 checkpoints)
# with Qwen2.5-0.5B-Instruct tokenizer files, converted with the repository's convert_model parser/prepare/main
# on cuda:0. After quantizing a module the converter itself runs it forward on GPU ("advance state"), which
# executes the converted biased layers. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : RuntimeError about tensors on different devices (cpu vs cuda) from the converted
#                        layer's bias addition during conversion.
#   expected_behaviour : conversion completes.
#   other              : anything else.
import json, os, shutil, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3.conversion.convert_model import parser, prepare, main
QWEN = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
H, HEADS, IM, V = 128, 2, 256, 151936
torch.manual_seed(0); n = lambda *s: (torch.randn(*s) * 0.05).half()
p = "model.layers.0"
t = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     f"{p}.input_layernorm.weight": torch.ones(H).half(), f"{p}.post_attention_layernorm.weight": torch.ones(H).half(),
     f"{p}.mlp.gate_proj.weight": n(IM, H), f"{p}.mlp.up_proj.weight": n(IM, H), f"{p}.mlp.down_proj.weight": n(H, IM)}
for k in "qkv": t[f"{p}.self_attn.{k}_proj.weight"] = n(H, H); t[f"{p}.self_attn.{k}_proj.bias"] = n(H)
t[f"{p}.self_attn.o_proj.weight"] = n(H, H)
root = tempfile.mkdtemp(); src, work, out = (os.path.join(root, x) for x in ("src", "work", "out")); os.makedirs(src)
for f in ("tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt"): shutil.copy(os.path.join(QWEN, f), src)
json.dump(dict(architectures=["Qwen2ForCausalLM"], hidden_size=H, intermediate_size=IM, num_attention_heads=HEADS, num_key_value_heads=HEADS,
               num_hidden_layers=1, vocab_size=V, hidden_act="silu", rms_norm_eps=1e-6, rope_theta=10000.0, max_position_embeddings=2048,
               bos_token_id=151643, eos_token_id=151645, tie_word_embeddings=False, torch_dtype="float16"), open(os.path.join(src, "config.json"), "w"))
save_file(t, os.path.join(src, "model.safetensors"))
argv = ["-i", src, "-w", work, "-o", out, "-b", "4", "-cr", "4", "-cc", "256"]
if any("--devices" in a.option_strings for a in parser._actions): argv += ["-d", "0"]
try:
    a = parser.parse_args(argv); in_args, job_state, ok, err = prepare(a); assert ok, err
    main(in_args, job_state)
except RuntimeError as e:
    dev = "device" in str(e) and "cpu" in str(e) and "cuda" in str(e)
    rt.report("stated_behaviour" if dev else "other", e, message=str(e).splitlines()[0]); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e).splitlines()[0] if str(e) else ""); raise SystemExit
rt.report("expected_behaviour", output_files=sorted(os.listdir(out)))
