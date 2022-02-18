import tkinter
from distutils.version import StrictVersion as Version
import sys
import os
import platform
import ctypes

from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTk(tkinter.Tk):
    def __init__(self, *args,
                 fg_color="CTkColorManager",
                 **kwargs):

        self.enable_macos_dark_title_bar()
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.fg_color = CTkColorManager.WINDOW_BG if fg_color == "CTkColorManager" else fg_color

        if "bg" in kwargs:
            self.fg_color = kwargs["bg"]
            del kwargs["bg"]
        elif "background" in kwargs:
            self.fg_color = kwargs["background"]
            del kwargs["background"]

        super().__init__(*args, **kwargs)

        AppearanceModeTracker.add(self.set_appearance_mode, self)
        super().configure(bg=CTkColorManager.single_color(self.fg_color, self.appearance_mode))

        self.window_exists = False  # indicates if the window is already shown through .update or .mainloop

        if sys.platform.startswith("win"):
            if self.appearance_mode == 1:
                self.windows_set_titlebar_color("dark")
            else:
                self.windows_set_titlebar_color("light")

    def destroy(self):
        AppearanceModeTracker.remove(self.set_appearance_mode)
        self.disable_macos_dark_title_bar()
        super().destroy()

    def update(self):
        if self.window_exists is False:
            self.deiconify()
            self.window_exists = True
        super().update()

    def mainloop(self, *args, **kwargs):
        if self.window_exists is False:
            self.deiconify()
            self.window_exists = True
        super().mainloop(*args, **kwargs)

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        bg_changed = False

        if "bg" in kwargs:
            self.fg_color = kwargs["bg"]
            bg_changed = True
            kwargs["bg"] = CTkColorManager.single_color(self.fg_color, self.appearance_mode)
        elif "background" in kwargs:
            self.fg_color = kwargs["background"]
            bg_changed = True
            kwargs["background"] = CTkColorManager.single_color(self.fg_color, self.appearance_mode)
        elif "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            kwargs["bg"] = CTkColorManager.single_color(self.fg_color, self.appearance_mode)
            del kwargs["fg_color"]
            bg_changed = True

        elif len(args) > 0 and type(args[0]) == dict:
            if "bg" in args[0]:
                self.fg_color=args[0]["bg"]
                bg_changed = True
                args[0]["bg"] = CTkColorManager.single_color(self.fg_color, self.appearance_mode)
            elif "background" in args[0]:
                self.fg_color=args[0]["background"]
                bg_changed = True
                args[0]["background"] = CTkColorManager.single_color(self.fg_color, self.appearance_mode)

        if bg_changed:
            from .customtkinter_slider import CTkSlider
            from .customtkinter_progressbar import CTkProgressBar
            from .customtkinter_label import CTkLabel
            from .customtkinter_frame import CTkFrame
            from .customtkinter_entry import CTkEntry
            from .customtkinter_checkbox import CTkCheckBox
            from .customtkinter_button import CTkButton

            for child in self.winfo_children():
                if isinstance(child, (CTkFrame, CTkButton, CTkLabel, CTkSlider, CTkCheckBox, CTkEntry, CTkProgressBar)):
                    child.configure(bg_color=self.fg_color)

        super().configure(*args, **kwargs)

    @staticmethod
    def enable_macos_dark_title_bar():
        if sys.platform == "darwin":  # macOS
            if Version(platform.python_version()) < Version("3.10"):
                if Version(tkinter.Tcl().call("info", "patchlevel")) >= Version("8.6.9"):  # Tcl/Tk >= 8.6.9
                    os.system("defaults write -g NSRequiresAquaSystemAppearance -bool No")

    @staticmethod
    def disable_macos_dark_title_bar():
        if sys.platform == "darwin":  # macOS
            if Version(platform.python_version()) < Version("3.10"):
                if Version(tkinter.Tcl().call("info", "patchlevel")) >= Version("8.6.9"):  # Tcl/Tk >= 8.6.9
                    os.system("defaults delete -g NSRequiresAquaSystemAppearance")
                    # This command reverts the dark-mode setting for all programs.

    def windows_set_titlebar_color(self, color_mode: str):
        """
        Set the titlebar color of the window to light or dark theme on Microsoft Windows.

        Credits for this function:
        https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter/70724666#70724666

        MORE INFO:
        https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
        """

        if self.window_exists is False:
            super().withdraw()  # hide window if it not already exists to not show the .update call which is needed

        super().update()

        if color_mode.lower() == "dark":
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        elif color_mode.lower() == "light":
            DWMWA_USE_IMMERSIVE_DARK_MODE = 19
        else:
            return

        set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ctypes.windll.user32.GetParent
        hwnd = get_parent(self.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = 2
        value = ctypes.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ctypes.byref(value),
                             ctypes.sizeof(value))

    def set_appearance_mode(self, mode_string):
        if mode_string.lower() == "dark":
            self.appearance_mode = 1
        elif mode_string.lower() == "light":
            self.appearance_mode = 0

        if sys.platform.startswith("win"):
            if self.appearance_mode == 1:
                self.windows_set_titlebar_color("dark")
            else:
                self.windows_set_titlebar_color("light")

        super().configure(bg=CTkColorManager.single_color(self.fg_color, self.appearance_mode))
