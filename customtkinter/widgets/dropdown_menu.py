import tkinter
import sys
import copy
import re
from typing import Union

from ..theme_manager import ThemeManager
from ..appearance_mode_tracker import AppearanceModeTracker
from ..scaling_tracker import ScalingTracker


class DropdownMenu(tkinter.Menu):
    def __init__(self, *args,
                 min_character_width=18,
                 fg_color="default_theme",
                 hover_color="default_theme",
                 text_color="default_theme",
                 text_font="default_theme",
                 command=None,
                 values=None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        ScalingTracker.add_widget(self.set_scaling, self)
        self._widget_scaling = ScalingTracker.get_widget_scaling(self)
        self._spacing_scaling = ScalingTracker.get_spacing_scaling(self)

        AppearanceModeTracker.add(self.set_appearance_mode, self)
        self._appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.min_character_width = min_character_width
        self.fg_color = ThemeManager.theme["color"]["dropdown_color"] if fg_color == "default_theme" else fg_color
        self.hover_color = ThemeManager.theme["color"]["dropdown_hover"] if hover_color == "default_theme" else hover_color
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font

        self.configure_menu_for_platforms()

        self.values = values
        self.command = command

        self.add_menu_commands()

    def configure_menu_for_platforms(self):
        """ apply platform specific appearance attributes """

        if sys.platform == "darwin":
            self.configure(tearoff=False,
                           font=self.apply_font_scaling(self.text_font))

        elif sys.platform.startswith("win"):
            self.configure(tearoff=False,
                           relief="flat",
                           activebackground=ThemeManager.single_color(self.hover_color, self._appearance_mode),
                           borderwidth=0,
                           activeborderwidth=self.apply_widget_scaling(4),
                           bg=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                           fg=ThemeManager.single_color(self.text_color, self._appearance_mode),
                           activeforeground=ThemeManager.single_color(self.text_color, self._appearance_mode),
                           font=self.apply_font_scaling(self.text_font),
                           cursor="hand2")

        else:
            self.configure(tearoff=False,
                           relief="flat",
                           activebackground=ThemeManager.single_color(self.hover_color, self._appearance_mode),
                           borderwidth=0,
                           activeborderwidth=0,
                           bg=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                           fg=ThemeManager.single_color(self.text_color, self._appearance_mode),
                           activeforeground=ThemeManager.single_color(self.text_color, self._appearance_mode),
                           font=self.apply_font_scaling(self.text_font))

    def add_menu_commands(self):
        if sys.platform.startswith("linux"):
            for value in self.values:
                self.add_command(label="  " + value.ljust(self.min_character_width) + "  ",
                                 command=lambda v=value: self.button_callback(v),
                                 compound="left")
        else:
            for value in self.values:
                self.add_command(label=value.ljust(self.min_character_width),
                                 command=lambda v=value: self.button_callback(v),
                                 compound="left")

    def open(self, x: Union[int, float], y: Union[int, float]):
        if sys.platform == "darwin":
            y += self.apply_widget_scaling(8)
        else:
            y += self.apply_widget_scaling(3)

        if sys.platform == "darwin" or sys.platform.startswith("win"):
            self.post(int(x), int(y))
        else:  # Linux
            self.tk_popup(int(x), int(y))

    def button_callback(self, value):
        if self.command is not None:
            self.command(value)

    def configure(self, **kwargs):
        if "values" in kwargs:
            self.values = kwargs.pop("values")
            self.delete(0, "end")  # delete all old commands
            self.add_menu_commands()

        if "fg_color" in kwargs:
            self.fg_color = kwargs.pop("fg_color")
            self.configure(bg=ThemeManager.single_color(self.fg_color, self._appearance_mode))

        if "hover_color" in kwargs:
            self.hover_color = kwargs.pop("hover_color")
            self.configure(activebackground=ThemeManager.single_color(self.hover_color, self._appearance_mode))

        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")
            self.configure(fg=ThemeManager.single_color(self.text_color, self._appearance_mode))

        if "text_font" in kwargs:
            self.text_font = kwargs.pop("text_font")
            self.configure(font=self.apply_font_scaling(self.text_font))

        super().configure(**kwargs)

    def apply_widget_scaling(self, value: Union[int, float, str]) -> Union[float, str]:
        if isinstance(value, (int, float)):
            return value * self._widget_scaling
        else:
            return value

    def apply_font_scaling(self, font):
        if type(font) == tuple or type(font) == list:
            font_list = list(font)
            for i in range(len(font_list)):
                if (type(font_list[i]) == int or type(font_list[i]) == float) and font_list[i] < 0:
                    font_list[i] = int(font_list[i] * self._widget_scaling)
            return tuple(font_list)

        elif type(font) == str:
            for negative_number in re.findall(r" -\d* ", font):
                font = font.replace(negative_number, f" {int(int(negative_number) * self._widget_scaling)} ")
            return font

        elif isinstance(font, tkinter.font.Font):
            new_font_object = copy.copy(font)
            if font.cget("size") < 0:
                new_font_object.config(size=int(font.cget("size") * self._widget_scaling))
            return new_font_object

        else:
            return font

    def set_scaling(self, new_widget_scaling, new_spacing_scaling, new_window_scaling):
        self._widget_scaling = new_widget_scaling
        self._spacing_scaling = new_spacing_scaling

        self.configure(font=self.apply_font_scaling(self.text_font))

        if sys.platform.startswith("win"):
            self.configure(activeborderwidth=self.apply_widget_scaling(4))

    def set_appearance_mode(self, mode_string):
        """ colors won't update on appearance mode change when dropdown is open, because it's not necessary """

        if mode_string.lower() == "dark":
            self._appearance_mode = 1
        elif mode_string.lower() == "light":
            self._appearance_mode = 0

        self.configure_menu_for_platforms()
