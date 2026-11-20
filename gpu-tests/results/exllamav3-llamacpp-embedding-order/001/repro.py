# Trigger: a positive-sized output.weight precedes token_embd.weight in GGUFReader.tensors.
# Fixture: two tiny GGUF files written with gguf.GGUFWriter (gguf 0.17.0), identical tensors in two orders:
#   A: output.weight (F16), token_embd.weight (F16), blk.0.attn_q.weight (F32)
#   B: token_embd.weight (F16), output.weight (F16), blk.0.attn_q.weight (F32)
# No norm tensors, because the fix also starts excluding *norm.weight, which would change results for an
# unrelated reason. eval/compare_q_llamacpp.get_storage_info from the worktree is called on each file
# (unmodified, including its disk_lru_cache; each run uses fresh temporary paths so no cached value is reused).
#
# Classification, fixed before running:
#   stated_behaviour   : order A counts token_embd.weight in the layer aggregate (A's sum differs from B's,
#                        and A's layer bpw equals the F16/F32 mix of embedding + attn_q).
#   expected_behaviour : A and B give identical results.
#   other              : anything else.
import os, sys, tempfile
import numpy as np
import rt
rt.check_import()
WT = os.environ["EXL3_WT"]; sys.path.insert(0, os.path.join(WT, "eval"))
import gguf
from compare_q_llamacpp import get_storage_info

V, H = 64, 32
rng = np.random.default_rng(0)
emb = rng.standard_normal((V, H)).astype(np.float16); out = rng.standard_normal((V, H)).astype(np.float16)
q = rng.standard_normal((H, H)).astype(np.float32)
def write(path, order):
    w = gguf.GGUFWriter(path, "llama")
    for name in order: w.add_tensor(name, {"token_embd.weight": emb, "output.weight": out, "blk.0.attn_q.weight": q}[name])
    w.write_header_to_file(); w.write_kv_data_to_file(); w.write_tensors_to_file(); w.close()
d = tempfile.mkdtemp()
pa, pb = os.path.join(d, "a_output_first.gguf"), os.path.join(d, "b_embd_first.gguf")
write(pa, ["output.weight", "token_embd.weight", "blk.0.attn_q.weight"])
write(pb, ["token_embd.weight", "output.weight", "blk.0.attn_q.weight"])
try:
    from gguf import GGUFReader
    print("A order:", [t.name for t in GGUFReader(pa).tensors], flush=True)
    ra, rb = get_storage_info(pa), get_storage_info(pb)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
print("A:", ra, "B:", rb, flush=True)
mix = (emb.size * 16 + q.size * 32) / (emb.size + q.size)
notes = dict(result_output_first=list(ra), result_embd_first=list(rb), mixed_layer_bpw_if_embedding_counted=mix)
if tuple(ra) == tuple(rb): rt.report("expected_behaviour", **notes)
elif abs(ra[0] - mix) < 1e-9 and ra[2] > rb[2]: rt.report("stated_behaviour", **notes)
else: rt.report("other", **notes)
