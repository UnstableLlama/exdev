# Trigger: size_to_longest_edge_and_patch_size(input_size=(230, 1), max_size=(224, 192), patch_size=(16, 32)).
# Called directly from exllamav3.util.vision in the worktree. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : the result exceeds max_size in some dimension (the ledger's transcription gives (240, 32)).
#   expected_behaviour : the result is patch-aligned and no larger than (224, 192) in each dimension.
#   other              : anything else.
import rt
rt.check_import()
from exllamav3.util.vision import size_to_longest_edge_and_patch_size as f
inp, mx, ps = (230, 1), (224, 192), (16, 32)
try:
    out = tuple(int(x) for x in f(inp, mx, ps))
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
aligned = all(o % p == 0 for o, p in zip(out, ps)); within = all(o <= m for o, m in zip(out, mx))
notes = dict(output=list(out), aligned=aligned, within_max=within)
if not within: rt.report("stated_behaviour", **notes)
elif aligned: rt.report("expected_behaviour", **notes)
else: rt.report("other", **notes)
