import tkinter

from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkLabel(CTkBaseClass):
    def __init__(self, *args,
                 bg_color=None,
                 fg_color="default_theme",
                 text_color="default_theme",
                 corner_radius="default_theme",
                 width=140,
                 height=28,
                 text="CTkLabel",
                 text_font="default_theme",
                 **kwargs):

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        if "master" in kwargs:
            super().__init__(*args, bg_color=bg_color, width=width, height=height, master=kwargs["master"])
            del kwargs["master"]
        else:
            super().__init__(*args, bg_color=bg_color, width=width, height=height)

        # color
        self.fg_color = ThemeManager.theme["color"]["label"] if fg_color == "default_theme" else fg_color
        if self.fg_color is None:
            self.fg_color = self.bg_color
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["label_corner_radius"] if corner_radius == "default_theme" else corner_radius

        # text
        self.text = text
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font

        # configure grid system (1x1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(self._desired_width),
                                height=self.apply_widget_scaling(self._desired_height))
        self.canvas.grid(row=0, column=0, sticky="nswe")
        self.draw_engine = DrawEngine(self.canvas)

        self.text_label = tkinter.Label(master=self,
                                        highlightthickness=0,
                                        bd=0,
                                        text=self.text,
                                        font=self.apply_font_scaling(self.text_font),
                                        **kwargs)
        self.text_label.grid(row=0, column=0, padx=self.apply_widget_scaling(self.corner_radius))

        self.bind('<Configure>', self.update_dimensions_event)
        self.draw()

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width), height=self.apply_widget_scaling(self._desired_height))
        self.text_label.configure(font=self.apply_font_scaling(self.text_font))
        self.text_label.grid(row=0, column=0, padx=self.apply_widget_scaling(self.corner_radius))

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
                                                                             0)

        if no_color_updates is False or requires_recoloring:
            if ThemeManager.single_color(self.fg_color, self._appearance_mode) is not None:
                self.canvas.itemconfig("inner_parts",
                                       fill=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.fg_color, self._appearance_mode))

                self.text_label.configure(fg=ThemeManager.single_color(self.text_color, self._appearance_mode),
                                          bg=ThemeManager.single_color(self.fg_color, self._appearance_mode))
            else:
                self.canvas.itemconfig("inner_parts",
                                       fill=ThemeManager.single_color(self.bg_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.bg_color, self._appearance_mode))

                self.text_label.configure(fg=ThemeManager.single_color(self.text_color, self._appearance_mode),
                                          bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

            self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "text" in kwargs:
            self.set_text(kwargs["text"])
            del kwargs["text"]

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

        if "text_color" in kwargs:
            self.text_color = kwargs["text_color"]
            require_redraw = True
            del kwargs["text_color"]

        if "width" in kwargs:
            self.set_dimensions(width=kwargs["width"])
            del kwargs["width"]

        if "height" in kwargs:
            self.set_dimensions(height=kwargs["height"])
            del kwargs["height"]

        self.text_label.configure(*args, **kwargs)

        if require_redraw:
            self.draw()

    def set_text(self, text):
        self.text = text
        self.text_label.configure(text=self.text, width=len(self.text))
