# Trigger: pass any list, including [], as FormatronFilter.vocab_processors.
# FormatronFilter(tokenizer, formatter_builder=FormatterBuilder(), vocab_processors=[]) with the Qwen2.5-0.5B-
# Instruct tokenizer (@ 7ae557604adf67be50417f59c2c2f167def9a775); formatron 0.5.0 as installed. A control
# with vocab_processors=None is also constructed. Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : TypeError "unhashable type: 'list'" (lru_cache key) for the [] case while None works.
#   expected_behaviour : the [] case constructs.
#   other              : anything else.
import rt
rt.check_import()
from exllamav3 import Config, Tokenizer, FormatronFilter
from formatron.formatter import FormatterBuilder
tok = Tokenizer.from_config(Config.from_directory("/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"))
def make(vp):
    f = FormatterBuilder(); f.append_line("x")
    return FormatronFilter(tok, formatter_builder=f, vocab_processors=vp)
try:
    make(None); ctl = "ok"
except Exception as e:
    ctl = f"{type(e).__name__}: {e}"
try:
    make([])
except TypeError as e:
    rt.report("stated_behaviour" if "unhashable" in str(e) and ctl == "ok" else "other", e, control_none=ctl, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, control_none=ctl, message=str(e)); raise SystemExit
rt.report("expected_behaviour", control_none=ctl)
