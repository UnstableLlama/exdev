# Trigger: a tokenizer whose actual_vocab_size exceeds raw_vocab_size; construction builds the id-to-piece list
# with and without special tokens.
# Fixture (disclosed): a copy of Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775 (weights
# symlinked) whose tokenizer_config.json gains one special added token, id 151700 "<|extra_x|>", beyond the base
# tokenizer's raw_vocab_size, as tokenizers with config-only added tokens have. Tokenizer.from_config runs
# unmodified; the ordinary id-to-piece list length and piece_to_id for the added piece are checked.
# Classification, fixed before running:
#   stated_behaviour   : the ordinary list is longer than actual_vocab_size (extension appended twice) or
#                        piece_to_id["<|extra_x|>"] != 151700.
#   expected_behaviour : list length == actual_vocab_size and piece_to_id["<|extra_x|>"] == 151700.
#   other              : anything else.
import json, os, shutil, tempfile
import rt
rt.check_import()
from exllamav3 import Config, Tokenizer
Q = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"; d = tempfile.mkdtemp()
for f in os.listdir(Q):
    if f == "model.safetensors": os.symlink(os.path.join(Q, f), os.path.join(d, f))
    elif f != "tokenizer_config.json": shutil.copy(os.path.join(Q, f), d)
tc = json.load(open(os.path.join(Q, "tokenizer_config.json")))
tc.setdefault("added_tokens_decoder", {})["151700"] = {"content": "<|extra_x|>", "lstrip": False, "normalized": False, "rstrip": False, "single_word": False, "special": True}
json.dump(tc, open(os.path.join(d, "tokenizer_config.json"), "w"))
tok = Tokenizer.from_config(Config.from_directory(d))
lst = tok.get_id_to_piece_list(); p2i = tok.get_piece_to_id_dict()
notes = dict(raw_vocab_size=tok.raw_vocab_size(), actual_vocab_size=tok.actual_vocab_size, ordinary_list_len=len(lst),
             with_special_len=len(tok.get_id_to_piece_list(True)), piece_to_id_extra=p2i.get("<|extra_x|>"),
             extra_positions=[i for i, p in enumerate(lst) if p == "<|extra_x|>"])
print(notes, flush=True)
if notes["actual_vocab_size"] <= notes["raw_vocab_size"]: rt.report("other", note="fixture did not extend the vocabulary", **notes)
elif len(lst) > tok.actual_vocab_size or p2i.get("<|extra_x|>") != 151700: rt.report("stated_behaviour", **notes)
else: rt.report("expected_behaviour", **notes)
