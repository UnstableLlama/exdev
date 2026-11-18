"""Placeholder modules for third-party packages that eval/compare_q*.py imports at module level
but that the code under test never calls. Any use of a stub is disclosed in result.json."""
import importlib.abc, importlib.machinery, sys, types
from unittest.mock import MagicMock
NAMES = {"gptqmodel", "aqlm", "awq", "vptq", "bitsandbytes", "transformers", "exllamav2", "datasets", "matplotlib", "adjustText", "llama_cpp", "gguf"}
class _M(types.ModuleType):
    __path__ = []
    def __getattr__(self, k):
        if k.startswith("__"): raise AttributeError(k)
        return MagicMock(name=f"{self.__name__}.{k}")
class F(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, name, path=None, target=None):
        return importlib.machinery.ModuleSpec(name, self, is_package=True) if name.split(".")[0] in NAMES else None
    def create_module(self, spec): return _M(spec.name)
    def exec_module(self, m): pass
sys.meta_path.insert(0, F())
