__version__ = "4.1.0"

import os
import sys
from tkinter.constants import *

# import manager classes
from .settings import Settings
from .appearance_mode_tracker import AppearanceModeTracker
from .theme_manager import ThemeManager
from .scaling_tracker import ScalingTracker
from .font_manager import FontManager
from .draw_engine import DrawEngine

AppearanceModeTracker.init_appearance_mode()
ThemeManager.load_theme("blue")  # load default theme
FontManager.init_font_manager()

# determine draw method based on current platform
if sys.platform == "darwin":
    DrawEngine.preferred_drawing_method = "polygon_shapes"
else:
    DrawEngine.preferred_drawing_method = "font_shapes"

# load Roboto fonts (used on Windows/Linux)
script_directory = os.path.dirname(os.path.abspath(__file__))
FontManager.load_font(os.path.join(script_directory, "assets", "fonts", "Roboto", "Roboto-Regular.ttf"))
FontManager.load_font(os.path.join(script_directory, "assets", "fonts", "Roboto", "Roboto-Medium.ttf"))

# load font necessary for rendering the widgets (used on Windows/Linux)
if FontManager.load_font(os.path.join(script_directory, "assets", "fonts", "CustomTkinter_shapes_font-fine.otf")) is False:
    # change draw method if font loading failed
    if DrawEngine.preferred_drawing_method == "font_shapes":
        sys.stderr.write("customtkinter.__init__ warning: " +
                         "Preferred drawing method 'font_shapes' can not be used because the font file could not be loaded.\n" +
                         "Using 'circle_shapes' instead. The rendering quality will be bad!")
        DrawEngine.preferred_drawing_method = "circle_shapes"

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


def set_appearance_mode(mode_string: str):
    """ possible values: light, dark, system """
    AppearanceModeTracker.set_appearance_mode(mode_string)


def get_appearance_mode() -> str:
    """ get current state of the appearance mode (light or dark) """
    if AppearanceModeTracker.appearance_mode == 0:
        return "Light"
    elif AppearanceModeTracker.appearance_mode == 1:
        return "Dark"


def set_default_color_theme(color_string: str):
    """ set color theme or load custom theme file by passing the path """
    ThemeManager.load_theme(color_string)


def set_widget_scaling(scaling_value: float):
    """ set scaling for the widget dimensions """
    ScalingTracker.set_widget_scaling(scaling_value)


def set_spacing_scaling(scaling_value: float):
    """ set scaling for geometry manager calls (place, pack, grid)"""
    ScalingTracker.set_spacing_scaling(scaling_value)


def set_window_scaling(scaling_value: float):
    """ set scaling for window dimensions """
    ScalingTracker.set_window_scaling(scaling_value)


def deactivate_automatic_dpi_awareness():
    """ deactivate DPI awareness of current process (windll.shcore.SetProcessDpiAwareness(0)) """
    ScalingTracker.deactivate_automatic_dpi_awareness = False
