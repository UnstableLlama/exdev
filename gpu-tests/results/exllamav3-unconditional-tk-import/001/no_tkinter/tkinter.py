# Environment shim: makes "import tkinter" fail, modelling a Python build without Tk. Not upstream code.
raise ImportError("tkinter is not available in this environment (test shim)")
