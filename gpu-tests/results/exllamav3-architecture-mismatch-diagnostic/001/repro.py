# Trigger: instantiate a configuration class against a config.json whose single
# architecture differs from the class's arch_string, with assertions enabled.
import json, os, tempfile
import rt
rt.check_import()
from exllamav3.models.llama import LlamaConfig
assert __debug__, "assertions must be enabled"
d = tempfile.mkdtemp()
json.dump({"architectures": ["NotLlamaForCausalLM"]}, open(os.path.join(d, "config.json"), "w"))
try:
    LlamaConfig(d)
except NameError as e:
    rt.report("stated_behaviour" if "expect_arch" in str(e) else "other", e, message=str(e))
except AssertionError as e:
    m = str(e)
    ok = "NotLlamaForCausalLM" in m and "LlamaForCausalLM" in m.replace("NotLlamaForCausalLM", "")
    rt.report("expected_behaviour" if ok else "other", e, message=m)
except Exception as e:
    rt.report("other", e, message=str(e))
else:
    rt.report("other", note="no exception raised")
