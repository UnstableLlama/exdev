# Trigger: select --length equal to the encoded corpus length.
# The corpus length N is computed here with the repository's Tokenizer on the same wikitext-2-raw-v1 test text the
# script builds ("\n\n".join of the test split, offline cache); then the unmodified script runs with -l N -r 1.
# A full window [0, N) exists. (The script would need to run the model on N tokens to score it; the classification
# only concerns whether a window is produced.) Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the script fails with RuntimeError from torch.cat on an empty list (no window produced).
#   expected_behaviour : a window is produced (the script proceeds to scoring it, whatever happens then) or a clear
#                        error explains that no full window fits.
#   other              : anything else.
import os, re, subprocess, sys
import rt
rt.check_import()
WT = os.environ["EXL3_WT"]; M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
SCRIPT = os.path.join(WT, "eval", "ppl_transformers.py")
def run(*args):
    env = dict(os.environ, HF_DATASETS_OFFLINE="1", HF_HUB_OFFLINE="1")
    r = subprocess.run([sys.executable, SCRIPT, "-m", M, *args], capture_output=True, text=True, timeout=900, env=env)
    sys.stdout.write(r.stdout[-3000:]); sys.stderr.write(r.stderr[-3000:])
    err = (r.stderr.strip().splitlines() or [""])[-1]
    return r.returncode, r.stdout, err
os.environ["HF_DATASETS_OFFLINE"] = "1"
from datasets import load_dataset
from exllamav3 import Config, Tokenizer
tok = Tokenizer.from_config(Config.from_directory(M))
N = int(tok.encode("\n\n".join(load_dataset("wikitext", "wikitext-2-raw-v1", split="test")["text"])).shape[-1])
print("corpus tokens:", N, flush=True)
rc, out, err = run("-l", str(N), "-r", "1")
notes = dict(corpus_tokens=N, returncode=rc, last_stderr_line=err)
if rc != 0 and "torch.cat" in err or (rc != 0 and "expected a non-empty list" in err): rt.report("stated_behaviour", etype="RuntimeError", **notes)
elif "Evaluating" in out or "no full window" in err.lower(): rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
