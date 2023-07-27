import tkinter
import copy
from typing import Union, Tuple, List, Dict, Callable, Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from .theme import ThemeManager
from .font import CTkFont
from .ctk_button import CTkButton
from .ctk_frame import CTkFrame
from .utility import check_kwargs_empty


class CTkSegmentedButton(CTkFrame):
    """
    Segmented button with corner radius, border width, variable support.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 master: any,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: Optional[int] = None,
                 border_width: int = 3,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 selected_color: Optional[Union[str, Tuple[str, str]]] = None,
                 selected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 unselected_color: Optional[Union[str, Tuple[str, str]]] = None,
                 unselected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,
                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,

                 font: Optional[Union[tuple, CTkFont]] = None,
                 values: Optional[list] = None,
                 variable: Union[tkinter.Variable, None] = None,
                 dynamic_resizing: bool = True,
                 command: Union[Callable[[str], None], None] = None,
                 state: str = "normal"):

        super().__init__(master=master, bg_color=bg_color, width=width, height=height)

        self._sb_fg_color = ThemeManager.theme["CTkSegmentedButton"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)

        self._sb_selected_color = ThemeManager.theme["CTkSegmentedButton"]["selected_color"] if selected_color is None else self._check_color_type(selected_color)
        self._sb_selected_hover_color = ThemeManager.theme["CTkSegmentedButton"]["selected_hover_color"] if selected_hover_color is None else self._check_color_type(selected_hover_color)

        self._sb_unselected_color = ThemeManager.theme["CTkSegmentedButton"]["unselected_color"] if unselected_color is None else self._check_color_type(unselected_color)
        self._sb_unselected_hover_color = ThemeManager.theme["CTkSegmentedButton"]["unselected_hover_color"] if unselected_hover_color is None else self._check_color_type(unselected_hover_color)

        self._sb_text_color = ThemeManager.theme["CTkSegmentedButton"]["text_color"] if text_color is None else self._check_color_type(text_color)
        self._sb_text_color_disabled = ThemeManager.theme["CTkSegmentedButton"]["text_color_disabled"] if text_color_disabled is None else self._check_color_type(text_color_disabled)

        self._sb_corner_radius = ThemeManager.theme["CTkSegmentedButton"]["corner_radius"] if corner_radius is None else corner_radius
        self._sb_border_width = ThemeManager.theme["CTkSegmentedButton"]["border_width"] if border_width is None else border_width

        self._background_corner_colors = background_corner_colors  # rendering options for DrawEngine

        self._command: Callable[[str], None] = command
        self._font = CTkFont() if font is None else font
        self._state = state

        self._buttons_dict: Dict[str, CTkButton] = {}  # mapped from value to button object
        if values is None:
            self._value_list: List[str] = ["CTkSegmentedButton"]
        else:
            self._value_list: List[str] = values  # Values ordered like buttons rendered on widget

        self._dynamic_resizing = dynamic_resizing
        if not self._dynamic_resizing:
            self.grid_propagate(False)

        self._check_unique_values(self._value_list)
        self._current_value: str = ""
        if len(self._value_list) > 0:
            self._create_buttons_from_values()
            self._create_button_grid()

        self._variable = variable
        self._variable_callback_blocked: bool = False
        self._variable_callback_name: Union[str, None] = None

        if self._variable is not None:
            self._variable_callback_name = self._variable.trace_add("write", self._variable_callback)
            self.set(self._variable.get(), from_variable_callback=True)

        super().configure(corner_radius=self._sb_corner_radius, fg_color="transparent")

    def destroy(self):
        if self._variable is not None:  # remove old callback
            self._variable.trace_remove("write", self._variable_callback_name)

        super().destroy()

    def _set_dimensions(self, width: int = None, height: int = None):
        super()._set_dimensions(width, height)

        for button in self._buttons_dict.values():
            button.configure(height=height)

    def _variable_callback(self, var_name, index, mode):
        if not self._variable_callback_blocked:
            self.set(self._variable.get(), from_variable_callback=True)

    def _get_index_by_value(self, value: str):
        for index, value_from_list in enumerate(self._value_list):
            if value_from_list == value:
                return index

        raise ValueError(f"CTkSegmentedButton does not contain value '{value}'")

    def _configure_button_corners_for_index(self, index: int):
        if index == 0 and len(self._value_list) == 1:
            if self._background_corner_colors is None:
                self._buttons_dict[self._value_list[index]].configure(background_corner_colors=(self._bg_color, self._bg_color, self._bg_color, self._bg_color))
            else:
                self._buttons_dict[self._value_list[index]].configure(background_corner_colors=self._background_corner_colors)

        elif index == 0:
            if self._background_corner_colors is None:
                self._buttons_dict[self._value_list[index]].configure(background_corner_colors=(self._bg_color, self._sb_fg_color, self._sb_fg_color, self._bg_color))
            else:
                self._buttons_dict[self._value_list[index]].configure(background_corner_colors=(self._background_corner_colors[0], self._sb_fg_color, self._sb_fg_color, self._background_corner_colors[3]))

        elif index == len(self._value_list) - 1:
            if self._background_corner_colors is None:
                self._buttons_dict[self._value_list[index]].configure(background_corner_colors=(self._sb_fg_color, self._bg_color, self._bg_color, self._sb_fg_color))
            else:
                self._buttons_dict[self._value_list[index]].configure(background_corner_colors=(self._sb_fg_color, self._background_corner_colors[1], self._background_corner_colors[2], self._sb_fg_color))

        else:
            self._buttons_dict[self._value_list[index]].configure(background_corner_colors=(self._sb_fg_color, self._sb_fg_color, self._sb_fg_color, self._sb_fg_color))

    def _unselect_button_by_value(self, value: str):
        if value in self._buttons_dict:
            self._buttons_dict[value].configure(fg_color=self._sb_unselected_color,
                                                hover_color=self._sb_unselected_hover_color)

    def _select_button_by_value(self, value: str):
        if self._current_value is not None and self._current_value != "":
            self._unselect_button_by_value(self._current_value)

        self._current_value = value

        self._buttons_dict[value].configure(fg_color=self._sb_selected_color,
                                            hover_color=self._sb_selected_hover_color)

    def _create_button(self, index: int, value: str) -> CTkButton:
        new_button = CTkButton(self,
                               width=0,
                               height=self._current_height,
                               corner_radius=self._sb_corner_radius,
                               border_width=self._sb_border_width,
                               fg_color=self._sb_unselected_color,
                               border_color=self._sb_fg_color,
                               hover_color=self._sb_unselected_hover_color,
                               text_color=self._sb_text_color,
                               text_color_disabled=self._sb_text_color_disabled,
                               text=value,
                               font=self._font,
                               state=self._state,
                               command=lambda v=value: self.set(v, from_button_callback=True),
                               background_corner_colors=None,
                               round_width_to_even_numbers=False,
                               round_height_to_even_numbers=False)  # DrawEngine rendering option (so that theres no gap between buttons)

        return new_button

    @staticmethod
    def _check_unique_values(values: List[str]):
        """ raises exception if values are not unique """
        if len(values) != len(set(values)):
            raise ValueError("CTkSegmentedButton values are not unique")

    def _create_button_grid(self):
        # remove minsize from every grid cell in the first row
        number_of_columns, _ = self.grid_size()
        for n in range(number_of_columns):
            self.grid_columnconfigure(n, weight=1, minsize=0)
        self.grid_rowconfigure(0, weight=1)

        for index, value in enumerate(self._value_list):
            self.grid_columnconfigure(index, weight=1, minsize=self._current_height)
            self._buttons_dict[value].grid(row=0, column=index, sticky="nsew")

    def _create_buttons_from_values(self):
        assert len(self._buttons_dict) == 0
        assert len(self._value_list) > 0

        for index, value in enumerate(self._value_list):
            self._buttons_dict[value] = self._create_button(index, value)
            self._configure_button_corners_for_index(index)

    def configure(self, **kwargs):
        if "width" in kwargs:
            super().configure(width=kwargs.pop("width"))

        if "height" in kwargs:
            super().configure(height=kwargs.pop("height"))

        if "corner_radius" in kwargs:
            self._sb_corner_radius = kwargs.pop("corner_radius")
            super().configure(corner_radius=self._sb_corner_radius)
            for button in self._buttons_dict.values():
                button.configure(corner_radius=self._sb_corner_radius)

        if "border_width" in kwargs:
            self._sb_border_width = kwargs.pop("border_width")
            for button in self._buttons_dict.values():
                button.configure(border_width=self._sb_border_width)

        if "bg_color" in kwargs:
            super().configure(bg_color=kwargs.pop("bg_color"))

            if len(self._buttons_dict) > 0:
                self._configure_button_corners_for_index(0)
            if len(self._buttons_dict) > 1:
                max_index = len(self._buttons_dict) - 1
                self._configure_button_corners_for_index(max_index)

        if "fg_color" in kwargs:
            self._sb_fg_color = self._check_color_type(kwargs.pop("fg_color"))
            for index, button in enumerate(self._buttons_dict.values()):
                button.configure(border_color=self._sb_fg_color)
                self._configure_button_corners_for_index(index)

        if "selected_color" in kwargs:
            self._sb_selected_color = self._check_color_type(kwargs.pop("selected_color"))
            if self._current_value in self._buttons_dict:
                self._buttons_dict[self._current_value].configure(fg_color=self._sb_selected_color)

        if "selected_hover_color" in kwargs:
            self._sb_selected_hover_color = self._check_color_type(kwargs.pop("selected_hover_color"))
            if self._current_value in self._buttons_dict:
                self._buttons_dict[self._current_value].configure(hover_color=self._sb_selected_hover_color)

        if "unselected_color" in kwargs:
            self._sb_unselected_color = self._check_color_type(kwargs.pop("unselected_color"))
            for value, button in self._buttons_dict.items():
                if value != self._current_value:
                    button.configure(fg_color=self._sb_unselected_color)

        if "unselected_hover_color" in kwargs:
            self._sb_unselected_hover_color = self._check_color_type(kwargs.pop("unselected_hover_color"))
            for value, button in self._buttons_dict.items():
                if value != self._current_value:
                    button.configure(hover_color=self._sb_unselected_hover_color)

        if "text_color" in kwargs:
            self._sb_text_color = self._check_color_type(kwargs.pop("text_color"))
            for button in self._buttons_dict.values():
                button.configure(text_color=self._sb_text_color)

        if "text_color_disabled" in kwargs:
            self._sb_text_color_disabled = self._check_color_type(kwargs.pop("text_color_disabled"))
            for button in self._buttons_dict.values():
                button.configure(text_color_disabled=self._sb_text_color_disabled)

        if "background_corner_colors" in kwargs:
            self._background_corner_colors = kwargs.pop("background_corner_colors")
            for i in range(len(self._buttons_dict)):
                self._configure_button_corners_for_index(i)

        if "font" in kwargs:
            self._font = kwargs.pop("font")
            for button in self._buttons_dict.values():
                button.configure(font=self._font)

        if "values" in kwargs:
            for button in self._buttons_dict.values():
                button.destroy()
            self._buttons_dict.clear()
            self._value_list = kwargs.pop("values")

            self._check_unique_values(self._value_list)

            if len(self._value_list) > 0:
                self._create_buttons_from_values()
                self._create_button_grid()

            if self._current_value in self._value_list:
                self._select_button_by_value(self._current_value)

        if "variable" in kwargs:
            if self._variable is not None:  # remove old callback
                self._variable.trace_remove("write", self._variable_callback_name)

            self._variable = kwargs.pop("variable")

            if self._variable is not None and self._variable != "":
                self._variable_callback_name = self._variable.trace_add("write", self._variable_callback)
                self.set(self._variable.get(), from_variable_callback=True)
            else:
                self._variable = None

        if "dynamic_resizing" in kwargs:
            self._dynamic_resizing = kwargs.pop("dynamic_resizing")
            if not self._dynamic_resizing:
                self.grid_propagate(False)
            else:
                self.grid_propagate(True)

        if "command" in kwargs:
            self._command = kwargs.pop("command")

        if "state" in kwargs:
            self._state = kwargs.pop("state")
            for button in self._buttons_dict.values():
                button.configure(state=self._state)

        check_kwargs_empty(kwargs, raise_error=True)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "width":
            return super().cget(attribute_name)
        elif attribute_name == "height":
            return super().cget(attribute_name)
        elif attribute_name == "corner_radius":
            return self._sb_corner_radius
        elif attribute_name == "border_width":
            return self._sb_border_width

        elif attribute_name == "bg_color":
            return super().cget(attribute_name)
        elif attribute_name == "fg_color":
            return self._sb_fg_color
        elif attribute_name == "selected_color":
            return self._sb_selected_color
        elif attribute_name == "selected_hover_color":
            return self._sb_selected_hover_color
        elif attribute_name == "unselected_color":
            return self._sb_unselected_color
        elif attribute_name == "unselected_hover_color":
            return self._sb_unselected_hover_color
        elif attribute_name == "text_color":
            return self._sb_text_color
        elif attribute_name == "text_color_disabled":
            return self._sb_text_color_disabled

        elif attribute_name == "font":
            return self._font
        elif attribute_name == "values":
            return copy.copy(self._value_list)
        elif attribute_name == "variable":
            return self._variable
        elif attribute_name == "dynamic_resizing":
            return self._dynamic_resizing
        elif attribute_name == "command":
            return self._command

        else:
            raise ValueError(f"'{attribute_name}' is not a supported argument. Look at the documentation for supported arguments.")

    def set(self, value: str, from_variable_callback: bool = False, from_button_callback: bool = False):
        if value == self._current_value:
            return
        elif value in self._buttons_dict:
            self._select_button_by_value(value)

            if self._variable is not None and not from_variable_callback:
                self._variable_callback_blocked = True
                self._variable.set(value)
                self._variable_callback_blocked = False
        else:
            if self._current_value in self._buttons_dict:
                self._unselect_button_by_value(self._current_value)
            self._current_value = value

            if self._variable is not None and not from_variable_callback:
                self._variable_callback_blocked = True
                self._variable.set(value)
                self._variable_callback_blocked = False

        if from_button_callback:
            if self._command is not None:
                self._command(self._current_value)

    def get(self) -> str:
        return self._current_value

    def index(self, value: str) -> int:
        return self._value_list.index(value)

    def insert(self, index: int, value: str):
        if value not in self._buttons_dict:
            if value != "":
                self._value_list.insert(index, value)
                self._buttons_dict[value] = self._create_button(index, value)

                self._configure_button_corners_for_index(index)
                if index > 0:
                    self._configure_button_corners_for_index(index - 1)
                if index < len(self._buttons_dict) - 1:
                    self._configure_button_corners_for_index(index + 1)

                self._create_button_grid()

                if value == self._current_value:
                    self._select_button_by_value(self._current_value)
            else:
                raise ValueError(f"CTkSegmentedButton can not insert value ''")
        else:
            raise ValueError(f"CTkSegmentedButton can not insert value '{value}', already part of the values")

    def move(self, new_index: int, value: str):
        if 0 <= new_index < len(self._value_list):
            if value in self._buttons_dict:
                self.delete(value)
                self.insert(new_index, value)
            else:
                raise ValueError(f"CTkSegmentedButton has no value named '{value}'")
        else:
            raise ValueError(f"CTkSegmentedButton new_index {new_index} not in range of value list with len {len(self._value_list)}")

    def delete(self, value: str):
        if value in self._buttons_dict:
            self._buttons_dict[value].destroy()
            self._buttons_dict.pop(value)
            index_to_remove = self._get_index_by_value(value)
            self._value_list.pop(index_to_remove)

            # removed index was outer right element
            if index_to_remove == len(self._buttons_dict) and len(self._buttons_dict) > 0:
                self._configure_button_corners_for_index(index_to_remove - 1)

            # removed index was outer left element
            if index_to_remove == 0 and len(self._buttons_dict) > 0:
                self._configure_button_corners_for_index(0)

            #if index_to_remove <= len(self._buttons_dict) - 1:
            #    self._configure_button_corners_for_index(index_to_remove)

            self._create_button_grid()
        else:
            raise ValueError(f"CTkSegmentedButton does not contain value '{value}'")

    def bind(self, sequence=None, command=None, add=None):
        raise NotImplementedError

    def unbind(self, sequence=None, funcid=None):
        raise NotImplementedError

