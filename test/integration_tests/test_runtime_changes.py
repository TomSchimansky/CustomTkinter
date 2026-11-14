"""
Changes the appearance mode, scaling and window size of a window with all widgets at runtime,
and checks with screenshots that the window looks the same as before after changing it back.
"""

import pytest

import customtkinter
from conftest import update, grab


@pytest.fixture
def all_widgets(frame):
    root = frame.winfo_toplevel()
    root.event_generate("<Motion>", warp=True, x=root.winfo_width() - 2, y=root.winfo_height() - 2)

    container = customtkinter.CTkFrame(frame)
    container.pack(fill="both", expand=True)
    widgets = [
        customtkinter.CTkButton(container, text="Button"),
        customtkinter.CTkButton(container, text="Border", border_width=2, fg_color="transparent"),
        customtkinter.CTkLabel(container, text="Label", fg_color=("gray80", "gray30"), corner_radius=6),
        customtkinter.CTkEntry(container, placeholder_text="Entry"),
        customtkinter.CTkCheckBox(container, text="CheckBox"),
        customtkinter.CTkSwitch(container, text="Switch"),
        customtkinter.CTkRadioButton(container, text="RadioButton"),
        customtkinter.CTkSlider(container),
        customtkinter.CTkProgressBar(container),
        customtkinter.CTkOptionMenu(container, values=["OptionMenu"]),
        customtkinter.CTkComboBox(container, values=["ComboBox"]),
        customtkinter.CTkSegmentedButton(container, values=["one", "two", "three"]),
        customtkinter.CTkTextbox(container, width=160, height=60),
    ]
    widgets[4].select()
    widgets[5].select()
    widgets[8].set(0.4)
    widgets[11].set("two")
    widgets[12].insert("1.0", "Textbox\nwith two lines")
    tabview = customtkinter.CTkTabview(container, width=260, height=150)
    tabview.add("Tab 1")
    tabview.add("Tab 2")
    customtkinter.CTkButton(tabview.tab("Tab 1"), text="in tab").pack()
    scrollable = customtkinter.CTkScrollableFrame(container, label_text="ScrollableFrame", height=80)
    for index in range(8):
        customtkinter.CTkLabel(scrollable, text=f"row {index}").pack()
    widgets += [tabview, scrollable]

    for index, widget in enumerate(widgets):
        widget.grid(row=index // 3, column=index % 3, padx=6, pady=6)
    root.focus_force()  # no blinking insert cursor
    update(root, 0.3)
    return container


def assert_same_image(before, after, what):
    from PIL import ImageChops
    assert before.size == after.size, f"size changed after {what}"
    difference = ImageChops.difference(before, after).getbbox()
    assert difference is None, f"different pixels after {what} in the area {difference}"


def test_appearance_mode_round_trip(all_widgets):
    before = grab(all_widgets)
    customtkinter.set_appearance_mode("dark")
    update(all_widgets, 0.2)
    dark = grab(all_widgets)
    assert dark != before
    customtkinter.set_appearance_mode("light")
    update(all_widgets, 0.2)
    assert_same_image(before, grab(all_widgets), "dark and light mode")


@pytest.mark.parametrize("scaling", [0.8, 1.5, 2])
def test_widget_scaling_round_trip(all_widgets, scaling):
    before = grab(all_widgets)
    customtkinter.set_widget_scaling(scaling)
    update(all_widgets, 0.2)
    customtkinter.set_widget_scaling(1)
    update(all_widgets, 0.2)
    assert_same_image(before, grab(all_widgets), f"widget scaling {scaling}")


def test_window_resize_round_trip(all_widgets):
    root = all_widgets.winfo_toplevel()
    before = grab(all_widgets)
    geometry = root.geometry()
    root.geometry("500x400")
    update(root, 0.2)
    root.geometry("1000x800")
    update(root, 0.2)
    root.geometry(geometry)
    update(root, 0.3)
    assert_same_image(before, grab(all_widgets), "resizing the window")


def test_drawing_method_redraw(all_widgets):
    """ all widgets redrawn with the same drawing method look the same """
    before = grab(all_widgets)
    for widget in all_widgets.winfo_children():
        if hasattr(widget, "_draw"):
            widget._draw()
    update(all_widgets, 0.2)
    assert_same_image(before, grab(all_widgets), "redrawing")
