import tkinter
import sys
from typing import Union, Tuple, Callable

from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..settings import Settings
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkSwitch(CTkBaseClass):
    """
    Switch with rounded corners, border, label, command, variable support.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 master: any = None,
                 width: int = 100,
                 height: int = 24,
                 switch_width: int = 36,
                 switch_height: int = 18,
                 corner_radius: Union[int, str] = "default_theme",
                 border_width: Union[int, str] = "default_theme",
                 button_length: Union[int, str] = "default_theme",

                 bg_color: Union[str, Tuple[str, str], None] = None,
                 fg_color: Union[str, Tuple[str, str]] = "default_theme",
                 border_color: Union[str, Tuple[str, str], None] = None,
                 progress_color: Union[str, Tuple[str, str]] = "default_theme",
                 button_color: Union[str, Tuple[str, str]] = "default_theme",
                 button_hover_color: Union[str, Tuple[str, str]] = "default_theme",
                 text_color: Union[str, Tuple[str, str]] = "default_theme",
                 text_color_disabled: Union[str, Tuple[str, str]] = "default_theme",

                 text: str = "CTkSwitch",
                 font: any = "default_theme",
                 textvariable: tkinter.Variable = None,
                 onvalue: Union[int, str] = 1,
                 offvalue: Union[int, str] = 0,
                 variable: tkinter.Variable = None,
                 command: Callable = None,
                 state: str = tkinter.NORMAL,
                 **kwargs):

        # transfer basic functionality (_bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

        # dimensions
        self._switch_width = switch_width
        self._switch_height = switch_height

        # color
        self._border_color = border_color
        self._fg_color = ThemeManager.theme["color"]["switch"] if fg_color == "default_theme" else fg_color
        self._progress_color = ThemeManager.theme["color"]["switch_progress"] if progress_color == "default_theme" else progress_color
        self._button_color = ThemeManager.theme["color"]["switch_button"] if button_color == "default_theme" else button_color
        self._button_hover_color = ThemeManager.theme["color"]["switch_button_hover"] if button_hover_color == "default_theme" else button_hover_color
        self._text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self._text_color_disabled = ThemeManager.theme["color"]["text_disabled"] if text_color_disabled == "default_theme" else text_color_disabled

        # text
        self._text = text
        self._text_label = None
        self._font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if font == "default_theme" else font

        # shape
        self._corner_radius = ThemeManager.theme["shape"]["switch_corner_radius"] if corner_radius == "default_theme" else corner_radius
        # self.button_corner_radius = ThemeManager.theme["shape"]["switch_button_corner_radius"] if button_corner_radius == "default_theme" else button_corner_radius
        self._border_width = ThemeManager.theme["shape"]["switch_border_width"] if border_width == "default_theme" else border_width
        self._button_length = ThemeManager.theme["shape"]["switch_button_length"] if button_length == "default_theme" else button_length
        self._hover_state: bool = False
        self._check_state: bool = False  # True if switch is activated
        self._state = state
        self._onvalue = onvalue
        self._offvalue = offvalue

        # callback and control variables
        self._command = command
        self._variable: tkinter.Variable = variable
        self._variable_callback_blocked = False
        self._variable_callback_name = None
        self._textvariable = textvariable

        # configure grid system (3x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=self._apply_widget_scaling(6))
        self.grid_columnconfigure(2, weight=0)

        self._bg_canvas = CTkCanvas(master=self,
                                    highlightthickness=0,
                                    width=self._apply_widget_scaling(self._current_width),
                                    height=self._apply_widget_scaling(self._current_height))
        self._bg_canvas.grid(row=0, column=0, columnspan=3, sticky="nswe")

        self._canvas = CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._switch_width),
                                 height=self._apply_widget_scaling(self._switch_height))
        self._canvas.grid(row=0, column=0, sticky="nswe")
        self._draw_engine = DrawEngine(self._canvas)

        self._canvas.bind("<Enter>", self._on_enter)
        self._canvas.bind("<Leave>", self._on_leave)
        self._canvas.bind("<Button-1>", self.toggle)

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

        self._text_label.bind("<Enter>", self._on_enter)
        self._text_label.bind("<Leave>", self._on_leave)
        self._text_label.bind("<Button-1>", self.toggle)

        if self._variable is not None and self._variable != "":
            self._variable_callback_name = self._variable.trace_add("write", self._variable_callback)
            self.c_heck_state = True if self._variable.get() == self._onvalue else False

        self._draw()  # initial draw
        self._set_cursor()

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        self.grid_columnconfigure(1, weight=0, minsize=self._apply_widget_scaling(6))
        self._text_label.configure(font=self._apply_font_scaling(self._font))

        self._bg_canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                                  height=self._apply_widget_scaling(self._desired_height))
        self._canvas.configure(width=self._apply_widget_scaling(self._switch_width),
                               height=self._apply_widget_scaling(self._switch_height))
        self._draw()

    def _set_dimensions(self, width: int = None, height: int = None):
        super()._set_dimensions(width, height)

        self._bg_canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                                  height=self._apply_widget_scaling(self._desired_height))

    def destroy(self):
        # remove variable_callback from variable callbacks if variable exists
        if self._variable is not None:
            self._variable.trace_remove("write", self._variable_callback_name)

        super().destroy()

    def _set_cursor(self):
        if Settings.cursor_manipulation_enabled:
            if self._state == tkinter.DISABLED:
                if sys.platform == "darwin" and Settings.cursor_manipulation_enabled:
                    self._canvas.configure(cursor="arrow")
                    if self._text_label is not None:
                        self._text_label.configure(cursor="arrow")
                elif sys.platform.startswith("win") and Settings.cursor_manipulation_enabled:
                    self._canvas.configure(cursor="arrow")
                    if self._text_label is not None:
                        self._text_label.configure(cursor="arrow")

            elif self._state == tkinter.NORMAL:
                if sys.platform == "darwin" and Settings.cursor_manipulation_enabled:
                    self._canvas.configure(cursor="pointinghand")
                    if self._text_label is not None:
                        self._text_label.configure(cursor="pointinghand")
                elif sys.platform.startswith("win") and Settings.cursor_manipulation_enabled:
                    self._canvas.configure(cursor="hand2")
                    if self._text_label is not None:
                        self._text_label.configure(cursor="hand2")

    def _draw(self, no_color_updates=False):

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
            self._bg_canvas.configure(bg=ThemeManager.single_color(self._bg_color, self._appearance_mode))
            self._canvas.configure(bg=ThemeManager.single_color(self._bg_color, self._appearance_mode))

            if self._border_color is None:
                self._canvas.itemconfig("border_parts", fill=ThemeManager.single_color(self._bg_color, self._appearance_mode),
                                        outline=ThemeManager.single_color(self._bg_color, self._appearance_mode))
            else:
                self._canvas.itemconfig("border_parts", fill=ThemeManager.single_color(self._border_color, self._appearance_mode),
                                        outline=ThemeManager.single_color(self._border_color, self._appearance_mode))

            self._canvas.itemconfig("inner_parts", fill=ThemeManager.single_color(self._fg_color, self._appearance_mode),
                                    outline=ThemeManager.single_color(self._fg_color, self._appearance_mode))

            if self._progress_color is None:
                self._canvas.itemconfig("progress_parts", fill=ThemeManager.single_color(self._fg_color, self._appearance_mode),
                                        outline=ThemeManager.single_color(self._fg_color, self._appearance_mode))
            else:
                self._canvas.itemconfig("progress_parts", fill=ThemeManager.single_color(self._progress_color, self._appearance_mode),
                                        outline=ThemeManager.single_color(self._progress_color, self._appearance_mode))

            self._canvas.itemconfig("slider_parts", fill=ThemeManager.single_color(self._button_color, self._appearance_mode),
                                    outline=ThemeManager.single_color(self._button_color, self._appearance_mode))

            if self._state == tkinter.DISABLED:
                self._text_label.configure(fg=(ThemeManager.single_color(self._text_color_disabled, self._appearance_mode)))
            else:
                self._text_label.configure(fg=ThemeManager.single_color(self._text_color, self._appearance_mode))

            self._text_label.configure(bg=ThemeManager.single_color(self._bg_color, self._appearance_mode))

    def configure(self, require_redraw=False, **kwargs):
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
            self._font = kwargs.pop("font")
            self._text_label.configure(font=self._apply_font_scaling(self._font))

        if "state" in kwargs:
            self._state = kwargs.pop("state")
            self._set_cursor()
            require_redraw = True

        if "fg_color" in kwargs:
            self._fg_color = kwargs.pop("fg_color")
            require_redraw = True

        if "progress_color" in kwargs:
            new_progress_color = kwargs.pop("progress_color")
            if new_progress_color is None:
                self._progress_color = self._fg_color
            else:
                self._progress_color = new_progress_color
            require_redraw = True

        if "button_color" in kwargs:
            self._button_color = kwargs.pop("button_color")
            require_redraw = True

        if "button_hover_color" in kwargs:
            self._button_hover_color = kwargs.pop("button_hover_color")
            require_redraw = True

        if "border_color" in kwargs:
            self._border_color = kwargs.pop("border_color")
            require_redraw = True

        if "border_width" in kwargs:
            self._border_width = kwargs.pop("border_width")
            require_redraw = True

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
        self._hover_state = True

        if self._state is not tkinter.DISABLED:
            self._canvas.itemconfig("slider_parts",
                                    fill=ThemeManager.single_color(self._button_hover_color, self._appearance_mode),
                                    outline=ThemeManager.single_color(self._button_hover_color, self._appearance_mode))

    def _on_leave(self, event=0):
        self._hover_state = False
        self._canvas.itemconfig("slider_parts",
                                fill=ThemeManager.single_color(self._button_color, self._appearance_mode),
                                outline=ThemeManager.single_color(self._button_color, self._appearance_mode))

    def _variable_callback(self, var_name, index, mode):
        if not self._variable_callback_blocked:
            if self._variable.get() == self._onvalue:
                self.select(from_variable_callback=True)
            elif self._variable.get() == self._offvalue:
                self.deselect(from_variable_callback=True)

    def bind(self, sequence=None, command=None, add=None):
        """ called on the tkinter.Canvas """
        return self._canvas.bind(sequence, command, add)

    def unbind(self, sequence, funcid=None):
        """ called on the tkinter.Canvas """
        return self._canvas.unbind(sequence, funcid)

    def focus(self):
        return self._text_label.focus()

    def focus_set(self):
        return self._text_label.focus_set()

    def focus_force(self):
        return self._text_label.focus_force()
