# Trigger: with assertions enabled, Job.prepare_for_queue rejects a job whose required pages exceed the cache
# capacity and evaluates its assertion message.
# Fixture: Qwen/Qwen2.5-0.5B-Instruct @ 7ae557604adf67be50417f59c2c2f167def9a775 unquantized, Cache with
# max_num_tokens=512; a job with a ~700-token prompt and max_new_tokens=64 is enqueued on the Generator.
# Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : AttributeError naming max_total_tokens, raised from exllamav3/generator/job.py.
#   expected_behaviour : AssertionError whose message carries the cache-capacity diagnostic (mentions tokens).
#   other              : anything else (including the job being accepted).
import sys
import torch
import rt
rt.check_import()
assert sys.flags.optimize == 0
from exllamav3 import Model, Config, Cache, Tokenizer, Generator, Job
M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
try:
    config = Config.from_directory(M); model = Model.from_config(config)
    cache = Cache(model, max_num_tokens=512); model.load(progressbar=False)
    tok = Tokenizer.from_config(config); gen = Generator(model=model, cache=cache, tokenizer=tok)
except Exception as e:
    rt.report("did_not_run", e, message=str(e)); raise SystemExit
ids = tok.encode("word " * 700)
print("prompt tokens:", ids.shape[-1], flush=True)
try:
    gen.enqueue(Job(input_ids=ids, max_new_tokens=64))
except AttributeError as e:
    site = rt._site(e.__traceback__) or ""
    rt.report("stated_behaviour" if "max_total_tokens" in str(e) and site.startswith("exllamav3/generator/job.py") else "other", e, message=str(e)); raise SystemExit
except AssertionError as e:
    rt.report("expected_behaviour" if "token" in str(e) else "other", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("other", message="job accepted", prompt_tokens=int(ids.shape[-1]))
