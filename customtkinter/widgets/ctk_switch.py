import tkinter
import sys

from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..settings import Settings
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkSwitch(CTkBaseClass):
    def __init__(self, *args,
                 text="CTkSwitch",
                 text_font="default_theme",
                 text_color="default_theme",
                 text_color_disabled="default_theme",
                 bg_color=None,
                 border_color=None,
                 fg_color="default_theme",
                 progress_color="default_theme",
                 button_color="default_theme",
                 button_hover_color="default_theme",
                 width=36,
                 height=18,
                 corner_radius="default_theme",
                 # button_corner_radius="default_theme",
                 border_width="default_theme",
                 button_length="default_theme",
                 command=None,
                 onvalue=1,
                 offvalue=0,
                 variable=None,
                 textvariable=None,
                 state=tkinter.NORMAL,
                 **kwargs):

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=width, height=height, **kwargs)

        # color
        self.border_color = border_color
        self.fg_color = ThemeManager.theme["color"]["switch"] if fg_color == "default_theme" else fg_color
        self.progress_color = ThemeManager.theme["color"]["switch_progress"] if progress_color == "default_theme" else progress_color
        self.button_color = ThemeManager.theme["color"]["switch_button"] if button_color == "default_theme" else button_color
        self.button_hover_color = ThemeManager.theme["color"]["switch_button_hover"] if button_hover_color == "default_theme" else button_hover_color
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.text_color_disabled = ThemeManager.theme["color"]["text_button_disabled"] if text_color_disabled == "default_theme" else text_color_disabled

        # text
        self.text = text
        self.text_label = None
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["switch_corner_radius"] if corner_radius == "default_theme" else corner_radius
        # self.button_corner_radius = ThemeManager.theme["shape"]["switch_button_corner_radius"] if button_corner_radius == "default_theme" else button_corner_radius
        self.border_width = ThemeManager.theme["shape"]["switch_border_width"] if border_width == "default_theme" else border_width
        self.button_length = ThemeManager.theme["shape"]["switch_button_length"] if button_length == "default_theme" else button_length
        self.hover_state = False
        self.check_state = False  # True if switch is activated
        self.state = state
        self.onvalue = onvalue
        self.offvalue = offvalue

        # if self.corner_radius < self.button_corner_radius:
        #     self.corner_radius = self.button_corner_radius

        # callback and control variables
        self.callback_function = command
        self.variable: tkinter.Variable = variable
        self.variable_callback_blocked = False
        self.variable_callback_name = None
        self.textvariable = textvariable

        # configure grid system (3x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=self.apply_widget_scaling(6))
        self.grid_columnconfigure(2, weight=0)

        self.bg_canvas = CTkCanvas(master=self,
                                   highlightthickness=0,
                                   width=self.apply_widget_scaling(self._current_width),
                                   height=self.apply_widget_scaling(self._current_height))
        self.bg_canvas.grid(row=0, column=0, padx=0, pady=0, columnspan=3, rowspan=1, sticky="nswe")

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(self._current_width),
                                height=self.apply_widget_scaling(self._current_height))
        self.canvas.grid(row=0, column=0, padx=0, pady=0, columnspan=1, sticky="nswe")
        self.draw_engine = DrawEngine(self.canvas)

        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.toggle)

        self.draw()  # initial draw
        self.set_cursor()

        if self.variable is not None:
            self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
            if self.variable.get() == self.onvalue:
                self.select(from_variable_callback=True)
            elif self.variable.get() == self.offvalue:
                self.deselect(from_variable_callback=True)

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        self.grid_columnconfigure(1, weight=0, minsize=self.apply_widget_scaling(6))
        self.text_label.configure(font=self.apply_font_scaling(self.text_font))

        self.bg_canvas.configure(width=self.apply_widget_scaling(self._desired_width), height=self.apply_widget_scaling(self._desired_height))
        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width), height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def destroy(self):
        # remove variable_callback from variable callbacks if variable exists
        if self.variable is not None:
            self.variable.trace_remove("write", self.variable_callback_name)

        super().destroy()

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

    def draw(self, no_color_updates=False):

        if self.check_state is True:
            requires_recoloring = self.draw_engine.draw_rounded_slider_with_border_and_button(self.apply_widget_scaling(self._current_width),
                                                                                              self.apply_widget_scaling(self._current_height),
                                                                                              self.apply_widget_scaling(self.corner_radius),
                                                                                              self.apply_widget_scaling(self.border_width),
                                                                                              self.apply_widget_scaling(self.button_length),
                                                                                              self.apply_widget_scaling(self.corner_radius),
                                                                                              1, "w")
        else:
            requires_recoloring = self.draw_engine.draw_rounded_slider_with_border_and_button(self.apply_widget_scaling(self._current_width),
                                                                                              self.apply_widget_scaling(self._current_height),
                                                                                              self.apply_widget_scaling(self.corner_radius),
                                                                                              self.apply_widget_scaling(self.border_width),
                                                                                              self.apply_widget_scaling(self.button_length),
                                                                                              self.apply_widget_scaling(self.corner_radius),
                                                                                              0, "w")

        if no_color_updates is False or requires_recoloring:
            self.bg_canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))
            self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

            if self.border_color is None:
                self.canvas.itemconfig("border_parts", fill=ThemeManager.single_color(self.bg_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.bg_color, self._appearance_mode))
            else:
                self.canvas.itemconfig("border_parts", fill=ThemeManager.single_color(self.border_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.border_color, self._appearance_mode))

            self.canvas.itemconfig("inner_parts", fill=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                   outline=ThemeManager.single_color(self.fg_color, self._appearance_mode))

            if self.progress_color is None:
                self.canvas.itemconfig("progress_parts", fill=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.fg_color, self._appearance_mode))
            else:
                self.canvas.itemconfig("progress_parts", fill=ThemeManager.single_color(self.progress_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.progress_color, self._appearance_mode))

            self.canvas.itemconfig("slider_parts", fill=ThemeManager.single_color(self.button_color, self._appearance_mode),
                                   outline=ThemeManager.single_color(self.button_color, self._appearance_mode))

        if self.text_label is None:
            self.text_label = tkinter.Label(master=self,
                                            bd=0,
                                            text=self.text,
                                            justify=tkinter.LEFT,
                                            font=self.apply_font_scaling(self.text_font))
            self.text_label.grid(row=0, column=2, padx=0, pady=0, sticky="w")
            self.text_label["anchor"] = "w"

            self.text_label.bind("<Enter>", self.on_enter)
            self.text_label.bind("<Leave>", self.on_leave)
            self.text_label.bind("<Button-1>", self.toggle)

            if self.textvariable is not None:
                self.text_label.configure(textvariable=self.textvariable)

        if self.state == tkinter.DISABLED:
            self.text_label.configure(fg=(ThemeManager.single_color(self.text_color_disabled, self._appearance_mode)))
        else:
            self.text_label.configure(fg=ThemeManager.single_color(self.text_color, self._appearance_mode))

        self.text_label.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

        self.set_text(self.text)

    def set_text(self, text):
        self.text = text
        if self.text_label is not None:
            self.text_label.configure(text=self.text)

    def toggle(self, event=None):
        if self.state is not tkinter.DISABLED:
            if self.check_state is True:
                self.check_state = False
            else:
                self.check_state = True

            self.draw(no_color_updates=True)

            if self.callback_function is not None:
                self.callback_function()

            if self.variable is not None:
                self.variable_callback_blocked = True
                self.variable.set(self.onvalue if self.check_state is True else self.offvalue)
                self.variable_callback_blocked = False

    def select(self, from_variable_callback=False):
        if self.state is not tkinter.DISABLED or from_variable_callback:
            self.check_state = True

            self.draw(no_color_updates=True)

            if self.variable is not None and not from_variable_callback:
                self.variable_callback_blocked = True
                self.variable.set(self.onvalue)
                self.variable_callback_blocked = False

            if self.callback_function is not None:
                self.callback_function()

    def deselect(self, from_variable_callback=False):
        if self.state is not tkinter.DISABLED or from_variable_callback:
            self.check_state = False

            self.draw(no_color_updates=True)

            if self.variable is not None and not from_variable_callback:
                self.variable_callback_blocked = True
                self.variable.set(self.offvalue)
                self.variable_callback_blocked = False

            if self.callback_function is not None:
                self.callback_function()

    def get(self):
        return self.onvalue if self.check_state is True else self.offvalue

    def on_enter(self, event=0):
        self.hover_state = True

        if self.state is not tkinter.DISABLED:
            self.canvas.itemconfig("slider_parts", fill=ThemeManager.single_color(self.button_hover_color, self._appearance_mode),
                                   outline=ThemeManager.single_color(self.button_hover_color, self._appearance_mode))

    def on_leave(self, event=0):
        self.hover_state = False
        self.canvas.itemconfig("slider_parts", fill=ThemeManager.single_color(self.button_color, self._appearance_mode),
                               outline=ThemeManager.single_color(self.button_color, self._appearance_mode))

    def variable_callback(self, var_name, index, mode):
        if not self.variable_callback_blocked:
            if self.variable.get() == self.onvalue:
                self.select(from_variable_callback=True)
            elif self.variable.get() == self.offvalue:
                self.deselect(from_variable_callback=True)

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "state" in kwargs:
            self.state = kwargs["state"]
            self.set_cursor()
            require_redraw = True
            del kwargs["state"]

        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            require_redraw = True
            del kwargs["fg_color"]

        if "bg_color" in kwargs:
            if kwargs["bg_color"] is None:
                self.bg_color = self.detect_color_of_master()
            else:
                self.bg_color = kwargs["bg_color"]
            require_redraw = True
            del kwargs["bg_color"]

        if "progress_color" in kwargs:
            if kwargs["progress_color"] is None:
                self.progress_color = self.fg_color
            else:
                self.progress_color = kwargs["progress_color"]
            require_redraw = True
            del kwargs["progress_color"]

        if "button_color" in kwargs:
            self.button_color = kwargs["button_color"]
            require_redraw = True
            del kwargs["button_color"]

        if "button_hover_color" in kwargs:
            self.button_hover_color = kwargs["button_hover_color"]
            require_redraw = True
            del kwargs["button_hover_color"]

        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
            require_redraw = True
            del kwargs["border_color"]

        if "border_width" in kwargs:
            self.border_width = kwargs["border_width"]
            require_redraw = True
            del kwargs["border_width"]

        if "command" in kwargs:
            self.callback_function = kwargs["command"]
            del kwargs["command"]

        if "textvariable" in kwargs:
            self.text_label.configure(textvariable=kwargs["textvariable"])
            del kwargs["textvariable"]

        if "variable" in kwargs:
            if self.variable is not None:
                self.variable.trace_remove("write", self.variable_callback_name)

            self.variable = kwargs["variable"]

            if self.variable is not None and self.variable != "":
                self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
                if self.variable.get() == self.onvalue:
                    self.select(from_variable_callback=True)
                elif self.variable.get() == self.offvalue:
                    self.deselect(from_variable_callback=True)
            else:
                self.variable = None

            del kwargs["variable"]

        super().configure(*args, **kwargs)

        if require_redraw:
            self.draw()
