# Trigger: import exllamav3 in an environment where tkinter cannot be imported, without enabling visualization.
# Environment manipulation, disclosed: no_tkinter/tkinter.py (beside this file) is placed first on sys.path and
# raises ImportError on import, modelling a Python without Tk. Upstream code is not modified or stubbed;
# only the stdlib GUI module is made unavailable. A control first confirms that tkinter is then unimportable.
# Classification, fixed before running:
#   stated_behaviour   : importing exllamav3 raises ImportError originating from the tkinter import
#                        (through exllamav3/generator/visualizer.py).
#   expected_behaviour : exllamav3 imports and Generator is available.
#   other              : anything else.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "no_tkinter"))
import rt
try:
    import tkinter
    rt.report("did_not_run", message="shim did not take effect; tkinter imported"); raise SystemExit
except ImportError:
    pass
sys.modules.pop("tkinter", None)
try:
    import exllamav3
    from exllamav3 import Generator
except ImportError as e:
    import traceback
    frames = [f"{os.path.relpath(f.filename, os.environ['EXL3_WT'])}:{f.lineno}" for f in traceback.extract_tb(e.__traceback__) if os.path.realpath(f.filename).startswith(os.path.realpath(os.environ["EXL3_WT"]))]
    hit = "tkinter" in str(e) and any("visualizer.py" in f for f in frames)
    rt.report("stated_behaviour" if hit else "other", e, worktree_frames=frames, message=str(e)); raise SystemExit
except Exception as e:
    rt.report("other", e, message=str(e)); raise SystemExit
rt.check_import()
rt.report("expected_behaviour", generator=Generator.__module__)
