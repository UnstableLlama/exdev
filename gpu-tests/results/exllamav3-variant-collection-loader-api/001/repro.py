# Trigger: load a model whose Config uses a variant tensor collection. At e370ed28 there is no public st_variants
# keyword on Config (none found in models/config.py); variant collections are installed by model_init's --override
# path, which wraps config.stc in VariantSafetensorsCollection. This script does exactly what that path does:
# Config.from_directory(Qwen2.5-0.5B-Instruct), vstc = VariantSafetensorsCollection(config.stc),
# vstc.add_stc(["model.norm.weight"], SafetensorsCollection(<same dir>)), config.stc = vstc, then
# Model.from_config(config).load("cuda:0"). Upstream is not modified.
# Classification, fixed before running:
#   stated_behaviour   : load raises TypeError (unsupported keyword such as float2half) or AttributeError from the
#                        variant collection's loader interface.
#   expected_behaviour : the model loads.
#   other              : anything else.
import rt
rt.check_import()
from exllamav3 import Config, Model
from exllamav3.loader.safetensors import SafetensorsCollection, VariantSafetensorsCollection
M = "/home/unstable/exdev-gpu-work/models/Qwen2.5-0.5B-Instruct"
config = Config.from_directory(M)
vstc = VariantSafetensorsCollection(config.stc); vstc.add_stc(["model.norm.weight"], SafetensorsCollection(M)); config.stc = vstc
model = Model.from_config(config)
try:
    model.load("cuda:0", progressbar=False)
except (TypeError, AttributeError) as e:
    rt.report("stated_behaviour", e, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.report("expected_behaviour")
