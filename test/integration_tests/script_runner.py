"""
Runs a CustomTkinter script for a short time and reports errors, used by test_scripts.py:

    python script_runner.py <script.py> [seconds]

The mainloop is stopped after the given time. Exceptions in the script and in tkinter callbacks
are printed to stderr and the exit code is 1.
"""

import os
import runpy
import sys
import tkinter
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter  # noqa: E402

script = os.path.abspath(sys.argv[1])
seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
errors = []


def report_callback_exception(self, exc, value, tb):
    errors.append("".join(traceback.format_exception(exc, value, tb)))


tkinter.Tk.report_callback_exception = report_callback_exception
original_mainloop = tkinter.Misc.mainloop


def mainloop(self, n=0):
    root = self._root()
    root.after(int(seconds * 1000), root.destroy)
    original_mainloop(self, n)


tkinter.Misc.mainloop = mainloop
customtkinter.CTk.mainloop = mainloop

os.chdir(os.path.dirname(script))
sys.argv = [script]
try:
    runpy.run_path(script, run_name="__main__")
except SystemExit:
    pass
except Exception:
    errors.append(traceback.format_exc())

for error in errors:
    sys.stderr.write(error + "\n")
sys.exit(1 if errors else 0)
