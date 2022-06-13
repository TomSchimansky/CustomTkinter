import tkinter
import sys
from distutils.version import StrictVersion as Version
import platform
from typing import Union

from ..theme_manager import ThemeManager
from ..appearance_mode_tracker import AppearanceModeTracker
from ..scaling_tracker import ScalingTracker


class DropdownMenuFallback(tkinter.Menu):
    def __init__(self, *args,
                 fg_color="#555555",
                 button_hover_color="gray35",
                 text_color="default_theme",
                 text_font="default_theme",
                 command=None,
                 values=None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        ScalingTracker.add_widget(self.set_scaling, self)
        self._widget_scaling = ScalingTracker.get_widget_scaling(self)
        self._spacing_scaling = ScalingTracker.get_spacing_scaling(self)

        self.fg_color = fg_color
        self.button_hover_color = button_hover_color
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font

        self.menu = tkinter.Menu(master=self)

        if sys.platform.startswith("win"):
            self.menu.configure()

        self.values = values
        self.command = command

        for value in self.values:
            self.menu.add_command(label=value.ljust(16), command=lambda v=value: self.button_callback(v))

    def open(self, x, y):
        if sys.platform == "darwin":
            y = y + 8

        self.menu.post(x, y)

    def button_callback(self, value):
        if self.command is not None:
            self.command(value)

    def set_scaling(self, new_widget_scaling, new_spacing_scaling, new_window_scaling):
        self._widget_scaling = new_widget_scaling
        self._spacing_scaling = new_spacing_scaling
