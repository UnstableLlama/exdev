# Trigger: return_logits with a vocabulary whose size is a multiple of 32 but not 128 (here 160).
# Fixture: a tiny random 1-layer LlamaForCausalLM with vocab_size 160 and a 160-entry word-level tokenizer built with
# the tokenizers library (t0..t159; t0 = <unk>, t1 = bos, t2 = eos), so tokenizer and model vocabularies agree. A
# 4-token greedy job with return_logits=True runs through the repository's Generator. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the job fails with a shape/size error when held logits (160 wide) receive the head output
#                        (256 wide), or the returned logits are not 160 wide.
#   expected_behaviour : the job completes and returns logits of width 160 (or the documented vocab width).
#   other              : anything else.
import json, os, tempfile
import torch
from safetensors.torch import save_file
from tokenizers import Tokenizer as HFT, models, pre_tokenizers
import rt
rt.check_import()
from exllamav3 import Model, Config, Cache, Tokenizer, Generator, Job
from exllamav3.generator.sampler import ArgmaxSampler
H, V = 256, 160
d = tempfile.mkdtemp()
t = HFT(models.WordLevel({f"t{i}": i for i in range(V)}, unk_token="t0")); t.pre_tokenizer = pre_tokenizers.WhitespaceSplit(); t.save(os.path.join(d, "tokenizer.json"))
json.dump({"bos_token": "t1", "eos_token": "t2", "unk_token": "t0", "tokenizer_class": "PreTrainedTokenizerFast"}, open(os.path.join(d, "tokenizer_config.json"), "w"))
torch.manual_seed(0); n = lambda *s: (torch.randn(*s) * 0.05).half()
w = {"model.embed_tokens.weight": n(V, H), "model.norm.weight": torch.ones(H).half(), "lm_head.weight": n(V, H),
     "model.layers.0.input_layernorm.weight": torch.ones(H).half(), "model.layers.0.post_attention_layernorm.weight": torch.ones(H).half(),
     "model.layers.0.mlp.gate_proj.weight": n(512, H), "model.layers.0.mlp.up_proj.weight": n(512, H), "model.layers.0.mlp.down_proj.weight": n(H, 512)}
for k in "qkvo": w[f"model.layers.0.self_attn.{k}_proj.weight"] = n(H, H)
json.dump(dict(architectures=["LlamaForCausalLM"], hidden_size=H, intermediate_size=512, num_attention_heads=4, num_key_value_heads=4, num_hidden_layers=1,
               vocab_size=V, hidden_act="silu", rms_norm_eps=1e-5, rope_theta=10000.0, max_position_embeddings=512, bos_token_id=1, eos_token_id=2,
               tie_word_embeddings=False), open(os.path.join(d, "config.json"), "w"))
save_file(w, os.path.join(d, "model.safetensors"))
try:
    config = Config.from_directory(d); model = Model.from_config(config); cache = Cache(model, max_num_tokens=1024); model.load(progressbar=False)
    tok = Tokenizer.from_config(config); gen = Generator(model=model, cache=cache, tokenizer=tok)
    with torch.inference_mode(): head_w = model.forward(torch.tensor([[5, 6, 7]])).shape[-1]
    print("head output width:", head_w, "generator padded_vocab_size:", gen.padded_vocab_size, flush=True)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
try:
    gen.enqueue(Job(input_ids=torch.tensor([[5, 6, 7, 8]]), max_new_tokens=4, sampler=ArgmaxSampler(), return_logits=True))
    widths = []
    while gen.num_remaining_jobs():
        for r in gen.iterate():
            if r.get("logits") is not None: widths.append(int(r["logits"].shape[-1]))
except RuntimeError as e:
    rt.report("stated_behaviour", e, head_width=head_w, padded_vocab_size=gen.padded_vocab_size, message=str(e).splitlines()[0]); raise SystemExit
except Exception as e:
    rt.report("other", e, head_width=head_w, message=str(e)); raise SystemExit
notes = dict(head_width=head_w, padded_vocab_size=gen.padded_vocab_size, returned_logit_widths=widths)
rt.report("expected_behaviour" if widths and all(x == V for x in widths) else "stated_behaviour" if widths else "other", **notes)
