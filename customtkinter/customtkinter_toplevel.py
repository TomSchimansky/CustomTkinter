import tkinter
from distutils.version import StrictVersion as Version
import sys
import os
import platform
import ctypes

from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_theme_manager import CTkThemeManager


class CTkToplevel(tkinter.Toplevel):
    def __init__(self, *args,
                 fg_color="default_theme",
                 **kwargs):

        self.enable_macos_dark_title_bar()
        super().__init__(*args, **kwargs)
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.fg_color = CTkThemeManager.theme["color"]["window_bg_color"] if fg_color == "default_theme" else fg_color

        if "bg" in kwargs:
            self.fg_color = kwargs["bg"]
            del kwargs["bg"]
        elif "background" in kwargs:
            self.fg_color = kwargs["background"]
            del kwargs["background"]

        AppearanceModeTracker.add(self.set_appearance_mode, self)
        super().configure(bg=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))
        super().title("CTkToplevel")

        if sys.platform.startswith("win"):
            if self.appearance_mode == 1:
                self.windows_set_titlebar_color("dark")
            else:
                self.windows_set_titlebar_color("light")

    def destroy(self):
        AppearanceModeTracker.remove(self.set_appearance_mode)
        self.disable_macos_dark_title_bar()
        super().destroy()

    def resizable(self, *args, **kwargs):
        super().resizable(*args, **kwargs)

        if sys.platform.startswith("win"):
            if self.appearance_mode == 1:
                self.windows_set_titlebar_color("dark")
            else:
                self.windows_set_titlebar_color("light")

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        bg_changed = False

        if "bg" in kwargs:
            self.fg_color = kwargs["bg"]
            bg_changed = True
            kwargs["bg"] = CTkThemeManager.single_color(self.fg_color, self.appearance_mode)
        elif "background" in kwargs:
            self.fg_color = kwargs["background"]
            bg_changed = True
            kwargs["background"] = CTkThemeManager.single_color(self.fg_color, self.appearance_mode)
        elif "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            kwargs["bg"] = CTkThemeManager.single_color(self.fg_color, self.appearance_mode)
            del kwargs["fg_color"]
            bg_changed = True

        elif len(args) > 0 and type(args[0]) == dict:
            if "bg" in args[0]:
                self.fg_color=args[0]["bg"]
                bg_changed = True
                args[0]["bg"] = CTkThemeManager.single_color(self.fg_color, self.appearance_mode)
            elif "background" in args[0]:
                self.fg_color=args[0]["background"]
                bg_changed = True
                args[0]["background"] = CTkThemeManager.single_color(self.fg_color, self.appearance_mode)

        if bg_changed:
            from .customtkinter_slider import CTkSlider
            from .customtkinter_progressbar import CTkProgressBar
            from .customtkinter_label import CTkLabel
            from .customtkinter_frame import CTkFrame
            from .customtkinter_entry import CTkEntry
            from customtkinter.customtkinter_checkbox import CTkCheckBox
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

        if sys.platform.startswith("win"):

            super().withdraw()  # hide window so that it can be redrawn after the titlebar change so that the color change is visible
            super().update()

            if color_mode.lower() == "dark":
                value = 1
            elif color_mode.lower() == "light":
                value = 0
            else:
                return

            try:
                hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19

                # try with DWMWA_USE_IMMERSIVE_DARK_MODE
                if ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                                                              ctypes.byref(ctypes.c_int(value)),
                                                              ctypes.sizeof(ctypes.c_int(value))) != 0:
                    # try with DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20h1
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1,
                                                               ctypes.byref(ctypes.c_int(value)),
                                                               ctypes.sizeof(ctypes.c_int(value)))

            except Exception as err:
                print(err)

            self.deiconify()

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

        super().configure(bg=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))
