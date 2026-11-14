import sys
import os
import shutil
import tkinter
from typing import Union


class FontManager:

    linux_font_path = "~/.fonts/"
    _default_font_holder_name = "__ctk_default_font_holder"

    @classmethod
    def init_font_manager(cls):
        # Linux
        if sys.platform.startswith("linux"):
            try:
                if not os.path.isdir(os.path.expanduser(cls.linux_font_path)):
                    os.mkdir(os.path.expanduser(cls.linux_font_path))
                return True
            except Exception as err:
                sys.stderr.write("FontManager error: " + str(err) + "\n")
                return False

        # other platforms
        else:
            return True

    @classmethod
    def windows_load_font(cls, font_path: Union[str, bytes], private: bool = True, enumerable: bool = False) -> bool:
        """ Function taken from: https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter/30631309#30631309 """

        from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

        FR_PRIVATE = 0x10
        FR_NOT_ENUM = 0x20

        if isinstance(font_path, bytes):
            path_buffer = create_string_buffer(font_path)
            add_font_resource_ex = windll.gdi32.AddFontResourceExA
        elif isinstance(font_path, str):
            path_buffer = create_unicode_buffer(font_path)
            add_font_resource_ex = windll.gdi32.AddFontResourceExW
        else:
            raise TypeError('font_path must be of type bytes or str')

        flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
        num_fonts_added = add_font_resource_ex(byref(path_buffer), flags, 0)
        return bool(min(num_fonts_added, 1))

    @classmethod
    def keep_default_fonts_allocated(cls, widget: tkinter.Misc):
        """ Tk frees a font as soon as no widget uses it anymore. Every new tkinter Label, Entry, Text and Menu
        first allocates its default font (TkDefaultFont, ...) before CustomTkinter sets its own font. If no other
        widget uses the default font, Tk loads it again for every widget, which takes about 1 ms on Linux (fontconfig).
        A hidden canvas with a text item for each default font keeps them allocated. It's created directly in Tcl,
        so it doesn't appear in winfo_children(). Called once per root window. """
        root = widget._root()
        if root.__dict__.get("_ctk_default_font_holder") is not None:
            return
        holder = f"{'' if root._w == '.' else root._w}.{cls._default_font_holder_name}"
        try:
            if not int(root.tk.call("winfo", "exists", holder)):
                root.tk.call("canvas", holder, "-width", 0, "-height", 0, "-highlightthickness", 0, "-takefocus", 0)
                for font in ("TkDefaultFont", "TkTextFont", "TkFixedFont", "TkMenuFont"):
                    root.tk.call(holder, "create", "text", 0, 0, "-text", "", "-font", font)
            root.__dict__["_ctk_default_font_holder"] = holder
        except tkinter.TclError:
            root.__dict__["_ctk_default_font_holder"] = ""  # don't try again

    @classmethod
    def load_font(cls, font_path: str) -> bool:
        # Windows
        if sys.platform.startswith("win"):
            return cls.windows_load_font(font_path, private=True, enumerable=False)

        # Linux
        elif sys.platform.startswith("linux"):
            try:
                shutil.copy(font_path, os.path.expanduser(cls.linux_font_path))
                return True
            except Exception as err:
                sys.stderr.write("FontManager error: " + str(err) + "\n")
                return False

        # macOS and others
        else:
            return False
