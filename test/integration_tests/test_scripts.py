"""
Starts the examples and the manual test scripts, each for a short time in its own process,
and fails if any of them raises an exception.
"""

import glob
import os
import subprocess
import sys

import pytest

REPOSITORY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUNNER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "script_runner.py")

SCRIPTS = sorted(glob.glob(os.path.join(REPOSITORY, "examples", "*.py"))
                 + glob.glob(os.path.join(REPOSITORY, "test", "manual_integration_tests", "**", "*.py"), recursive=True))

# scripts that need a person to close a dialog
INTERACTIVE = {"test_filedialog.py"}


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda path: os.path.relpath(path, REPOSITORY))
def test_script_runs_without_errors(script):
    if os.path.basename(script) in INTERACTIVE:
        pytest.skip("needs user input")
    try:
        result = subprocess.run([sys.executable, RUNNER, script, "1"], capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        pytest.fail(f"{os.path.basename(script)} didn't finish")
    assert result.returncode == 0, result.stderr[-3000:]
