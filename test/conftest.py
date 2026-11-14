"""
Shared fixtures for the unit and integration tests.

Run all tests from the repository root with:

    python -m pytest test

On Linux without a desktop session, run them in a virtual X server:

    xvfb-run -a python -m pytest test
"""

import os
import sys
import time
import tkinter

import pytest

# use the customtkinter package of this repository and not an installed version
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter  # noqa: E402

DEFAULT_DRAWING_METHOD = customtkinter.DrawEngine.preferred_drawing_method


def _display_available() -> bool:
    try:
        root = tkinter.Tk()
        root.destroy()
        return True
    except tkinter.TclError:
        return False


def pytest_collection_modifyitems(config, items):
    if not _display_available():
        skip = pytest.mark.skip(reason="no display available, on Linux run the tests with: xvfb-run -a python -m pytest test")
        for item in items:
            item.add_marker(skip)


def update(widget: tkinter.Misc, seconds: float = 0.0):
    """ process all pending events, optionally for some time """
    end = time.perf_counter() + seconds
    widget.update()
    while time.perf_counter() < end:
        widget.update()
        time.sleep(0.01)
    widget.update()


def grab(widget: tkinter.Misc):
    """ screenshot of a widget as PIL image, skips the test if screenshots are not possible """
    try:
        from PIL import ImageGrab
    except ImportError:
        pytest.skip("Pillow is needed for screenshots")
    update(widget, 0.1)
    x, y = widget.winfo_rootx(), widget.winfo_rooty()
    bbox = (x, y, x + widget.winfo_width(), y + widget.winfo_height())
    try:
        if sys.platform.startswith("linux"):
            return ImageGrab.grab(bbox=bbox, xdisplay=None).convert("RGB")
        return ImageGrab.grab(bbox=bbox).convert("RGB")
    except Exception as err:  # for example no permission for screen recording on macOS
        pytest.skip(f"screenshot not possible: {err}")


def color_rgb(widget: tkinter.Misc, color: str) -> tuple:
    return tuple(value // 257 for value in widget.winfo_rgb(color))


def color_distance(a: tuple, b: tuple) -> int:
    return sum(abs(x - y) for x, y in zip(a, b))


@pytest.fixture(scope="session")
def root():
    """ one CTk window for all tests """
    customtkinter.set_appearance_mode("light")
    app = customtkinter.CTk()
    app.geometry("900x700+0+0")
    app.title("CustomTkinter tests")
    update(app, 0.2)
    yield app
    app.destroy()


@pytest.fixture
def frame(root):
    """ a fresh CTkFrame inside the test window for every test, destroyed afterwards """
    container = customtkinter.CTkFrame(root, width=860, height=660)
    container.pack(fill="both", expand=True, padx=10, pady=10)
    update(root)
    yield container
    container.destroy()
    update(root)


@pytest.fixture(autouse=True)
def reset_global_state():
    """ restore the global CustomTkinter settings after every test """
    yield
    customtkinter.set_appearance_mode("light")
    customtkinter.set_widget_scaling(1.0)
    customtkinter.set_window_scaling(1.0)
    customtkinter.DrawEngine.preferred_drawing_method = DEFAULT_DRAWING_METHOD
    if customtkinter.ThemeManager._currently_loaded_theme != "blue":
        customtkinter.set_default_color_theme("blue")
