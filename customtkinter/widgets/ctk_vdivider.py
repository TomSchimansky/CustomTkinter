from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


def get_padding_dimensions(length, thickness, px=None, py=None):
    return thickness + px[0] + px[1], length + py[0] + py[1]


def get_padding_tuple(pad=None):
    p = (0, 0)

    if pad is not None:
        if type(pad) in (list, tuple) and len(pad) == 2:
            p = pad[0], pad[1]
        else:
            p = pad, pad

    return p


class CTkVerticalDivider(CTkBaseClass):
    def __init__(self, *args,
                 bg_color=None,
                 fg_color="default_theme",
                 length=160,
                 thickness=8,
                 padx: int | list | tuple = None,
                 pady: int | list | tuple = None,
                 overwrite_preferred_drawing_method: str = None,
                 **kwargs):

        self.x_padding = get_padding_tuple(padx)
        self.y_padding = get_padding_tuple(pady)

        total_dimensions = get_padding_dimensions(
            length, thickness,
            self.x_padding,
            self.y_padding)

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=total_dimensions[0], height=total_dimensions[1], **kwargs)

        # determine fg_color
        if fg_color == "default_theme":
            if isinstance(self.master, CTkVerticalDivider):
                if self.master.fg_color == ThemeManager.theme["color"]["frame_low"]:
                    self.fg_color = ThemeManager.theme["color"]["frame_high"]
                else:
                    self.fg_color = ThemeManager.theme["color"]["frame_low"]
            else:
                self.fg_color = ThemeManager.theme["color"]["frame_low"]
        else:
            self.fg_color = fg_color

        self.corner_radius = thickness / 2

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(thickness),
                                height=self.apply_widget_scaling(length),
                                )
        self.canvas.place(x=get_padding_tuple(padx)[0], y=get_padding_tuple(pady)[0], anchor="nw")
        self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))
        self.draw_engine = DrawEngine(self.canvas)
        self._overwrite_preferred_drawing_method = overwrite_preferred_drawing_method

        self.bind('<Configure>', self.update_dimensions_event)

        self.draw()

    def set_dimensions(self, width=None, height=None, padx=None, pady=None):

        total_dimensions = get_padding_dimensions(
            height, width,
            get_padding_tuple(padx),
            get_padding_tuple(pady))

        super().set_dimensions(total_dimensions[0], total_dimensions[1])

        self.canvas.configure(width=self.apply_widget_scaling(width),
                              height=self.apply_widget_scaling(height))

        self.canvas.place(x=get_padding_tuple(padx)[0], y=get_padding_tuple(pady)[0], anchor="nw")

        self.draw()

    def draw(self, no_color_updates=False):

        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border(
            self.apply_widget_scaling(self._current_width) - self.x_padding[0] - self.x_padding[1],
            self.apply_widget_scaling(self._current_height) - self.y_padding[0] - self.y_padding[1],
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
            self.set_dimensions(height=kwargs["length"])
            del kwargs["length"]

        if "thickness" in kwargs:
            self.set_dimensions(width=kwargs["thickness"])
            del kwargs["thickness"]

        if "padx" in kwargs:
            self.set_dimensions(padx=kwargs["padx"])
            del kwargs["padx"]

        if "pady" in kwargs:
            self.set_dimensions(pady=kwargs["pady"])
            del kwargs["pady"]

        super().configure(*args, **kwargs)

        if require_redraw:
            self.draw()
