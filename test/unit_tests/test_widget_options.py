"""
Constructor arguments, configure() and cget() of all widgets.

For every widget and every constructor argument, the test checks that:
 - the value passed to the constructor is returned by cget()
 - the value passed to configure() is returned by cget()
Unknown arguments must raise a ValueError in the constructor, configure() and cget().
"""

import inspect
import tkinter

import pytest
from PIL import Image

import customtkinter
from conftest import update

WIDGETS = ["CTkButton", "CTkCheckBox", "CTkComboBox", "CTkEntry", "CTkFrame", "CTkLabel", "CTkOptionMenu", "CTkProgressBar",
           "CTkRadioButton", "CTkScrollableFrame", "CTkScrollbar", "CTkSegmentedButton", "CTkSlider", "CTkSwitch",
           "CTkTabview", "CTkTextbox"]

# arguments that can only be set when the widget is created
CONSTRUCTOR_ONLY = {
    ("CTkProgressBar", "orientation"), ("CTkScrollableFrame", "orientation"), ("CTkScrollbar", "orientation"),
    ("CTkScrollbar", "minimum_pixel_length"), ("CTkSegmentedButton", "orientation"), ("CTkTextbox", "activate_scrollbars"),
}

# arguments for internal use by other widgets, they have no cget() and configure()
INTERNAL = {
    ("CTkButton", "round_width_to_even_numbers"), ("CTkButton", "round_height_to_even_numbers"),
    ("CTkFrame", "overwrite_preferred_drawing_method"),
}


def constructor_arguments(widget_name: str):
    cls = getattr(customtkinter, widget_name)
    return [name for name in inspect.signature(cls.__init__).parameters if name not in ("self", "master", "args", "kwargs")]


def make_value(widget_name: str, argument: str, root):
    """ a valid value for an argument, which is different from the default value """
    if argument == "bg_color":
        return "#2b2b2b"
    if argument == "background_corner_colors":
        return ("#111111", "#222222", "#333333", "#444444")
    if argument == "fg_color" or argument.endswith("_color") or argument.endswith("_color_disabled"):
        return ("#123456", "#654321")
    if argument == "orientation":
        return "horizontal" if widget_name == "CTkScrollableFrame" else "vertical"
    if argument == "anchor" and widget_name == "CTkTabview":
        return "s"
    if argument == "variable":
        if widget_name == "CTkSlider":
            return tkinter.DoubleVar(root, 15)
        if widget_name == "CTkProgressBar":
            return tkinter.DoubleVar(root, 0.3)
        return tkinter.StringVar(root, "a")
    if argument == "corner_radius" and widget_name == "CTkSlider":
        return 1000  # the slider uses at least the button_corner_radius as corner_radius
    values = {
        "width": 123, "height": 45, "corner_radius": 7, "border_width": 3, "border_spacing": 4,
        "round_width_to_even_numbers": False, "round_height_to_even_numbers": False,
        "text": "Test text", "label_text": "Label text", "placeholder_text": "hint",
        "font": ("Arial", 17), "dropdown_font": ("Arial", 15), "label_font": ("Arial", 16), "segmented_button_font": ("Arial", 14),
        "textvariable": tkinter.StringVar(root, "from variable"),
        "image": customtkinter.CTkImage(Image.new("RGB", (20, 20), "red"), size=(20, 20)),
        "state": "disabled", "hover": False, "command": print, "compound": "top", "anchor": "w", "label_anchor": "e",
        "checkbox_width": 30, "checkbox_height": 30, "radiobutton_width": 26, "radiobutton_height": 26,
        "switch_width": 50, "switch_height": 22, "button_length": 6, "button_corner_radius": 5,
        "border_width_unchecked": 2, "border_width_checked": 5,
        "onvalue": "yes", "offvalue": "no", "value": "a", "values": ["a", "b", "c"], "dynamic_resizing": False,
        "justify": "center", "mode": "indeterminate", "determinate_speed": 2, "indeterminate_speed": 3,
        "from_": 10, "to": 20, "number_of_steps": 5, "scroll_step": 0.5, "minimum_pixel_length": 30,
        "wraplength": 50, "activate_scrollbars": False, "overwrite_preferred_drawing_method": "circle_shapes",
    }
    return values[argument]


def all_widget_arguments():
    return [(widget, argument) for widget in WIDGETS for argument in constructor_arguments(widget)]


def assert_same(value, expected):
    if isinstance(expected, tuple) and isinstance(value, list):
        value = tuple(value)
    assert value == expected


@pytest.mark.parametrize("widget_name,argument", all_widget_arguments())
def test_constructor_argument_is_returned_by_cget(frame, widget_name, argument):
    if (widget_name, argument) in INTERNAL:
        pytest.skip("internal argument without cget()")
    value = make_value(widget_name, argument, frame)
    widget = getattr(customtkinter, widget_name)(frame, **{argument: value})
    widget.pack()
    update(frame)
    assert_same(widget.cget(argument), value)


@pytest.mark.parametrize("widget_name,argument", all_widget_arguments())
def test_configure_argument_is_returned_by_cget(frame, widget_name, argument):
    if (widget_name, argument) in INTERNAL:
        pytest.skip("internal argument without cget()")
    widget = getattr(customtkinter, widget_name)(frame)
    widget.pack()
    update(frame)
    value = make_value(widget_name, argument, frame)
    if (widget_name, argument) in CONSTRUCTOR_ONLY:
        with pytest.raises(ValueError):
            widget.configure(**{argument: value})
        return
    widget.configure(**{argument: value})
    update(frame)
    assert_same(widget.cget(argument), value)


@pytest.mark.parametrize("widget_name", WIDGETS)
def test_unknown_arguments_raise_value_error(frame, widget_name):
    cls = getattr(customtkinter, widget_name)
    with pytest.raises((ValueError, TypeError)):  # widgets without **kwargs raise a TypeError
        cls(frame, not_an_argument=1)
    widget = cls(frame)
    with pytest.raises(ValueError):
        widget.configure(not_an_argument=1)
    with pytest.raises(ValueError):
        widget.cget("not_an_argument")


@pytest.mark.parametrize("widget_name", WIDGETS)
@pytest.mark.parametrize("appearance_mode", ["light", "dark"])
def test_create_update_destroy(frame, widget_name, appearance_mode):
    customtkinter.set_appearance_mode(appearance_mode)
    widget = getattr(customtkinter, widget_name)(frame)
    widget.pack(padx=10, pady=10)
    update(frame)
    assert widget.winfo_exists()
    # CTkScrollableFrame is the inner frame in the scrolled canvas, the visible frame is its _parent_frame
    visible = widget._parent_frame if widget_name == "CTkScrollableFrame" else widget
    assert visible.winfo_width() > 1 and visible.winfo_height() > 1
    widget.destroy()
    update(frame)
    assert not widget.winfo_exists()


@pytest.mark.parametrize("widget_name", ["CTkButton", "CTkFrame", "CTkLabel", "CTkScrollableFrame", "CTkTabview"])
def test_transparent_fg_color(frame, widget_name):
    widget = getattr(customtkinter, widget_name)(frame, fg_color="transparent")
    widget.pack()
    update(frame)
    assert widget.cget("fg_color") == "transparent"


@pytest.mark.parametrize("widget_name", ["CTkButton", "CTkCheckBox", "CTkEntry", "CTkLabel", "CTkSlider", "CTkSwitch"])
def test_single_color_and_color_tuple(frame, widget_name):
    widget = getattr(customtkinter, widget_name)(frame, fg_color="#ff0000")
    assert widget.cget("fg_color") == "#ff0000"
    widget.configure(fg_color=("#00ff00", "#0000ff"))
    assert tuple(widget.cget("fg_color")) == ("#00ff00", "#0000ff")


@pytest.mark.parametrize("bad_color", [("#111111",), ("#111111", "#222222", "#333333"), 123])
def test_invalid_color_raises(frame, bad_color):
    with pytest.raises((ValueError, TypeError)):
        customtkinter.CTkButton(frame, fg_color=bad_color)


def test_transparent_not_allowed_for_text_color(frame):
    with pytest.raises(ValueError):
        customtkinter.CTkButton(frame, text_color="transparent")
