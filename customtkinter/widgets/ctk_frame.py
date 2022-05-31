from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkFrame(CTkBaseClass):
    def __init__(self, *args,
                 bg_color=None,
                 fg_color="default_theme",
                 border_color="default_theme",
                 border_width="default_theme",
                 corner_radius="default_theme",
                 width=200,
                 height=200,
                 overwrite_preferred_drawing_method: str = None,
                 **kwargs):

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=width, height=height, **kwargs)

        # color
        self.border_color = ThemeManager.theme["color"]["frame_border"] if border_color == "default_theme" else border_color

        # determine fg_color of frame
        if fg_color == "default_theme":
            if isinstance(self.master, CTkFrame):
                if self.master.fg_color == ThemeManager.theme["color"]["frame_low"]:
                    self.fg_color = ThemeManager.theme["color"]["frame_high"]
                else:
                    self.fg_color = ThemeManager.theme["color"]["frame_low"]
            else:
                self.fg_color = ThemeManager.theme["color"]["frame_low"]
        else:
            self.fg_color = fg_color

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["frame_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = ThemeManager.theme["shape"]["frame_border_width"] if border_width == "default_theme" else border_width

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

    def winfo_children(self):
        """ winfo_children of CTkFrame without self.canvas widget,
        because it's not a child but part of the CTkFrame itself """

        child_widgets = super().winfo_children()
        try:
            child_widgets.remove(self.canvas)
            return child_widgets
        except ValueError:
            return child_widgets

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width), height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def set_dimensions(self, width=None, height=None):
        super().set_dimensions(width, height)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width),
                              height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def draw(self, no_color_updates=False):

        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border(self.apply_widget_scaling(self._current_width),
                                                                             self.apply_widget_scaling(self._current_height),
                                                                             self.apply_widget_scaling(self.corner_radius),
                                                                             self.apply_widget_scaling(self.border_width),
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

            self.canvas.itemconfig("border_parts",
                                   fill=ThemeManager.single_color(self.border_color, self._appearance_mode),
                                   outline=ThemeManager.single_color(self.border_color, self._appearance_mode))
            self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

        self.canvas.tag_lower("inner_parts")
        self.canvas.tag_lower("border_parts")

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            require_redraw = True
            del kwargs["fg_color"]

            # check if CTk widgets are children of the frame and change their bg_color to new frame fg_color
            for child in self.winfo_children():
                if isinstance(child, CTkBaseClass):
                    child.configure(bg_color=self.fg_color)

        if "bg_color" in kwargs:
            if kwargs["bg_color"] is None:
                self.bg_color = self.detect_color_of_master()
            else:
                self.bg_color = kwargs["bg_color"]
            require_redraw = True

            del kwargs["bg_color"]

        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
            require_redraw = True
            del kwargs["border_color"]

        if "corner_radius" in kwargs:
            self.corner_radius = kwargs["corner_radius"]
            require_redraw = True
            del kwargs["corner_radius"]

        if "border_width" in kwargs:
            self.border_width = kwargs["border_width"]
            require_redraw = True
            del kwargs["border_width"]

        if "width" in kwargs:
            self.set_dimensions(width=kwargs["width"])
            del kwargs["width"]

        if "height" in kwargs:
            self.set_dimensions(height=kwargs["height"])
            del kwargs["height"]

        super().configure(*args, **kwargs)

        if require_redraw:
            self.draw()
