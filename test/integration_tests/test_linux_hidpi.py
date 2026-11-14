"""
Linux HiDPI scaling with Xft.dpi, tested in a separate X server, so the settings of the desktop are not changed.
Needs Xvfb and xrdb (Debian and Ubuntu: apt install xvfb x11-xserver-utils).
"""

import json
import os
import shutil
import subprocess
import sys

import pytest

REPOSITORY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

pytestmark = [
    pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Xft.dpi is only used on Linux"),
    pytest.mark.skipif(shutil.which("Xvfb") is None or shutil.which("xrdb") is None, reason="needs Xvfb and xrdb"),
]

CHILD_SCRIPT = """
import json, sys
sys.path.insert(0, sys.argv[1])
import customtkinter
app = customtkinter.CTk()
button = customtkinter.CTkButton(app, width=100, height=30, font=("Arial", 20))
button.pack()
app.update()
print(json.dumps({
    "widget_scaling": button._get_widget_scaling(),
    "window_scaling": app._get_window_scaling(),
    "button_width": button._canvas.winfo_reqwidth(),
    "tk_scaling": float(app.tk.call("tk", "scaling")),
    "font_size": int(button._text_label.tk.splitlist(button._text_label.cget("font"))[1]),
}))
app.destroy()
"""


@pytest.fixture(scope="module")
def x_server():
    process = subprocess.Popen(["Xvfb", "-displayfd", "1", "-noreset", "-screen", "0", "1280x900x24"],
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    display = ":" + process.stdout.readline().strip()
    yield display
    process.terminate()
    process.wait(timeout=5)


def run_app(display, resources=None, environment=None):
    env = dict(os.environ, DISPLAY=display)
    env.pop("GDK_SCALE", None)
    env.update(environment or {})
    subprocess.run(["xrdb", "-nocpp", "-load", "-"], input=resources or "", text=True, env=env, check=True)
    result = subprocess.run([sys.executable, "-c", CHILD_SCRIPT, REPOSITORY], capture_output=True, text=True,
                            env=env, timeout=60)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout.strip().splitlines()[-1])


def test_default_dpi(x_server):
    values = run_app(x_server)
    assert values["widget_scaling"] == 1
    assert values["button_width"] == 100


@pytest.mark.parametrize("dpi, scaling", [(96, 1), (144, 1.5), (192, 2)])
def test_xft_dpi(x_server, dpi, scaling):
    values = run_app(x_server, f"Xft.dpi: {dpi}\n")
    assert values["widget_scaling"] == pytest.approx(scaling)
    assert values["window_scaling"] == pytest.approx(scaling)
    assert values["button_width"] == round(100 * scaling)
    assert values["tk_scaling"] == pytest.approx(dpi / 72, abs=0.01)
    assert values["font_size"] == -round(20 * scaling)


def test_gdk_scale_without_xft_dpi(x_server):
    values = run_app(x_server, "", {"GDK_SCALE": "2"})
    assert values["widget_scaling"] == 2
    assert values["button_width"] == 200
