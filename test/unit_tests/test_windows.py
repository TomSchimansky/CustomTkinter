"""
CTk, CTkToplevel and CTkInputDialog.
"""

import sys
import tkinter

import pytest

import customtkinter
from conftest import update


@pytest.fixture
def window(root):
    """ a separate CTkToplevel for every test """
    toplevel = customtkinter.CTkToplevel(root)
    toplevel.geometry("300x200+50+50")
    update(toplevel, 0.2)
    yield toplevel
    if toplevel.winfo_exists():
        toplevel.destroy()
    update(root)


# several Tk interpreters at the same time are not reliable with Tk 8.6 on macOS, update() can block forever
several_interpreters = pytest.mark.skipif(sys.platform == "darwin" and tkinter.TkVersion < 9,
                                          reason="several Tk interpreters at the same time are not reliable with Tk 8.6 on macOS")


@pytest.fixture
def app(root):
    """ the CTk window of the tests, restored afterwards, a second CTk would need a second Tk interpreter """
    min_size, max_size = (root._min_width, root._min_height), (root._max_width, root._max_height)
    root.geometry("300x200+50+50")
    update(root, 0.2)
    yield root
    root.unbind("<Configure>")
    root.bind_class(root._configure_bindtag, "<Configure>", root._update_dimensions_event)
    for child in root.winfo_children():
        child.destroy()
    root.minsize(*min_size)
    root.maxsize(*max_size)
    root.resizable(True, True)
    root.title("CustomTkinter tests")
    root.configure(fg_color=customtkinter.ThemeManager.theme["CTk"]["fg_color"])
    if root.state() != "normal":
        root.deiconify()
    root.geometry("900x700+0+0")
    update(root, 0.2)


@pytest.mark.parametrize("window_fixture", ["app", "window"])
class TestWindowGeometry:
    def test_geometry_returns_size_without_scaling(self, request, window_fixture):
        win = request.getfixturevalue(window_fixture)
        win.geometry("320x210")
        update(win, 0.2)
        assert win.geometry().startswith("320x210")
        assert (win.winfo_width(), win.winfo_height()) == (320, 210)

    def test_geometry_with_window_scaling(self, request, window_fixture):
        win = request.getfixturevalue(window_fixture)
        # with 1.5, the 900x700 test window would be larger than the screen of the macOS CI runner, macOS and Tk then
        # resize it in an endless loop
        customtkinter.set_window_scaling(1.25)
        win.geometry("300x200")
        update(win, 0.3)
        assert (win.winfo_width(), win.winfo_height()) == (375, 250)
        assert win.geometry().startswith("300x200")

    def test_minsize_and_maxsize(self, request, window_fixture):
        win = request.getfixturevalue(window_fixture)
        win.minsize(250, 150)
        win.maxsize(400, 300)
        win.geometry("100x100")
        update(win, 0.2)
        assert win.winfo_width() >= 250 and win.winfo_height() >= 150
        win.geometry("600x600")
        update(win, 0.2)
        assert win.winfo_width() <= 400 and win.winfo_height() <= 300

    def test_size_is_tracked_after_resize_by_user(self, request, window_fixture):
        win = request.getfixturevalue(window_fixture)
        win.tk.call("wm", "geometry", win._w, "340x260")  # like a resize with the mouse
        update(win, 0.3)
        assert (win._current_width, win._current_height) == (340, 260)

    def test_size_is_tracked_with_app_configure_binding(self, request, window_fixture):
        win = request.getfixturevalue(window_fixture)
        events = []
        win.bind("<Configure>", events.append)  # replaces bindings of the window without add="+"
        win.tk.call("wm", "geometry", win._w, "350x270")
        update(win, 0.3)
        assert (win._current_width, win._current_height) == (350, 270)
        assert events

    def test_window_handler_only_for_window_events(self, request, window_fixture):
        win = request.getfixturevalue(window_fixture)
        for i in range(5):
            customtkinter.CTkButton(win).pack()
        update(win, 0.2)
        calls = []
        win.bind_class(win._configure_bindtag, "<Configure>", lambda event: calls.append(event.widget))
        win.tk.call("wm", "geometry", win._w, "360x280")
        update(win, 0.3)
        assert calls and all(widget is win for widget in calls)

    def test_fg_color(self, request, window_fixture):
        win = request.getfixturevalue(window_fixture)
        win.configure(fg_color="#123456")
        assert win.cget("fg_color") == "#123456"
        assert win.cget("bg") == "#123456"
        win.configure(fg_color=("#ffffff", "#000000"))
        customtkinter.set_appearance_mode("dark")
        update(win)
        assert win.cget("bg") == "#000000"

    def test_withdraw_deiconify(self, request, window_fixture):
        win = request.getfixturevalue(window_fixture)
        win.withdraw()
        update(win, 0.2)
        assert win.state() == "withdrawn"
        win.deiconify()
        update(win, 0.2)
        assert win.state() == "normal"

    def test_resizable(self, request, window_fixture):
        win = request.getfixturevalue(window_fixture)
        win.resizable(False, True)
        assert tuple(bool(v) for v in win.resizable()) == (False, True)

    def test_title(self, request, window_fixture):
        win = request.getfixturevalue(window_fixture)
        win.title("Test title")
        assert win.title() == "Test title"


@several_interpreters
def test_ctk_class_name(root):
    app = customtkinter.CTk(className="MyApp")
    try:
        assert app.winfo_class() == "Myapp"  # Tk capitalizes the first letter only, use this in StartupWMClass on Linux
    finally:
        app.destroy()


def test_unknown_window_argument_raises():
    with pytest.raises(ValueError):
        customtkinter.CTk(not_an_argument=1)


def test_single_global_click_handler_after_toplevels(root):
    for _ in range(3):
        toplevel = customtkinter.CTkToplevel(root)
        update(root, 0.05)
        toplevel.destroy()
    update(root)
    script = root.tk.call("bind", "all", "<Button-1>")
    assert script.count("set_focus") == 1


def test_toplevel_destroy_while_after_callbacks_pending(root):
    toplevel = customtkinter.CTkToplevel(root)
    customtkinter.CTkButton(toplevel).pack()
    toplevel.destroy()
    update(root, 0.5)  # pending after() callbacks of the toplevel must not raise


@several_interpreters
def test_new_root_after_destroy():
    app = customtkinter.CTk()
    customtkinter.CTkButton(app).pack()
    update(app, 0.1)
    app.destroy()
    app2 = customtkinter.CTk()
    button = customtkinter.CTkButton(app2)
    button.pack()
    update(app2, 0.1)
    assert button.winfo_ismapped()
    app2.destroy()


# ---------------------------------------------------------------- CTkInputDialog

def run_dialog(root, action):
    """ opens a CTkInputDialog, runs action(dialog) after it is shown, returns get_input() """
    result = {}

    def run_action(dialog):
        try:
            action(dialog)
        except BaseException as error:  # close the dialog, otherwise get_input() blocks forever
            result["error"] = error
            dialog.destroy()

    def open_dialog():
        dialog = customtkinter.CTkInputDialog(text="Number:", title="Test dialog")
        root.after(400, run_action, dialog)
        result["input"] = dialog.get_input()
        result["dialog"] = dialog

    root.after(10, open_dialog)
    deadline = 50
    while "input" not in result and deadline > 0:
        update(root, 0.1)
        deadline -= 1
    if "error" in result:
        raise result["error"]
    assert "input" in result, "dialog did not close"
    return result["input"], result["dialog"]


def test_input_dialog_ok(root):
    def type_and_ok(dialog):
        dialog._entry.insert(0, "42")
        dialog._ok_event()
    value, dialog = run_dialog(root, type_and_ok)
    assert value == "42"
    assert not dialog.winfo_exists()


def test_input_dialog_return_key(root):
    def type_and_return(dialog):
        dialog._entry.insert(0, "abc")
        dialog._entry._entry.focus_force()  # key events only reach the window with the keyboard focus
        dialog.update()
        dialog._entry._entry.event_generate("<Return>")
    value, _ = run_dialog(root, type_and_return)
    assert value == "abc"


def test_input_dialog_cancel(root):
    value, _ = run_dialog(root, lambda dialog: dialog._cancel_event())
    assert value is None


def test_input_dialog_close_window(root):
    value, _ = run_dialog(root, lambda dialog: dialog._on_closing())
    assert value is None


def test_input_dialog_grab_retries_until_viewable(root, monkeypatch):
    calls = {"n": 0}
    real_grab_set = tkinter.Misc.grab_set

    def late_grab_set(widget):
        calls["n"] += 1
        if calls["n"] <= 2:
            raise tkinter.TclError("grab failed: window not viewable")
        return real_grab_set(widget)

    monkeypatch.setattr(tkinter.Misc, "grab_set", late_grab_set)

    def check_and_cancel(dialog):
        assert calls["n"] >= 3
        dialog._cancel_event()
    value, _ = run_dialog(root, check_and_cancel)
    assert value is None


@several_interpreters
@pytest.mark.parametrize("call_before", [None, "withdraw", "iconify"])
def test_macos_window_is_brought_to_front(monkeypatch, call_before):
    """ on macOS the window can open behind the terminal, mainloop() brings it to the front once """
    import types
    import customtkinter.windows.ctk_tk as ctk_tk_module
    calls = []
    monkeypatch.setattr(ctk_tk_module, "sys", types.SimpleNamespace(platform="darwin"))
    monkeypatch.setattr(customtkinter.CTk, "_macos_bring_to_front", lambda self: calls.append(self))
    app = customtkinter.CTk()
    try:
        if call_before is not None:
            getattr(app, call_before)()
        app.after(100, app.quit)
        app.mainloop()
        app.after(100, app.quit)
        app.mainloop()  # only the first mainloop() brings the window to the front
        assert len(calls) == (1 if call_before is None else 0)
    finally:
        app.destroy()


def test_macos_bring_to_front_resets_topmost(root):
    root._macos_bring_to_front()
    update(root, 0.1)
    assert not root.attributes("-topmost")
