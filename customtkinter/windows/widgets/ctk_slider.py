import tkinter
import sys
from typing import Union, Tuple, Callable, Optional

from .core_rendering import CTkCanvas
from .theme import ThemeManager
from .core_rendering import DrawEngine
from .core_widget_classes import CTkBaseClass


class CTkSlider(CTkBaseClass):
    """
    Slider with rounded corners, border, number of steps, variable support, vertical orientation.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 master: any,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 corner_radius: Optional[int] = None,
                 button_corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,
                 button_length: Optional[int] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Union[str, Tuple[str, str]] = "transparent",
                 progress_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,

                 from_: int = 0,
                 to: int = 1,
                 state: str = "normal",
                 number_of_steps: Union[int, None] = None,
                 hover: bool = True,
                 command: Union[Callable[[float], None], None] = None,
                 variable: Union[tkinter.Variable, None] = None,
                 orientation: str = "horizontal",
                 **kwargs):

        # set default dimensions according to orientation
        if width is None:
            if orientation.lower() == "vertical":
                width = 16
            else:
                width = 200
        if height is None:
            if orientation.lower() == "vertical":
                height = 200
            else:
                height = 16

        # transfer basic functionality (_bg_color, size, __appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

        # color
        self._border_color = self._check_color_type(border_color, transparency=True)
        self._fg_color = ThemeManager.theme["CTkSlider"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
        self._progress_color = ThemeManager.theme["CTkSlider"]["progress_color"] if progress_color is None else self._check_color_type(progress_color, transparency=True)
        self._button_color = ThemeManager.theme["CTkSlider"]["button_color"] if button_color is None else self._check_color_type(button_color)
        self._button_hover_color = ThemeManager.theme["CTkSlider"]["button_hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)

        # shape
        self._corner_radius = ThemeManager.theme["CTkSlider"]["corner_radius"] if corner_radius is None else corner_radius
        self._button_corner_radius = ThemeManager.theme["CTkSlider"]["button_corner_radius"] if button_corner_radius is None else button_corner_radius
        self._border_width = ThemeManager.theme["CTkSlider"]["border_width"] if border_width is None else border_width
        self._button_length = ThemeManager.theme["CTkSlider"]["button_length"] if button_length is None else button_length
        self._value: float = 0.5  # initial value of slider in percent
        self._orientation = orientation
        self._hover_state: bool = False
        self._hover = hover
        self._from_ = from_
        self._to = to
        self._number_of_steps = number_of_steps
        self._output_value = self._from_ + (self._value * (self._to - self._from_))

        if self._corner_radius < self._button_corner_radius:
            self._corner_radius = self._button_corner_radius

        # callback and control variables
        self._command = command
        self._variable: tkinter.Variable = variable
        self._variable_callback_blocked: bool = False
        self._variable_callback_name: Union[bool, None] = None
        self._state = state

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._canvas = CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._desired_width),
                                 height=self._apply_widget_scaling(self._desired_height))
        self._canvas.grid(column=0, row=0, rowspan=1, columnspan=1, sticky="nswe")
        self._draw_engine = DrawEngine(self._canvas)

        self._create_bindings()
        self._set_cursor()
        self._draw()  # initial draw

        if self._variable is not None:
            self._variable_callback_name = self._variable.trace_add("write", self._variable_callback)
            self._variable_callback_blocked = True
            self.set(self._variable.get(), from_variable_callback=True)
            self._variable_callback_blocked = False

    def _create_bindings(self, sequence: Optional[str] = None):
        """ set necessary bindings for functionality of widget, will overwrite other bindings """
        if sequence is None or sequence == "<Enter>":
            self._canvas.bind("<Enter>", self._on_enter)
        if sequence is None or sequence == "<Leave>":
            self._canvas.bind("<Leave>", self._on_leave)
        if sequence is None or sequence == "<Button-1>":
            self._canvas.bind("<Button-1>", self._clicked)
        if sequence is None or sequence == "<B1-Motion>":
            self._canvas.bind("<B1-Motion>", self._clicked)

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw(no_color_updates=True)

    def _set_dimensions(self, width=None, height=None):
        super()._set_dimensions(width, height)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw()

    def destroy(self):
        # remove variable_callback from variable callbacks if variable exists
        if self._variable is not None:
            self._variable.trace_remove("write", self._variable_callback_name)

        super().destroy()

    def _set_cursor(self):
        if self._state == "normal" and self._cursor_manipulation_enabled:
            if sys.platform == "darwin":
                self.configure(cursor="pointinghand")
            elif sys.platform.startswith("win"):
                self.configure(cursor="hand2")

        elif self._state == "disabled" and self._cursor_manipulation_enabled:
            if sys.platform == "darwin":
                self.configure(cursor="arrow")
            elif sys.platform.startswith("win"):
                self.configure(cursor="arrow")

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

        if self._orientation.lower() == "horizontal":
            orientation = "w"
        elif self._orientation.lower() == "vertical":
            orientation = "s"
        else:
            orientation = "w"

        requires_recoloring = self._draw_engine.draw_rounded_slider_with_border_and_button(self._apply_widget_scaling(self._current_width),
                                                                                           self._apply_widget_scaling(self._current_height),
                                                                                           self._apply_widget_scaling(self._corner_radius),
                                                                                           self._apply_widget_scaling(self._border_width),
                                                                                           self._apply_widget_scaling(self._button_length),
                                                                                           self._apply_widget_scaling(self._button_corner_radius),
                                                                                           self._value, orientation)

        if no_color_updates is False or requires_recoloring:
            self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))

            if self._border_color == "transparent":
                self._canvas.itemconfig("border_parts", fill=self._apply_appearance_mode(self._bg_color),
                                        outline=self._apply_appearance_mode(self._bg_color))
            else:
                self._canvas.itemconfig("border_parts", fill=self._apply_appearance_mode(self._border_color),
                                        outline=self._apply_appearance_mode(self._border_color))

            self._canvas.itemconfig("inner_parts", fill=self._apply_appearance_mode(self._fg_color),
                                    outline=self._apply_appearance_mode(self._fg_color))

            if self._progress_color == "transparent":
                self._canvas.itemconfig("progress_parts", fill=self._apply_appearance_mode(self._fg_color),
                                        outline=self._apply_appearance_mode(self._fg_color))
            else:
                self._canvas.itemconfig("progress_parts", fill=self._apply_appearance_mode(self._progress_color),
                                        outline=self._apply_appearance_mode(self._progress_color))

            if self._hover_state is True:
                self._canvas.itemconfig("slider_parts",
                                        fill=self._apply_appearance_mode(self._button_hover_color),
                                        outline=self._apply_appearance_mode(self._button_hover_color))
            else:
                self._canvas.itemconfig("slider_parts",
                                        fill=self._apply_appearance_mode(self._button_color),
                                        outline=self._apply_appearance_mode(self._button_color))

    def configure(self, require_redraw=False, **kwargs):
        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")
            require_redraw = True

        if "button_corner_radius" in kwargs:
            self._button_corner_radius = kwargs.pop("button_corner_radius")
            require_redraw = True

        if "border_width" in kwargs:
            self._border_width = kwargs.pop("border_width")
            require_redraw = True

        if "button_length" in kwargs:
            self._button_length = kwargs.pop("button_length")
            require_redraw = True

        if "fg_color" in kwargs:
            self._fg_color = self._check_color_type(kwargs.pop("fg_color"))
            require_redraw = True

        if "border_color" in kwargs:
            self._border_color = self._check_color_type(kwargs.pop("border_color"), transparency=True)
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

        if "from_" in kwargs:
            self._from_ = kwargs.pop("from_")

        if "to" in kwargs:
            self._to = kwargs.pop("to")

        if "state" in kwargs:
            self._state = kwargs.pop("state")
            self._set_cursor()
            require_redraw = True

        if "number_of_steps" in kwargs:
            self._number_of_steps = kwargs.pop("number_of_steps")

        if "hover" in kwargs:
            self._hover = kwargs.pop("hover")

        if "command" in kwargs:
            self._command = kwargs.pop("command")

        if "variable" in kwargs:
            if self._variable is not None:
                self._variable.trace_remove("write", self._variable_callback_name)

            self._variable = kwargs.pop("variable")

            if self._variable is not None and self._variable != "":
                self._variable_callback_name = self._variable.trace_add("write", self._variable_callback)
                self.set(self._variable.get(), from_variable_callback=True)
            else:
                self._variable = None

        if "orientation" in kwargs:
            self._orientation = kwargs.pop("orientation")
            require_redraw = True

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "corner_radius":
            return self._corner_radius
        elif attribute_name == "button_corner_radius":
            return self._button_corner_radius
        elif attribute_name == "border_width":
            return self._border_width
        elif attribute_name == "button_length":
            return self._button_length

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

        elif attribute_name == "from_":
            return self._from_
        elif attribute_name == "to":
            return self._to
        elif attribute_name == "state":
            return self._state
        elif attribute_name == "number_of_steps":
            return self._number_of_steps
        elif attribute_name == "hover":
            return self._hover
        elif attribute_name == "command":
            return self._command
        elif attribute_name == "variable":
            return self._variable
        elif attribute_name == "orientation":
            return self._orientation

        else:
            return super().cget(attribute_name)

    def _clicked(self, event=None):
        if self._state == "normal":
            if self._orientation.lower() == "horizontal":
                self._value = self._reverse_widget_scaling(event.x / self._current_width)
            else:
                self._value = 1 - self._reverse_widget_scaling(event.y / self._current_height)

            if self._value > 1:
                self._value = 1
            if self._value < 0:
                self._value = 0

            self._output_value = self._round_to_step_size(self._from_ + (self._value * (self._to - self._from_)))
            self._value = (self._output_value - self._from_) / (self._to - self._from_)

            self._draw(no_color_updates=False)

            if self._variable is not None:
                self._variable_callback_blocked = True
                self._variable.set(round(self._output_value) if isinstance(self._variable, tkinter.IntVar) else self._output_value)
                self._variable_callback_blocked = False

            if self._command is not None:
                self._command(self._output_value)

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

    def _round_to_step_size(self, value) -> float:
        if self._number_of_steps is not None:
            step_size = (self._to - self._from_) / self._number_of_steps
            value = self._to - (round((self._to - value) / step_size) * step_size)
            return value
        else:
            return value

    def get(self) -> float:
        return self._output_value

    def set(self, output_value, from_variable_callback=False):
        if self._from_ < self._to:
            if output_value > self._to:
                output_value = self._to
            elif output_value < self._from_:
                output_value = self._from_
        else:
            if output_value < self._to:
                output_value = self._to
            elif output_value > self._from_:
                output_value = self._from_

        self._output_value = self._round_to_step_size(output_value)
        self._value = (self._output_value - self._from_) / (self._to - self._from_)

        self._draw(no_color_updates=False)

        if self._variable is not None and not from_variable_callback:
            self._variable_callback_blocked = True
            self._variable.set(round(self._output_value) if isinstance(self._variable, tkinter.IntVar) else self._output_value)
            self._variable_callback_blocked = False

    def _variable_callback(self, var_name, index, mode):
        if not self._variable_callback_blocked:
            self.set(self._variable.get(), from_variable_callback=True)

    def bind(self, sequence: str = None, command: Callable = None, add: Union[str, bool] = True):
        """ called on the tkinter.Canvas """
        if not (add == "+" or add is True):
            raise ValueError("'add' argument can only be '+' or True to preserve internal callbacks")
        self._canvas.bind(sequence, command, add=True)

    def unbind(self, sequence: str = None, funcid: str = None):
        """ called on the tkinter.Label and tkinter.Canvas """
        if funcid is not None:
            raise ValueError("'funcid' argument can only be None, because there is a bug in" +
                             " tkinter and its not clear whether the internal callbacks will be unbinded or not")
        self._canvas.unbind(sequence, None)
        self._create_bindings(sequence=sequence)  # restore internal callbacks for sequence

    def focus(self):
        return self._canvas.focus()

    def focus_set(self):
        return self._canvas.focus_set()

    def focus_force(self):
        return self._canvas.focus_force()
