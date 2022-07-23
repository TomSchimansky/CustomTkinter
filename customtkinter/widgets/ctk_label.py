import sys
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
                 anchor="center",  # label anchor: center, n, e, s, w
                 **kwargs):

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        if "master" in kwargs:
            super().__init__(*args, bg_color=bg_color, width=width, height=height, master=kwargs.pop("master"))
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
        self.anchor = anchor
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
                                        anchor=self.anchor,
                                        text=self.text,
                                        font=self.apply_font_scaling(self.text_font),
                                        **kwargs)
        text_label_grid_sticky = self.anchor if self.anchor != "center" else ""
        self.text_label.grid(row=0, column=0, padx=self.apply_widget_scaling(self.corner_radius),
                             sticky=text_label_grid_sticky)

        self.bind('<Configure>', self.update_dimensions_event)
        self.draw()

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width), height=self.apply_widget_scaling(self._desired_height))
        self.text_label.configure(font=self.apply_font_scaling(self.text_font))
        text_label_grid_sticky = self.anchor if self.anchor != "center" else ""
        self.text_label.grid(row=0, column=0, padx=self.apply_widget_scaling(self.corner_radius),
                             sticky=text_label_grid_sticky)

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

    def config(self, **kwargs):
        sys.stderr.write("Warning: Use .configure() instead of .config()")
        self.configure(**kwargs)

    def configure(self, require_redraw=False, **kwargs):
        if "anchor" in kwargs:
            self.anchor = kwargs.pop("anchor")
            text_label_grid_sticky = self.anchor if self.anchor != "center" else ""
            self.text_label.grid(row=0, column=0, padx=self.apply_widget_scaling(self.corner_radius),
                                 sticky=text_label_grid_sticky)

        if "text" in kwargs:
            self.text = kwargs["text"]
            self.text_label.configure(text=self.text)
            del kwargs["text"]

        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            require_redraw = True
            del kwargs["fg_color"]

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

        if "bg_color" in kwargs:
            super().configure(bg_color=kwargs.pop("bg_color"), require_redraw=require_redraw)
        else:
            super().configure(require_redraw=require_redraw)

        self.text_label.configure(**kwargs)  # pass remaining kwargs to label

    def set_text(self, text):
        """ Will be removed in the next major release """

        self.text = text
        self.text_label.configure(text=self.text)
