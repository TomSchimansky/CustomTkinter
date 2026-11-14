import ctypes
import subprocess

import pytest

import customtkinter
from customtkinter import ScalingTracker
from conftest import update


# ---------------------------------------------------------------- widget and window scaling

def test_widget_scaling_scales_widgets(frame):
    button = customtkinter.CTkButton(frame, width=100, height=30)
    button.pack()
    update(frame)
    assert button._canvas.winfo_reqwidth() == 100
    customtkinter.set_widget_scaling(2)
    update(frame)
    assert button._canvas.winfo_reqwidth() == 200
    assert button._canvas.winfo_reqheight() == 60
    assert button.cget("width") == 100  # values of the user are independent of scaling


def test_scaling_has_a_minimum(root):
    customtkinter.set_widget_scaling(0.1)
    assert ScalingTracker.widget_scaling == 0.4
    customtkinter.set_window_scaling(0)
    assert ScalingTracker.window_scaling == 0.4


def test_scaling_changes_all_widgets(frame):
    widgets = [customtkinter.CTkButton(frame), customtkinter.CTkEntry(frame), customtkinter.CTkSlider(frame),
               customtkinter.CTkSwitch(frame), customtkinter.CTkProgressBar(frame), customtkinter.CTkComboBox(frame),
               customtkinter.CTkSegmentedButton(frame, values=["a", "b"]), customtkinter.CTkTextbox(frame),
               customtkinter.CTkTabview(frame), customtkinter.CTkScrollableFrame(frame)]
    for widget in widgets:
        widget.pack()
    update(frame)
    for scaling in (1.25, 0.75, 2, 1):
        customtkinter.set_widget_scaling(scaling)
        update(frame)
        for widget in widgets:
            assert widget._get_widget_scaling() == pytest.approx(ScalingTracker.window_dpi_scaling_dict[frame.winfo_toplevel()] * scaling)


def test_widgets_of_a_toplevel_use_its_scaling(root):
    toplevel = customtkinter.CTkToplevel(root)
    try:
        button = customtkinter.CTkButton(toplevel)
        assert ScalingTracker.get_window_root_of_widget(button) is toplevel
        assert button._set_scaling in ScalingTracker.window_widgets_dict[toplevel]
    finally:
        toplevel.destroy()


def test_deactivate_automatic_dpi_awareness(root, monkeypatch):
    monkeypatch.setattr(ScalingTracker, "deactivate_automatic_dpi_awareness", False)
    customtkinter.deactivate_automatic_dpi_awareness()
    assert ScalingTracker.deactivate_automatic_dpi_awareness is True
    assert ScalingTracker.get_window_dpi_scaling(root) == 1


# ---------------------------------------------------------------- Linux: Xft.dpi

class FakeTk:
    def __init__(self):
        self.tk_scaling = None
        self.variables = set()

    def call(self, *args):
        if args[:2] == ("info", "exists"):
            return args[2] in self.variables
        if args[0] == "set":
            self.variables.add(args[1])
        elif args[:2] == ("tk", "scaling"):
            self.tk_scaling = args[2]
        return ""


class FakeWindow:
    def __init__(self, screen=":42.0"):
        self.tk = FakeTk()
        self.screen = screen

    def winfo_screen(self):
        return self.screen


@pytest.fixture
def xft_dpi(monkeypatch):
    """ replaces the Xft.dpi lookup, returns a dict to set the value and count the lookups """
    state = {"dpi": None, "reads": 0}

    def read_xft_dpi(display_name):
        state["reads"] += 1
        return state["dpi"]

    monkeypatch.setattr(ScalingTracker, "_read_xft_dpi", staticmethod(read_xft_dpi))
    monkeypatch.setattr(ScalingTracker, "_linux_xft_dpi_cache", {})
    monkeypatch.delenv("GDK_SCALE", raising=False)
    return state


@pytest.mark.parametrize("dpi, scaling", [(96, 1), (120, 1.25), (144, 1.5), (192, 2), (480, 4), (48, 0.5), (30, 0.5)])
def test_linux_scaling_from_xft_dpi(xft_dpi, dpi, scaling):
    xft_dpi["dpi"] = dpi
    window = FakeWindow()
    assert ScalingTracker._get_linux_dpi_scaling(window) == pytest.approx(scaling)
    assert window.tk.tk_scaling == pytest.approx(dpi / 72)


def test_linux_tk_scaling_is_set_once(xft_dpi):
    xft_dpi["dpi"] = 144
    window = FakeWindow()
    ScalingTracker._get_linux_dpi_scaling(window)
    window.tk.tk_scaling = "changed by the user"
    ScalingTracker._get_linux_dpi_scaling(window)
    assert window.tk.tk_scaling == "changed by the user"


def test_linux_xft_dpi_is_cached_per_display(xft_dpi):
    xft_dpi["dpi"] = 144
    for _ in range(5):
        ScalingTracker._get_linux_dpi_scaling(FakeWindow(":1.0"))
    ScalingTracker._get_linux_dpi_scaling(FakeWindow(":2.0"))
    assert xft_dpi["reads"] == 2


@pytest.mark.parametrize("gdk_scale, scaling", [(None, 1), ("2", 2), ("1.5", 1.5), ("10", 4), ("invalid", 1)])
def test_linux_gdk_scale_without_xft_dpi(xft_dpi, monkeypatch, gdk_scale, scaling):
    if gdk_scale is not None:
        monkeypatch.setenv("GDK_SCALE", gdk_scale)
    window = FakeWindow()
    assert ScalingTracker._get_linux_dpi_scaling(window) == scaling
    assert window.tk.tk_scaling is None


def test_linux_invalid_xft_dpi_is_ignored(xft_dpi):
    for dpi in (0, 10, 5000):
        ScalingTracker._linux_xft_dpi_cache.clear()
        xft_dpi["dpi"] = dpi
        assert ScalingTracker._get_linux_dpi_scaling(FakeWindow()) == 1


def test_linux_destroyed_window(xft_dpi):
    class DestroyedWindow:
        def winfo_screen(self):
            import tkinter
            raise tkinter.TclError("bad window path name")

    assert ScalingTracker._get_linux_dpi_scaling(DestroyedWindow()) == 1


@pytest.fixture
def without_libx11(monkeypatch):
    """ makes _read_xft_dpi use 'xrdb -query' """
    def no_library(*args, **kwargs):
        raise OSError("no libX11")
    monkeypatch.setattr(ctypes, "CDLL", no_library)


@pytest.mark.parametrize("resources, dpi", [
    ("Xft.antialias:\t1\nXft.dpi:\t144\nXft.hinting:\t1\n", 144),
    ("Xft.dpi: 120.5\n", 120.5),
    ("*customization:\t-color\nXcursor.size:\t24\n", None),
    ("", None),
])
def test_read_xft_dpi_from_xrdb(without_libx11, monkeypatch, resources, dpi):
    calls = []

    def run(args, **kwargs):
        calls.append((args, kwargs.get("env")))
        return subprocess.CompletedProcess(args, 0, stdout=resources, stderr="")

    monkeypatch.setattr(subprocess, "run", run)
    assert ScalingTracker._read_xft_dpi(":7.0") == dpi
    assert calls[0][0] == ["xrdb", "-query"]
    assert calls[0][1]["DISPLAY"] == ":7.0"


def test_read_xft_dpi_without_xrdb(without_libx11, monkeypatch):
    def run(args, **kwargs):
        raise FileNotFoundError("xrdb")

    monkeypatch.setattr(subprocess, "run", run)
    assert ScalingTracker._read_xft_dpi(":7.0") is None
