# Trigger: get_storage_info is called with arguments already cached under lcpp_get_storage_info before the change
# at ab875ba73053 (which fixed the GGUF accounting when output.weight precedes token_embd.weight).
# The same script runs first at the parent 9a24e0ce520a ("priming" role, recorded as affected) and then at
# ab875ba73053, with one fixed GGUF path inside this result directory (output.weight before token_embd.weight;
# the llamacpp-embedding-order fixture). eval/compare_q_llamacpp.get_storage_info's own @disk_lru_cache stores
# results in __disk_lru_cache__ beside this script, so the second run sees the first run's cache entry, exactly
# as a user upgrading in place would. Each run also computes the value with a fresh, never-cached path.
# Upstream is not modified.
# Classification, fixed before running (meaningful at ab875ba73053, where the code is fixed):
#   stated_behaviour   : the cached-path result differs from the fresh-path result (stale pre-change tuple returned).
#   expected_behaviour : the cached-path result equals the fresh-path result.
#   other              : anything else (e.g. no cache entry existed).
import os, shutil, sys, tempfile
import numpy as np
import rt
rt.check_import()
WT = os.environ["EXL3_WT"]; sys.path.insert(0, os.path.join(WT, "eval"))
import gguf
from compare_q_llamacpp import get_storage_info
here = os.path.dirname(os.path.abspath(__file__)); fixed = os.path.join(here, "fixture", "a_output_first.gguf")
V, H = 64, 32
rng = np.random.default_rng(0)
emb = rng.standard_normal((V, H)).astype(np.float16); out = rng.standard_normal((V, H)).astype(np.float16); q = rng.standard_normal((H, H)).astype(np.float32)
def write(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    w = gguf.GGUFWriter(path, "llama")
    for name, a in (("output.weight", out), ("token_embd.weight", emb), ("blk.0.attn_q.weight", q)): w.add_tensor(name, a)
    w.write_header_to_file(); w.write_kv_data_to_file(); w.write_tensors_to_file(); w.close()
cache_dir = os.path.join(here, "__disk_lru_cache__")
had_cache = os.path.isdir(cache_dir) and any(f.startswith("lcpp_get_storage_info") for f in os.listdir(cache_dir))
if not os.path.exists(fixed): write(fixed)
fresh = os.path.join(tempfile.mkdtemp(), "a_output_first.gguf"); write(fresh)
r_cached, r_fresh = get_storage_info(fixed), get_storage_info(fresh)
notes = dict(cache_existed_before_call=had_cache, result_fixed_path=list(r_cached), result_fresh_path=list(r_fresh))
print(notes, flush=True)
if not had_cache: rt.report("other", note="priming run: no cache entry existed yet", **notes)
elif tuple(r_cached) != tuple(r_fresh): rt.report("stated_behaviour", **notes)
else: rt.report("expected_behaviour", **notes)
