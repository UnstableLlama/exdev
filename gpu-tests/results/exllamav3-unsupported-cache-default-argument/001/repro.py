# Trigger: run eval/longctx.py as a script (its imports succeed in this environment: real transformers).
# The script is run unmodified with runpy as __main__ and argv ['-h'], so argparse prints help and exits
# right after all arguments are registered; evaluation itself (which needs a model) is not started.
# Classification, fixed before running:
#   stated_behaviour   : TypeError from model_init.add_args (unexpected keyword default_cache_size), raised
#                        before parse_args.
#   expected_behaviour : arguments register, parse_args runs (-h prints help, SystemExit 0), and the help
#                        shows the 65536 cache default.
#   other              : anything else.
import contextlib, io, os, runpy, sys, traceback
import rt
rt.check_import()
WT = os.environ["EXL3_WT"]; script = os.path.join(WT, "eval", "longctx.py")
sys.argv = [script, "-h"]; buf = io.StringIO(); err = None; code = None
try:
    with contextlib.redirect_stdout(buf):
        runpy.run_path(script, run_name="__main__")
except SystemExit as e:
    code = e.code
except BaseException as e:
    err = e; traceback.print_exception(e, file=sys.stderr)
help_text = buf.getvalue(); print(help_text)
notes = dict(system_exit_code=code, help_mentions_65536="65536" in help_text, help_has_cache_size="cache_size" in help_text)
if isinstance(err, TypeError) and "default_cache_size" in str(err):
    rt.report("stated_behaviour", err, message=str(err), **notes)
elif err is None and code == 0 and notes["help_mentions_65536"]:
    rt.report("expected_behaviour", **notes)
else:
    rt.report("other", err, message=str(err) if err else None, **notes)
