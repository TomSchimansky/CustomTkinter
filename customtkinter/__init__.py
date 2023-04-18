__version__ = "5.1.2"

import os
import sys
import tkinter.filedialog as filedialog
from tkinter import BooleanVar, DoubleVar, IntVar, StringVar, Variable
from tkinter.constants import *

# import windows
from .windows import CTk, CTkInputDialog, CTkToplevel
# import widgets
from .windows.widgets import (CTkButton, CTkCheckBox, CTkComboBox, CTkEntry,
                              CTkFrame, CTkLabel, CTkOptionMenu,
                              CTkProgressBar, CTkRadioButton,
                              CTkScrollableFrame, CTkScrollbar,
                              CTkSegmentedButton, CTkSlider, CTkSwitch,
                              CTkTabview, CTkTextbox)
# import manager classes
from .windows.widgets.appearance_mode import AppearanceModeTracker
# import base widgets
from .windows.widgets.core_rendering import CTkCanvas, DrawEngine
from .windows.widgets.core_widget_classes import CTkBaseClass
# import font classes
from .windows.widgets.font import CTkFont, FontManager
# import image classes
from .windows.widgets.image import CTkImage
from .windows.widgets.scaling import ScalingTracker
from .windows.widgets.theme import ThemeManager

_ = Variable, StringVar, IntVar, DoubleVar, BooleanVar, CENTER, filedialog  # prevent IDE from removing unused imports


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
    ScalingTracker.deactivate_automatic_dpi_awareness = True
