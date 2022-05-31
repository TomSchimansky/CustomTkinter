import tkinter

from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkProgressBar(CTkBaseClass):
    """ tkinter custom progressbar, values from 0 to 1 """

    def __init__(self, *args,
                 variable=None,
                 bg_color=None,
                 border_color="default_theme",
                 fg_color="default_theme",
                 progress_color="default_theme",
                 corner_radius="default_theme",
                 width=None,
                 height=None,
                 border_width="default_theme",
                 orient="horizontal",
                 **kwargs):

        # set default dimensions according to orientation
        if width is None:
            if orient.lower() == "vertical":
                width = 8
            else:
                width = 200
        if height is None:
            if orient.lower() == "vertical":
                height = 200
            else:
                height = 8

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=width, height=height, **kwargs)

        # color
        self.border_color = ThemeManager.theme["color"]["progressbar_border"] if border_color == "default_theme" else border_color
        self.fg_color = ThemeManager.theme["color"]["progressbar"] if fg_color == "default_theme" else fg_color
        self.progress_color = ThemeManager.theme["color"]["progressbar_progress"] if progress_color == "default_theme" else progress_color

        # control variable
        self.variable = variable
        self.variable_callback_blocked = False
        self.variable_callback_name = None

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["progressbar_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = ThemeManager.theme["shape"]["progressbar_border_width"] if border_width == "default_theme" else border_width
        self.value = 0.5
        self.orient = orient

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(self._desired_width),
                                height=self.apply_widget_scaling(self._desired_height))
        self.canvas.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nswe")
        self.draw_engine = DrawEngine(self.canvas)

        # Each time an item is resized due to pack position mode, the binding Configure is called on the widget
        self.bind('<Configure>', self.update_dimensions_event)

        self.draw()  # initial draw

        if self.variable is not None:
            self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
            self.variable_callback_blocked = True
            self.set(self.variable.get(), from_variable_callback=True)
            self.variable_callback_blocked = False

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width), height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def set_dimensions(self, width=None, height=None):
        super().set_dimensions(width, height)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width),
                              height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def destroy(self):
        if self.variable is not None:
            self.variable.trace_remove("write", self.variable_callback_name)

        super().destroy()

    def draw(self, no_color_updates=False):
        if self.orient.lower() == "horizontal":
            orientation = "w"
        elif self.orient.lower() == "vertical":
            orientation = "s"
        else:
            orientation = "w"

        requires_recoloring = self.draw_engine.draw_rounded_progress_bar_with_border(self.apply_widget_scaling(self._current_width),
                                                                                     self.apply_widget_scaling(self._current_height),
                                                                                     self.apply_widget_scaling(self.corner_radius),
                                                                                     self.apply_widget_scaling(self.border_width),
                                                                                     self.value,
                                                                                     orientation)

        if no_color_updates is False or requires_recoloring:
            self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))
            self.canvas.itemconfig("border_parts",
                                   fill=ThemeManager.single_color(self.border_color, self._appearance_mode),
                                   outline=ThemeManager.single_color(self.border_color, self._appearance_mode))
            self.canvas.itemconfig("inner_parts",
                                   fill=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                   outline=ThemeManager.single_color(self.fg_color, self._appearance_mode))
            self.canvas.itemconfig("progress_parts",
                                   fill=ThemeManager.single_color(self.progress_color, self._appearance_mode),
                                   outline=ThemeManager.single_color(self.progress_color, self._appearance_mode))

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "bg_color" in kwargs:
            if kwargs["bg_color"] is None:
                self.bg_color = self.detect_color_of_master()
            else:
                self.bg_color = kwargs["bg_color"]
            require_redraw = True
            del kwargs["bg_color"]

        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            del kwargs["fg_color"]
            require_redraw = True

        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
            del kwargs["border_color"]
            require_redraw = True

        if "progress_color" in kwargs:
            self.progress_color = kwargs["progress_color"]
            del kwargs["progress_color"]
            require_redraw = True

        if "border_width" in kwargs:
            self.border_width = kwargs["border_width"]
            del kwargs["border_width"]
            require_redraw = True

        if "variable" in kwargs:
            if self.variable is not None:
                self.variable.trace_remove("write", self.variable_callback_name)

            self.variable = kwargs["variable"]

            if self.variable is not None and self.variable != "":
                self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
                self.set(self.variable.get(), from_variable_callback=True)
            else:
                self.variable = None

            del kwargs["variable"]

        if "width" in kwargs:
            self.set_dimensions(width=kwargs["width"])
            del kwargs["width"]

        if "height" in kwargs:
            self.set_dimensions(height=kwargs["height"])
            del kwargs["height"]

        super().configure(*args, **kwargs)

        if require_redraw is True:
            self.draw()

    def variable_callback(self, var_name, index, mode):
        if not self.variable_callback_blocked:
            self.set(self.variable.get(), from_variable_callback=True)

    def set(self, value, from_variable_callback=False):
        self.value = value

        if self.value > 1:
            self.value = 1
        elif self.value < 0:
            self.value = 0

        self.draw(no_color_updates=True)

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(round(self.value) if isinstance(self.variable, tkinter.IntVar) else self.value)
            self.variable_callback_blocked = False
