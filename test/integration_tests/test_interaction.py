"""
Mouse and keyboard interaction with events sent to the widget under the mouse pointer,
like the window system does, so the tests also check which part of a widget gets the event.
"""

import sys
import tkinter

import pytest

import customtkinter
from conftest import update

WHEEL_USES_BUTTON_EVENTS = sys.platform.startswith("linux") and tkinter.TkVersion < 8.7


class Recorder:
    def __init__(self):
        self.calls = []

    def __call__(self, *args):
        self.calls.append(args)


def target_at(widget, x, y):
    """ the tkinter widget at position x, y of widget, and the position relative to it """
    root_x, root_y = widget.winfo_rootx() + x, widget.winfo_rooty() + y
    target = widget.winfo_containing(root_x, root_y)
    assert target is not None, f"no widget at {x}, {y}"
    return target, root_x - target.winfo_rootx(), root_y - target.winfo_rooty()


def mouse(widget, x, y, *sequences, **kwargs):
    target, target_x, target_y = target_at(widget, x, y)
    for sequence in sequences:
        target.event_generate(sequence, x=target_x, y=target_y, **kwargs)
    update(widget)
    return target


def click(widget, x=None, y=None, release_at=None):
    x = widget.winfo_width() // 2 if x is None else x
    y = widget.winfo_height() // 2 if y is None else y
    target = mouse(widget, x, y, "<Enter>", "<Motion>", "<Button-1>")
    release_x, release_y = release_at if release_at else (x, y)
    target_x = release_x - (target.winfo_rootx() - widget.winfo_rootx())
    target_y = release_y - (target.winfo_rooty() - widget.winfo_rooty())
    if not (0 <= release_x < widget.winfo_width() and 0 <= release_y < widget.winfo_height()):
        # the window system sends <Leave> when the pointer leaves the widget, also while the button is pressed
        target.event_generate("<B1-Motion>", x=target_x, y=target_y)
        target.event_generate("<Leave>", x=target_x, y=target_y)
    target.event_generate("<ButtonRelease-1>", x=target_x, y=target_y)
    update(widget)


def drag(widget, x_from, x_to, y):
    target = mouse(widget, x_from, y, "<Enter>", "<Button-1>")
    for x in range(x_from, x_to, 10 if x_to > x_from else -10):
        target.event_generate("<B1-Motion>", x=x - (target.winfo_rootx() - widget.winfo_rootx()), y=y)
    target.event_generate("<B1-Motion>", x=x_to - (target.winfo_rootx() - widget.winfo_rootx()), y=y)
    target.event_generate("<ButtonRelease-1>", x=x_to - (target.winfo_rootx() - widget.winfo_rootx()), y=y)
    update(widget)


def type_text(entry_widget, text):
    entry_widget.focus_force()
    update(entry_widget)
    for character in text:
        keysym = {" ": "space"}.get(character, character)
        entry_widget.event_generate("<KeyPress>", keysym=keysym)
    update(entry_widget)


def wheel(widget, steps):
    """ mouse wheel over the middle of widget, positive steps scroll up """
    target, x, y = target_at(widget, widget.winfo_width() // 2, widget.winfo_height() // 2)
    target.event_generate("<Motion>", x=x, y=y, warp=True)
    update(widget)
    for _ in range(abs(steps)):
        if WHEEL_USES_BUTTON_EVENTS:
            target.event_generate("<Button-4>" if steps > 0 else "<Button-5>", x=x, y=y)
        else:
            delta = 120 if sys.platform != "darwin" else 1
            target.event_generate("<MouseWheel>", x=x, y=y, delta=delta if steps > 0 else -delta)
    update(widget, 0.05)


@pytest.fixture
def place(frame):
    def place_widget(widget):
        widget.pack(padx=20, pady=10)
        update(frame, 0.05)
        return widget
    return place_widget


# ---------------------------------------------------------------- buttons

@pytest.fixture
def button_with_command(frame, place):
    command = Recorder()
    button = place(customtkinter.CTkButton(frame, text="click me", width=160, height=40, command=command))
    return button, command


def test_button_click(button_with_command):
    button, command = button_with_command
    click(button)  # on the text label
    click(button, 4, 20)  # on the canvas, next to the text
    assert len(command.calls) == 2


def test_button_release_outside_does_not_click(button_with_command):
    button, command = button_with_command
    click(button, release_at=(400, 20))
    assert command.calls == []


def test_disabled_button_does_not_click(button_with_command):
    button, command = button_with_command
    button.configure(state="disabled")
    click(button)
    assert command.calls == []


def test_button_hover(frame, place):
    button = place(customtkinter.CTkButton(frame, fg_color="#ff0000", hover_color="#0000ff"))
    canvas = button._canvas
    shapes = [canvas_id for canvas_id in canvas.find_withtag("inner_parts") if canvas.type(canvas_id) != "image"]
    fill = lambda: canvas.itemcget(shapes[0], "fill")
    assert fill() == "#ff0000"
    mouse(button, 10, 10, "<Enter>")
    assert fill() == "#0000ff"
    mouse(button, 10, 10, "<Leave>")
    assert fill() == "#ff0000"


@pytest.mark.parametrize("widget_class", [customtkinter.CTkCheckBox, customtkinter.CTkSwitch])
def test_toggle_by_clicking_box_and_text(frame, place, widget_class):
    command = Recorder()
    widget = place(widget_class(frame, text="a long text to click on", command=command))
    click(widget, 8, widget.winfo_height() // 2)  # box
    assert widget.get() == 1
    click(widget, widget.winfo_width() - 20, widget.winfo_height() // 2)  # text
    assert widget.get() == 0
    assert len(command.calls) == 2


def test_radiobuttons(frame, place):
    variable = tkinter.StringVar(value="a")
    radio_a = place(customtkinter.CTkRadioButton(frame, text="a", value="a", variable=variable))
    radio_b = place(customtkinter.CTkRadioButton(frame, text="b", value="b", variable=variable))
    click(radio_b, 8, radio_b.winfo_height() // 2)
    assert variable.get() == "b"
    assert radio_b._check_state and not radio_a._check_state


# ---------------------------------------------------------------- slider

def test_slider_click_and_drag(frame, place):
    command = Recorder()
    slider = place(customtkinter.CTkSlider(frame, from_=0, to=100, width=200, command=command))
    click(slider, 150, slider.winfo_height() // 2)
    assert slider.get() == pytest.approx(75, abs=4)
    drag(slider, 150, 50, slider.winfo_height() // 2)
    assert slider.get() == pytest.approx(25, abs=4)
    assert len(command.calls) >= 2


def test_slider_with_steps(frame, place):
    slider = place(customtkinter.CTkSlider(frame, from_=0, to=10, number_of_steps=10, width=200))
    click(slider, 115, slider.winfo_height() // 2)
    assert slider.get() in (5, 6)
    assert slider.get() == int(slider.get())


# ---------------------------------------------------------------- keyboard

def test_entry_typing_and_placeholder(frame, place):
    entry = place(customtkinter.CTkEntry(frame, placeholder_text="name"))
    other = place(customtkinter.CTkEntry(frame))
    assert entry._entry.get() == "name"  # placeholder is shown
    type_text(entry._entry, "abc def")
    assert entry.get() == "abc def"
    entry.delete(0, "end")
    other._entry.focus_force()
    update(frame, 0.05)
    assert entry._entry.get() == "name"
    assert entry.get() == ""


def test_combobox_typing(frame, place):
    combobox = place(customtkinter.CTkComboBox(frame, values=["one", "two"]))
    combobox.set("")
    type_text(combobox._entry, "three")
    assert combobox.get() == "three"


def test_textbox_typing(frame, place):
    textbox = place(customtkinter.CTkTextbox(frame, width=200, height=80))
    type_text(textbox._textbox, "hello")
    assert textbox.get("1.0", "end-1c") == "hello"


# ---------------------------------------------------------------- segmented button and tabview

def test_segmented_button_click(frame, place):
    command = Recorder()
    segmented = place(customtkinter.CTkSegmentedButton(frame, values=["left", "middle", "right"], command=command))
    click(segmented, segmented.winfo_width() - 10, segmented.winfo_height() // 2)
    assert segmented.get() == "right"
    click(segmented, 10, segmented.winfo_height() // 2)
    assert segmented.get() == "left"
    assert command.calls == [("right",), ("left",)]


def test_tabview_switch_by_click(frame, place):
    tabview = place(customtkinter.CTkTabview(frame, width=300, height=200))
    tabview.add("first")
    second = tabview.add("second")
    customtkinter.CTkLabel(second, text="content of second").pack()
    update(frame, 0.05)
    buttons = tabview._segmented_button
    click(buttons, buttons.winfo_width() - 10, buttons.winfo_height() // 2)
    update(frame, 0.2)
    assert tabview.get() == "second"
    assert second.winfo_ismapped()


def test_option_menu_dropdown(frame, place):
    command = Recorder()
    option_menu = place(customtkinter.CTkOptionMenu(frame, values=["one", "two", "three"], command=command))
    click(option_menu)
    update(frame, 0.1)
    menu = option_menu._dropdown_menu
    try:
        assert menu.is_open()
        menu.invoke(2)
    finally:
        menu.close()
        update(frame, 0.1)
    assert option_menu.get() == "three"
    assert command.calls == [("three",)]


# ---------------------------------------------------------------- scrolling

def test_scrollable_frame_mouse_wheel(frame, place):
    scrollable = place(customtkinter.CTkScrollableFrame(frame, width=200, height=150))
    labels = [customtkinter.CTkLabel(scrollable, text=f"row {index}") for index in range(40)]
    for label in labels:
        label.pack()
    update(frame, 0.1)
    assert scrollable._parent_canvas.yview()[0] == 0
    wheel(scrollable._parent_canvas, -3)  # scroll down over a label inside the frame
    assert scrollable._parent_canvas.yview()[0] > 0
    wheel(scrollable._parent_canvas, 10)
    assert scrollable._parent_canvas.yview()[0] == 0


def test_textbox_mouse_wheel(frame, place):
    textbox = place(customtkinter.CTkTextbox(frame, width=200, height=80))
    textbox.insert("1.0", "\n".join(f"line {index}" for index in range(100)))
    update(frame, 0.05)
    wheel(textbox._textbox, -3)
    assert textbox._textbox.yview()[0] > 0
