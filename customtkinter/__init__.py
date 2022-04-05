__version__ = "3.9"

from .customtkinter_input_dialog import CTkInputDialog
from .customtkinter_button import CTkButton
from .customtkinter_slider import CTkSlider
from .customtkinter_frame import CTkFrame
from .customtkinter_progressbar import CTkProgressBar
from .customtkinter_label import CTkLabel
from .customtkinter_entry import CTkEntry
from .customtkinter_checkbox import CTkCheckBox
from .customtkinter_radiobutton import CTkRadioButton
from .customtkinter_tk import CTk
from .customtkinter_canvas import CTkCanvas
from .customtkinter_switch import CTkSwitch
from .customtkinter_toplevel import CTkToplevel
from .customtkinter_settings import CTkSettings

from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_theme_manager import CTkThemeManager

from distutils.version import StrictVersion as Version
import tkinter
import os
import sys
import shutil


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
    CTkThemeManager.load_theme(color_string)


# Load fonts:
if sys.platform.startswith("win"):
    from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

    FR_PRIVATE = 0x10
    FR_NOT_ENUM = 0x20


    def loadfont(fontpath, private=True, enumerable=False):
        """ Function taken from: https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter/30631309#30631309 """

        if isinstance(fontpath, bytes):
            pathbuf = create_string_buffer(fontpath)
            AddFontResourceEx = windll.gdi32.AddFontResourceExA
        elif isinstance(fontpath, str):
            pathbuf = create_unicode_buffer(fontpath)
            AddFontResourceEx = windll.gdi32.AddFontResourceExW
        else:
            raise TypeError('fontpath must be of type str or unicode')

        flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
        num_fonts_added = AddFontResourceEx(byref(pathbuf), flags, 0)
        return bool(num_fonts_added)


    # load text fonts and custom font with circle shapes for round corner rendering
    script_directory = os.path.dirname(os.path.abspath(__file__))
    CTkSettings.circle_font_is_ready = loadfont(os.path.join(script_directory, "assets", "fonts", "CustomTkinter_shapes_font-fine.otf"))
    loadfont(os.path.join(script_directory, "assets", "fonts", "Roboto", "Roboto-Regular.ttf"))
    loadfont(os.path.join(script_directory, "assets", "fonts", "Roboto", "Roboto-Medium.ttf"))

    # correct drawing method if font could not be loaded
    if not CTkSettings.circle_font_is_ready:
        if CTkSettings.preferred_drawing_method == "font_shapes":
            sys.stderr.write("WARNING (customtkinter.CTkSettings): " +
                             "Preferred drawing method 'font_shapes' can not be used because the font file could not be loaded.\n" +
                             "Using 'circle_shapes' instead. The rendering quality will be very bad!")
            CTkSettings.preferred_drawing_method = "circle_shapes"

elif sys.platform == "linux":
    try:
        if not os.path.isdir(os.path.expanduser('~/.fonts/')):
            os.mkdir(os.path.expanduser('~/.fonts/'))

        script_directory = os.path.dirname(os.path.abspath(__file__))

        # copy fonts in user font folder
        shutil.copy(os.path.join(script_directory, "assets", "fonts", "Roboto", "Roboto-Regular.ttf"),
                    os.path.expanduser("~/.fonts/"))
        shutil.copy(os.path.join(script_directory, "assets", "fonts", "Roboto", "Roboto-Medium.ttf"),
                    os.path.expanduser("~/.fonts/"))
        shutil.copy(os.path.join(script_directory, "assets", "fonts", "CustomTkinter_shapes_font-fine.otf"),
                    os.path.expanduser("~/.fonts/"))

    except Exception as err:
        sys.stderr.write(str(err) + "\n")
        sys.stderr.write("WARNING (customtkinter.CTkSettings): " +
                         "Preferred drawing method 'font_shapes' can not be used because the font file could not be copied to ~/.fonts/.\n" +
                         "Using 'circle_shapes' instead. The rendering quality will be very bad!\n")
        CTkSettings.preferred_drawing_method = "circle_shapes"


