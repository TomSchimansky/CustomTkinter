import tkinter
import sys
import math

from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..settings import Settings
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkButton(CTkBaseClass):
    """ tkinter custom button with border, rounded corners and hover effect """

    def __init__(self, *args,
                 bg_color=None,
                 fg_color="default_theme",
                 hover_color="default_theme",
                 border_color="default_theme",
                 border_width="default_theme",
                 command=None,
                 textvariable=None,
                 width=140,
                 height=28,
                 corner_radius="default_theme",
                 text_font="default_theme",
                 text_color="default_theme",
                 text_color_disabled="default_theme",
                 text="CTkButton",
                 hover=True,
                 image=None,
                 compound=tkinter.LEFT,
                 state=tkinter.NORMAL,
                 **kwargs):

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=width, height=height, **kwargs)

        self.configure_basic_grid()

        # color variables
        self.fg_color = ThemeManager.theme["color"]["button"] if fg_color == "default_theme" else fg_color
        self.hover_color = ThemeManager.theme["color"]["button_hover"] if hover_color == "default_theme" else hover_color
        self.border_color = ThemeManager.theme["color"]["button_border"] if border_color == "default_theme" else border_color

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["button_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = ThemeManager.theme["shape"]["button_border_width"] if border_width == "default_theme" else border_width

        # text and font and image
        self.image = image
        self.image_label = None
        self.text = text
        self.text_label = None
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.text_color_disabled = ThemeManager.theme["color"]["text_button_disabled"] if text_color_disabled == "default_theme" else text_color_disabled
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font

        # callback and hover functionality
        self.function = command
        self.textvariable = textvariable
        self.state = state
        self.hover = hover
        self.compound = compound
        self.click_animation_running = False

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(self._desired_width),
                                height=self.apply_widget_scaling(self._desired_height))
        self.canvas.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew")
        self.draw_engine = DrawEngine(self.canvas)

        # event bindings
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<Button-1>", self.clicked)
        self.bind('<Configure>', self.update_dimensions_event)

        self.set_cursor()
        self.draw()  # initial draw

    def configure_basic_grid(self):
        # Configuration of a grid system (2x2) in which all parts of CTkButton are centered
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        if self.text_label is not None:
            self.text_label.destroy()
            self.text_label = None
        if self.image_label is not None:
            self.image_label.destroy()
            self.image_label = None

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width),
                              height=self.apply_widget_scaling(self._desired_height))
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
                                                                             self.apply_widget_scaling(self.border_width))

        if no_color_updates is False or requires_recoloring:

            self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

            # set color for the button border parts (outline)
            self.canvas.itemconfig("border_parts",
                                   outline=ThemeManager.single_color(self.border_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.border_color, self._appearance_mode))

            # set color for inner button parts
            if self.fg_color is None:
                self.canvas.itemconfig("inner_parts",
                                       outline=ThemeManager.single_color(self.bg_color, self._appearance_mode),
                                       fill=ThemeManager.single_color(self.bg_color, self._appearance_mode))
            else:
                self.canvas.itemconfig("inner_parts",
                                       outline=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                       fill=ThemeManager.single_color(self.fg_color, self._appearance_mode))

        # create text label if text given
        if self.text is not None and self.text != "":

            if self.text_label is None:
                self.text_label = tkinter.Label(master=self,
                                                font=self.apply_font_scaling(self.text_font),
                                                textvariable=self.textvariable)

                self.text_label.bind("<Enter>", self.on_enter)
                self.text_label.bind("<Leave>", self.on_leave)
                self.text_label.bind("<Button-1>", self.clicked)
                self.text_label.bind("<Button-1>", self.clicked)

            if no_color_updates is False:
                # set text_label fg color (text color)
                self.text_label.configure(fg=ThemeManager.single_color(self.text_color, self._appearance_mode))

                if self.state == tkinter.DISABLED:
                    self.text_label.configure(fg=(ThemeManager.single_color(self.text_color_disabled, self._appearance_mode)))
                else:
                    self.text_label.configure(fg=ThemeManager.single_color(self.text_color, self._appearance_mode))

                if self.fg_color is None:
                    self.text_label.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))
                else:
                    self.text_label.configure(bg=ThemeManager.single_color(self.fg_color, self._appearance_mode))

            self.text_label.configure(text=self.text)  # set text

        else:
            # delete text_label if no text given
            if self.text_label is not None:
                self.text_label.destroy()
                self.text_label = None

        # create image label if image given
        if self.image is not None:

            if self.image_label is None:
                self.image_label = tkinter.Label(master=self)

                self.image_label.bind("<Enter>", self.on_enter)
                self.image_label.bind("<Leave>", self.on_leave)
                self.image_label.bind("<Button-1>", self.clicked)
                self.image_label.bind("<Button-1>", self.clicked)

            if no_color_updates is False:
                # set image_label bg color (background color of label)
                if self.fg_color is None:
                    self.image_label.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))
                else:
                    self.image_label.configure(bg=ThemeManager.single_color(self.fg_color, self._appearance_mode))

            self.image_label.configure(image=self.image)  # set image

        else:
            # delete text_label if no text given
            if self.image_label is not None:
                self.image_label.destroy()
                self.image_label = None

        # create grid layout with just an image given
        if self.image_label is not None and self.text_label is None:
            self.image_label.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="",
                                  pady=(self.apply_widget_scaling(self.border_width), self.apply_widget_scaling(self.border_width) + 1))  # bottom pady with +1 for rounding to even

        # create grid layout with just text given
        if self.image_label is None and self.text_label is not None:
            self.text_label.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="",
                                 padx=self.apply_widget_scaling(self.corner_radius),
                                 pady=(self.apply_widget_scaling(self.border_width), self.apply_widget_scaling(self.border_width) + 1))  # bottom pady with +1 for rounding to even

        # create grid layout of image and text label in 2x2 grid system with given compound
        if self.image_label is not None and self.text_label is not None:
            if self.compound == tkinter.LEFT or self.compound == "left":
                self.image_label.grid(row=0, column=0, sticky="e", rowspan=2, columnspan=1,
                                      padx=(max(self.apply_widget_scaling(self.corner_radius), self.apply_widget_scaling(self.border_width)), 2),
                                      pady=(self.apply_widget_scaling(self.border_width), self.apply_widget_scaling(self.border_width) + 1))
                self.text_label.grid(row=0, column=1, sticky="w", rowspan=2, columnspan=1,
                                     padx=(2, max(self.apply_widget_scaling(self.corner_radius), self.apply_widget_scaling(self.border_width))),
                                     pady=(self.apply_widget_scaling(self.border_width), self.apply_widget_scaling(self.border_width) + 1))
            elif self.compound == tkinter.TOP or self.compound == "top":
                self.image_label.grid(row=0, column=0, sticky="s", columnspan=2, rowspan=1,
                                      padx=max(self.apply_widget_scaling(self.corner_radius), self.apply_widget_scaling(self.border_width)),
                                      pady=(self.apply_widget_scaling(self.border_width), 2))
                self.text_label.grid(row=1, column=0, sticky="n", columnspan=2, rowspan=1,
                                     padx=max(self.apply_widget_scaling(self.corner_radius), self.apply_widget_scaling(self.border_width)),
                                     pady=(2, self.apply_widget_scaling(self.border_width)))
            elif self.compound == tkinter.RIGHT or self.compound == "right":
                self.image_label.grid(row=0, column=1, sticky="w", rowspan=2, columnspan=1,
                                      padx=(2, max(self.apply_widget_scaling(self.corner_radius), self.apply_widget_scaling(self.border_width))),
                                      pady=(self.apply_widget_scaling(self.border_width), self.apply_widget_scaling(self.border_width) + 1))
                self.text_label.grid(row=0, column=0, sticky="e", rowspan=2, columnspan=1,
                                     padx=(max(self.apply_widget_scaling(self.corner_radius), self.apply_widget_scaling(self.border_width)), 2),
                                     pady=(self.apply_widget_scaling(self.border_width), self.apply_widget_scaling(self.border_width) + 1))
            elif self.compound == tkinter.BOTTOM or self.compound == "bottom":
                self.image_label.grid(row=1, column=0, sticky="n", columnspan=2, rowspan=1,
                                      padx=max(self.apply_widget_scaling(self.corner_radius), self.apply_widget_scaling(self.border_width)),
                                      pady=(2, self.apply_widget_scaling(self.border_width)))
                self.text_label.grid(row=0, column=0, sticky="s", columnspan=2, rowspan=1,
                                     padx=max(self.apply_widget_scaling(self.corner_radius), self.apply_widget_scaling(self.border_width)),
                                     pady=(self.apply_widget_scaling(self.border_width), 2))

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "text" in kwargs:
            self.set_text(kwargs["text"])
            del kwargs["text"]

        if "state" in kwargs:
            self.state = kwargs["state"]
            self.set_cursor()
            require_redraw = True
            del kwargs["state"]

        if "image" in kwargs:
            self.set_image(kwargs["image"])
            del kwargs["image"]

        if "compound" in kwargs:
            self.compound = kwargs["compound"]
            require_redraw = True
            del kwargs["compound"]

        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            require_redraw = True
            del kwargs["fg_color"]

        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
            require_redraw = True
            del kwargs["border_color"]

        if "bg_color" in kwargs:
            if kwargs["bg_color"] is None:
                self.bg_color = self.detect_color_of_master()
            else:
                self.bg_color = kwargs["bg_color"]
            require_redraw = True
            del kwargs["bg_color"]

        if "hover_color" in kwargs:
            self.hover_color = kwargs["hover_color"]
            require_redraw = True
            del kwargs["hover_color"]

        if "text_color" in kwargs:
            self.text_color = kwargs["text_color"]
            require_redraw = True
            del kwargs["text_color"]

        if "command" in kwargs:
            self.function = kwargs["command"]
            del kwargs["command"]

        if "textvariable" in kwargs:
            self.textvariable = kwargs["textvariable"]
            if self.text_label is not None:
                self.text_label.configure(textvariable=self.textvariable)
            del kwargs["textvariable"]

        if "width" in kwargs:
            self.set_dimensions(width=kwargs["width"])
            del kwargs["width"]

        if "height" in kwargs:
            self.set_dimensions(height=kwargs["height"])
            del kwargs["height"]

        super().configure(*args, **kwargs)

        if require_redraw:
            self.draw()

    def set_cursor(self):
        if Settings.cursor_manipulation_enabled:
            if self.state == tkinter.DISABLED:
                if sys.platform == "darwin" and self.function is not None and Settings.cursor_manipulation_enabled:
                    self.configure(cursor="arrow")
                elif sys.platform.startswith("win") and self.function is not None and Settings.cursor_manipulation_enabled:
                    self.configure(cursor="arrow")

            elif self.state == tkinter.NORMAL:
                if sys.platform == "darwin" and self.function is not None and Settings.cursor_manipulation_enabled:
                    self.configure(cursor="pointinghand")
                elif sys.platform.startswith("win") and self.function is not None and Settings.cursor_manipulation_enabled:
                    self.configure(cursor="hand2")

    def set_text(self, text):
        self.text = text
        self.draw()

    def set_image(self, image):
        self.image = image
        self.draw()

    def on_enter(self, event=0):
        if self.hover is True and self.state == tkinter.NORMAL:
            if self.hover_color is None:
                inner_parts_color = self.fg_color
            else:
                inner_parts_color = self.hover_color

            # set color of inner button parts to hover color
            self.canvas.itemconfig("inner_parts",
                                   outline=ThemeManager.single_color(inner_parts_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

            # set text_label bg color to button hover color
            if self.text_label is not None:
                self.text_label.configure(bg=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

            # set image_label bg color to button hover color
            if self.image_label is not None:
                self.image_label.configure(bg=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

    def on_leave(self, event=0):
        self.click_animation_running = False

        if self.hover is True:
            if self.fg_color is None:
                inner_parts_color = self.bg_color
            else:
                inner_parts_color = self.fg_color

            # set color of inner button parts
            self.canvas.itemconfig("inner_parts",
                                   outline=ThemeManager.single_color(inner_parts_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

            # set text_label bg color (label color)
            if self.text_label is not None:
                self.text_label.configure(bg=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

            # set image_label bg color (image bg color)
            if self.image_label is not None:
                self.image_label.configure(bg=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

    def click_animation(self):
        if self.click_animation_running:
            self.on_enter()

    def clicked(self, event=0):
        if self.function is not None:
            if self.state is not tkinter.DISABLED:

                # click animation: change color with .on_leave() and back to normal after 100ms with click_animation()
                self.on_leave()
                self.click_animation_running = True
                self.after(100, self.click_animation)

                self.function()
