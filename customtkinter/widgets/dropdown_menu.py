import tkinter
import sys
import copy
import re
from typing import Union, Tuple, Callable, List

from ..theme_manager import ThemeManager
from ..appearance_mode_tracker import AppearanceModeTracker
from ..scaling_tracker import ScalingTracker
from ..utility.ctk_font import CTkFont


class DropdownMenu(tkinter.Menu):
    def __init__(self, *args,
                 min_character_width: int = 18,

                 fg_color: Union[str, Tuple[str, str]] = "default_theme",
                 hover_color: Union[str, Tuple[str, str]] = "default_theme",
                 text_color: Union[str, Tuple[str, str]] = "default_theme",

                 font: Union[tuple, CTkFont] = "default_theme",
                 command: Callable = None,
                 values: List[str] = None,
                 **kwargs):

        super().__init__(*args, **kwargs)

        ScalingTracker.add_widget(self._set_scaling, self)
        self._widget_scaling = ScalingTracker.get_widget_scaling(self)
        self._spacing_scaling = ScalingTracker.get_spacing_scaling(self)

        AppearanceModeTracker.add(self._set_appearance_mode, self)
        self._appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self._min_character_width = min_character_width
        self._fg_color = ThemeManager.theme["color"]["dropdown_color"] if fg_color == "default_theme" else fg_color
        self._hover_color = ThemeManager.theme["color"]["dropdown_hover"] if hover_color == "default_theme" else hover_color
        self._text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color

        # font
        self._font = CTkFont() if font == "default_theme" else self._check_font_type(font)
        if isinstance(self._font, CTkFont):
            self._font.add_size_configure_callback(self._update_font)

        self._configure_menu_for_platforms()

        self._values = values
        self._command = command

        self._add_menu_commands()

    def _update_font(self):
        """ pass font to tkinter widgets with applied font scaling """
        super().configure(font=self._apply_font_scaling(self._font))

    def destroy(self):
        if isinstance(self._font, CTkFont):
            self._font.remove_size_configure_callback(self._update_font)
        super().destroy()

    def _configure_menu_for_platforms(self):
        """ apply platform specific appearance attributes, configure all colors """

        if sys.platform == "darwin":
            super().configure(tearoff=False,
                              font=self._apply_font_scaling(self._font))

        elif sys.platform.startswith("win"):
            super().configure(tearoff=False,
                              relief="flat",
                              activebackground=ThemeManager.single_color(self._hover_color, self._appearance_mode),
                              borderwidth=self._apply_widget_scaling(4),
                              activeborderwidth=self._apply_widget_scaling(4),
                              bg=ThemeManager.single_color(self._fg_color, self._appearance_mode),
                              fg=ThemeManager.single_color(self._text_color, self._appearance_mode),
                              activeforeground=ThemeManager.single_color(self._text_color, self._appearance_mode),
                              font=self._apply_font_scaling(self._font),
                              cursor="hand2")

        else:
            super().configure(tearoff=False,
                              relief="flat",
                              activebackground=ThemeManager.single_color(self._hover_color, self._appearance_mode),
                              borderwidth=0,
                              activeborderwidth=0,
                              bg=ThemeManager.single_color(self._fg_color, self._appearance_mode),
                              fg=ThemeManager.single_color(self._text_color, self._appearance_mode),
                              activeforeground=ThemeManager.single_color(self._text_color, self._appearance_mode),
                              font=self._apply_font_scaling(self._font))

    def _add_menu_commands(self):
        """ delete existing menu labels and createe new labels with command according to values list """

        self.delete(0, "end")  # delete all old commands

        if sys.platform.startswith("linux"):
            for value in self._values:
                self.add_command(label="  " + value.ljust(self._min_character_width) + "  ",
                                 command=lambda v=value: self._button_callback(v),
                                 compound="left")
        else:
            for value in self._values:
                self.add_command(label=value.ljust(self._min_character_width),
                                 command=lambda v=value: self._button_callback(v),
                                 compound="left")

    def _button_callback(self, value):
        if self._command is not None:
            self._command(value)

    def open(self, x: Union[int, float], y: Union[int, float]):

        if sys.platform == "darwin":
            y += self._apply_widget_scaling(8)
        else:
            y += self._apply_widget_scaling(3)

        if sys.platform == "darwin" or sys.platform.startswith("win"):
            self.post(int(x), int(y))
        else:  # Linux
            self.tk_popup(int(x), int(y))

    def configure(self, **kwargs):
        if "fg_color" in kwargs:
            self._fg_color = kwargs.pop("fg_color")
            super().configure(bg=ThemeManager.single_color(self._fg_color, self._appearance_mode))

        if "hover_color" in kwargs:
            self._hover_color = kwargs.pop("hover_color")
            super().configure(activebackground=ThemeManager.single_color(self._hover_color, self._appearance_mode))

        if "text_color" in kwargs:
            self._text_color = kwargs.pop("text_color")
            super().configure(fg=ThemeManager.single_color(self._text_color, self._appearance_mode))

        if "font" in kwargs:
            if isinstance(self._font, CTkFont):
                self._font.remove_size_configure_callback(self._update_font)
            self._font = self._check_font_type(kwargs.pop("font"))
            if isinstance(self._font, CTkFont):
                self._font.add_size_configure_callback(self._update_font)

            self._update_font()

        if "command" in kwargs:
            self._command = kwargs.pop("command")

        if "values" in kwargs:
            self._values = kwargs.pop("values")
            self._add_menu_commands()

        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "min_character_width":
            return self._min_character_width

        elif attribute_name == "fg_color":
            return self._fg_color
        elif attribute_name == "hover_color":
            return self._hover_color
        elif attribute_name == "text_color":
            return self._text_color

        elif attribute_name == "font":
            return self._font
        elif attribute_name == "command":
            return self._command
        elif attribute_name == "values":
            return self._values

        else:
            return super().cget(attribute_name)

    def _apply_widget_scaling(self, value: Union[int, float, str]) -> Union[float, str]:
        if isinstance(value, (int, float)):
            return value * self._widget_scaling
        else:
            return value

    def _apply_font_scaling(self, font: Union[Tuple, CTkFont]) -> tuple:
        """ Takes CTkFont object and returns tuple font with scaled size, has to be called again for every change of font object """
        if type(font) == tuple:
            if len(font) == 1:
                return font
            elif len(font) == 2:
                return font[0], -abs(round(font[1] * self._widget_scaling))
            elif len(font) == 3:
                return font[0], -abs(round(font[1] * self._widget_scaling)), font[2]
            else:
                raise ValueError(f"Can not scale font {font}. font needs to be tuple of len 1, 2 or 3")

        elif isinstance(font, CTkFont):
            return font.create_scaled_tuple(self._widget_scaling)
        else:
            raise ValueError(f"Can not scale font '{font}' of type {type(font)}. font needs to be tuple or instance of CTkFont")

    @staticmethod
    def _check_font_type(font: any):
        if isinstance(font, CTkFont):
            return font

        elif type(font) == tuple and len(font) == 1:
            sys.stderr.write(f"Warning: font {font} given without size, will be extended with default text size of current theme\n")
            return font[0], ThemeManager.theme["text"]["size"]

        elif type(font) == tuple and 2 <= len(font) <= 3:
            return font

        else:
            raise ValueError(f"Wrong font type {type(font)}\n" +
                             f"For consistency, Customtkinter requires the font argument to be a tuple of len 2 or 3 or an instance of CTkFont.\n" +
                             f"\nUsage example:\n" +
                             f"font=customtkinter.CTkFont(family='<name>', size=<size in px>)\n" +
                             f"font=('<name>', <size in px>)\n")

    def _set_scaling(self, new_widget_scaling, new_spacing_scaling, new_window_scaling):
        self._widget_scaling = new_widget_scaling
        self._spacing_scaling = new_spacing_scaling

        self._configure_menu_for_platforms()

    def _set_appearance_mode(self, mode_string):
        """ colors won't update on appearance mode change when dropdown is open, because it's not necessary """

        if mode_string.lower() == "dark":
            self._appearance_mode = 1
        elif mode_string.lower() == "light":
            self._appearance_mode = 0

        self._configure_menu_for_platforms()
