import tkinter
import sys
from typing import Union, Tuple, Callable, List, Optional

from ..theme import ThemeManager
from ..font import CTkFont
from ..appearance_mode import CTkAppearanceModeBaseClass
from ..scaling import CTkScalingBaseClass


class DropdownMenu(tkinter.Menu, CTkAppearanceModeBaseClass, CTkScalingBaseClass):
    def __init__(self, *args,
                 min_character_width: int = 18,

                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,

                 font: Optional[Union[tuple, CTkFont]] = None,
                 command: Union[Callable, None] = None,
                 values: Optional[List[str]] = None,
                 **kwargs):

        # call init methods of super classes
        tkinter.Menu.__init__(self, *args, **kwargs)
        CTkAppearanceModeBaseClass.__init__(self)
        CTkScalingBaseClass.__init__(self, scaling_type="widget")

        self._min_character_width = min_character_width
        self._fg_color = ThemeManager.theme["DropdownMenu"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
        self._hover_color = ThemeManager.theme["DropdownMenu"]["hover_color"] if hover_color is None else self._check_color_type(hover_color)
        self._text_color = ThemeManager.theme["DropdownMenu"]["text_color"] if text_color is None else self._check_color_type(text_color)

        # font
        self._font = CTkFont() if font is None else self._check_font_type(font)
        if isinstance(self._font, CTkFont):
            self._font.add_size_configure_callback(self._update_font)

        self._configure_menu_for_platforms()

        self._values = values
        self._command = command

        self._add_menu_commands()

    def destroy(self):
        if isinstance(self._font, CTkFont):
            self._font.remove_size_configure_callback(self._update_font)

        # call destroy methods of super classes
        tkinter.Menu.destroy(self)
        CTkAppearanceModeBaseClass.destroy(self)

    def _update_font(self):
        """ pass font to tkinter widgets with applied font scaling """
        super().configure(font=self._apply_font_scaling(self._font))

    def _configure_menu_for_platforms(self):
        """ apply platform specific appearance attributes, configure all colors """

        if sys.platform == "darwin":
            super().configure(tearoff=False,
                              font=self._apply_font_scaling(self._font))

        elif sys.platform.startswith("win"):
            super().configure(tearoff=False,
                              relief="flat",
                              activebackground=self._apply_appearance_mode(self._hover_color),
                              borderwidth=self._apply_widget_scaling(4),
                              activeborderwidth=self._apply_widget_scaling(4),
                              bg=self._apply_appearance_mode(self._fg_color),
                              fg=self._apply_appearance_mode(self._text_color),
                              activeforeground=self._apply_appearance_mode(self._text_color),
                              font=self._apply_font_scaling(self._font),
                              cursor="hand2")

        else:
            super().configure(tearoff=False,
                              relief="flat",
                              activebackground=self._apply_appearance_mode(self._hover_color),
                              borderwidth=0,
                              activeborderwidth=0,
                              bg=self._apply_appearance_mode(self._fg_color),
                              fg=self._apply_appearance_mode(self._text_color),
                              activeforeground=self._apply_appearance_mode(self._text_color),
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
            self._fg_color = self._check_color_type(kwargs.pop("fg_color"))
            super().configure(bg=self._apply_appearance_mode(self._fg_color))

        if "hover_color" in kwargs:
            self._hover_color = self._check_color_type(kwargs.pop("hover_color"))
            super().configure(activebackground=self._apply_appearance_mode(self._hover_color))

        if "text_color" in kwargs:
            self._text_color = self._check_color_type(kwargs.pop("text_color"))
            super().configure(fg=self._apply_appearance_mode(self._text_color))

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
            raise ValueError(f"Wrong font type {type(font)} for font '{font}'\n" +
                             f"For consistency, Customtkinter requires the font argument to be a tuple of len 2 or 3 or an instance of CTkFont.\n" +
                             f"\nUsage example:\n" +
                             f"font=customtkinter.CTkFont(family='<name>', size=<size in px>)\n" +
                             f"font=('<name>', <size in px>)\n")

    def _set_scaling(self, new_widget_scaling, new_window_scaling):
        super()._set_scaling(new_widget_scaling, new_window_scaling)
        self._configure_menu_for_platforms()

    def _set_appearance_mode(self, mode_string):
        """ colors won't update on appearance mode change when dropdown is open, because it's not necessary """
        super()._set_appearance_mode(mode_string)
        self._configure_menu_for_platforms()
