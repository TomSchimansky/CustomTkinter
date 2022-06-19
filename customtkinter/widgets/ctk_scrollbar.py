from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkScrollbar(CTkBaseClass):
    def __init__(self, *args,
                 bg_color=None,
                 fg_color=None,
                 scrollbar_color="default_theme",
                 scrollbar_hover_color="default_theme",
                 border_spacing="default_theme",
                 corner_radius="default_theme",
                 width=None,
                 height=None,
                 orientation="vertical",
                 command=None,
                 hover=True,
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

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=width, height=height, **kwargs)

        # color
        self.fg_color = fg_color
        self.scrollbar_color = ThemeManager.theme["color"]["scrollbar"] if scrollbar_color == "default_theme" else scrollbar_color
        self.scrollbar_hover_color = ThemeManager.theme["color"]["scrollbar_hover"] if scrollbar_hover_color == "default_theme" else scrollbar_hover_color

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["scrollbar_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_spacing = ThemeManager.theme["shape"]["scrollbar_border_spacing"] if border_spacing == "default_theme" else border_spacing

        self.hover = hover
        self.hover_state = False
        self.command = command
        self.orientation = orientation
        self.start_value: float = 0  # 0 to 1
        self.end_value: float = 1  # 0 to 1

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(self._current_width),
                                height=self.apply_widget_scaling(self._current_height))
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.canvas.configure(bg="green")
        self.draw_engine = DrawEngine(self.canvas)

        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.tag_bind("border_parts", "<Button-1>", self.clicked)
        self.canvas.bind("<B1-Motion>", self.clicked)
        self.canvas.bind("<MouseWheel>", self.mouse_scroll_event)
        self.bind('<Configure>', self.update_dimensions_event)

        self.draw()

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width), height=self.apply_widget_scaling(self._desired_height))
        self.draw(no_color_updates=True)

    def set_dimensions(self, width=None, height=None):
        super().set_dimensions(width, height)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width),
                              height=self.apply_widget_scaling(self._desired_height))
        self.draw(no_color_updates=True)

    def draw(self, no_color_updates=False):
        requires_recoloring = self.draw_engine.draw_rounded_scrollbar(self.apply_widget_scaling(self._current_width),
                                                                      self.apply_widget_scaling(self._current_height),
                                                                      self.apply_widget_scaling(self.corner_radius),
                                                                      self.apply_widget_scaling(self.border_spacing),
                                                                      self.start_value, self.end_value,
                                                                      self.orientation)

        if no_color_updates is False or requires_recoloring:
            if self.hover_state is True:
                self.canvas.itemconfig("scrollbar_parts",
                                       fill=ThemeManager.single_color(self.scrollbar_hover_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.scrollbar_hover_color, self._appearance_mode))
            else:
                self.canvas.itemconfig("scrollbar_parts",
                                       fill=ThemeManager.single_color(self.scrollbar_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.scrollbar_color, self._appearance_mode))

            if self.fg_color is None:
                self.canvas.itemconfig("border_parts",
                                       fill=ThemeManager.single_color(self.bg_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.bg_color, self._appearance_mode))
            else:
                self.canvas.itemconfig("border_parts",
                                       fill=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.fg_color, self._appearance_mode))

    def set(self, start_value: float, end_value: float):
        self.start_value = float(start_value)
        self.end_value = float(end_value)
        self.scrollbar_height = self.end_value - self.start_value
        self.draw()

    def get(self):
        return self.start_value, self.end_value

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
            require_redraw = True
            del kwargs["fg_color"]

        if "scrollbar_color" in kwargs:
            self.scrollbar_color = kwargs["scrollbar_color"]
            require_redraw = True
            del kwargs["scrollbar_color"]

        if "scrollbar_hover_color" in kwargs:
            self.scrollbar_hover_color = kwargs["scrollbar_hover_color"]
            require_redraw = True
            del kwargs["scrollbar_hover_color"]

        if "command" in kwargs:
            self.command = kwargs["command"]
            del kwargs["command"]

        if "corner_radius" in kwargs:
            self.corner_radius = kwargs["corner_radius"]
            require_redraw = True
            del kwargs["corner_radius"]

        if "border_spacing" in kwargs:
            self.border_spacing = kwargs["border_spacing"]
            require_redraw = True
            del kwargs["border_spacing"]

        if "width" in kwargs:
            self.set_dimensions(width=kwargs["width"])
            del kwargs["width"]

        if "height" in kwargs:
            self.set_dimensions(height=kwargs["height"])
            del kwargs["height"]

        super().configure(*args, **kwargs)

        if require_redraw:
            self.draw()

    def on_enter(self, event=0):
        if self.hover is True:
            self.hover_state = True
            self.canvas.itemconfig("scrollbar_parts",
                                   outline=ThemeManager.single_color(self.scrollbar_hover_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.scrollbar_hover_color, self._appearance_mode))

    def on_leave(self, event=0):
        self.hover_state = False
        self.canvas.itemconfig("scrollbar_parts",
                               outline=ThemeManager.single_color(self.scrollbar_color, self._appearance_mode),
                               fill=ThemeManager.single_color(self.scrollbar_color, self._appearance_mode))

    def clicked(self, event):
        if self.orientation == "vertical":
            value = ((event.y - self.border_spacing) / (self._current_height - 2 * self.border_spacing)) / self._widget_scaling
            current_scrollbar_length = self.end_value - self.start_value
            value = max(current_scrollbar_length / 2, min(value, 1 - (current_scrollbar_length / 2)))
            self.start_value = value - (current_scrollbar_length / 2)
            self.end_value = value + (current_scrollbar_length / 2)
            self.draw()

            if self.command is not None:
                self.command('moveto', self.start_value)

    def mouse_scroll_event(self, event=None):
        if self.command is not None:
            self.command('scroll', event.delta, 'units')

