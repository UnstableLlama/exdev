# Trigger: in a clean installation with earlier prerequisites satisfied (torch, the built native extension and
# the package's dependencies present), import exllamav3.modules.
# Classification, fixed before running:
#   stated_behaviour   : ModuleNotFoundError for exllamav3.util.tp_split, raised from exllamav3/modules/transformer.py.
#   expected_behaviour : exllamav3.modules imports and exposes TransformerBlock and ParallelDecoderBlock.
#   other              : anything else.
import os, sys
import rt
WT = os.path.realpath(os.environ["EXL3_WT"])
print("tp_split.py present in worktree:", os.path.exists(os.path.join(WT, "exllamav3", "util", "tp_split.py")), flush=True)
try:
    import exllamav3.modules as M
except ModuleNotFoundError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if "tp_split" in str(e) and site.startswith("exllamav3/modules/transformer.py") else "other", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("expected_behaviour" if hasattr(M, "TransformerBlock") and hasattr(M, "ParallelDecoderBlock") else "other")
