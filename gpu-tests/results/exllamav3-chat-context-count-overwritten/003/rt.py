"""Small reporting helper copied beside each repro.py. Does not touch exllamav3."""
import json, os, sys, traceback
WT = os.path.realpath(os.environ["EXL3_WT"])

def _site(tb):
    found = None
    for fr in traceback.extract_tb(tb):
        p = os.path.realpath(fr.filename)
        if p.startswith(WT + os.sep):
            found = f"{os.path.relpath(p, WT)}:{fr.lineno}"
    return found

def check_import():
    import exllamav3
    p = os.path.realpath(exllamav3.__file__)
    assert p.startswith(WT + os.sep), f"exllamav3 imported from {p}, not the worktree"

def report(behaviour, exc=None, **notes):
    r = {"behaviour": behaviour, "exception_type": None, "exception_site": None, "notes": notes}
    if exc is not None:
        r["exception_type"] = type(exc).__name__
        r["exception_site"] = _site(exc.__traceback__)
        traceback.print_exception(exc, file=sys.stderr)
    print("\nRESULT " + json.dumps(r, default=str), flush=True)
