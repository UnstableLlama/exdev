# Trigger: follow the image-dump option description in doc/convert.md ("-img / image_dump: Save all tensors as
# images"). Checks (1) which option strings the converter's parser registers, and (2) what a conversion with
# -img actually writes: a tiny random 1-layer LlamaForCausalLM (Qwen2.5 tokenizer files) is converted with the
# repository's convert_model parser/prepare/main and -img, and the image files in the work directory are
# compared with the tensors of the source model. Upstream is not modified.
# Classification, fixed before running (on the "all tensors" claim, the part a run can check):
#   stated_behaviour   : images are written only for some tensors (the quantized Linear targets), not all.
#   expected_behaviour : an image is written for every source tensor.
#   other              : anything else.
import glob, json, os, shutil, tempfile
import torch
from safetensors.torch import save_file
import rt
rt.check_import()
from exllamav3.conversion.convert_model import parser, prepare, main
WT = os.environ["EXL3_WT"]; QWEN = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
doc = open(os.path.join(WT, "doc", "convert.md")).read()
doc_line = [l for l in doc.splitlines() if "image_dump" in l]
opts = [a.option_strings for a in parser._actions if "image_dump" in a.dest]
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
argv = ["-i", src, "-w", work, "-o", out, "-b", "4", "-cr", "4", "-cc", "256", "-img"]
if any("--devices" in a.option_strings for a in parser._actions): argv += ["-d", "0"]
try:
    a = parser.parse_args(argv); in_args, job_state, ok, err = prepare(a); assert ok, err
    main(in_args, job_state)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
imgs = sorted(os.path.relpath(p, work) for p in glob.glob(os.path.join(work, "**", "*.png"), recursive=True))
notes = dict(doc_line=doc_line, parser_option_strings=opts, source_tensors=len(t), images_written=len(imgs), image_files=imgs)
print(notes, flush=True)
if 0 < len(imgs) < len(t): rt.report("stated_behaviour", **notes)
elif len(imgs) >= len(t): rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
