__version__ = "3.12"

import os
import sys

# import manager classes
from .settings import Settings
from .appearance_mode_tracker import AppearanceModeTracker
from .theme_manager import ThemeManager
from .scaling_tracker import ScalingTracker
from .font_manager import FontManager

Settings.init_font_character_mapping()
Settings.init_drawing_method()

AppearanceModeTracker.init_appearance_mode()

ThemeManager.load_theme("blue")

FontManager.init_font_manager()

# load Roboto fonts
script_directory = os.path.dirname(os.path.abspath(__file__))
FontManager.load_font(os.path.join(script_directory, "assets", "fonts", "Roboto", "Roboto-Regular.ttf"))
FontManager.load_font(os.path.join(script_directory, "assets", "fonts", "Roboto", "Roboto-Medium.ttf"))

# load font necessary for rendering the widgets on Windows, Linux
if FontManager.load_font(os.path.join(script_directory, "assets", "fonts", "CustomTkinter_shapes_font-fine.otf")) is True:
    Settings.circle_font_is_ready = True
else:
    Settings.circle_font_is_ready = False

    if Settings.preferred_drawing_method == "font_shapes":
        sys.stderr.write("customtkinter.__init__ warning: " +
                         "Preferred drawing method 'font_shapes' can not be used because the font file could not be loaded.\n" +
                         "Using 'circle_shapes' instead. The rendering quality will be bad!")
        Settings.preferred_drawing_method = "circle_shapes"

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


def set_appearance_mode(mode_string):
    AppearanceModeTracker.set_appearance_mode(mode_string)


def get_appearance_mode():
    if AppearanceModeTracker.appearance_mode == 0:
        return "Light"
    elif AppearanceModeTracker.appearance_mode == 1:
        return "Dark"


def set_default_color_theme(color_string):
    ThemeManager.load_theme(color_string)


def deactivate_dpi_awareness(deactivate_awareness: bool):
    Settings.deactivate_automatic_dpi_awareness = deactivate_awareness


def set_user_scaling(scaling_value: float):
    ScalingTracker.set_spacing_scaling(scaling_value)
    ScalingTracker.set_widget_scaling(scaling_value)
