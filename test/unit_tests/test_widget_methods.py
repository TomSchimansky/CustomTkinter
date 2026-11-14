"""
Methods, commands, variables and states of the widgets.
"""

import tkinter

import pytest

import customtkinter
from conftest import update


class Recorder:
    """ callable that records all calls """
    def __init__(self):
        self.calls = []

    def __call__(self, *args):
        self.calls.append(args)


# ---------------------------------------------------------------- CTkButton

class TestCTkButton:
    def test_invoke_calls_command(self, frame):
        command = Recorder()
        button = customtkinter.CTkButton(frame, command=command)
        button.invoke()
        assert command.calls == [()]

    def test_invoke_returns_command_result(self, frame):
        button = customtkinter.CTkButton(frame, command=lambda: 42)
        assert button.invoke() == 42

    def test_disabled_button_does_not_invoke(self, frame):
        command = Recorder()
        button = customtkinter.CTkButton(frame, command=command, state="disabled")
        button.invoke()
        assert command.calls == []
        button.configure(state="normal")
        button.invoke()
        assert command.calls == [()]

    def test_click_calls_command(self, frame):
        command = Recorder()
        button = customtkinter.CTkButton(frame, command=command)
        button.pack()
        update(frame)
        button._on_enter()
        button._on_release()
        assert command.calls == [()]

    def test_release_outside_does_not_call_command(self, frame):
        command = Recorder()
        button = customtkinter.CTkButton(frame, command=command)
        button.pack()
        update(frame)
        button._on_enter()
        button._on_leave()
        button._on_release()
        assert command.calls == []

    def test_textvariable_updates_text(self, frame):
        variable = tkinter.StringVar(frame, "first")
        button = customtkinter.CTkButton(frame, textvariable=variable)
        button.pack()
        update(frame)
        assert button._text_label.cget("text") == "first"
        variable.set("second")
        update(frame)
        assert button._text_label.cget("text") == "second"

    def test_text_and_image_labels(self, frame):
        from PIL import Image
        image = customtkinter.CTkImage(Image.new("RGB", (10, 10), "blue"), size=(10, 10))
        button = customtkinter.CTkButton(frame, text="", image=image)
        button.pack()
        update(frame)
        assert button._image_label is not None
        button.configure(image=None, text="text")
        update(frame)
        assert button._image_label is None
        assert button._text_label.cget("text") == "text"

    def test_hover_changes_color(self, frame):
        button = customtkinter.CTkButton(frame, fg_color="#111111", hover_color="#222222")
        button.pack()
        update(frame)
        fill = lambda: button._canvas.itemcget(button._canvas.find_withtag("inner_parts")[-1], "fill")
        assert fill() == "#111111"
        button._on_enter()
        assert fill() == "#222222"
        button._on_leave()
        assert fill() == "#111111"

    def test_no_hover_effect_when_hover_false(self, frame):
        button = customtkinter.CTkButton(frame, fg_color="#111111", hover_color="#222222", hover=False)
        button.pack()
        update(frame)
        button._on_enter()
        assert button._canvas.itemcget(button._canvas.find_withtag("inner_parts")[-1], "fill") == "#111111"


# ---------------------------------------------------------------- bind / unbind

@pytest.mark.parametrize("widget_name", ["CTkButton", "CTkCheckBox", "CTkComboBox", "CTkEntry", "CTkLabel", "CTkOptionMenu",
                                         "CTkProgressBar", "CTkRadioButton", "CTkScrollbar", "CTkSlider", "CTkSwitch", "CTkTextbox"])
def test_bind_requires_add(frame, widget_name):
    widget = getattr(customtkinter, widget_name)(frame)
    with pytest.raises(ValueError):
        widget.bind("<Enter>", print, add=False)
    widget.bind("<Enter>", print)
    widget.bind("<Enter>", print, add="+")
    widget.unbind("<Enter>")


def test_bind_receives_events(frame):
    events = Recorder()
    button = customtkinter.CTkButton(frame)
    button.pack()
    update(frame)
    button.bind("<<TestEvent>>", events)
    button._canvas.event_generate("<<TestEvent>>")
    update(frame)
    assert len(events.calls) == 1


def test_unbind_keeps_internal_hover_callbacks(frame):
    button = customtkinter.CTkButton(frame, fg_color="#111111", hover_color="#222222")
    button.pack()
    update(frame)
    button.bind("<Enter>", print)
    button.unbind("<Enter>")
    button._canvas.event_generate("<Enter>")
    update(frame)
    assert button._canvas.itemcget(button._canvas.find_withtag("inner_parts")[-1], "fill") == "#222222"


# ---------------------------------------------------------------- CTkCheckBox and CTkSwitch

@pytest.mark.parametrize("widget_name", ["CTkCheckBox", "CTkSwitch"])
class TestCheckBoxAndSwitch:
    def test_select_deselect_toggle(self, frame, widget_name):
        widget = getattr(customtkinter, widget_name)(frame)
        assert widget.get() == 0
        widget.select()
        assert widget.get() == 1
        widget.deselect()
        assert widget.get() == 0
        widget.toggle()
        assert widget.get() == 1
        widget.toggle()
        assert widget.get() == 0

    def test_on_and_off_values(self, frame, widget_name):
        widget = getattr(customtkinter, widget_name)(frame, onvalue="yes", offvalue="no")
        assert widget.get() == "no"
        widget.select()
        assert widget.get() == "yes"

    def test_toggle_calls_command_select_does_not(self, frame, widget_name):
        command = Recorder()
        widget = getattr(customtkinter, widget_name)(frame, command=command)
        widget.select()
        widget.deselect()
        assert command.calls == []
        widget.toggle()
        assert len(command.calls) == 1

    def test_variable_both_directions(self, frame, widget_name):
        variable = tkinter.StringVar(frame, "off")
        widget = getattr(customtkinter, widget_name)(frame, variable=variable, onvalue="on", offvalue="off")
        assert widget.get() == "off"
        variable.set("on")
        update(frame)
        assert widget.get() == "on"
        widget.deselect()
        assert variable.get() == "off"
        widget.toggle()
        assert variable.get() == "on"

    def test_disabled_does_not_toggle(self, frame, widget_name):
        widget = getattr(customtkinter, widget_name)(frame, state="disabled")
        widget.toggle()
        assert widget.get() == 0

    def test_destroy_removes_variable_trace(self, frame, widget_name):
        variable = tkinter.StringVar(frame, "0")
        widget = getattr(customtkinter, widget_name)(frame, variable=variable, onvalue="1", offvalue="0")
        traces_before = len(variable.trace_info())
        widget.destroy()
        assert len(variable.trace_info()) == traces_before - 1
        variable.set("1")  # must not fail after the widget is destroyed


# ---------------------------------------------------------------- CTkRadioButton

class TestCTkRadioButton:
    def test_group_with_variable(self, frame):
        variable = tkinter.StringVar(frame, "")
        buttons = [customtkinter.CTkRadioButton(frame, variable=variable, value=value) for value in ("a", "b", "c")]
        buttons[1].invoke()
        assert variable.get() == "b"
        assert [button._check_state for button in buttons] == [False, True, False]
        variable.set("c")
        update(frame)
        assert [button._check_state for button in buttons] == [False, False, True]

    def test_invoke_selects_and_calls_command(self, frame):
        command = Recorder()
        button = customtkinter.CTkRadioButton(frame, command=command, value=1)
        button.invoke()
        assert button._check_state is True
        button.invoke()  # like tkinter.Radiobutton, the command is called again
        assert len(command.calls) == 2

    def test_select_deselect(self, frame):
        button = customtkinter.CTkRadioButton(frame)
        button.select()
        assert button._check_state is True
        button.deselect()
        assert button._check_state is False

    def test_disabled_does_not_invoke(self, frame):
        command = Recorder()
        button = customtkinter.CTkRadioButton(frame, command=command, state="disabled")
        button.invoke()
        assert command.calls == []


# ---------------------------------------------------------------- CTkEntry

class TestCTkEntry:
    def test_insert_get_delete(self, frame):
        entry = customtkinter.CTkEntry(frame)
        entry.insert(0, "Hello")
        entry.insert("end", " World")
        assert entry.get() == "Hello World"
        entry.delete(0, 6)
        assert entry.get() == "World"
        entry.delete(0, "end")
        assert entry.get() == ""

    def test_placeholder_is_not_returned_by_get(self, frame):
        entry = customtkinter.CTkEntry(frame, placeholder_text="hint")
        entry.pack()
        update(frame)
        assert entry._entry.get() == "hint"  # visible in the entry
        assert entry.get() == ""
        entry.insert(0, "text")
        assert entry.get() == "text"

    def test_placeholder_disappears_on_focus_and_comes_back(self, frame):
        entry = customtkinter.CTkEntry(frame, placeholder_text="hint")
        entry.pack()
        update(frame)
        entry._entry_focus_in()
        assert entry._entry.get() == ""
        entry._entry_focus_out()
        assert entry._entry.get() == "hint"

    def test_textvariable(self, frame):
        variable = tkinter.StringVar(frame, "start")
        entry = customtkinter.CTkEntry(frame, textvariable=variable)
        assert entry.get() == "start"
        entry.delete(0, "end")
        entry.insert(0, "typed")
        assert variable.get() == "typed"

    def test_disabled_and_readonly_state(self, frame):
        entry = customtkinter.CTkEntry(frame, state="readonly")
        entry.insert(0, "x")
        assert entry.get() == ""
        entry.configure(state="normal")
        entry.insert(0, "x")
        assert entry.get() == "x"

    def test_selection_and_cursor(self, frame):
        entry = customtkinter.CTkEntry(frame)
        entry.insert(0, "abcdef")
        entry.select_range(1, 3)
        assert entry.select_present()
        entry.select_clear()
        assert not entry.select_present()
        entry.icursor(2)
        assert entry.index("insert") == 2

    def test_show_option(self, frame):
        entry = customtkinter.CTkEntry(frame, show="*")
        entry.insert(0, "secret")
        assert entry.get() == "secret"
        assert entry.cget("show") == "*"


# ---------------------------------------------------------------- CTkComboBox and CTkOptionMenu

@pytest.mark.parametrize("widget_name", ["CTkComboBox", "CTkOptionMenu"])
class TestComboBoxAndOptionMenu:
    def test_initial_value_is_first_value(self, frame, widget_name):
        widget = getattr(customtkinter, widget_name)(frame, values=["a", "b"])
        assert widget.get() == "a"

    def test_set_does_not_call_command(self, frame, widget_name):
        command = Recorder()
        widget = getattr(customtkinter, widget_name)(frame, values=["a", "b"], command=command)
        widget.set("b")
        assert widget.get() == "b"
        assert command.calls == []

    def test_selection_in_dropdown_calls_command(self, frame, widget_name):
        command = Recorder()
        widget = getattr(customtkinter, widget_name)(frame, values=["a", "b"], command=command)
        widget._dropdown_callback("b")
        assert widget.get() == "b"
        assert command.calls == [("b",)]

    def test_variable(self, frame, widget_name):
        variable = tkinter.StringVar(frame, "b")
        widget = getattr(customtkinter, widget_name)(frame, values=["a", "b", "c"], variable=variable)
        assert widget.get() == "b"
        variable.set("c")
        update(frame)
        assert widget.get() == "c"
        widget._dropdown_callback("a")
        assert variable.get() == "a"

    def test_index(self, frame, widget_name):
        widget = getattr(customtkinter, widget_name)(frame, values=["a", "b", "c"])
        assert widget.index("c") == 2

    def test_cget_returns_copy_of_values(self, frame, widget_name):
        widget = getattr(customtkinter, widget_name)(frame, values=["a", "b"])
        widget.cget("values").append("d")
        assert widget.cget("values") == ["a", "b"]

    def test_dropdown_menu_contains_values(self, frame, widget_name):
        widget = getattr(customtkinter, widget_name)(frame, values=["a", "b", "c"])
        menu = widget._dropdown_menu
        labels = [menu.entrycget(i, "label").strip() for i in range(menu.index("end") + 1)]
        assert labels == ["a", "b", "c"]
        widget.configure(values=["x"])
        assert menu.index("end") == 0

    def test_disabled_does_not_open_dropdown(self, frame, widget_name):
        widget = getattr(customtkinter, widget_name)(frame, values=["a", "b"], state="disabled")
        widget.pack()
        update(frame)
        widget._clicked()
        update(frame)
        assert not widget._dropdown_menu.winfo_ismapped()


def test_combobox_entry_typing(frame):
    combobox = customtkinter.CTkComboBox(frame, values=["a", "b"])
    combobox.set("")
    combobox._entry.insert(0, "typed")
    assert combobox.get() == "typed"


def test_combobox_readonly_state(frame):
    combobox = customtkinter.CTkComboBox(frame, values=["a", "b"], state="readonly")
    combobox._entry.insert(0, "x")
    assert combobox.get() == "a"
    combobox.set("b")
    assert combobox.get() == "b"


def test_optionmenu_dynamic_resizing(frame):
    option_menu = customtkinter.CTkOptionMenu(frame, values=["short", "a much longer value than the default width"])
    option_menu.pack()
    update(frame)
    width_short = option_menu.winfo_width()
    option_menu.set("a much longer value than the default width")
    update(frame)
    assert option_menu.winfo_width() > width_short
    option_menu.configure(dynamic_resizing=False)
    option_menu.set("short")
    update(frame)


# ---------------------------------------------------------------- CTkSegmentedButton

class TestCTkSegmentedButton:
    def test_set_get_index(self, frame):
        segmented = customtkinter.CTkSegmentedButton(frame, values=["a", "b", "c"])
        assert segmented.get() == ""
        segmented.set("b")
        assert segmented.get() == "b"
        assert segmented.index("c") == 2
        assert segmented.len() == 3

    def test_click_calls_command(self, frame):
        command = Recorder()
        segmented = customtkinter.CTkSegmentedButton(frame, values=["a", "b"], command=command)
        segmented._buttons_dict["b"].invoke()
        assert segmented.get() == "b"
        assert command.calls == [("b",)]

    def test_insert_move_delete(self, frame):
        segmented = customtkinter.CTkSegmentedButton(frame, values=["a", "b"])
        segmented.insert(1, "x")
        assert segmented.cget("values") == ["a", "x", "b"]
        segmented.move(0, "b")
        assert segmented.cget("values") == ["b", "a", "x"]
        segmented.delete("a")
        assert segmented.cget("values") == ["b", "x"]

    def test_duplicate_or_missing_values_raise(self, frame):
        segmented = customtkinter.CTkSegmentedButton(frame, values=["a", "b"])
        with pytest.raises(ValueError):
            segmented.insert(0, "a")
        with pytest.raises(ValueError):
            segmented.delete("missing")
        with pytest.raises(ValueError):
            customtkinter.CTkSegmentedButton(frame, values=["a", "a"])

    def test_variable(self, frame):
        variable = tkinter.StringVar(frame, "b")
        segmented = customtkinter.CTkSegmentedButton(frame, values=["a", "b"], variable=variable)
        assert segmented.get() == "b"
        segmented._buttons_dict["a"].invoke()
        assert variable.get() == "a"
        variable.set("b")
        update(frame)
        assert segmented.get() == "b"

    def test_disabled_state(self, frame):
        command = Recorder()
        segmented = customtkinter.CTkSegmentedButton(frame, values=["a", "b"], state="disabled", command=command)
        segmented._buttons_dict["a"].invoke()
        assert command.calls == []
        assert segmented.get() == ""

    def test_vertical_orientation(self, frame):
        segmented = customtkinter.CTkSegmentedButton(frame, values=["a", "b", "c"], orientation="vertical")
        segmented.pack()
        update(frame)
        buttons = segmented._buttons_dict
        assert buttons["a"].winfo_y() < buttons["b"].winfo_y() < buttons["c"].winfo_y()


# ---------------------------------------------------------------- CTkTabview

class TestCTkTabview:
    def test_add_get_set(self, frame):
        tabview = customtkinter.CTkTabview(frame)
        first = tabview.add("One")
        tabview.add("Two")
        assert isinstance(first, customtkinter.CTkFrame)
        assert tabview.tab("One") is first
        assert tabview.get() == "One"
        tabview.set("Two")
        assert tabview.get() == "Two"
        assert tabview.len() == 2
        assert tabview.index("Two") == 1

    def test_command_on_tab_change(self, frame):
        command = Recorder()
        tabview = customtkinter.CTkTabview(frame, command=command)
        tabview.add("One")
        tabview.add("Two")
        tabview._segmented_button._buttons_dict["Two"].invoke()
        assert tabview.get() == "Two"
        assert command.calls == [()]

    def test_only_selected_tab_is_shown(self, frame):
        tabview = customtkinter.CTkTabview(frame)
        tabview.pack()
        one, two = tabview.add("One"), tabview.add("Two")
        update(frame)
        assert one.winfo_ismapped() and not two.winfo_ismapped()
        tabview.set("Two")
        update(frame, 0.2)  # the previous tab is hidden after 100 ms to avoid flickering
        assert two.winfo_ismapped() and not one.winfo_ismapped()

    def test_insert_move_rename_delete(self, frame):
        tabview = customtkinter.CTkTabview(frame)
        tabview.add("A")
        tabview.add("C")
        tabview.insert(1, "B")
        assert tabview._name_list == ["A", "B", "C"]
        assert tabview._segmented_button.cget("values") == ["A", "B", "C"]
        assert tabview.index("B") == 1
        tabview.move(0, "C")
        assert tabview._name_list == ["C", "A", "B"]
        tab_b = tabview.tab("B")
        tabview.rename("B", "Bee")
        assert tabview.tab("Bee") is tab_b
        tabview.delete("A")
        assert tabview._name_list == ["C", "Bee"]

    def test_delete_current_tab_selects_another(self, frame):
        tabview = customtkinter.CTkTabview(frame)
        tabview.add("A")
        tabview.add("B")
        tabview.set("A")
        tabview.delete("A")
        assert tabview.get() == "B"
        tabview.delete("B")
        assert tabview.get() == ""

    def test_invalid_names_raise(self, frame):
        tabview = customtkinter.CTkTabview(frame)
        tabview.add("A")
        with pytest.raises(ValueError):
            tabview.add("A")
        with pytest.raises(ValueError):
            tabview.tab("missing")
        with pytest.raises(ValueError):
            tabview.set("missing")
        with pytest.raises(ValueError):
            tabview.delete("missing")

    def test_configure_without_tabs(self, frame):
        tabview = customtkinter.CTkTabview(frame)
        tabview.configure(corner_radius=3, border_width=2, anchor="s")  # failed with KeyError when no tab was added
        tabview.add("A")
        tabview.configure(corner_radius=8)
        assert tabview.cget("corner_radius") == 8


# ---------------------------------------------------------------- CTkSlider

class TestCTkSlider:
    def test_set_get_and_clamping(self, frame):
        slider = customtkinter.CTkSlider(frame, from_=0, to=100)
        slider.set(30)
        assert slider.get() == pytest.approx(30)
        slider.set(150)
        assert slider.get() == pytest.approx(100)
        slider.set(-5)
        assert slider.get() == pytest.approx(0)

    def test_reversed_range(self, frame):
        slider = customtkinter.CTkSlider(frame, from_=100, to=0)
        slider.set(25)
        assert slider.get() == pytest.approx(25)
        slider.set(200)
        assert slider.get() == pytest.approx(100)

    def test_number_of_steps_rounds_values(self, frame):
        slider = customtkinter.CTkSlider(frame, from_=0, to=10, number_of_steps=5)
        slider.set(3.1)
        assert slider.get() == pytest.approx(4)

    def test_variable_both_directions(self, frame):
        variable = tkinter.DoubleVar(frame, 2)
        slider = customtkinter.CTkSlider(frame, from_=0, to=10, variable=variable)
        assert slider.get() == pytest.approx(2)
        variable.set(7)
        update(frame)
        assert slider.get() == pytest.approx(7)
        slider.set(4)
        assert variable.get() == pytest.approx(4)

    def test_click_calls_command(self, frame):
        command = Recorder()
        slider = customtkinter.CTkSlider(frame, from_=0, to=1, command=command, width=200)
        slider.pack()
        update(frame)

        class Event:
            x, y = 150, 8
        slider._clicked(Event())
        assert len(command.calls) == 1
        assert 0.6 < command.calls[0][0] < 0.9

    def test_mouse_wheel_moves_slider(self, frame):
        slider = customtkinter.CTkSlider(frame, from_=0, to=1)
        slider.set(0.5)

        class Wheel:
            num, delta = 4, 120
        slider._mouse_scroll_event(Wheel())
        assert slider.get() > 0.5

    def test_disabled_ignores_clicks(self, frame):
        command = Recorder()
        slider = customtkinter.CTkSlider(frame, command=command, state="disabled")
        slider.pack()
        update(frame)

        class Event:
            x, y = 10, 8
        slider._clicked(Event())
        assert command.calls == []


# ---------------------------------------------------------------- CTkProgressBar

class TestCTkProgressBar:
    def test_set_get(self, frame):
        progressbar = customtkinter.CTkProgressBar(frame)
        progressbar.set(0.25)
        assert progressbar.get() == pytest.approx(0.25)
        progressbar.set(2)
        assert progressbar.get() == pytest.approx(1)
        progressbar.set(-1)
        assert progressbar.get() == pytest.approx(0)

    def test_variable(self, frame):
        variable = tkinter.DoubleVar(frame, 0.4)
        progressbar = customtkinter.CTkProgressBar(frame, variable=variable)
        assert progressbar.get() == pytest.approx(0.4)
        variable.set(0.8)
        update(frame)
        assert progressbar.get() == pytest.approx(0.8)

    def test_determinate_step(self, frame):
        progressbar = customtkinter.CTkProgressBar(frame, determinate_speed=1)
        progressbar.set(0)
        progressbar.step()
        assert 0 < progressbar.get() < 0.1

    @pytest.mark.parametrize("mode", ["determinate", "indeterminate"])
    def test_start_stop(self, root, frame, mode):
        progressbar = customtkinter.CTkProgressBar(frame, mode=mode)
        progressbar.pack()
        progressbar.set(0)
        progressbar.start()
        update(root, 0.3)
        progressbar.stop()
        value = progressbar._indeterminate_value if mode == "indeterminate" else progressbar.get()
        update(root, 0.1)
        assert value != 0
        assert (progressbar._indeterminate_value if mode == "indeterminate" else progressbar.get()) == value  # stopped


# ---------------------------------------------------------------- CTkScrollbar

class TestCTkScrollbar:
    def test_set_get(self, frame):
        scrollbar = customtkinter.CTkScrollbar(frame)
        scrollbar.set(0.2, 0.6)
        assert scrollbar.get() == pytest.approx((0.2, 0.6))

    def test_connected_to_textbox(self, root, frame):
        textbox = tkinter.Text(frame, height=5)
        scrollbar = customtkinter.CTkScrollbar(frame, command=textbox.yview)
        textbox.configure(yscrollcommand=scrollbar.set)
        textbox.pack(side="left")
        scrollbar.pack(side="right", fill="y")
        textbox.insert("1.0", "\n".join(str(i) for i in range(100)))
        update(root, 0.1)
        start, end = scrollbar.get()
        assert start == 0 and end < 0.2
        textbox.yview_moveto(0.5)
        update(root, 0.1)
        assert scrollbar.get()[0] == pytest.approx(0.5, abs=0.02)


# ---------------------------------------------------------------- CTkTextbox

class TestCTkTextbox:
    def test_insert_get_delete(self, frame):
        textbox = customtkinter.CTkTextbox(frame)
        textbox.insert("1.0", "line 1\nline 2")
        assert textbox.get("1.0", "end-1c") == "line 1\nline 2"
        textbox.delete("1.0", "2.0")
        assert textbox.get("1.0", "end-1c") == "line 2"

    def test_tags_and_search(self, frame):
        textbox = customtkinter.CTkTextbox(frame)
        textbox.insert("1.0", "find the word here")
        position = textbox.search("word", "1.0")
        assert position == "1.9"
        textbox.tag_add("found", position, f"{position}+4c")
        textbox.tag_config("found", foreground="red")
        assert textbox.tag_ranges("found")

    def test_font_option_is_not_allowed_in_tag_config(self, frame):
        textbox = customtkinter.CTkTextbox(frame)
        with pytest.raises(AttributeError):
            textbox.tag_config("x", font=("Arial", 12))

    def test_undo(self, frame):
        textbox = customtkinter.CTkTextbox(frame, undo=True)
        textbox.insert("1.0", "abc")
        textbox.edit_separator()
        textbox.insert("end", "def")
        textbox.edit_undo()
        assert textbox.get("1.0", "end-1c") == "abc"

    def test_disabled_state(self, frame):
        textbox = customtkinter.CTkTextbox(frame, state="disabled")
        textbox.insert("1.0", "x")
        assert textbox.get("1.0", "end-1c") == ""

    def test_scrollbars_appear_when_needed(self, root, frame):
        textbox = customtkinter.CTkTextbox(frame, width=200, height=100, wrap="none")
        textbox.pack()
        update(root, 0.2)
        assert not textbox._y_scrollbar.winfo_ismapped()
        textbox.insert("1.0", "\n".join("x" * 100 for _ in range(50)))
        update(root, 0.3)
        assert textbox._y_scrollbar.winfo_ismapped()
        assert textbox._x_scrollbar.winfo_ismapped()


# ---------------------------------------------------------------- CTkLabel and CTkFrame

class TestCTkLabel:
    def test_text_and_wraplength(self, frame):
        label = customtkinter.CTkLabel(frame, text="a long text that wraps into several lines", wraplength=60)
        label.pack()
        update(frame)
        assert label._label.cget("text") == "a long text that wraps into several lines"
        assert label._label.winfo_reqheight() > 40

    def test_textvariable(self, frame):
        variable = tkinter.StringVar(frame, "from variable")
        label = customtkinter.CTkLabel(frame, textvariable=variable)
        label.pack()
        update(frame)
        assert label._label.cget("text") == "from variable"


class TestCTkFrame:
    def test_winfo_children_without_canvas(self, frame):
        inner = customtkinter.CTkFrame(frame)
        label = customtkinter.CTkLabel(inner)
        assert inner.winfo_children() == [label]

    def test_transparent_child_uses_parent_color(self, frame):
        outer = customtkinter.CTkFrame(frame, fg_color="#336699")
        button = customtkinter.CTkButton(outer)
        assert button.cget("bg_color") == "#336699"

    def test_child_color_follows_parent_configure(self, frame):
        outer = customtkinter.CTkFrame(frame, fg_color="#336699")
        inner = customtkinter.CTkFrame(outer, fg_color="transparent")
        outer.configure(fg_color="#993366")
        assert inner.cget("bg_color") == "#993366"

    def test_tkinter_widget_as_master(self, frame):
        tk_frame = tkinter.Frame(frame, bg="#123123")
        button = customtkinter.CTkButton(tk_frame)
        assert button.cget("bg_color") == "#123123"
        tk_frame.configure(bg="#321321")
        assert button.cget("bg_color") == "#321321"


# ---------------------------------------------------------------- CTkScrollableFrame

class TestCTkScrollableFrame:
    def test_geometry_managers_place_the_outer_frame(self, frame):
        scrollable = customtkinter.CTkScrollableFrame(frame)
        scrollable.pack(fill="x")
        update(frame)
        assert scrollable._parent_frame.winfo_manager() == "pack"
        scrollable.pack_forget()
        scrollable.grid(row=0, column=0)
        update(frame)
        assert scrollable._parent_frame.winfo_manager() == "grid"
        scrollable.grid_forget()
        scrollable.place(x=0, y=0)
        update(frame)
        assert scrollable._parent_frame.winfo_manager() == "place"

    @pytest.mark.parametrize("orientation", ["vertical", "horizontal"])
    def test_content_scrolls(self, root, frame, orientation):
        scrollable = customtkinter.CTkScrollableFrame(frame, width=200, height=150, orientation=orientation)
        scrollable.pack()
        for i in range(40):
            customtkinter.CTkLabel(scrollable, text=f"item {i}").pack(side="top" if orientation == "vertical" else "left")
        update(root, 0.2)
        view = scrollable._parent_canvas.yview if orientation == "vertical" else scrollable._parent_canvas.xview
        assert view()[0] == 0 and view()[1] < 1
        view("moveto", 0.5)
        update(root, 0.1)
        assert view()[0] == pytest.approx(0.5, abs=0.05)

    def test_label_text(self, frame):
        scrollable = customtkinter.CTkScrollableFrame(frame, label_text="Title")
        assert scrollable._label.cget("text") == "Title"
        scrollable.configure(label_text="")
        assert scrollable.cget("label_text") == ""

    def test_scroll_check_with_tcl_widget_string(self, frame):
        scrollable = customtkinter.CTkScrollableFrame(frame)
        assert scrollable._check_if_valid_scroll(".tcl_created_widget") is False  # #2866
        inner = customtkinter.CTkLabel(scrollable)
        assert scrollable._check_if_valid_scroll(inner._label) is True
