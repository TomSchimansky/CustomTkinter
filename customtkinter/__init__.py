__version__ = "3.12"

# import widgets
from .widgets.ctk_button import CTkButton
from .widgets.ctk_checkbox import CTkCheckBox
from .widgets.ctk_entry import CTkEntry
from .widgets.ctk_slider import CTkSlider
from .widgets.ctk_frame import CTkFrame
from .widgets.ctk_progressbar import CTkProgressBar
from .widgets.ctk_label import CTkLabel
from .widgets.ctk_radiobutton import CTkRadioButton
from .widgets.ctk_canvas import CTkCanvas
from .widgets.ctk_switch import CTkSwitch

# import windows
from .windows.ctk_tk import CTk
from .windows.ctk_toplevel import CTkToplevel
from .windows.ctk_input_dialog import CTkInputDialog

# import other classes
from .ctk_settings import CTkSettings
from .appearance_mode_tracker import AppearanceModeTracker
from .ctk_theme_manager import CTkThemeManager
from .scaling_tracker import ScalingTracker

import os
import sys
import shutil


def set_appearance_mode(mode_string):
    AppearanceModeTracker.set_appearance_mode(mode_string)


def get_appearance_mode():
    if AppearanceModeTracker.appearance_mode == 0:
        return "Light"
    elif AppearanceModeTracker.appearance_mode == 1:
        return "Dark"


def set_default_color_theme(color_string):
    CTkThemeManager.load_theme(color_string)


def deactivate_dpi_awareness(deactivate_awareness: bool):
    CTkSettings.deactivate_automatic_dpi_awareness = deactivate_awareness


def set_user_scaling(scaling_value: float):
    ScalingTracker.set_spacing_scaling(scaling_value)
    ScalingTracker.set_widget_scaling(scaling_value)


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
            raise TypeError('fontpath must be of type bytes or str')

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

elif sys.platform.startswith("linux"):
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


