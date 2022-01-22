__version__ = "2.0"

from .customtkinter_button import CTkButton
from .customtkinter_slider import CTkSlider
from .customtkinter_frame import CTkFrame
from .customtkinter_progressbar import CTkProgressBar
from .customtkinter_label import CTkLabel
from .customtkinter_entry import CTkEntry
from .customtkinter_dialog import CTkDialog
from .customtkinter_checkbox import CTkCheckBox
from .customtkinter_tk import CTk

from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager

from distutils.version import StrictVersion as Version
import tkinter
import os
import sys


def enable_macos_darkmode():
    if sys.platform == "darwin":  # macOS
        if Version(tkinter.Tcl().call("info", "patchlevel")) >= Version("8.6.9"):  # Tcl/Tk >= 8.6.9
            os.system("defaults write -g NSRequiresAquaSystemAppearance -bool No")

            sys.stderr.write("WARNING (customtkinter.enable_macos_darkmode): " +
                             "This command forces macOS dark-mode on all programs. " +
                             "This can cause bugs on some other programs.\n" +
                             "Disable it by calling customtkinter.disable_macos_darkmode() at the end of the program.\n")
        else:
            sys.stderr.write("WARNING (customtkinter.enable_macos_darkmode): " +
                             "Currently this works only with anaconda python version (Tcl/Tk >= 8.6.9).\n" +
                             "(python.org Tcl/Tk version is only 8.6.8)\n")
    else:
        sys.stderr.write("WARNING (customtkinter.enable_macos_darkmode): " +
                         "System is not macOS, but the following: {}\n".format(sys.platform))


def disable_macos_darkmode():
    if sys.platform == "darwin":  # macOS
        if Version(tkinter.Tcl().call("info", "patchlevel")) >= Version("8.6.9"):  # Tcl/Tk >= 8.6.9
            os.system("defaults delete -g NSRequiresAquaSystemAppearance")
            # This command reverts the dark-mode setting for all programs.


def set_appearance_mode(mode_string):
    AppearanceModeTracker.set_appearance_mode(mode_string)


def get_appearance_mode():
    if AppearanceModeTracker.appearance_mode == 0:
        return "Light"
    elif AppearanceModeTracker.appearance_mode == 1:
        return "Dark"


def set_default_color_theme(color_string):
    CTkColorManager.initialize_color_theme(color_string)
