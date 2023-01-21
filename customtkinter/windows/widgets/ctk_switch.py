import tkinter
import sys
from typing import Union, Tuple, Callable, Optional

from .core_rendering import CTkCanvas
from .theme import ThemeManager
from .core_rendering import DrawEngine
from .core_widget_classes import CTkBaseClass
from .font import CTkFont


class CTkSwitch(CTkBaseClass):
    """
    Switch with rounded corners, border, label, command, variable support.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 master: any,
                 width: int = 100,
                 height: int = 24,
                 switch_width: int = 36,
                 switch_height: int = 18,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,
                 button_length: Optional[int] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Union[str, Tuple[str, str]] = "transparent",
                 progress_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

                 text: str = "CTkSwitch",
                 font: Optional[Union[tuple, CTkFont]] = None,
                 textvariable: Union[tkinter.Variable, None] = None,
                 onvalue: Union[int, str] = 1,
                 offvalue: Union[int, str] = 0,
                 variable: Union[tkinter.Variable, None] = None,
                 hover: bool = True,
                 command: Union[Callable, None] = None,
                 state: str = tkinter.NORMAL,
                 **kwargs):

        # transfer basic functionality (_bg_color, size, __appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

        # dimensions
        self._switch_width = switch_width
        self._switch_height = switch_height

        # color
        self._border_color = self._check_color_type(border_color, transparency=True)
        self._fg_color = ThemeManager.theme["CTkSwitch"]["fg_Color"] if fg_color is None else self._check_color_type(fg_color)
        self._progress_color = ThemeManager.theme["CTkSwitch"]["progress_color"] if progress_color is None else self._check_color_type(progress_color, transparency=True)
        self._button_color = ThemeManager.theme["CTkSwitch"]["button_color"] if button_color is None else self._check_color_type(button_color)
        self._button_hover_color = ThemeManager.theme["CTkSwitch"]["button_hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)
        self._text_color = ThemeManager.theme["CTkSwitch"]["text_color"] if text_color is None else self._check_color_type(text_color)
        self._text_color_disabled = ThemeManager.theme["CTkSwitch"]["text_color_disabled"] if text_color_disabled is None else self._check_color_type(text_color_disabled)

        # text
        self._text = text
        self._text_label = None

        # font
        self._font = CTkFont() if font is None else self._check_font_type(font)
        if isinstance(self._font, CTkFont):
            self._font.add_size_configure_callback(self._update_font)

        # shape
        self._corner_radius = ThemeManager.theme["CTkSwitch"]["corner_radius"] if corner_radius is None else corner_radius
        self._border_width = ThemeManager.theme["CTkSwitch"]["border_width"] if border_width is None else border_width
        self._button_length = ThemeManager.theme["CTkSwitch"]["button_length"] if button_length is None else button_length
        self._hover_state: bool = False
        self._check_state: bool = False  # True if switch is activated
        self._hover = hover
        self._state = state
        self._onvalue = onvalue
        self._offvalue = offvalue

        # callback and control variables
        self._command = command
        self._variable = variable
        self._variable_callback_blocked = False
        self._variable_callback_name = None
        self._textvariable = textvariable

        # configure grid system (3x1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0, minsize=self._apply_widget_scaling(6))
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._bg_canvas = CTkCanvas(master=self,
                                    highlightthickness=0,
                                    width=self._apply_widget_scaling(self._current_width),
                                    height=self._apply_widget_scaling(self._current_height))
        self._bg_canvas.grid(row=0, column=0, columnspan=3, sticky="nswe")

        self._canvas = CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._switch_width),
                                 height=self._apply_widget_scaling(self._switch_height))
        self._canvas.grid(row=0, column=0, sticky="")
        self._draw_engine = DrawEngine(self._canvas)

        self._text_label = tkinter.Label(master=self,
                                         bd=0,
                                         padx=0,
                                         pady=0,
                                         text=self._text,
                                         justify=tkinter.LEFT,
                                         font=self._apply_font_scaling(self._font),
                                         textvariable=self._textvariable)
        self._text_label.grid(row=0, column=2, sticky="w")
        self._text_label["anchor"] = "w"

        if self._variable is not None and self._variable != "":
            self._variable_callback_name = self._variable.trace_add("write", self._variable_callback)
            self._check_state = True if self._variable.get() == self._onvalue else False

        self._create_bindings()
        self._set_cursor()
        self._draw()  # initial draw

    def _create_bindings(self, sequence: Optional[str] = None):
        """ set necessary bindings for functionality of widget, will overwrite other bindings """
        if sequence is None or sequence == "<Enter>":
            self._canvas.bind("<Enter>", self._on_enter)
            self._text_label.bind("<Enter>", self._on_enter)
        if sequence is None or sequence == "<Leave>":
            self._canvas.bind("<Leave>", self._on_leave)
            self._text_label.bind("<Leave>", self._on_leave)
        if sequence is None or sequence == "<Button-1>":
            self._canvas.bind("<Button-1>", self.toggle)
            self._text_label.bind("<Button-1>", self.toggle)

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        self.grid_columnconfigure(1, weight=0, minsize=self._apply_widget_scaling(6))
        self._text_label.configure(font=self._apply_font_scaling(self._font))

        self._bg_canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                                  height=self._apply_widget_scaling(self._desired_height))
        self._canvas.configure(width=self._apply_widget_scaling(self._switch_width),
                               height=self._apply_widget_scaling(self._switch_height))
        self._draw(no_color_updates=True)

    def _set_dimensions(self, width: int = None, height: int = None):
        super()._set_dimensions(width, height)

        self._bg_canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                                  height=self._apply_widget_scaling(self._desired_height))

    def _update_font(self):
        """ pass font to tkinter widgets with applied font scaling and update grid with workaround """
        self._text_label.configure(font=self._apply_font_scaling(self._font))

        # Workaround to force grid to be resized when text changes size.
        # Otherwise grid will lag and only resizes if other mouse action occurs.
        self._bg_canvas.grid_forget()
        self._bg_canvas.grid(row=0, column=0, columnspan=3, sticky="nswe")

    def destroy(self):
        # remove variable_callback from variable callbacks if variable exists
        if self._variable is not None:
            self._variable.trace_remove("write", self._variable_callback_name)

        if isinstance(self._font, CTkFont):
            self._font.remove_size_configure_callback(self._update_font)

        super().destroy()

    def _set_cursor(self):
        if self._cursor_manipulation_enabled:
            if self._state == tkinter.DISABLED:
                if sys.platform == "darwin":
                    self._canvas.configure(cursor="arrow")
                    if self._text_label is not None:
                        self._text_label.configure(cursor="arrow")
                elif sys.platform.startswith("win"):
                    self._canvas.configure(cursor="arrow")
                    if self._text_label is not None:
                        self._text_label.configure(cursor="arrow")

            elif self._state == tkinter.NORMAL:
                if sys.platform == "darwin":
                    self._canvas.configure(cursor="pointinghand")
                    if self._text_label is not None:
                        self._text_label.configure(cursor="pointinghand")
                elif sys.platform.startswith("win"):
                    self._canvas.configure(cursor="hand2")
                    if self._text_label is not None:
                        self._text_label.configure(cursor="hand2")

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

        if self._check_state is True:
            requires_recoloring = self._draw_engine.draw_rounded_slider_with_border_and_button(self._apply_widget_scaling(self._switch_width),
                                                                                               self._apply_widget_scaling(self._switch_height),
                                                                                               self._apply_widget_scaling(self._corner_radius),
                                                                                               self._apply_widget_scaling(self._border_width),
                                                                                               self._apply_widget_scaling(self._button_length),
                                                                                               self._apply_widget_scaling(self._corner_radius),
                                                                                               1, "w")
        else:
            requires_recoloring = self._draw_engine.draw_rounded_slider_with_border_and_button(self._apply_widget_scaling(self._switch_width),
                                                                                               self._apply_widget_scaling(self._switch_height),
                                                                                               self._apply_widget_scaling(self._corner_radius),
                                                                                               self._apply_widget_scaling(self._border_width),
                                                                                               self._apply_widget_scaling(self._button_length),
                                                                                               self._apply_widget_scaling(self._corner_radius),
                                                                                               0, "w")

        if no_color_updates is False or requires_recoloring:
            self._bg_canvas.configure(bg=self._apply_appearance_mode(self._bg_color))
            self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))

            if self._border_color == "transparent":
                self._canvas.itemconfig("border_parts",
                                        fill=self._apply_appearance_mode(self._bg_color),
                                        outline=self._apply_appearance_mode(self._bg_color))
            else:
                self._canvas.itemconfig("border_parts",
                                        fill=self._apply_appearance_mode(self._border_color),
                                        outline=self._apply_appearance_mode(self._border_color))

            self._canvas.itemconfig("inner_parts",
                                    fill=self._apply_appearance_mode(self._fg_color),
                                    outline=self._apply_appearance_mode(self._fg_color))

            if self._progress_color == "transparent":
                self._canvas.itemconfig("progress_parts",
                                        fill=self._apply_appearance_mode(self._fg_color),
                                        outline=self._apply_appearance_mode(self._fg_color))
            else:
                self._canvas.itemconfig("progress_parts",
                                        fill=self._apply_appearance_mode(self._progress_color),
                                        outline=self._apply_appearance_mode(self._progress_color))

            self._canvas.itemconfig("slider_parts",
                                    fill=self._apply_appearance_mode(self._button_color),
                                    outline=self._apply_appearance_mode(self._button_color))

            if self._state == tkinter.DISABLED:
                self._text_label.configure(fg=(self._apply_appearance_mode(self._text_color_disabled)))
            else:
                self._text_label.configure(fg=self._apply_appearance_mode(self._text_color))

            self._text_label.configure(bg=self._apply_appearance_mode(self._bg_color))

    def configure(self, require_redraw=False, **kwargs):
        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")
            require_redraw = True

        if "border_width" in kwargs:
            self._border_width = kwargs.pop("border_width")
            require_redraw = True

        if "button_length" in kwargs:
            self._button_length = kwargs.pop("button_length")
            require_redraw = True

        if "switch_width" in kwargs:
            self._switch_width = kwargs.pop("switch_width")
            self._canvas.configure(width=self._apply_widget_scaling(self._switch_width))
            require_redraw = True

        if "switch_height" in kwargs:
            self._switch_height = kwargs.pop("switch_height")
            self._canvas.configure(height=self._apply_widget_scaling(self._switch_height))
            require_redraw = True

        if "text" in kwargs:
            self._text = kwargs.pop("text")
            self._text_label.configure(text=self._text)

        if "font" in kwargs:
            if isinstance(self._font, CTkFont):
                self._font.remove_size_configure_callback(self._update_font)
            self._font = self._check_font_type(kwargs.pop("font"))
            if isinstance(self._font, CTkFont):
                self._font.add_size_configure_callback(self._update_font)

            self._update_font()

        if "state" in kwargs:
            self._state = kwargs.pop("state")
            self._set_cursor()
            require_redraw = True

        if "fg_color" in kwargs:
            self._fg_color = self._check_color_type(kwargs.pop("fg_color"))
            require_redraw = True

        if "progress_color" in kwargs:
            self._progress_color = self._check_color_type(kwargs.pop("progress_color"), transparency=True)
            require_redraw = True

        if "button_color" in kwargs:
            self._button_color = self._check_color_type(kwargs.pop("button_color"))
            require_redraw = True

        if "button_hover_color" in kwargs:
            self._button_hover_color = self._check_color_type(kwargs.pop("button_hover_color"))
            require_redraw = True

        if "border_color" in kwargs:
            self._border_color = self._check_color_type(kwargs.pop("border_color"), transparency=True)
            require_redraw = True

        if "hover" in kwargs:
            self._hover = kwargs.pop("hover")

        if "command" in kwargs:
            self._command = kwargs.pop("command")

        if "textvariable" in kwargs:
            self._textvariable = kwargs.pop("textvariable")
            self._text_label.configure(textvariable=self._textvariable)

        if "variable" in kwargs:
            if self._variable is not None and self._variable != "":
                self._variable.trace_remove("write", self._variable_callback_name)

            self._variable = kwargs.pop("variable")

            if self._variable is not None and self._variable != "":
                self._variable_callback_name = self._variable.trace_add("write", self._variable_callback)
                self._check_state = True if self._variable.get() == self._onvalue else False
                require_redraw = True

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "corner_radius":
            return self._corner_radius
        elif attribute_name == "border_width":
            return self._border_width
        elif attribute_name == "button_length":
            return self._button_length
        elif attribute_name == "switch_width":
            return self._switch_width
        elif attribute_name == "switch_height":
            return self._switch_height

        elif attribute_name == "fg_color":
            return self._fg_color
        elif attribute_name == "border_color":
            return self._border_color
        elif attribute_name == "progress_color":
            return self._progress_color
        elif attribute_name == "button_color":
            return self._button_color
        elif attribute_name == "button_hover_color":
            return self._button_hover_color
        elif attribute_name == "text_color":
            return self._text_color
        elif attribute_name == "text_color_disabled":
            return self._text_color_disabled

        elif attribute_name == "text":
            return self._text
        elif attribute_name == "font":
            return self._font
        elif attribute_name == "textvariable":
            return self._textvariable
        elif attribute_name == "onvalue":
            return self._onvalue
        elif attribute_name == "offvalue":
            return self._offvalue
        elif attribute_name == "variable":
            return self._variable
        elif attribute_name == "hover":
            return self._hover
        elif attribute_name == "command":
            return self._command
        elif attribute_name == "state":
            return self._state

        else:
            return super().cget(attribute_name)

    def toggle(self, event=None):
        if self._state is not tkinter.DISABLED:
            if self._check_state is True:
                self._check_state = False
            else:
                self._check_state = True

            self._draw(no_color_updates=True)

            if self._variable is not None:
                self._variable_callback_blocked = True
                self._variable.set(self._onvalue if self._check_state is True else self._offvalue)
                self._variable_callback_blocked = False

            if self._command is not None:
                self._command()

    def select(self, from_variable_callback=False):
        if self._state is not tkinter.DISABLED or from_variable_callback:
            self._check_state = True

            self._draw(no_color_updates=True)

            if self._variable is not None and not from_variable_callback:
                self._variable_callback_blocked = True
                self._variable.set(self._onvalue)
                self._variable_callback_blocked = False

    def deselect(self, from_variable_callback=False):
        if self._state is not tkinter.DISABLED or from_variable_callback:
            self._check_state = False

            self._draw(no_color_updates=True)

            if self._variable is not None and not from_variable_callback:
                self._variable_callback_blocked = True
                self._variable.set(self._offvalue)
                self._variable_callback_blocked = False

    def get(self) -> Union[int, str]:
        return self._onvalue if self._check_state is True else self._offvalue

    def _on_enter(self, event=0):
        if self._hover is True and self._state == "normal":
            self._hover_state = True
            self._canvas.itemconfig("slider_parts",
                                    fill=self._apply_appearance_mode(self._button_hover_color),
                                    outline=self._apply_appearance_mode(self._button_hover_color))

    def _on_leave(self, event=0):
        self._hover_state = False
        self._canvas.itemconfig("slider_parts",
                                fill=self._apply_appearance_mode(self._button_color),
                                outline=self._apply_appearance_mode(self._button_color))

    def _variable_callback(self, var_name, index, mode):
        if not self._variable_callback_blocked:
            if self._variable.get() == self._onvalue:
                self.select(from_variable_callback=True)
            elif self._variable.get() == self._offvalue:
                self.deselect(from_variable_callback=True)

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
