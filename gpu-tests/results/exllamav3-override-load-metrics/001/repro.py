# Trigger: nonempty overrides with -lm/--load_metrics, reaching the metrics block of model_init.init.
# model_init.add_args / parse_args with -m Qwen2.5-0.5B-Instruct, -or <yaml> (one override: model.norm.weight from
# the same directory) and -lm, then model_init.init(args), exactly as CLIs such as examples/chat.py do.
# Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : AttributeError for 'metrics' on the variant collection, from exllamav3/model_init.py.
#   expected_behaviour : loader metrics print and init returns.
#   other              : anything else.
import argparse, os, tempfile
import rt
rt.check_import()
from exllamav3 import model_init
M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
y = os.path.join(tempfile.mkdtemp(), "ov.yaml")
open(y, "w").write(f"sources:\n  - id: a\n    model_dir: {M}\noverrides:\n  - key: model.norm.weight\n    source: a\n")
p = argparse.ArgumentParser(); model_init.add_args(p, cache=False)
args = p.parse_args(["-m", M, "-or", y, "-lm"])
try:
    model_init.init(args, load=True) if "load" in model_init.init.__code__.co_varnames else model_init.init(args)
except AttributeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if "metrics" in str(e) and site.startswith("exllamav3/model_init.py") else "other", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("expected_behaviour")
