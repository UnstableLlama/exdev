# Trigger: tokenizer.json has truncation max_length 4096, and calibration's split_raw encodes whole input files
# for 100 rows of 2048 tokens.
# Fixture: a copy of Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775 (weights symlinked)
# whose tokenizer.json gets "truncation": {max_length: 4096, ...} (the field some published tokenizers carry).
# The repository's Tokenizer.from_config and conversion.calibration_data.get_default_calibration
# (cal_rows 100, cal_cols 2048) run unmodified; only the fixture file is changed.
# Classification, fixed before running:
#   stated_behaviour   : some calibration rows are shorter than 2048 tokens (the split_raw sources run out
#                        after the first 4096 tokens).
#   expected_behaviour : every calibration row is 2048 tokens wide.
#   other              : anything else.
import json, os, shutil, tempfile
import rt
rt.check_import()
from exllamav3 import Config, Tokenizer
from exllamav3.conversion.calibration_data import get_default_calibration
Q = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
d = tempfile.mkdtemp()
for f in os.listdir(Q):
    if f == "model.safetensors": os.symlink(os.path.join(Q, f), os.path.join(d, f))
    elif f != "tokenizer.json": shutil.copy(os.path.join(Q, f), d)
tj = json.load(open(os.path.join(Q, "tokenizer.json")))
tj["truncation"] = {"direction": "Right", "max_length": 4096, "strategy": "LongestFirst", "stride": 0}
json.dump(tj, open(os.path.join(d, "tokenizer.json"), "w"))
try:
    tok = Tokenizer.from_config(Config.from_directory(d))
    long_len = int(tok.encode("hello world " * 5000).shape[-1])
    rows = get_default_calibration({"cal_cols": 2048, "cal_rows": 100}, tok)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
widths = [int(r.shape[-1]) for r in rows]
short = [w for w in widths if w < 2048]
notes = dict(rows=len(widths), short_rows=len(short), short_widths=sorted(set(short)), encode_len_of_10000_token_text=long_len)
print(notes, flush=True)
if short: rt.report("stated_behaviour", **notes)
elif widths: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
