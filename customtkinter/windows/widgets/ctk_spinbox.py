import tkinter
import sys
import copy
from typing import Union, Tuple, Callable, List, Optional, Any

from .core_rendering import CTkCanvas
from .theme import ThemeManager
from .core_rendering import DrawEngine
from .core_widget_classes import CTkBaseClass
from .font import CTkFont


class CTkSpinBox(CTkBaseClass):
    """
    Spinbox with rounded corners, border, variable support.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 master: Any,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

                 font: Optional[Union[tuple, CTkFont]] = None,
                 format: Optional[str] = "{}",
                 from_: Optional[Union[int, float]] = None,
                 to: Optional[Union[int, float]] = None,
                 values: Optional[List] = None,
                 default_value: Optional[Union[int, float, str]] = None,
                 step_button: Optional[Union[int, float]] = None,
                 step_scroll: Optional[Union[int, float]] = None,
                 state: str = tkinter.NORMAL,
                 hover: bool = True,
                 variable: Union[tkinter.Variable, None] = None,
                 command: Union[Callable[[Union[int, float, str]], Any], None] = None,
                 justify: str = "left",
                 **kwargs):

        # transfer basic functionality (_bg_color, size, __appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

        # shape
        self._corner_radius = ThemeManager.theme["CTkSpinBox"]["corner_radius"] if corner_radius is None else corner_radius
        self._border_width = ThemeManager.theme["CTkSpinBox"]["border_width"] if border_width is None else border_width

        # color
        self._fg_color = ThemeManager.theme["CTkSpinBox"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
        self._border_color = ThemeManager.theme["CTkSpinBox"]["border_color"] if border_color is None else self._check_color_type(border_color)
        self._button_color = ThemeManager.theme["CTkSpinBox"]["button_color"] if button_color is None else self._check_color_type(button_color)
        self._button_hover_color = ThemeManager.theme["CTkSpinBox"]["button_hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)
        self._text_color = ThemeManager.theme["CTkSpinBox"]["text_color"] if text_color is None else self._check_color_type(text_color)
        self._text_color_disabled = ThemeManager.theme["CTkSpinBox"]["text_color_disabled"] if text_color_disabled is None else self._check_color_type(text_color_disabled)

        # font
        self._font = CTkFont() if font is None else self._check_font_type(font)
        if isinstance(self._font, CTkFont):
            self._font.add_size_configure_callback(self._update_font)

        # callback and hover functionality
        self._command = command
        self._original_variable = variable
        self._state = state
        self._hover = hover

        # spinbox functionality
        self._format = format
        if values is not None:
            #converted to str to allow index method with Entry's value
            self._values = values
            inner = self._format[self._format.index("{"):self._format.index("}")+1]
            self._formatted_values = list(map(inner.format, self._values))
        else:
            self._values = None
            self._formatted_values = None
        self._from = from_
        self._to = to
        if step_button is None and step_scroll is None:
            self._step_button = 1
            self._step_scroll = 1
        else:
            self._step_button = step_button if step_button is not None else step_scroll
            self._step_scroll = step_scroll if step_scroll is not None else step_button

        # configure grid system (1x1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._canvas = CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._desired_width),
                                 height=self._apply_widget_scaling(self._desired_height))
        self.draw_engine = DrawEngine(self._canvas)

        self._entry = tkinter.Entry(master=self,
                                    state=self._state,
                                    width=1,
                                    bd=0,
                                    justify=justify,
                                    highlightthickness=0,
                                    font=self._apply_font_scaling(self._font))

        self._create_grid()
        self._create_bindings()
        self._draw()  # initial draw

        if self._original_variable is not None:
            self._support_variabile = tkinter.StringVar(value=self._format.format(self._original_variable.get()))
            self._entry.configure(textvariable=self._support_variabile)
            self._support_variabile.trace_add("write", self._update_original_variable)
        elif default_value is not None:
            self.set(default_value)

    def _update_original_variable(self, *args):
        value = self.get()
        if value:
            try:
                if isinstance(self._original_variable, tkinter.IntVar):
                    value = round(float(value))
                elif isinstance(self._original_variable, tkinter.DoubleVar):
                    value = float(value)
                elif isinstance(self._original_variable, tkinter.BooleanVar):
                    value = bool(value)
            except ValueError:
                pass
            else:
                self._original_variable.set(value)

    def _create_bindings(self, sequence: Optional[str] = None):
        """ set necessary bindings for functionality of widget, will overwrite other bindings """
        if sequence is None:
            self._canvas.tag_bind("right_parts", "<Enter>", self._on_enter)
            self._canvas.tag_bind("dropdown_arrow", "<Enter>", self._on_enter)
            self._canvas.tag_bind("dropup_arrow", "<Enter>", self._on_enter)
            self._canvas.tag_bind("right_parts", "<Leave>", self._on_leave)
            self._canvas.tag_bind("dropdown_arrow", "<Leave>", self._on_leave)
            self._canvas.tag_bind("dropup_arrow", "<Leave>", self._on_leave)
            self._canvas.tag_bind("right_parts", "<Button-1>", self._clicked)
            self._canvas.tag_bind("dropdown_arrow", "<Button-1>", self._clicked)
            self._canvas.tag_bind("dropup_arrow", "<Button-1>", self._clicked)
            self._canvas.bind("<MouseWheel>", self._clicked)
            self._entry.bind("<MouseWheel>", self._clicked)
            self._entry.bind("<FocusOut>", self._clicked) #to force format if user updates manually

    def _create_grid(self):
        self._canvas.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew")

        left_section_width = self._current_width - self._current_height
        self._entry.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="ew",
                         padx=(max(self._apply_widget_scaling(self._corner_radius), self._apply_widget_scaling(3)),
                               max(self._apply_widget_scaling(self._current_width - left_section_width + 3), self._apply_widget_scaling(3))),
                         pady=self._apply_widget_scaling(self._border_width))

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        # change entry font size and grid padding
        self._entry.configure(font=self._apply_font_scaling(self._font))
        self._create_grid()

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw(no_color_updates=True)

    def _set_dimensions(self, width: int = None, height: int = None):
        super()._set_dimensions(width, height)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw()

    def _update_font(self):
        """ pass font to tkinter widgets with applied font scaling and update grid with workaround """
        self._entry.configure(font=self._apply_font_scaling(self._font))

        # Workaround to force grid to be resized when text changes size.
        # Otherwise grid will lag and only resizes if other mouse action occurs.
        self._canvas.grid_forget()
        self._canvas.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew")

    def destroy(self):
        if isinstance(self._font, CTkFont):
            self._font.remove_size_configure_callback(self._update_font)

        super().destroy()

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

        left_section_width = self._current_width - self._current_height
        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border_vertical_split(self._apply_widget_scaling(self._current_width),
                                                                                            self._apply_widget_scaling(self._current_height),
                                                                                            self._apply_widget_scaling(self._corner_radius),
                                                                                            self._apply_widget_scaling(self._border_width),
                                                                                            self._apply_widget_scaling(left_section_width))

        requires_recoloring_2 = self.draw_engine.draw_arrow(self._apply_widget_scaling(self._current_width - (self._current_height / 2)),
                                                                     self._apply_widget_scaling(self._current_height / 3 * 2),
                                                                     self._apply_widget_scaling(self._current_height / 3),
                                                                     direction="down")

        requires_recoloring_3 = self.draw_engine.draw_arrow(self._apply_widget_scaling(self._current_width - (self._current_height / 2)),
                                                                     self._apply_widget_scaling(self._current_height / 3),
                                                                     self._apply_widget_scaling(self._current_height / 3),
                                                                     direction="up")

        if no_color_updates is False or requires_recoloring or requires_recoloring_2 or requires_recoloring_3:

            self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))

            self._canvas.itemconfig("inner_parts_left",
                                    outline=self._apply_appearance_mode(self._fg_color),
                                    fill=self._apply_appearance_mode(self._fg_color))
            self._canvas.itemconfig("border_parts_left",
                                    outline=self._apply_appearance_mode(self._border_color),
                                    fill=self._apply_appearance_mode(self._border_color))
            self._canvas.itemconfig("inner_parts_right",
                                    outline=self._apply_appearance_mode(self._button_color),
                                    fill=self._apply_appearance_mode(self._button_color))
            self._canvas.itemconfig("border_parts_right",
                                    outline=self._apply_appearance_mode(self._button_color),
                                    fill=self._apply_appearance_mode(self._button_color))

            self._entry.configure(bg=self._apply_appearance_mode(self._fg_color),
                                  fg=self._apply_appearance_mode(self._text_color),
                                  readonlybackground=self._apply_appearance_mode(self._fg_color),
                                  disabledbackground=self._apply_appearance_mode(self._fg_color),
                                  disabledforeground=self._apply_appearance_mode(self._text_color_disabled),
                                  highlightcolor=self._apply_appearance_mode(self._fg_color),
                                  insertbackground=self._apply_appearance_mode(self._text_color))

            if self._state == tkinter.DISABLED:
                self._canvas.itemconfig("dropdown_arrow",
                                        fill=self._apply_appearance_mode(self._text_color_disabled))
                self._canvas.itemconfig("dropup_arrow",
                                        fill=self._apply_appearance_mode(self._text_color_disabled))
            else:
                self._canvas.itemconfig("dropdown_arrow",
                                        fill=self._apply_appearance_mode(self._text_color))
                self._canvas.itemconfig("dropup_arrow",
                                        fill=self._apply_appearance_mode(self._text_color))

    def configure(self, require_redraw=False, **kwargs):
        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")
            require_redraw = True

        if "border_width" in kwargs:
            self._border_width = kwargs.pop("border_width")
            self._create_grid()
            require_redraw = True

        if "fg_color" in kwargs:
            self._fg_color = self._check_color_type(kwargs.pop("fg_color"))
            require_redraw = True

        if "border_color" in kwargs:
            self._border_color = self._check_color_type(kwargs.pop("border_color"))
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

        if "font" in kwargs:
            if isinstance(self._font, CTkFont):
                self._font.remove_size_configure_callback(self._update_font)
            self._font = self._check_font_type(kwargs.pop("font"))
            if isinstance(self._font, CTkFont):
                self._font.add_size_configure_callback(self._update_font)

            self._update_font()

        if "values" in kwargs:
            self._values = list(map(str, kwargs.pop("values")))
            inner = self._format[self._format.index("{"):self._format.index("}")+1]
            self._formatted_values = list(map(inner.format, self._values))
            self.set(self.get()) #to verify current value is still valid
        
        if "from_" in kwargs:
            self._from = kwargs.pop("from_")
            self.set(self.get()) #to clamp current value to new limit
        
        if "to" in kwargs:
            self._to = kwargs.pop("to")
            self.set(self.get()) #to clamp current value to new limit
        
        if "format" in kwargs:
            value = self.get()
            self._format = kwargs.pop("format")
            if self._values is not None:
                inner = self._format[self._format.index("{"):self._format.index("}")+1]
                self._formatted_values = list(map(inner.format, self._values))
            self.set(value) #to update current value's format
        
        if "step_button" in kwargs:
            self._step_button = kwargs.pop("step_button")
        
        if "step_scroll" in kwargs:
            self._step_scroll = kwargs.pop("step_scroll")
        
        if "default_value" in kwargs:
            kwargs.pop("default_value")

        if "state" in kwargs:
            self._state = kwargs.pop("state")
            self._entry.configure(state=self._state)
            require_redraw = True

        if "hover" in kwargs:
            self._hover = kwargs.pop("hover")

        if "variable" in kwargs:
            self._original_variable = kwargs.pop("variable")
            self._entry.configure(textvariable=self._original_variable)

        if "command" in kwargs:
            self._command = kwargs.pop("command")

        if "justify" in kwargs:
            self._entry.configure(justify=kwargs.pop("justify"))

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "corner_radius":
            return self._corner_radius
        elif attribute_name == "border_width":
            return self._border_width

        elif attribute_name == "fg_color":
            return self._fg_color
        elif attribute_name == "border_color":
            return self._border_color
        elif attribute_name == "button_color":
            return self._button_color
        elif attribute_name == "button_hover_color":
            return self._button_hover_color
        elif attribute_name == "text_color":
            return self._text_color
        elif attribute_name == "text_color_disabled":
            return self._text_color_disabled

        elif attribute_name == "font":
            return self._font
        elif attribute_name == "values":
            return copy.copy(self._values)
        elif attribute_name in ["from_", "from"]:
            return self._from
        elif attribute_name == "to":
            return self._to
        elif attribute_name == "format":
            return self._format
        elif attribute_name == "step_button":
            return self._step_button
        elif attribute_name == "step_scroll":
            return self._step_scroll
        elif attribute_name == "default_value":
            return "#N/A"
        elif attribute_name == "state":
            return self._state
        elif attribute_name == "hover":
            return self._hover
        elif attribute_name == "variable":
            return self._original_variable
        elif attribute_name == "command":
            return self._command
        elif attribute_name == "justify":
            return self._entry.cget("justify")
        else:
            return super().cget(attribute_name)

    def _on_enter(self, event=0):
        if self._hover is True and self._state == tkinter.NORMAL:
            if sys.platform == "darwin" and self._cursor_manipulation_enabled:
                self._canvas.configure(cursor="pointinghand")
            elif sys.platform.startswith("win") and self._cursor_manipulation_enabled:
                self._canvas.configure(cursor="hand2")

            # set color of inner button parts to hover color
            self._canvas.itemconfig("inner_parts_right",
                                    outline=self._apply_appearance_mode(self._button_hover_color),
                                    fill=self._apply_appearance_mode(self._button_hover_color))
            self._canvas.itemconfig("border_parts_right",
                                    outline=self._apply_appearance_mode(self._button_hover_color),
                                    fill=self._apply_appearance_mode(self._button_hover_color))

    def _on_leave(self, event=0):
        if sys.platform == "darwin" and self._cursor_manipulation_enabled:
            self._canvas.configure(cursor="arrow")
        elif sys.platform.startswith("win") and self._cursor_manipulation_enabled:
            self._canvas.configure(cursor="arrow")

        # set color of inner button parts
        self._canvas.itemconfig("inner_parts_right",
                                outline=self._apply_appearance_mode(self._button_color),
                                fill=self._apply_appearance_mode(self._button_color))
        self._canvas.itemconfig("border_parts_right",
                                outline=self._apply_appearance_mode(self._button_color),
                                fill=self._apply_appearance_mode(self._button_color))

    def set(self, value: Union[int, float, str]):
        formatted_value = self._format.format(value)

        if self._state == "readonly":
            self._entry.configure(state="normal")
            self._entry.delete(0, tkinter.END)
            self._entry.insert(0, formatted_value)
            self._entry.configure(state="readonly")
        else:
            self._entry.delete(0, tkinter.END)
            self._entry.insert(0, formatted_value)

    def get(self) -> str:
        value = self._entry.get()
        pre = self._format.split("{")[0]
        post = self._format.split("}")[-1]
        value = value.replace(pre, "")
        value = value.replace(post, "")
        return value

    def _clicked(self, event: tkinter.Event=None):
        if self._state is not tkinter.DISABLED:
            if event.type == tkinter.EventType.ButtonPress:
                is_up = event.y < self._canvas.winfo_height() / 2
                delta = self._step_button
            elif event.type == tkinter.EventType.MouseWheel:
                is_up = event.delta > 0
                delta = self._step_scroll
            else:
                is_up = False
                delta = 0
            if not is_up:
                delta = -delta

            current_value = self.get()

            if self._values is not None and self._values:
                try:
                    idx = self._formatted_values.index(current_value) + delta
                except ValueError:
                    idx = 0 if is_up else -1
                else:
                    idx = 0 if idx < 0 else idx
                    idx = -1 if idx >= len(self._values) else idx
                new_value = self._values[idx]
            else:
                try:
                    if current_value.find(".") < 0:
                        new_value = int(current_value) + delta
                    else:
                        new_value = float(current_value) + delta
                except ValueError:
                    new_value = 0

                if self._from is not None and new_value < self._from:
                    new_value = self._from
                if self._to is not None and new_value > self._to:
                    new_value = self._to

            self.set(new_value)

            if self._command is not None:
                self._command(new_value)

    def bind(self, sequence=None, command=None, add=True):
        """ called on the tkinter.Entry """
        if not (add == "+" or add is True):
            raise ValueError("'add' argument can only be '+' or True to preserve internal callbacks")
        self._entry.bind(sequence, command, add=True)

    def unbind(self, sequence=None, funcid=None):
        """ called on the tkinter.Entry """
        if funcid is not None:
            raise ValueError("'funcid' argument can only be None, because there is a bug in" +
                             " tkinter and its not clear whether the internal callbacks will be unbinded or not")
        self._entry.unbind(sequence, None)  # unbind all callbacks for sequence
        self._create_bindings(sequence=sequence)  # restore internal callbacks for sequence

    def focus(self):
        return self._entry.focus()

    def focus_set(self):
        return self._entry.focus_set()

    def focus_force(self):
        return self._entry.focus_force()
