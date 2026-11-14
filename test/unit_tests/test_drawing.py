import sys
import tkinter
import tkinter.font
from types import SimpleNamespace

import pytest

import customtkinter
from customtkinter import CTkCanvas, DrawEngine
from customtkinter.windows.widgets.core_rendering import aa_images
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu
from customtkinter.windows.widgets.utility.utility_functions import (pop_from_dict_by_set, check_kwargs_empty,
                                                                    wheel_event_steps, touchpad_scroll_deltas)
from conftest import update

DRAWING_METHODS = [method for method in DrawEngine.DRAWING_METHODS
                   if not (method == "image_shapes" and tkinter.TkVersion < 8.6)]


@pytest.fixture
def canvas(frame):
    canvas = CTkCanvas(frame, width=300, height=200, highlightthickness=0)
    canvas.pack()
    return canvas


# ---------------------------------------------------------------- DrawEngine with every drawing method

def build_all_widgets(master):
    widgets = [
        customtkinter.CTkButton(master, corner_radius=12, border_width=2),
        customtkinter.CTkButton(master, corner_radius=0, border_width=0, width=40, height=40),
        customtkinter.CTkButton(master, corner_radius=1000, height=50),
        customtkinter.CTkEntry(master, corner_radius=8, border_width=3),
        customtkinter.CTkCheckBox(master, corner_radius=4),
        customtkinter.CTkSwitch(master),
        customtkinter.CTkRadioButton(master),
        customtkinter.CTkSlider(master),
        customtkinter.CTkSlider(master, orientation="vertical", number_of_steps=5),
        customtkinter.CTkProgressBar(master),
        customtkinter.CTkProgressBar(master, orientation="vertical", mode="indeterminate"),
        customtkinter.CTkOptionMenu(master, values=["a", "b"]),
        customtkinter.CTkComboBox(master, values=["a", "b"]),
        customtkinter.CTkSegmentedButton(master, values=["one", "two", "three"]),
        customtkinter.CTkScrollbar(master),
        customtkinter.CTkScrollbar(master, orientation="horizontal"),
        customtkinter.CTkLabel(master, text="label", corner_radius=6, fg_color="gray50"),
        customtkinter.CTkTextbox(master, width=120, height=60),
        customtkinter.CTkFrame(master, width=60, height=40, corner_radius=20, border_width=4),
    ]
    for index, widget in enumerate(widgets):
        widget.grid(row=index // 4, column=index % 4, padx=2, pady=2)
    return widgets


@pytest.mark.parametrize("method", DRAWING_METHODS)
def test_all_widgets_with_drawing_method(method, frame):
    DrawEngine.preferred_drawing_method = method
    container = customtkinter.CTkFrame(frame)
    container.pack()
    widgets = build_all_widgets(container)
    update(frame)
    for widget in widgets:
        canvas = widget._canvas if hasattr(widget, "_canvas") else None
        if canvas is not None:
            assert len(canvas.find_all()) > 0, f"{type(widget).__name__} drew nothing with {method}"

    # interactions that redraw the widgets
    widgets[4].select()
    widgets[5].toggle()
    widgets[6].select()
    widgets[7].set(0.8)
    widgets[9].set(0.3)
    widgets[13].set("two")
    for scaling in (1.5, 1):
        customtkinter.set_widget_scaling(scaling)
        update(frame)
    for mode in ("dark", "light"):
        customtkinter.set_appearance_mode(mode)
        update(frame)
    for widget in widgets[:3]:
        widget.configure(width=150, height=36, corner_radius=8, border_width=1)
    update(frame)


@pytest.mark.parametrize("method", DRAWING_METHODS)
@pytest.mark.parametrize("size, corner_radius, border_width", [
    ((100, 30), 6, 0), ((100, 30), 6, 2), ((30, 30), 15, 3), ((200, 40), 0, 1), ((51, 23), 11, 1), ((4, 4), 2, 0),
])
def test_rounded_rect_redraw(method, size, corner_radius, border_width, canvas):
    DrawEngine.preferred_drawing_method = method
    engine = DrawEngine(canvas)
    assert engine.draw_rounded_rect_with_border(*size, corner_radius, border_width) is True  # new items need colors
    items = len(canvas.find_all())
    assert items > 0
    assert canvas.tag_exists("inner_parts")
    assert canvas.tag_exists("border_parts") == (border_width > 0) or method == "font_shapes"

    # the same shape again doesn't create new items
    engine.draw_rounded_rect_with_border(*size, corner_radius, border_width)
    assert len(canvas.find_all()) == items

    # a bigger shape keeps working
    engine.draw_rounded_rect_with_border(size[0] * 2, size[1] * 2, corner_radius * 2, border_width)
    update(canvas)


@pytest.mark.parametrize("method", DRAWING_METHODS)
def test_other_shapes(method, canvas):
    DrawEngine.preferred_drawing_method = method
    engine = DrawEngine(canvas)
    engine.draw_rounded_rect_with_border_vertical_split(200, 30, 8, 1, 100)
    canvas.delete("all")
    engine.draw_rounded_progress_bar_with_border(200, 10, 5, 1, 0.2, 0.7, "w")
    engine.draw_rounded_progress_bar_with_border(200, 10, 5, 1, 0.4, 0.9, "w")
    canvas.delete("all")
    engine.draw_rounded_progress_bar_with_border(10, 200, 5, 1, 0.2, 0.7, "s")
    canvas.delete("all")
    engine.draw_rounded_slider_with_border_and_button(200, 16, 8, 6, 10, 8, 0.5, "w")
    canvas.delete("all")
    engine.draw_rounded_slider_with_border_and_button(16, 200, 8, 6, 10, 8, 0.5, "s")
    canvas.delete("all")
    engine.draw_rounded_scrollbar(16, 200, 8, 2, 0.1, 0.4, "vertical")
    engine.draw_rounded_scrollbar(16, 200, 8, 2, 0.5, 0.9, "vertical")
    canvas.delete("all")
    engine.draw_rounded_scrollbar(200, 16, 8, 2, 0.1, 0.4, "horizontal")
    canvas.delete("all")
    engine.draw_checkmark(24, 24, 14)
    assert canvas.tag_exists("checkmark")
    engine.draw_dropdown_arrow(50, 15, 10)
    assert canvas.tag_exists("dropdown_arrow")
    engine.draw_dropdown_arrow(60, 15, 12)
    engine.draw_background_corners(100, 30)
    update(canvas)


def test_check_shapes_font_switches_to_image_shapes(root, monkeypatch, capsys):
    monkeypatch.setattr(DrawEngine, "_shapes_font_checked", False)
    monkeypatch.setattr(DrawEngine, "preferred_drawing_method", "font_shapes")
    monkeypatch.setattr(tkinter.font, "families", lambda *args, **kwargs: ("DejaVu Sans",))
    x11_widget = SimpleNamespace(tk=SimpleNamespace(call=lambda *args: "x11"))
    DrawEngine.check_shapes_font(x11_widget)
    assert DrawEngine.preferred_drawing_method == "image_shapes"
    assert "CustomTkinter_shapes_font" in capsys.readouterr().err

    # checked only once
    DrawEngine.preferred_drawing_method = "font_shapes"
    DrawEngine.check_shapes_font(x11_widget)
    assert DrawEngine.preferred_drawing_method == "font_shapes"


def test_check_shapes_font_keeps_font_shapes(root, monkeypatch):
    monkeypatch.setattr(DrawEngine, "_shapes_font_checked", False)
    monkeypatch.setattr(DrawEngine, "preferred_drawing_method", "font_shapes")
    monkeypatch.setattr(tkinter.font, "families", lambda *args, **kwargs: ("CustomTkinter_shapes_font",))
    DrawEngine.check_shapes_font(root)
    assert DrawEngine.preferred_drawing_method == "font_shapes"


# ---------------------------------------------------------------- CTkCanvas tag registry and coords cache

def test_tag_registry(canvas):
    a = canvas.create_rectangle(0, 0, 10, 10, tags="a")
    b = canvas.create_rectangle(0, 0, 10, 10, tags=("b", "shared"))
    c = canvas.create_oval(0, 0, 10, 10, tags="c shared")
    assert canvas.tag_exists("a") and canvas.tag_exists("shared")
    assert not canvas.tag_exists("missing")
    assert canvas._ids_with_tag("shared") == (b, c)
    assert canvas.tag_exists(a)
    assert canvas.tag_exists("a||missing")  # tag expressions are passed to Tcl

    canvas.delete("b")
    assert canvas._ids_with_tag("shared") == (c,)
    canvas.addtag_withtag("new", "a")
    assert canvas._ids_with_tag("new") == (a,)
    canvas.dtag("a", "new")
    assert not canvas.tag_exists("new")
    canvas.itemconfigure(c, tags=("renamed",))
    assert canvas._ids_with_tag("renamed") == (c,)
    assert not canvas.tag_exists("shared")
    canvas.delete("all")
    assert canvas.find_all() == ()
    assert not canvas.tag_exists("a") and not canvas.tag_exists("renamed")


def test_registry_matches_tcl_after_many_changes(canvas):
    for index in range(30):
        canvas.create_line(0, 0, index, index, tags=(f"line_{index % 3}", "lines"))
    canvas.delete("line_1")
    canvas.addtag_withtag("extra", "line_2")
    canvas.delete(canvas.find_withtag("line_0")[0])
    for tag in ("line_0", "line_1", "line_2", "lines", "extra"):
        assert canvas._ids_with_tag(tag) == tkinter.Canvas.find_withtag(canvas, tag)


def test_coords_cache(canvas, monkeypatch):
    item = canvas.create_rectangle(0, 0, 10, 10, tags="box")
    canvas.coords("box", 5, 5, 20, 20)
    assert canvas.coords("box") == [5, 5, 20, 20]

    tcl_calls = []
    original_coords = tkinter.Canvas.coords
    monkeypatch.setattr(tkinter.Canvas, "coords", lambda self, *args: tcl_calls.append(args) or original_coords(self, *args))
    canvas.coords("box", 5, 5, 20, 20)  # unchanged, no Tcl call
    assert tcl_calls == []
    canvas.coords("missing", 1, 2, 3, 4)  # no item with this tag, no Tcl call
    assert tcl_calls == []
    canvas.coords("box", 6, 6, 20, 20)
    assert len(tcl_calls) == 1

    # move invalidates the cache
    canvas.move("box", 10, 0)
    canvas.coords("box", 6, 6, 20, 20)
    monkeypatch.undo()
    assert canvas.coords(item) == [6, 6, 20, 20]


def test_itemconfig_with_tag(canvas):
    canvas.create_rectangle(0, 0, 10, 10, tags="parts", fill="red")
    canvas.create_polygon(0, 0, 10, 0, 10, 10, tags="parts", fill="red")
    canvas.itemconfig("parts", fill="blue", outline="blue")
    assert {canvas.itemcget(canvas_id, "fill") for canvas_id in canvas.find_withtag("parts")} == {"blue"}
    canvas.itemconfig("missing", fill="green")  # no error


@pytest.fixture
def decimal_comma_locale():
    """ sets a locale with a decimal comma for LC_NUMERIC, like apps do with locale.setlocale(locale.LC_ALL, "") """
    import locale
    previous = locale.setlocale(locale.LC_NUMERIC)
    for name in ("de_DE.UTF-8", "de_DE", "German_Germany", "fr_FR.UTF-8", "fr_FR"):
        try:
            locale.setlocale(locale.LC_NUMERIC, name)
        except locale.Error:
            continue
        if locale.localeconv()["decimal_point"] == ",":
            break
    else:
        pytest.skip("no locale with a decimal comma installed")
    yield
    locale.setlocale(locale.LC_NUMERIC, previous)


def test_float_widths_with_decimal_comma_locale(decimal_comma_locale, frame):
    canvas = CTkCanvas(frame, width=100.0, height=50.0)
    canvas.configure(width=120.0, height=60.5)
    line = canvas.create_line(0, 0, 10, 10, width=2.0)
    polygon = canvas.create_polygon(0, 0, 10, 0, 10, 10, width=8.0, tags="polygon")
    canvas.itemconfig("polygon", width=8.5)
    canvas.itemconfigure(line, width=3.0)
    assert float(canvas.itemcget(polygon, "width")) in (8, 8.5, 9)

    # polygon_shapes on macOS keeps the corner radius as float
    for method in DRAWING_METHODS:
        DrawEngine.preferred_drawing_method = method
        engine = DrawEngine(canvas)
        engine.draw_rounded_rect_with_border(100, 30, 7.5, 1)
        engine.draw_rounded_rect_with_border(100, 30, 8.0, 2.0)
        engine.draw_rounded_progress_bar_with_border(100, 15, 7.5, 0, 0, 0.5, "w")
        canvas.delete("all")
    for widget_class in (customtkinter.CTkProgressBar, customtkinter.CTkSlider, customtkinter.CTkSwitch):
        widget_class(frame).pack()
    customtkinter.set_widget_scaling(1.25)
    update(frame)


# ---------------------------------------------------------------- antialiased images

@pytest.mark.skipif(tkinter.TkVersion < 8.6, reason="Tk 8.5 can't load PNG images")
class TestAntialiasedImages:
    def test_circle_png(self, root):
        for radius in (0.5, 3, 7.5, 20, 60):
            size = aa_images.circle_image_size(radius)
            image = tkinter.PhotoImage(master=root, data=aa_images.circle_png(radius, (255, 0, 0)))
            assert (image.width(), image.height()) == (size, size)
            center = size // 2
            assert not image.transparency_get(center, center)
            if radius >= 3:
                assert image.transparency_get(0, 0)  # corner outside of the circle
            assert tuple(image.get(center, center))[:3] == (255, 0, 0)

    def test_shape_png(self, root):
        for kind in ("checkmark", "dropdown_arrow"):
            size = aa_images.shape_image_size(kind, 14, 3)
            image = tkinter.PhotoImage(master=root, data=aa_images.shape_png(kind, 14, 3, 0.25, 0.5, (0, 0, 0)))
            assert (image.width(), image.height()) == (size, size)
            opaque = [(x, y) for x in range(size) for y in range(size) if not image.transparency_get(x, y)]
            assert opaque, f"{kind} image is empty"

    def test_aa_circle_items(self, canvas):
        canvas.aa_circles_as_images = True
        circle = canvas.create_aa_circle(50, 50, 10, fill="red", tags="circle")
        assert canvas.type(circle) == "image"
        assert canvas.create_aa_circle(50, 50, 10, angle=90, fill="red") == 0  # second circle not needed
        image = canvas.itemcget(circle, "image")
        assert image

        canvas.coords("circle", 60, 60, 15)  # radius change swaps the image
        assert canvas.itemcget(circle, "image") != image
        assert canvas.coords(circle) == [60, 60]

        bigger = canvas.itemcget(circle, "image")
        canvas.itemconfig("circle", fill="blue")
        assert canvas.itemcget(circle, "image") not in (image, bigger)

        canvas.coords(circle, 60, 60, 0)  # radius 0 has no image
        assert canvas.itemcget(circle, "image") == ""
        canvas.itemconfig(circle, fill="")
        canvas.coords(circle, 60, 60, 10)
        assert canvas.itemcget(circle, "image") == ""  # no fill color, no image

        canvas.delete("circle")
        assert circle not in canvas._aa_image_items and circle not in canvas._aa_circle_canvas_ids

    def test_aa_image_cache_is_shared_per_window(self, frame):
        first, second = CTkCanvas(frame), CTkCanvas(frame)
        first.aa_circles_as_images = second.aa_circles_as_images = True
        circle_1 = first.create_aa_circle(10, 10, 8, fill="#123456")
        circle_2 = second.create_aa_circle(20, 20, 8, fill="#123456")
        assert first.itemcget(circle_1, "image") == second.itemcget(circle_2, "image")

    def test_aa_shape_items(self, canvas):
        shape = canvas.create_aa_shape("checkmark", 50.5, 40.25, 14, 3, fill="black", tags="checkmark")
        assert canvas.type(shape) == "image"
        image = canvas.itemcget(shape, "image")
        canvas.set_aa_shape("checkmark", "checkmark", 50.5, 40.25, 14, 3)
        assert canvas.itemcget(shape, "image") == image  # unchanged
        canvas.set_aa_shape("checkmark", "checkmark", 80.75, 40.25, 14, 3)
        assert canvas.itemcget(shape, "image") != image  # other subpixel position
        canvas.itemconfig("checkmark", state="hidden")
        assert canvas.itemcget(shape, "state") == "hidden"

    def test_image_shapes_widgets_use_no_text_items(self, frame):
        DrawEngine.preferred_drawing_method = "image_shapes"
        widgets = [customtkinter.CTkButton(frame), customtkinter.CTkCheckBox(frame), customtkinter.CTkSwitch(frame),
                   customtkinter.CTkSlider(frame), customtkinter.CTkOptionMenu(frame)]
        widgets[1].select()
        for widget in widgets:
            widget.pack()
        update(frame)
        for widget in widgets:
            types = {widget._canvas.type(canvas_id) for canvas_id in widget._canvas.find_all()}
            assert "text" not in types
            for canvas_id in widget._canvas.find_withtag("ctk_aa_image"):
                assert widget._canvas.itemcget(canvas_id, "image") != "" or widget._canvas._aa_image_items[canvas_id]["fill"] == ""


# ---------------------------------------------------------------- utility functions

def test_pop_from_dict_by_set():
    kwargs = {"a": 1, "b": 2, "c": 3}
    assert pop_from_dict_by_set(kwargs, {"a", "c", "x"}) == {"a": 1, "c": 3}
    assert kwargs == {"b": 2}


def test_check_kwargs_empty():
    assert check_kwargs_empty({}) is False
    assert check_kwargs_empty({"a": 1}) is True
    assert check_kwargs_empty({}, raise_error=True) is False
    with pytest.raises(ValueError, match="not_an_argument"):
        check_kwargs_empty({"not_an_argument": 1}, raise_error=True)


def test_wheel_event_steps():
    assert wheel_event_steps(SimpleNamespace(num=4, delta=0)) == 1
    assert wheel_event_steps(SimpleNamespace(num=5, delta=0)) == -1
    if sys.platform == "darwin" and tkinter.TkVersion < 8.7:  # one step has a delta of 1
        assert wheel_event_steps(SimpleNamespace(num="??", delta=3)) == 3
    else:  # one step has a delta of 120, on macOS since Tk 8.7
        assert wheel_event_steps(SimpleNamespace(num="??", delta=120)) == 1
        assert wheel_event_steps(SimpleNamespace(num="??", delta=-240)) == -2
        assert wheel_event_steps(SimpleNamespace(num="??", delta=30)) == 1  # high resolution wheel
        assert wheel_event_steps(SimpleNamespace(num="??", delta=-30)) == -1


@pytest.mark.parametrize("dx, dy", [(0, 0), (5, -3), (-120, 64), (32767, -32768)])
def test_touchpad_scroll_deltas(dx, dy):
    delta = ((dx & 0xffff) << 16) | (dy & 0xffff)
    assert touchpad_scroll_deltas(SimpleNamespace(delta=delta)) == (dx, dy)


# ---------------------------------------------------------------- dropdown menu

def test_dropdown_menu_values_and_command(root):
    selected = []
    menu = DropdownMenu(root, values=["a", "b", "c"], command=selected.append)
    try:
        assert menu.index("end") == 2
        menu.invoke(1)
        assert selected == ["b"]
        menu.configure(values=["x", "y"])
        assert menu.index("end") == 1
        assert menu.cget("values") == ["x", "y"]
    finally:
        menu.destroy()


def test_dropdown_menu_breaks_into_columns(root):
    menu = DropdownMenu(root, values=[f"value {index}" for index in range(300)])
    try:
        menu._break_into_columns()
        breaks = [index for index in range(300) if int(menu.entrycget(index, "columnbreak"))]
        assert breaks, "a menu taller than the screen should be split into columns"
        rows_per_column = breaks[0]
        assert rows_per_column * (menu.yposition(1) - menu.yposition(0)) <= root.winfo_screenheight()

        # fewer values: the column breaks are removed again
        menu.configure(values=["a", "b", "c"])
        menu._break_into_columns()
        assert not any(int(menu.entrycget(index, "columnbreak")) for index in range(3))
    finally:
        menu.destroy()
