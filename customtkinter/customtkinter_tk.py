import tkinter
from distutils.version import StrictVersion as Version
import sys
import os
import platform

from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTk(tkinter.Tk):
    def __init__(self, *args,
                 bg_color=CTkColorManager.WINDOW_BG,
                 **kwargs):

        self.enable_macos_dark_title_bar()
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.bg_color = bg_color
        if "bg" in kwargs:
            self.bg_color = kwargs["bg"]
            del kwargs["bg"]
        elif "background" in kwargs:
            self.bg_color = kwargs["background"]
            del kwargs["background"]

        super().__init__(*args, **kwargs)

        AppearanceModeTracker.add(self.set_appearance_mode)
        super().configure(bg=CTkColorManager.single_color(self.bg_color, self.appearance_mode))

    def destroy(self):
        AppearanceModeTracker.remove(self.set_appearance_mode)
        self.disable_macos_dark_title_bar()
        super().destroy()

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        if "bg" in kwargs:
            self.bg_color = kwargs["bg"]
        elif "background" in kwargs:
            self.bg_color = kwargs["background"]

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

    def set_appearance_mode(self, mode_string):
        if mode_string.lower() == "dark":
            self.appearance_mode = 1
        elif mode_string.lower() == "light":
            self.appearance_mode = 0

        super().configure(bg=CTkColorManager.single_color(self.bg_color, self.appearance_mode))
