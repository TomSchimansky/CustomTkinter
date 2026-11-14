import json
import os
import sys
import warnings

import pytest

import customtkinter
from customtkinter import CTkFont, CTkImage, ThemeManager, AppearanceModeTracker, ScalingTracker
from conftest import update

try:
    from PIL import Image
except ImportError:
    Image = None

needs_pillow = pytest.mark.skipif(Image is None, reason="Pillow is needed for CTkImage")

THEMES_DIR = os.path.join(os.path.dirname(customtkinter.__file__), "assets", "themes")


def item_fills(canvas, tag) -> set:
    """ fill colors of the canvas items with this tag, image items have no fill option """
    fills = set()
    for canvas_id in canvas.find_withtag(tag):
        if canvas.type(canvas_id) in ("polygon", "rectangle", "oval", "text", "arc", "line"):
            fills.add(canvas.itemcget(canvas_id, "fill"))
        elif canvas_id in canvas._aa_image_items:
            fills.add(canvas._aa_image_items[canvas_id]["fill"])
    return fills


def font_size(tk_widget) -> int:
    """ size of the font tuple of a tkinter widget, negative values are pixels """
    return int(tk_widget.tk.splitlist(tk_widget.cget("font"))[1])


# ---------------------------------------------------------------- CTkFont

class TestCTkFont:
    def test_defaults_come_from_theme(self, root):
        font = CTkFont()
        assert font.cget("family") == ThemeManager.theme["CTkFont"]["family"]
        assert font.cget("size") == ThemeManager.theme["CTkFont"]["size"]
        assert font.cget("weight") == ThemeManager.theme["CTkFont"]["weight"]

    def test_size_is_in_pixels(self, root):
        font = CTkFont(size=20)
        assert font.cget("size") == 20
        assert font.actual("size") != 0
        # tkinter uses negative sizes for pixels
        assert int(root.tk.call("font", "configure", font.name, "-size")) == -20

    def test_create_scaled_tuple(self, root):
        font = CTkFont(family="Arial", size=12, weight="bold", slant="italic", underline=True)
        family, size, style = font.create_scaled_tuple(1.5)
        assert family == "Arial"
        assert size == -18
        assert style.split() == ["bold", "italic", "underline"]

    def test_configure_updates_tuple_and_calls_callbacks(self, root):
        font = CTkFont(size=12)
        calls = []
        callback = lambda: calls.append(font.cget("size"))
        font.add_size_configure_callback(callback)
        font.configure(size=30, weight="bold", overstrike=True)
        assert calls == [30]
        assert font.create_scaled_tuple(1)[1] == -30
        assert "overstrike" in font.create_scaled_tuple(1)[2]

        font.remove_size_configure_callback(callback)
        font.remove_size_configure_callback(callback)  # removing twice is allowed
        font.configure(size=10)
        assert calls == [30]

    def test_config_is_not_supported(self, root):
        with pytest.raises(AttributeError):
            CTkFont().config(size=10)

    def test_copy_is_independent(self, root):
        font = CTkFont(family="Arial", size=17, weight="bold", slant="italic", underline=True)
        copied = font.copy()
        assert isinstance(copied, CTkFont)
        assert copied.name != font.name
        for attribute in ("family", "size", "weight", "slant", "underline", "overstrike"):
            assert copied.cget(attribute) == font.cget(attribute)
        copied.configure(size=40)
        assert font.cget("size") == 17
        del copied  # deleting the copy must not delete the Tcl font of the original
        assert int(root.tk.call("font", "configure", font.name, "-size")) == -17

    def test_widget_follows_font_changes(self, frame):
        font = CTkFont(size=13)
        label = customtkinter.CTkLabel(frame, text="font test", font=font)
        button = customtkinter.CTkButton(frame, text="font test", font=font)
        label.pack()
        button.pack()
        update(frame)
        assert font_size(label._label) == -13
        font.configure(size=26)
        update(frame)
        assert font_size(label._label) == -26
        assert font_size(button._text_label) == -26

    def test_widget_destroy_removes_font_callback(self, frame):
        font = CTkFont(size=13)
        widgets = [customtkinter.CTkButton(frame, font=font), customtkinter.CTkLabel(frame, font=font),
                   customtkinter.CTkEntry(frame, font=font), customtkinter.CTkComboBox(frame, font=font)]
        assert len(font._size_configure_callback_list) >= len(widgets)
        for widget in widgets:
            widget.destroy()
        assert font._size_configure_callback_list == []

    def test_font_tuple_without_size_gets_default_size(self, frame):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            button = customtkinter.CTkButton(frame, font=("Arial",))
        assert any("without size" in str(warning.message) for warning in caught)
        assert button.cget("font") == ("Arial", ThemeManager.theme["CTkFont"]["size"])

    @pytest.mark.parametrize("font", [("Arial", 14), ("Arial", 14, "bold"), ("Arial", 14, "bold italic"),
                                      ("Arial", 14, "bold", "italic"), ("Arial", -14, "bold italic underline overstrike")])
    def test_font_tuples(self, frame, font):
        for widget_class in (customtkinter.CTkButton, customtkinter.CTkLabel, customtkinter.CTkEntry,
                             customtkinter.CTkCheckBox, customtkinter.CTkOptionMenu, customtkinter.CTkTextbox):
            widget = widget_class(frame, font=font)
            widget.configure(font=font)
        customtkinter.set_widget_scaling(1.5)
        update(frame)

    def test_invalid_font_type_raises(self, frame):
        with pytest.raises(ValueError):
            customtkinter.CTkButton(frame, font=12)

    def test_widget_scaling_scales_font(self, frame):
        label = customtkinter.CTkLabel(frame, text="scaled", font=("Arial", 20))
        label.pack()
        assert font_size(label._label) == -20
        customtkinter.set_widget_scaling(2)
        update(frame)
        assert font_size(label._label) == -40


# ---------------------------------------------------------------- CTkImage

@needs_pillow
class TestCTkImage:
    def test_needs_an_image(self, root):
        with pytest.raises(ValueError):
            CTkImage()

    def test_wrong_type_raises(self, root):
        with pytest.raises(ValueError):
            CTkImage(light_image="image.png")
        with pytest.raises(ValueError):
            CTkImage(dark_image=root)

    def test_light_and_dark_must_have_same_size(self, root):
        with pytest.raises(ValueError):
            CTkImage(Image.new("RGB", (10, 10)), Image.new("RGB", (20, 10)))

    def test_cget(self, root):
        light, dark = Image.new("RGB", (10, 10), "white"), Image.new("RGB", (10, 10), "black")
        image = CTkImage(light, dark, size=(30, 40))
        assert image.cget("light_image") is light
        assert image.cget("dark_image") is dark
        assert image.cget("size") == (30, 40)

    def test_scaled_photo_image_size_and_cache(self, root):
        image = CTkImage(Image.new("RGB", (10, 10), "red"), size=(30, 20))
        photo = image.create_scaled_photo_image(1, "light")
        assert (photo.width(), photo.height()) == (30, 20)
        assert image.create_scaled_photo_image(1, "light") is photo
        scaled = image.create_scaled_photo_image(1.5, "light")
        assert (scaled.width(), scaled.height()) == (45, 30)

    def test_missing_mode_uses_other_image(self, root):
        only_light = CTkImage(light_image=Image.new("RGB", (4, 4), "red"))
        assert only_light.create_scaled_photo_image(1, "dark") is only_light.create_scaled_photo_image(1, "light")
        only_dark = CTkImage(dark_image=Image.new("RGB", (4, 4), "blue"))
        assert only_dark.create_scaled_photo_image(1, "light") is only_dark.create_scaled_photo_image(1, "dark")

    def test_light_and_dark_images(self, root):
        image = CTkImage(Image.new("RGB", (4, 4), (255, 0, 0)), Image.new("RGB", (4, 4), (0, 0, 255)), size=(4, 4))
        def pixel(photo):
            return tuple(int(value) for value in root.tk.splitlist(root.tk.call(str(photo), "get", 1, 1)))[:3]
        assert pixel(image.create_scaled_photo_image(1, "light")) == (255, 0, 0)
        assert pixel(image.create_scaled_photo_image(1, "dark")) == (0, 0, 255)

    def test_configure_calls_callbacks_and_clears_cache(self, root):
        image = CTkImage(Image.new("RGB", (4, 4), "red"), size=(10, 10))
        old_photo = image.create_scaled_photo_image(1, "light")
        calls = []
        image.add_configure_callback(lambda: calls.append(1))
        image.configure(light_image=Image.new("RGB", (4, 4), "green"), size=(12, 12))
        assert calls == [1]
        new_photo = image.create_scaled_photo_image(1, "light")
        assert new_photo is not old_photo
        assert new_photo.width() == 12

    def test_widgets_follow_image_changes(self, frame):
        image = CTkImage(Image.new("RGB", (4, 4), (255, 0, 0)), Image.new("RGB", (4, 4), (0, 0, 255)), size=(16, 16))
        button = customtkinter.CTkButton(frame, text="", image=image)
        label = customtkinter.CTkLabel(frame, text="", image=image)
        button.pack()
        label.pack()
        update(frame)
        assert str(button._image_label.cget("image")) == str(image.create_scaled_photo_image(1, "light"))
        assert str(label._label.cget("image")) == str(image.create_scaled_photo_image(1, "light"))

        customtkinter.set_appearance_mode("dark")
        update(frame)
        assert str(button._image_label.cget("image")) == str(image.create_scaled_photo_image(1, "dark"))
        assert str(label._label.cget("image")) == str(image.create_scaled_photo_image(1, "dark"))

        image.configure(size=(24, 24))
        update(frame)
        assert int(root_call(button, "image", "width", button._image_label.cget("image"))) == 24

        customtkinter.set_widget_scaling(2)
        update(frame)
        assert int(root_call(label, "image", "width", label._label.cget("image"))) == 48

    def test_widget_destroy_removes_image_callback(self, frame):
        image = CTkImage(Image.new("RGB", (4, 4)), size=(10, 10))
        button = customtkinter.CTkButton(frame, image=image)
        label = customtkinter.CTkLabel(frame, image=image)
        assert len(image._configure_callback_list) == 2
        button.destroy()
        label.destroy()
        assert image._configure_callback_list == []
        image.configure(size=(20, 20))  # must not update the destroyed widgets


def root_call(widget, *args):
    return widget.tk.call(*args)


# ---------------------------------------------------------------- FontManager

@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="fonts are copied only on Linux")
class TestFontManagerLinux:
    def test_load_font_copies_once(self, tmp_path, monkeypatch):
        monkeypatch.setattr(customtkinter.FontManager, "linux_font_path", str(tmp_path / "fonts"))
        assert customtkinter.FontManager.init_font_manager()
        font_file = tmp_path / "MyFont.otf"
        font_file.write_bytes(b"font data")
        assert customtkinter.FontManager.load_font(str(font_file))
        copied = tmp_path / "fonts" / "MyFont.otf"
        assert copied.read_bytes() == b"font data"

        # an identical file is not written again
        modification_time = copied.stat().st_mtime_ns
        os.utime(copied, ns=(modification_time - 10 ** 9, modification_time - 10 ** 9))
        assert customtkinter.FontManager.load_font(str(font_file))
        assert copied.stat().st_mtime_ns == modification_time - 10 ** 9

        # a changed file is copied again
        font_file.write_bytes(b"new font data")
        assert customtkinter.FontManager.load_font(str(font_file))
        assert copied.read_bytes() == b"new font data"

    def test_load_font_replaces_read_only_copy(self, tmp_path, monkeypatch):
        monkeypatch.setattr(customtkinter.FontManager, "linux_font_path", str(tmp_path))
        font_file = tmp_path / "source" / "Font.otf"
        font_file.parent.mkdir()
        font_file.write_bytes(b"version 2")
        copied = tmp_path / "Font.otf"
        copied.write_bytes(b"version 1")
        copied.chmod(0o444)
        assert customtkinter.FontManager.load_font(str(font_file))
        assert copied.read_bytes() == b"version 2"

    def test_load_missing_font_returns_false(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setattr(customtkinter.FontManager, "linux_font_path", str(tmp_path))
        assert customtkinter.FontManager.load_font(str(tmp_path / "missing.otf")) is False
        assert "FontManager error" in capsys.readouterr().err


def test_default_fonts_stay_allocated(root):
    holder = root.__dict__.get("_ctk_default_font_holder")
    assert holder is not None
    # created directly in Tcl, so it's not visible to the user
    assert all(not str(child).endswith(holder) for child in root.winfo_children())
    customtkinter.FontManager.keep_default_fonts_allocated(root)  # second call does nothing
    assert root.__dict__.get("_ctk_default_font_holder") == holder


# ---------------------------------------------------------------- ThemeManager

ALL_WIDGET_CLASSES = ["CTk", "CTkToplevel", "CTkFrame", "CTkButton", "CTkLabel", "CTkEntry", "CTkCheckBox", "CTkSwitch",
                      "CTkRadioButton", "CTkProgressBar", "CTkSlider", "CTkOptionMenu", "CTkComboBox", "CTkScrollbar",
                      "CTkSegmentedButton", "CTkTextbox", "CTkScrollableFrame", "CTkFont", "DropdownMenu"]


@pytest.mark.parametrize("theme_name", ["blue", "green", "dark-blue"])
def test_built_in_themes(theme_name, frame):
    customtkinter.set_default_color_theme(theme_name)
    for widget_class in ALL_WIDGET_CLASSES:
        assert widget_class in ThemeManager.theme
    # values for other platforms are removed
    assert "macOS" not in ThemeManager.theme["CTkFont"]
    assert isinstance(ThemeManager.theme["CTkFont"]["size"], int)

    button = customtkinter.CTkButton(frame)
    assert button.cget("fg_color") == ThemeManager.theme["CTkButton"]["fg_color"]
    for widget_class in (customtkinter.CTkSwitch, customtkinter.CTkSlider, customtkinter.CTkTabview,
                         customtkinter.CTkScrollableFrame, customtkinter.CTkTextbox):
        widget_class(frame).pack()
    update(frame)


def write_custom_theme(tmp_path, change) -> str:
    with open(os.path.join(THEMES_DIR, "blue.json")) as file:
        theme = json.load(file)
    change(theme)
    path = tmp_path / "custom_theme.json"
    path.write_text(json.dumps(theme))
    return str(path)


def test_custom_theme_file(tmp_path, frame):
    def change(theme):
        theme["CTkButton"]["fg_color"] = ["#112233", "#445566"]
        theme["CTkCheckbox"] = theme.pop("CTkCheckBox")  # old name
        theme["CTkLabel"].pop("border_width", None)

    customtkinter.set_default_color_theme(write_custom_theme(tmp_path, change))
    button = customtkinter.CTkButton(frame)
    assert button.cget("fg_color") == ["#112233", "#445566"]
    assert "CTkCheckBox" in ThemeManager.theme and "CTkCheckbox" not in ThemeManager.theme
    assert ThemeManager.theme["CTkLabel"]["border_width"] == 0
    customtkinter.CTkCheckBox(frame).pack()
    customtkinter.CTkLabel(frame).pack()
    update(frame)


def test_save_custom_theme(tmp_path):
    path = write_custom_theme(tmp_path, lambda theme: None)
    customtkinter.set_default_color_theme(path)
    ThemeManager.theme["CTkButton"]["corner_radius"] = 17
    ThemeManager.save_theme()
    with open(path) as file:
        assert json.load(file)["CTkButton"]["corner_radius"] == 17


def test_save_built_in_theme_raises():
    customtkinter.set_default_color_theme("green")
    with pytest.raises(ValueError):
        ThemeManager.save_theme()


def test_missing_theme_raises():
    with pytest.raises(FileNotFoundError):
        customtkinter.set_default_color_theme("this_theme_does_not_exist")


# ---------------------------------------------------------------- appearance mode

def test_set_and_get_appearance_mode(root):
    customtkinter.set_appearance_mode("dark")
    assert customtkinter.get_appearance_mode() == "Dark"
    assert AppearanceModeTracker.appearance_mode_set_by == "user"
    customtkinter.set_appearance_mode("LIGHT")
    assert customtkinter.get_appearance_mode() == "Light"
    customtkinter.set_appearance_mode("System")
    assert AppearanceModeTracker.appearance_mode_set_by == "system"
    assert customtkinter.get_appearance_mode() in ("Light", "Dark")


def test_widgets_follow_appearance_mode(frame):
    button = customtkinter.CTkButton(frame, fg_color=("#ff0000", "#0000ff"), border_width=2,
                                     border_color=("#00ff00", "#ffff00"))
    button.pack()
    frame.configure(fg_color=("#eeeeee", "#111111"))
    update(frame)
    assert item_fills(button._canvas, "inner_parts") == {"#ff0000"}
    assert item_fills(button._canvas, "border_parts") == {"#00ff00"}
    assert item_fills(frame._canvas, "inner_parts") == {"#eeeeee"}
    assert button._canvas.cget("bg") == "#eeeeee"  # transparent background takes the parent color

    customtkinter.set_appearance_mode("dark")
    update(frame)
    assert item_fills(button._canvas, "inner_parts") == {"#0000ff"}
    assert item_fills(button._canvas, "border_parts") == {"#ffff00"}
    assert item_fills(frame._canvas, "inner_parts") == {"#111111"}
    assert button._canvas.cget("bg") == "#111111"


def test_window_follows_appearance_mode(root):
    root.configure(fg_color=("#dddddd", "#222222"))
    try:
        assert root.cget("bg") == "#dddddd"
        customtkinter.set_appearance_mode("dark")
        assert root.cget("bg") == "#222222"
    finally:
        root.configure(fg_color=ThemeManager.theme["CTk"]["fg_color"])


def test_trackers_forget_destroyed_widgets(frame):
    appearance_callbacks = len(AppearanceModeTracker.callback_list)
    window = ScalingTracker.get_window_root_of_widget(frame)
    scaling_callbacks = len(ScalingTracker.window_widgets_dict[window])

    container = customtkinter.CTkFrame(frame)
    for widget_class in (customtkinter.CTkButton, customtkinter.CTkEntry, customtkinter.CTkComboBox,
                         customtkinter.CTkSlider, customtkinter.CTkTabview, customtkinter.CTkScrollableFrame,
                         customtkinter.CTkTextbox, customtkinter.CTkSegmentedButton):
        widget_class(container)
    assert len(AppearanceModeTracker.callback_list) > appearance_callbacks
    container.destroy()
    assert len(AppearanceModeTracker.callback_list) == appearance_callbacks
    assert len(ScalingTracker.window_widgets_dict[window]) == scaling_callbacks


def test_trackers_forget_destroyed_windows(root):
    windows = len(ScalingTracker.window_dpi_scaling_dict)
    toplevels = [customtkinter.CTkToplevel(root) for _ in range(3)]
    update(root)
    for toplevel in toplevels:
        toplevel.destroy()
    update(root)
    assert len(ScalingTracker.window_dpi_scaling_dict) == windows
    assert not any(toplevel in AppearanceModeTracker.app_list for toplevel in toplevels)
