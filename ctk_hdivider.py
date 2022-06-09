from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkHorizontalDivider(CTkBaseClass):
    def __init__(self, *args,
                 bg_color=None,
                 fg_color="default_theme",
                 length=160,
                 thickness=8,
                 overwrite_preferred_drawing_method: str = None,
                 **kwargs):

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=length, height=thickness, **kwargs)

        # determine fg_color
        if fg_color == "default_theme":
            if isinstance(self.master, CTkHorizontalDivider):
                if self.master.fg_color == ThemeManager.theme["color"]["frame_low"]:
                    self.fg_color = ThemeManager.theme["color"]["frame_high"]
                else:
                    self.fg_color = ThemeManager.theme["color"]["frame_low"]
            else:
                self.fg_color = ThemeManager.theme["color"]["frame_low"]
        else:
            self.fg_color = fg_color

        # shape
        self.corner_radius = corner_radius = thickness / 2

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(self._current_width),
                                height=self.apply_widget_scaling(self._current_height))
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))
        self.draw_engine = DrawEngine(self.canvas)
        self._overwrite_preferred_drawing_method = overwrite_preferred_drawing_method

        self.bind('<Configure>', self.update_dimensions_event)

        self.draw()


    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width),
                              height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def set_dimensions(self, width=None, height=None):
        super().set_dimensions(width, height)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width),
                              height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def draw(self, no_color_updates=False):

        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border(
            self.apply_widget_scaling(self._current_width),
            self.apply_widget_scaling(self._current_height),
            self.apply_widget_scaling(self.corner_radius),
            self.apply_widget_scaling(0),
            overwrite_preferred_drawing_method=self._overwrite_preferred_drawing_method)

        if no_color_updates is False or requires_recoloring:
            if self.fg_color is None:
                self.canvas.itemconfig("inner_parts",
                                       fill=ThemeManager.single_color(self.bg_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.bg_color, self._appearance_mode))
            else:
                self.canvas.itemconfig("inner_parts",
                                       fill=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.fg_color, self._appearance_mode))

            self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

        self.canvas.tag_lower("inner_parts")
        self.canvas.tag_lower("border_parts")

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

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

        if "length" in kwargs:
            self.set_dimensions(width=kwargs["length"])
            del kwargs["length"]

        if "thickness" in kwargs:
            self.set_dimensions(height=kwargs["thickness"])
            del kwargs["thickness"]

        super().configure(*args, **kwargs)

        if require_redraw:
            self.draw()
