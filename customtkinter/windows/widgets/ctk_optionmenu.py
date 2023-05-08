import tkinter
import copy
import sys
from typing import Union, Tuple, Callable, Optional

from .core_rendering import CTkCanvas
from .theme import ThemeManager
from .core_rendering import DrawEngine
from .core_widget_classes import CTkBaseClass
from .core_widget_classes import DropdownMenu
from .font import CTkFont


class CTkOptionMenu(CTkBaseClass):
    """
    Optionmenu with rounded corners, dropdown menu, variable support, command.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 master: any,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: Optional[Union[int]] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,
                 dropdown_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 dropdown_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 dropdown_text_color: Optional[Union[str, Tuple[str, str]]] = None,

                 font: Optional[Union[tuple, CTkFont]] = None,
                 dropdown_font: Optional[Union[tuple, CTkFont]] = None,
                 values: Optional[list] = None,
                 variable: Union[tkinter.Variable, None] = None,
                 state: str = tkinter.NORMAL,
                 hover: bool = True,
                 command: Union[Callable[[str], None], None] = None,
                 dynamic_resizing: bool = True,
                 anchor: str = "w",
                 **kwargs):

        # transfer basic functionality (_bg_color, size, __appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

        # color variables
        self._fg_color = ThemeManager.theme["CTkOptionMenu"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
        self._button_color = ThemeManager.theme["CTkOptionMenu"]["button_color"] if button_color is None else self._check_color_type(button_color)
        self._button_hover_color = ThemeManager.theme["CTkOptionMenu"]["button_hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)

        # shape
        self._corner_radius = ThemeManager.theme["CTkOptionMenu"]["corner_radius"] if corner_radius is None else corner_radius

        # text and font
        self._text_color = ThemeManager.theme["CTkOptionMenu"]["text_color"] if text_color is None else self._check_color_type(text_color)
        self._text_color_disabled = ThemeManager.theme["CTkOptionMenu"]["text_color_disabled"] if text_color_disabled is None else self._check_color_type(text_color_disabled)

        # font
        self._font = CTkFont() if font is None else self._check_font_type(font)
        if isinstance(self._font, CTkFont):
            self._font.add_size_configure_callback(self._update_font)

        # callback and hover functionality
        self._command = command
        self._variable = variable
        self._variable_callback_blocked: bool = False
        self._variable_callback_name: Union[str, None] = None
        self._state = state
        self._hover = hover
        self._dynamic_resizing = dynamic_resizing

        if values is None:
            self._values = ["CTkOptionMenu"]
        else:
            self._values = values

        if len(self._values) > 0:
            self._current_value = self._values[0]
        else:
            self._current_value = "CTkOptionMenu"

        self._dropdown_menu = DropdownMenu(master=self,
                                           values=self._values,
                                           command=self._dropdown_callback,
                                           fg_color=dropdown_fg_color,
                                           hover_color=dropdown_hover_color,
                                           text_color=dropdown_text_color,
                                           font=dropdown_font)

        # configure grid system (1x1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._canvas = CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._desired_width),
                                 height=self._apply_widget_scaling(self._desired_height))
        self._draw_engine = DrawEngine(self._canvas)

        self._text_label = tkinter.Label(master=self,
                                         font=self._apply_font_scaling(self._font),
                                         anchor=anchor,
                                         padx=0,
                                         pady=0,
                                         borderwidth=1,
                                         text=self._current_value)

        if self._cursor_manipulation_enabled:
            if sys.platform == "darwin":
                self.configure(cursor="pointinghand")
            elif sys.platform.startswith("win"):
                self.configure(cursor="hand2")

        self._create_grid()
        if not self._dynamic_resizing:
            self.grid_propagate(0)

        self._create_bindings()
        self._draw()  # initial draw

        if self._variable is not None:
            self._variable_callback_name = self._variable.trace_add("write", self._variable_callback)
            self._current_value = self._variable.get()
            self._text_label.configure(text=self._current_value)

    def _create_bindings(self, sequence: Optional[str] = None):
        """ set necessary bindings for functionality of widget, will overwrite other bindings """
        if sequence is None or sequence == "<Enter>":
            self._canvas.bind("<Enter>", self._on_enter)
            self._text_label.bind("<Enter>", self._on_enter)
        if sequence is None or sequence == "<Leave>":
            self._canvas.bind("<Leave>", self._on_leave)
            self._text_label.bind("<Leave>", self._on_leave)
        if sequence is None or sequence == "<Button-1>":
            self._canvas.bind("<Button-1>", self._clicked)
            self._text_label.bind("<Button-1>", self._clicked)

    def _create_grid(self):
        self._canvas.grid(row=0, column=0, sticky="nsew")

        left_section_width = self._current_width - self._current_height
        self._text_label.grid(row=0, column=0, sticky="ew",
                              padx=(max(self._apply_widget_scaling(self._corner_radius), self._apply_widget_scaling(3)),
                                    max(self._apply_widget_scaling(self._current_width - left_section_width + 3), self._apply_widget_scaling(3))))

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        # change label font size and grid padding
        self._text_label.configure(font=self._apply_font_scaling(self._font))
        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._create_grid()
        self._draw(no_color_updates=True)

    def _set_dimensions(self, width: int = None, height: int = None):
        super()._set_dimensions(width, height)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw()

    def _update_font(self):
        """ pass font to tkinter widgets with applied font scaling and update grid with workaround """
        self._text_label.configure(font=self._apply_font_scaling(self._font))

        # Workaround to force grid to be resized when text changes size.
        # Otherwise grid will lag and only resizes if other mouse action occurs.
        self._canvas.grid_forget()
        self._canvas.grid(row=0, column=0, sticky="nsew")

    def destroy(self):
        if self._variable is not None:  # remove old callback
            self._variable.trace_remove("write", self._variable_callback_name)

        if isinstance(self._font, CTkFont):
            self._font.remove_size_configure_callback(self._update_font)

        super().destroy()

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

        left_section_width = self._current_width - self._current_height
        requires_recoloring = self._draw_engine.draw_rounded_rect_with_border_vertical_split(self._apply_widget_scaling(self._current_width),
                                                                                             self._apply_widget_scaling(self._current_height),
                                                                                             self._apply_widget_scaling(self._corner_radius),
                                                                                             0,
                                                                                             self._apply_widget_scaling(left_section_width))

        requires_recoloring_2 = self._draw_engine.draw_dropdown_arrow(self._apply_widget_scaling(self._current_width - (self._current_height / 2)),
                                                                      self._apply_widget_scaling(self._current_height / 2),
                                                                      self._apply_widget_scaling(self._current_height / 3))

        if no_color_updates is False or requires_recoloring or requires_recoloring_2:
            self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))

            self._canvas.itemconfig("inner_parts_left",
                                    outline=self._apply_appearance_mode(self._fg_color),
                                    fill=self._apply_appearance_mode(self._fg_color))
            self._canvas.itemconfig("inner_parts_right",
                                    outline=self._apply_appearance_mode(self._button_color),
                                    fill=self._apply_appearance_mode(self._button_color))

            self._text_label.configure(fg=self._apply_appearance_mode(self._text_color))

            if self._state == tkinter.DISABLED:
                self._text_label.configure(fg=(self._apply_appearance_mode(self._text_color_disabled)))
                self._canvas.itemconfig("dropdown_arrow",
                                        fill=self._apply_appearance_mode(self._text_color_disabled))
            else:
                self._text_label.configure(fg=self._apply_appearance_mode(self._text_color))
                self._canvas.itemconfig("dropdown_arrow",
                                        fill=self._apply_appearance_mode(self._text_color))

            self._text_label.configure(bg=self._apply_appearance_mode(self._fg_color))

        self._canvas.update_idletasks()

    def configure(self, require_redraw=False, **kwargs):
        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")
            self._create_grid()
            require_redraw = True

        if "fg_color" in kwargs:
            self._fg_color = self._check_color_type(kwargs.pop("fg_color"))
            require_redraw = True

        if "button_color" in kwargs:
            self._button_color = self._check_color_type(kwargs.pop("button_color"))
            require_redraw = True

        if "button_hover_color" in kwargs:
            self._button_hover_color = self._check_color_type(kwargs.pop("button_hover_color"))
            require_redraw = True

        if "text_color" in kwargs:
            self._text_color = self._check_color_type(kwargs.pop("text_color"))
            require_redraw = True

        if "text_color_disabled" in kwargs:
            self._text_color_disabled = self._check_color_type(kwargs.pop("text_color_disabled"))
            require_redraw = True

        if "dropdown_fg_color" in kwargs:
            self._dropdown_menu.configure(fg_color=kwargs.pop("dropdown_fg_color"))

        if "dropdown_hover_color" in kwargs:
            self._dropdown_menu.configure(hover_color=kwargs.pop("dropdown_hover_color"))

        if "dropdown_text_color" in kwargs:
            self._dropdown_menu.configure(text_color=kwargs.pop("dropdown_text_color"))

        if "font" in kwargs:
            if isinstance(self._font, CTkFont):
                self._font.remove_size_configure_callback(self._update_font)
            self._font = self._check_font_type(kwargs.pop("font"))
            if isinstance(self._font, CTkFont):
                self._font.add_size_configure_callback(self._update_font)

            self._update_font()

        if "dropdown_font" in kwargs:
            self._dropdown_menu.configure(font=kwargs.pop("dropdown_font"))

        if "values" in kwargs:
            self._values = kwargs.pop("values")
            self._dropdown_menu.configure(values=self._values)

        if "variable" in kwargs:
            if self._variable is not None:  # remove old callback
                self._variable.trace_remove("write", self._variable_callback_name)

            self._variable = kwargs.pop("variable")

            if self._variable is not None and self._variable != "":
                self._variable_callback_name = self._variable.trace_add("write", self._variable_callback)
                self._current_value = self._variable.get()
                self._text_label.configure(text=self._current_value)
            else:
                self._variable = None

        if "state" in kwargs:
            self._state = kwargs.pop("state")
            require_redraw = True

        if "hover" in kwargs:
            self._hover = kwargs.pop("hover")

        if "command" in kwargs:
            self._command = kwargs.pop("command")

        if "dynamic_resizing" in kwargs:
            self._dynamic_resizing = kwargs.pop("dynamic_resizing")
            if not self._dynamic_resizing:
                self.grid_propagate(0)
            else:
                self.grid_propagate(1)

        if "anchor" in kwargs:
            self._text_label.configure(anchor=kwargs.pop("anchor"))

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "corner_radius":
            return self._corner_radius

        elif attribute_name == "fg_color":
            return self._fg_color
        elif attribute_name == "button_color":
            return self._button_color
        elif attribute_name == "button_hover_color":
            return self._button_hover_color
        elif attribute_name == "text_color":
            return self._text_color
        elif attribute_name == "text_color_disabled":
            return self._text_color_disabled
        elif attribute_name == "dropdown_fg_color":
            return self._dropdown_menu.cget("fg_color")
        elif attribute_name == "dropdown_hover_color":
            return self._dropdown_menu.cget("hover_color")
        elif attribute_name == "dropdown_text_color":
            return self._dropdown_menu.cget("text_color")

        elif attribute_name == "font":
            return self._font
        elif attribute_name == "dropdown_font":
            return self._dropdown_menu.cget("font")
        elif attribute_name == "values":
            return copy.copy(self._values)
        elif attribute_name == "variable":
            return self._variable
        elif attribute_name == "state":
            return self._state
        elif attribute_name == "hover":
            return self._hover
        elif attribute_name == "command":
            return self._command
        elif attribute_name == "dynamic_resizing":
            return self._dynamic_resizing
        elif attribute_name == "anchor":
            return self._text_label.cget("anchor")

        else:
            return super().cget(attribute_name)

    def _open_dropdown_menu(self):
        self._dropdown_menu.open(self.winfo_rootx(),
                                 self.winfo_rooty() + self._apply_widget_scaling(self._current_height + 0))

    def _on_enter(self, event=0):
        if self._hover is True and self._state == tkinter.NORMAL and len(self._values) > 0:
            # set color of inner button parts to hover color
            self._canvas.itemconfig("inner_parts_right",
                                    outline=self._apply_appearance_mode(self._button_hover_color),
                                    fill=self._apply_appearance_mode(self._button_hover_color))

    def _on_leave(self, event=0):
        # set color of inner button parts
        self._canvas.itemconfig("inner_parts_right",
                                outline=self._apply_appearance_mode(self._button_color),
                                fill=self._apply_appearance_mode(self._button_color))

    def _variable_callback(self, var_name, index, mode):
        if not self._variable_callback_blocked:
            self._current_value = self._variable.get()
            self._text_label.configure(text=self._current_value)

    def _dropdown_callback(self, value: str):
        self._current_value = value
        self._text_label.configure(text=self._current_value)

        if self._variable is not None:
            self._variable_callback_blocked = True
            self._variable.set(self._current_value)
            self._variable_callback_blocked = False

        if self._command is not None:
            self._command(self._current_value)

    def set(self, value: str):
        self._current_value = value
        self._text_label.configure(text=self._current_value)

        if self._variable is not None:
            self._variable_callback_blocked = True
            self._variable.set(self._current_value)
            self._variable_callback_blocked = False

    def get(self) -> str:
        return self._current_value

    def _clicked(self, event=0):
        if self._state is not tkinter.DISABLED and len(self._values) > 0:
            self._open_dropdown_menu()

    def bind(self, sequence: str = None, command: Callable = None, add: Union[str, bool] = True):
        """ called on the tkinter.Canvas """
        if not (add == "+" or add is True):
            raise ValueError("'add' argument can only be '+' or True to preserve internal callbacks")
        self._canvas.bind(sequence, command, add=True)
        self._text_label.bind(sequence, command, add=True)

    def unbind(self, sequence: str = None, funcid: str = None):
        """ called on the tkinter.Label and tkinter.Canvas """
        if funcid is not None:
            raise ValueError("'funcid' argument can only be None, because there is a bug in" +
                             " tkinter and its not clear whether the internal callbacks will be unbinded or not")
        self._canvas.unbind(sequence, None)
        self._text_label.unbind(sequence, None)
        self._create_bindings(sequence=sequence)  # restore internal callbacks for sequence

    def focus(self):
        return self._text_label.focus()

    def focus_set(self):
        return self._text_label.focus_set()

    def focus_force(self):
        return self._text_label.focus_force()
