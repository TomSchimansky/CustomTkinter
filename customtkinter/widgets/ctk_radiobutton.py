import tkinter
import sys
from typing import Union

from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..settings import Settings
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkRadioButton(CTkBaseClass):
    def __init__(self, *args,
                 bg_color=None,
                 fg_color="default_theme",
                 hover_color="default_theme",
                 border_color="default_theme",
                 border_width_unchecked="default_theme",
                 border_width_checked="default_theme",
                 width=22,
                 height=22,
                 corner_radius="default_theme",
                 text_font="default_theme",
                 text_color="default_theme",
                 text="CTkRadioButton",
                 text_color_disabled="default_theme",
                 hover=True,
                 command=None,
                 state=tkinter.NORMAL,
                 value=0,
                 variable=None,
                 textvariable=None,
                 **kwargs):

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=width, height=height, **kwargs)

        # color
        self.fg_color = ThemeManager.theme["color"]["button"] if fg_color == "default_theme" else fg_color
        self.hover_color = ThemeManager.theme["color"]["button_hover"] if hover_color == "default_theme" else hover_color
        self.border_color = ThemeManager.theme["color"]["checkbox_border"] if border_color == "default_theme" else border_color

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["radiobutton_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width_unchecked = ThemeManager.theme["shape"]["radiobutton_border_width_unchecked"] if border_width_unchecked == "default_theme" else border_width_unchecked
        self.border_width_checked = ThemeManager.theme["shape"]["radiobutton_border_width_checked"] if border_width_checked == "default_theme" else border_width_checked
        self.border_width = self.border_width_unchecked

        # text
        self.text = text
        self.text_label: Union[tkinter.Label, None] = None
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.text_color_disabled = ThemeManager.theme["color"]["text_disabled"] if text_color_disabled == "default_theme" else text_color_disabled
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font

        # callback and control variables
        self.command = command
        self.state = state
        self.hover = hover
        self.check_state = False
        self.value = value
        self.variable: tkinter.Variable = variable
        self.variable_callback_blocked = False
        self.textvariable = textvariable
        self.variable_callback_name = None

        # configure grid system (3x1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0, minsize=self.apply_widget_scaling(6))
        self.grid_columnconfigure(2, weight=1)

        self.bg_canvas = CTkCanvas(master=self,
                                   highlightthickness=0,
                                   width=self.apply_widget_scaling(self._current_width),
                                   height=self.apply_widget_scaling(self._current_height))
        self.bg_canvas.grid(row=0, column=0, padx=0, pady=0, columnspan=3, rowspan=1, sticky="nswe")

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(self._current_width),
                                height=self.apply_widget_scaling(self._current_height))
        self.canvas.grid(row=0, column=0, padx=0, pady=0, columnspan=1)
        self.draw_engine = DrawEngine(self.canvas)

        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.invoke)

        self.text_label = tkinter.Label(master=self,
                                        bd=0,
                                        text=self.text,
                                        justify=tkinter.LEFT,
                                        font=self.apply_font_scaling(self.text_font),
                                        textvariable=self.textvariable)
        self.text_label.grid(row=0, column=2, padx=0, pady=0, sticky="w")
        self.text_label["anchor"] = "w"

        self.text_label.bind("<Enter>", self.on_enter)
        self.text_label.bind("<Leave>", self.on_leave)
        self.text_label.bind("<Button-1>", self.invoke)

        if self.variable is not None:
            self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
            self.check_state = True if self.variable.get() == self.value else False

        self.draw()  # initial draw
        self.set_cursor()

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        self.grid_columnconfigure(1, weight=0, minsize=self.apply_widget_scaling(6))
        self.text_label.configure(font=self.apply_font_scaling(self.text_font))

        self.bg_canvas.configure(width=self.apply_widget_scaling(self._desired_width), height=self.apply_widget_scaling(self._desired_height))
        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width), height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def destroy(self):
        if self.variable is not None:
            self.variable.trace_remove("write", self.variable_callback_name)

        super().destroy()

    def draw(self, no_color_updates=False):
        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border(self.apply_widget_scaling(self._current_width),
                                                                             self.apply_widget_scaling(self._current_height),
                                                                             self.apply_widget_scaling(self.corner_radius),
                                                                             self.apply_widget_scaling(self.border_width))

        self.bg_canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))
        self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

        if self.check_state is False:
            self.canvas.itemconfig("border_parts",
                                   outline=ThemeManager.single_color(self.border_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.border_color, self._appearance_mode))
        else:
            self.canvas.itemconfig("border_parts",
                                   outline=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.fg_color, self._appearance_mode))

        self.canvas.itemconfig("inner_parts",
                               outline=ThemeManager.single_color(self.bg_color, self._appearance_mode),
                               fill=ThemeManager.single_color(self.bg_color, self._appearance_mode))

        if self.state == tkinter.DISABLED:
            self.text_label.configure(fg=ThemeManager.single_color(self.text_color_disabled, self._appearance_mode))
        else:
            self.text_label.configure(fg=ThemeManager.single_color(self.text_color, self._appearance_mode))

        self.text_label.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

    def configure(self, require_redraw=False, **kwargs):
        if "text" in kwargs:
            self.text = kwargs.pop("text")
            self.text_label.configure(text=self.text)

        if "state" in kwargs:
            self.state = kwargs.pop("state")
            self.set_cursor()
            require_redraw = True

        if "fg_color" in kwargs:
            self.fg_color = kwargs.pop("fg_color")
            require_redraw = True

        if "hover_color" in kwargs:
            self.hover_color = kwargs.pop("hover_color")
            require_redraw = True

        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")
            require_redraw = True

        if "border_color" in kwargs:
            self.border_color = kwargs.pop("border_color")
            require_redraw = True

        if "border_width" in kwargs:
            self.border_width = kwargs.pop("border_width")
            require_redraw = True

        if "command" in kwargs:
            self.command = kwargs.pop("command")

        if "textvariable" in kwargs:
            self.textvariable = kwargs.pop("textvariable")
            self.text_label.configure(textvariable=self.textvariable)

        if "variable" in kwargs:
            if self.variable is not None:
                self.variable.trace_remove("write", self.variable_callback_name)

            self.variable = kwargs.pop("variable")

            if self.variable is not None and self.variable != "":
                self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
                self.check_state = True if self.variable.get() == self.value else False
                require_redraw = True

        super().configure(require_redraw=require_redraw, **kwargs)

    def set_cursor(self):
        if Settings.cursor_manipulation_enabled:
            if self.state == tkinter.DISABLED:
                if sys.platform == "darwin" and Settings.cursor_manipulation_enabled:
                    self.canvas.configure(cursor="arrow")
                    if self.text_label is not None:
                        self.text_label.configure(cursor="arrow")
                elif sys.platform.startswith("win") and Settings.cursor_manipulation_enabled:
                    self.canvas.configure(cursor="arrow")
                    if self.text_label is not None:
                        self.text_label.configure(cursor="arrow")

            elif self.state == tkinter.NORMAL:
                if sys.platform == "darwin" and Settings.cursor_manipulation_enabled:
                    self.canvas.configure(cursor="pointinghand")
                    if self.text_label is not None:
                        self.text_label.configure(cursor="pointinghand")
                elif sys.platform.startswith("win") and Settings.cursor_manipulation_enabled:
                    self.canvas.configure(cursor="hand2")
                    if self.text_label is not None:
                        self.text_label.configure(cursor="hand2")

    def on_enter(self, event=0):
        if self.hover is True and self.state == tkinter.NORMAL:
            self.canvas.itemconfig("border_parts",
                                   fill=ThemeManager.single_color(self.hover_color, self._appearance_mode),
                                   outline=ThemeManager.single_color(self.hover_color, self._appearance_mode))

    def on_leave(self, event=0):
        if self.hover is True:
            if self.check_state is True:
                self.canvas.itemconfig("border_parts",
                                       fill=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.fg_color, self._appearance_mode))
            else:
                self.canvas.itemconfig("border_parts",
                                       fill=ThemeManager.single_color(self.border_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.border_color, self._appearance_mode))

    def variable_callback(self, var_name, index, mode):
        if not self.variable_callback_blocked:
            if self.variable.get() == self.value:
                self.select(from_variable_callback=True)
            else:
                self.deselect(from_variable_callback=True)

    def invoke(self, event=0):
        if self.state == tkinter.NORMAL:
            if self.check_state is False:
                self.check_state = True
                self.select()

        if self.command is not None:
            self.command()

    def select(self, from_variable_callback=False):
        self.check_state = True
        self.border_width = self.border_width_checked
        self.draw()

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(self.value)
            self.variable_callback_blocked = False

    def deselect(self, from_variable_callback=False):
        self.check_state = False
        self.border_width = self.border_width_unchecked
        self.draw()

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set("")
            self.variable_callback_blocked = False
