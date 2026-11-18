"""Run the unmodified eval/compare_q*.py command-line scripts in a subprocess, with real dependencies."""
import json, os, subprocess, sys, tempfile
import chatdrv
WT = os.environ["EXL3_WT"]; TMP = tempfile.mkdtemp()
M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
DATA = os.path.join(TMP, "data.json"); SPEC = os.path.join(TMP, "model.json")
json.dump({"tokenize_fn": "transformers", "tokenizer_dir": M, "dataset": "wiki2", "eval_stride": 256, "eval_len": 256, "max_rows": 2}, open(DATA, "w"))
json.dump([{"load_fn": "exllamav3", "fwd_fn": "exllamav3", "model_dir": M, "label": "qwen2.5-0.5b"}], open(SPEC, "w"))
def run(script, *args):
    r = subprocess.run([sys.executable, f"{WT}/eval/{script}", *args], capture_output=True, text=True, timeout=800)
    t = r.stdout + "\n" + r.stderr
    print(f"$ {script} {' '.join(args)}\n[returncode {r.returncode}]\n{t[-5000:]}", flush=True)
    return r.returncode, t
def tb(t): return chatdrv.tb_info(t, WT)
