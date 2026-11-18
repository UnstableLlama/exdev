# Trigger: import exllamav3 in an environment with the declared runtime dependencies and no Transformers.
import importlib.util
import rt
assert importlib.util.find_spec("transformers") is None, "transformers must be absent for this test"
try:
    rt.check_import()
except ModuleNotFoundError as e:
    rt.report("stated_behaviour" if e.name == "transformers" else "other", e, missing=e.name, message=str(e))
except Exception as e:
    rt.report("other", e, message=str(e))
else:
    rt.report("expected_behaviour", note="import exllamav3 succeeded without transformers")
