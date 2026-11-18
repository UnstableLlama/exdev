"""Load eval/compare_q.py from the worktree with third-party imports stubbed."""
import argparse, json, os, sys, tempfile
import stubmods
WT = os.environ["EXL3_WT"]; TMP = tempfile.mkdtemp()
sys.argv = [os.path.join(TMP, "compare_q.py")]          # the disk cache lives beside argv[0]
sys.path.insert(0, WT + "/eval")
import compare_q
DATA = {"tokenize_fn": "transformers", "tokenizer_dir": "unused", "dataset": "wiki2", "eval_stride": 16, "eval_len": 16}
SPEC = {"load_fn": "probe", "fwd_fn": "probe", "model_dir": "unused", "label": "probe"}
def args():
    d, m = os.path.join(TMP, "d.json"), os.path.join(TMP, "m.json")
    json.dump(DATA, open(d, "w")); json.dump([SPEC], open(m, "w"))
    return argparse.Namespace(dataspec=d, modelspec=[m], clear_cache=False, plot=False, vram=False, max_x=999999, max_y=999999, title="t", kld=False, mask=None)
