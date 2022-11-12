__version__ = "4.6.3"

import os
import sys
from tkinter import Variable, StringVar, IntVar, DoubleVar, BooleanVar
from tkinter.constants import *
import tkinter.filedialog as filedialog

_ = Variable, StringVar, IntVar, DoubleVar, BooleanVar, CENTER, filedialog  # prevent IDE from removing unused imports

# import manager classes
from .windows.widgets.appearance_mode.appearance_mode_tracker import AppearanceModeTracker
from .windows.widgets.font.font_manager import FontManager
from .windows.widgets.scaling.scaling_tracker import ScalingTracker
from .windows.widgets.theme.theme_manager import ThemeManager
from .windows.widgets.core_rendering.draw_engine import DrawEngine

AppearanceModeTracker.init_appearance_mode()

# load default blue theme
try:
    ThemeManager.load_theme("blue")
except FileNotFoundError as err:
    raise FileNotFoundError(f"{err}\n\nThe .json theme file for CustomTkinter could not be found.\n" +
                            f"If packaging with pyinstaller was used, have a look at the wiki:\n" +
                            f"https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging#windows-pyinstaller-auto-py-to-exe")

FontManager.init_font_manager()

# determine draw method based on current platform
if sys.platform == "darwin":
    DrawEngine.preferred_drawing_method = "polygon_shapes"
else:
    DrawEngine.preferred_drawing_method = "font_shapes"

if sys.platform.startswith("win") and sys.getwindowsversion().build < 9000:  # No automatic scaling on Windows < 8.1
    ScalingTracker.deactivate_automatic_dpi_awareness = True

# load Roboto fonts (used on Windows/Linux)
script_directory = os.path.dirname(os.path.abspath(__file__))
FontManager.load_font(os.path.join(script_directory, "assets", "fonts", "Roboto", "Roboto-Regular.ttf"))
FontManager.load_font(os.path.join(script_directory, "assets", "fonts", "Roboto", "Roboto-Medium.ttf"))

# load font necessary for rendering the widgets (used on Windows/Linux)
if FontManager.load_font(os.path.join(script_directory, "assets", "fonts", "CustomTkinter_shapes_font.otf")) is False:
    # change draw method if font loading failed
    if DrawEngine.preferred_drawing_method == "font_shapes":
        sys.stderr.write("customtkinter.__init__ warning: " +
                         "Preferred drawing method 'font_shapes' can not be used because the font file could not be loaded.\n" +
                         "Using 'circle_shapes' instead. The rendering quality will be bad!\n")
        DrawEngine.preferred_drawing_method = "circle_shapes"

# import widgets
from .windows.widgets.ctk_button import CTkButton
from .windows.widgets.ctk_checkbox import CTkCheckBox
from .windows.widgets.ctk_combobox import CTkComboBox
from .windows.widgets.ctk_entry import CTkEntry
from .windows.widgets.ctk_frame import CTkFrame
from .windows.widgets.ctk_label import CTkLabel
from .windows.widgets.ctk_optionmenu import CTkOptionMenu
from .windows.widgets.ctk_progressbar import CTkProgressBar
from .windows.widgets.ctk_radiobutton import CTkRadioButton
from .windows.widgets.ctk_scrollbar import CTkScrollbar
from .windows.widgets.ctk_segmented_button import CTkSegmentedButton
from .windows.widgets.ctk_slider import CTkSlider
from .windows.widgets.ctk_switch import CTkSwitch
from .windows.widgets.ctk_tabview import CTkTabview
from .windows.widgets.ctk_textbox import CTkTextbox

# import windows
from .windows.ctk_tk import CTk
from .windows.ctk_toplevel import CTkToplevel
from .windows.ctk_input_dialog import CTkInputDialog

# font classes
from .windows.widgets.font.ctk_font import CTkFont

# image classes
from .windows.widgets.image.ctk_image import CTkImage


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


def set_window_scaling(scaling_value: float):
    """ set scaling for window dimensions """
    ScalingTracker.set_window_scaling(scaling_value)


def deactivate_automatic_dpi_awareness():
    """ deactivate DPI awareness of current process (windll.shcore.SetProcessDpiAwareness(0)) """
    ScalingTracker.deactivate_automatic_dpi_awareness = False
