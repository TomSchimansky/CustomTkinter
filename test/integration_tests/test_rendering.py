"""
Checks the rendered pixels of the widgets for every drawing method with screenshots.
"""

import tkinter
import tkinter.font

import pytest

import customtkinter
from customtkinter import DrawEngine
from conftest import update, grab, color_distance

WHITE, RED, BLUE, GREEN, BLACK = (255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 160, 0), (0, 0, 0)
TOLERANCE = 60


def drawing_methods():
    methods = []
    for method in DrawEngine.DRAWING_METHODS:
        marks = []
        if method == "image_shapes" and tkinter.TkVersion < 8.6:
            marks.append(pytest.mark.skip(reason="Tk 8.5 can't load PNG images"))
        methods.append(pytest.param(method, marks=marks))
    return methods


@pytest.fixture(params=drawing_methods())
def method(request, root):
    if request.param == "font_shapes" and "CustomTkinter_shapes_font" not in tkinter.font.families(root):
        pytest.skip("Tk can't use the shapes font (built without Xft)")
    DrawEngine.preferred_drawing_method = request.param
    return request.param


@pytest.fixture
def white(frame):
    """ white container for the widgets """
    container = customtkinter.CTkFrame(frame, fg_color="#ffffff", corner_radius=0)
    container.pack(fill="both", expand=True)
    # move the mouse pointer away, otherwise widgets below it show their hover color
    root = frame.winfo_toplevel()
    root.event_generate("<Motion>", warp=True, x=root.winfo_width() - 2, y=root.winfo_height() - 2)
    update(root)
    return container


def near(pixel, color) -> bool:
    return color_distance(pixel, color) < TOLERANCE


def pixels(image) -> list:
    # getdata() is deprecated since Pillow 12.1
    return list(getattr(image, "get_flattened_data", image.getdata)())


def count_near(image, color, box=None) -> int:
    region = image.crop(box) if box else image
    return sum(1 for pixel in pixels(region) if near(pixel, color))


def show(widget, **pack_kwargs):
    widget.pack(padx=20, pady=20, **pack_kwargs)
    update(widget, 0.1)
    return grab(widget)


def test_button_fill_and_corners(method, white):
    image = show(customtkinter.CTkButton(white, width=120, height=40, corner_radius=10, border_width=0,
                                         fg_color="#ff0000", text=""))
    assert image.size == (120, 40)
    assert near(image.getpixel((60, 20)), RED)
    assert near(image.getpixel((60, 1)), RED)  # straight edges reach the border
    assert near(image.getpixel((1, 20)), RED)
    assert near(image.getpixel((0, 0)), WHITE)  # rounded corners
    assert near(image.getpixel((119, 39)), WHITE)


def test_button_border(method, white):
    image = show(customtkinter.CTkButton(white, width=120, height=40, corner_radius=10, border_width=4,
                                         fg_color="#ff0000", border_color="#0000ff", text=""))
    assert near(image.getpixel((60, 20)), RED)
    assert near(image.getpixel((60, 1)), BLUE)
    assert near(image.getpixel((60, 38)), BLUE)
    assert near(image.getpixel((1, 20)), BLUE)
    assert near(image.getpixel((0, 0)), WHITE)


def test_sharp_corners(method, white):
    image = show(customtkinter.CTkButton(white, width=80, height=30, corner_radius=0, fg_color="#ff0000", text=""))
    for corner in ((0, 0), (79, 0), (0, 29), (79, 29)):
        assert near(image.getpixel(corner), RED)


def test_antialiased_corners(method, white):
    if method in ("polygon_shapes", "circle_shapes") and white.tk.call("tk", "windowingsystem") != "aqua":
        pytest.skip(f"{method} is not antialiased on this platform")
    image = show(customtkinter.CTkButton(white, width=120, height=60, corner_radius=25, fg_color="#000000", text=""))
    corner = image.crop((0, 0, 25, 25))
    in_between = [pixel for pixel in pixels(corner) if 40 < pixel[0] < 215]
    assert len(in_between) >= 10, "the rounded corner has no antialiased pixels"


def test_dark_mode(method, white):
    button = customtkinter.CTkButton(white, width=100, height=30, fg_color=("#ff0000", "#0000ff"), text="")
    white.configure(fg_color=("#ffffff", "#000000"))
    assert near(show(button).getpixel((50, 15)), RED)
    customtkinter.set_appearance_mode("dark")
    image = grab(button)
    assert near(image.getpixel((50, 15)), BLUE)
    assert near(image.getpixel((0, 0)), BLACK)


def test_hover_color(method, white):
    button = customtkinter.CTkButton(white, width=100, height=30, fg_color="#ff0000", hover_color="#0000ff", text="")
    assert near(show(button).getpixel((50, 15)), RED)
    button._on_enter()
    assert near(grab(button).getpixel((50, 15)), BLUE)
    button._on_leave()
    assert near(grab(button).getpixel((50, 15)), RED)


def test_checkbox_checkmark(method, white):
    checkbox = customtkinter.CTkCheckBox(white, text="", width=24, checkbox_width=24, checkbox_height=24,
                                         fg_color="#0000ff", checkmark_color="#ffffff", border_color="#000000")
    image = show(checkbox)
    assert count_near(image, BLUE, (0, 0, 24, 24)) < 10  # unchecked: only the border
    checkbox.select()
    image = grab(checkbox)
    assert count_near(image, BLUE, (0, 0, 24, 24)) > 150
    assert count_near(image, WHITE, (6, 6, 18, 18)) > 10  # checkmark


def test_switch_position(method, white):
    switch = customtkinter.CTkSwitch(white, text="", width=50, switch_width=40, switch_height=20,
                                     fg_color="#ff0000", progress_color="#00a000", button_color="#0000ff")
    image = show(switch)
    assert count_near(image, BLUE, (0, 0, 20, 20)) > count_near(image, BLUE, (20, 0, 40, 20))
    assert near(image.getpixel((30, 10)), RED)
    switch.select()
    image = grab(switch)
    assert count_near(image, BLUE, (20, 0, 40, 20)) > count_near(image, BLUE, (0, 0, 20, 20))
    assert near(image.getpixel((10, 10)), GREEN)


def test_slider_position(method, white):
    slider = customtkinter.CTkSlider(white, width=200, height=20, from_=0, to=1, fg_color="#ff0000",
                                     progress_color="#00a000", button_color="#0000ff", button_hover_color="#0000ff")
    slider.set(0)
    image = show(slider)
    assert count_near(image, BLUE, (0, 0, 40, 20)) > 50
    assert count_near(image, BLUE, (160, 0, 200, 20)) == 0
    slider.set(1)
    image = grab(slider)
    assert count_near(image, BLUE, (160, 0, 200, 20)) > 50
    assert near(image.getpixel((100, 10)), GREEN)


@pytest.mark.parametrize("orientation", ["horizontal", "vertical"])
def test_progressbar(method, white, orientation):
    width, height = (200, 12) if orientation == "horizontal" else (12, 200)
    bar = customtkinter.CTkProgressBar(white, orientation=orientation, width=width, height=height,
                                       fg_color="#ff0000", progress_color="#0000ff", border_width=0)
    bar.set(0.5)
    image = show(bar)
    if orientation == "horizontal":
        assert near(image.getpixel((50, 6)), BLUE)
        assert near(image.getpixel((150, 6)), RED)
    else:  # vertical bars fill from the bottom
        assert near(image.getpixel((6, 150)), BLUE)
        assert near(image.getpixel((6, 50)), RED)


def test_segmented_button(method, white):
    segmented = customtkinter.CTkSegmentedButton(white, values=["a", "b"], width=160, height=30,
                                                 selected_color="#0000ff", unselected_color="#ff0000",
                                                 fg_color="#ff0000", text_color="#ff0000")
    segmented.set("b")
    image = show(segmented)
    width = image.size[0]
    assert near(image.getpixel((width // 4, 15)), RED)
    assert near(image.getpixel((3 * width // 4, 15)), BLUE)


def test_widget_scaling(method, white):
    button = customtkinter.CTkButton(white, width=100, height=30, corner_radius=8, fg_color="#ff0000", text="")
    assert show(button).size == (100, 30)
    customtkinter.set_widget_scaling(1.5)
    update(white, 0.1)
    image = grab(button)
    assert image.size == (150, 45)
    assert near(image.getpixel((75, 1)), RED)
    assert near(image.getpixel((0, 0)), WHITE)


@pytest.mark.parametrize("scaling", [1.2, 1.25, 1.5])
def test_no_gaps_with_fractional_scaling(method, white, scaling):
    """ the last pixel row and column of the canvas were not drawn with scaling like 125% """
    customtkinter.set_widget_scaling(scaling)
    tabview = customtkinter.CTkTabview(white, width=200, height=80, fg_color="#ffffff", segmented_button_fg_color="#ff0000",
                                       segmented_button_unselected_color="#ff0000", segmented_button_selected_color="#0000ff")
    tabview.add("Options")
    tabview.add("Notes")
    tabview.pack(padx=20, pady=20)
    update(white, 0.1)
    image = grab(tabview._segmented_button)
    width, height = image.size
    for corner in ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)):
        assert near(image.getpixel(corner), WHITE), f"corner {corner} is not drawn with the background color"
