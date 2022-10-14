import tkinter
import sys
from typing import Union, Tuple, Callable

from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..settings import Settings
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkButton(CTkBaseClass):
    """
    Button with rounded corners, border, hover effect, image support, click command and textvariable.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 master: any = None,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: Union[int, str] = "default_theme",
                 border_width: Union[int, str] = "default_theme",

                 bg_color: Union[str, Tuple[str, str], None] = None,
                 fg_color: Union[str, Tuple[str, str], None] = "default_theme",
                 hover_color: Union[str, Tuple[str, str]] = "default_theme",
                 border_color: Union[str, Tuple[str, str]] = "default_theme",
                 text_color: Union[str, Tuple[str, str]] = "default_theme",
                 text_color_disabled: Union[str, Tuple[str, str]] = "default_theme",

                 background_corner_colors: Tuple[Union[str, Tuple[str, str]]] = None,
                 round_width_to_even_numbers: bool = True,
                 round_height_to_even_numbers: bool = True,

                 text: str = "CTkButton",
                 font: any = "default_theme",
                 textvariable: tkinter.Variable = None,
                 image: tkinter.PhotoImage = None,
                 state: str = "normal",
                 hover: bool = True,
                 command: Callable = None,
                 compound: str = "left",
                 **kwargs):

        # transfer basic functionality (_bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

        # color
        self._fg_color = ThemeManager.theme["color"]["button"] if fg_color == "default_theme" else fg_color
        self._hover_color = ThemeManager.theme["color"]["button_hover"] if hover_color == "default_theme" else hover_color
        self._border_color = ThemeManager.theme["color"]["button_border"] if border_color == "default_theme" else border_color
        self._text_color = ThemeManager.theme["color"]["text_button"] if text_color == "default_theme" else text_color
        self._text_color_disabled = ThemeManager.theme["color"]["text_button_disabled"] if text_color_disabled == "default_theme" else text_color_disabled
        self._background_corner_colors = background_corner_colors  # rendering options for DrawEngine

        # shape
        self._corner_radius = ThemeManager.theme["shape"]["button_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self._border_width = ThemeManager.theme["shape"]["button_border_width"] if border_width == "default_theme" else border_width
        self._round_width_to_even_numbers = round_width_to_even_numbers  # rendering options for DrawEngine
        self._round_height_to_even_numbers = round_height_to_even_numbers  # rendering options for DrawEngine

        self._corner_radius = min(self._corner_radius, round(self._current_height/2))

        # text, font, image
        self._image = image
        self._image_label: Union[tkinter.Label, None] = None
        self._text = text
        self._text_label: Union[tkinter.Label, None] = None
        self._font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if font == "default_theme" else font

        # callback and hover functionality
        self._command = command
        self._textvariable = textvariable
        self._state = state
        self._hover = hover
        self._compound = compound
        self._click_animation_running: bool = False

        # configure grid system (2x2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # canvas
        self._canvas = CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._desired_width),
                                 height=self._apply_widget_scaling(self._desired_height))
        self._canvas.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew")
        self._draw_engine = DrawEngine(self._canvas)
        self._draw_engine.set_round_to_even_numbers(self._round_width_to_even_numbers, self._round_height_to_even_numbers)  # rendering options

        # canvas event bindings
        self._canvas.bind("<Enter>", self._on_enter)
        self._canvas.bind("<Leave>", self._on_leave)
        self._canvas.bind("<Button-1>", self._clicked)
        self._canvas.bind("<Button-1>", self._clicked)

        # configure cursor and initial draw
        self._set_cursor()
        self._draw()

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        if self._text_label is not None:
            self._text_label.configure(font=self._apply_font_scaling(self._font))

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw(no_color_updates=True)

    def _set_dimensions(self, width: int = None, height: int = None):
        super()._set_dimensions(width, height)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw()

    def _draw(self, no_color_updates=False):
        if self._background_corner_colors is not None:
            self._draw_engine.draw_background_corners(self._apply_widget_scaling(self._current_width),
                                                      self._apply_widget_scaling(self._current_height))
            self._canvas.itemconfig("background_corner_top_left", fill=ThemeManager.single_color(self._background_corner_colors[0], self._appearance_mode))
            self._canvas.itemconfig("background_corner_top_right", fill=ThemeManager.single_color(self._background_corner_colors[1], self._appearance_mode))
            self._canvas.itemconfig("background_corner_bottom_right", fill=ThemeManager.single_color(self._background_corner_colors[2], self._appearance_mode))
            self._canvas.itemconfig("background_corner_bottom_left", fill=ThemeManager.single_color(self._background_corner_colors[3], self._appearance_mode))
        else:
            self._canvas.delete("background_parts")

        requires_recoloring = self._draw_engine.draw_rounded_rect_with_border(self._apply_widget_scaling(self._current_width),
                                                                              self._apply_widget_scaling(self._current_height),
                                                                              self._apply_widget_scaling(self._corner_radius),
                                                                              self._apply_widget_scaling(self._border_width))

        if no_color_updates is False or requires_recoloring:

            self._canvas.configure(bg=ThemeManager.single_color(self._bg_color, self._appearance_mode))

            # set color for the button border parts (outline)
            self._canvas.itemconfig("border_parts",
                                    outline=ThemeManager.single_color(self._border_color, self._appearance_mode),
                                    fill=ThemeManager.single_color(self._border_color, self._appearance_mode))

            # set color for inner button parts
            if self._fg_color is None:
                self._canvas.itemconfig("inner_parts",
                                        outline=ThemeManager.single_color(self._bg_color, self._appearance_mode),
                                        fill=ThemeManager.single_color(self._bg_color, self._appearance_mode))
            else:
                self._canvas.itemconfig("inner_parts",
                                        outline=ThemeManager.single_color(self._fg_color, self._appearance_mode),
                                        fill=ThemeManager.single_color(self._fg_color, self._appearance_mode))

        # create text label if text given
        if self._text is not None and self._text != "":

            if self._text_label is None:
                self._text_label = tkinter.Label(master=self,
                                                 font=self._apply_font_scaling(self._font),
                                                 text=self._text,
                                                 padx=0,
                                                 pady=0,
                                                 borderwidth=1,
                                                 textvariable=self._textvariable)

                self._text_label.bind("<Enter>", self._on_enter)
                self._text_label.bind("<Leave>", self._on_leave)
                self._text_label.bind("<Button-1>", self._clicked)
                self._text_label.bind("<Button-1>", self._clicked)

            if no_color_updates is False:
                # set text_label fg color (text color)
                self._text_label.configure(fg=ThemeManager.single_color(self._text_color, self._appearance_mode))

                if self._state == tkinter.DISABLED:
                    self._text_label.configure(fg=(ThemeManager.single_color(self._text_color_disabled, self._appearance_mode)))
                else:
                    self._text_label.configure(fg=ThemeManager.single_color(self._text_color, self._appearance_mode))

                if self._fg_color is None:
                    self._text_label.configure(bg=ThemeManager.single_color(self._bg_color, self._appearance_mode))
                else:
                    self._text_label.configure(bg=ThemeManager.single_color(self._fg_color, self._appearance_mode))

        else:
            # delete text_label if no text given
            if self._text_label is not None:
                self._text_label.destroy()
                self._text_label = None

        # create image label if image given
        if self._image is not None:

            if self._image_label is None:
                self._image_label = tkinter.Label(master=self)

                self._image_label.bind("<Enter>", self._on_enter)
                self._image_label.bind("<Leave>", self._on_leave)
                self._image_label.bind("<Button-1>", self._clicked)
                self._image_label.bind("<Button-1>", self._clicked)

            if no_color_updates is False:
                # set image_label bg color (background color of label)
                if self._fg_color is None:
                    self._image_label.configure(bg=ThemeManager.single_color(self._bg_color, self._appearance_mode))
                else:
                    self._image_label.configure(bg=ThemeManager.single_color(self._fg_color, self._appearance_mode))

            self._image_label.configure(image=self._image)  # set image

        else:
            # delete text_label if no text given
            if self._image_label is not None:
                self._image_label.destroy()
                self._image_label = None

        # create grid layout with just an image given
        if self._image_label is not None and self._text_label is None:
            self._image_label.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="",
                                   pady=(self._apply_widget_scaling(self._border_width), self._apply_widget_scaling(self._border_width) + 1))  # bottom pady with +1 for rounding to even

        # create grid layout with just text given
        if self._image_label is None and self._text_label is not None:
            self._text_label.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="",
                                  padx=self._apply_widget_scaling(self._corner_radius),
                                  pady=(self._apply_widget_scaling(self._border_width), self._apply_widget_scaling(self._border_width) + 1))  # bottom pady with +1 for rounding to even

        # create grid layout of image and text label in 2x2 grid system with given compound
        if self._image_label is not None and self._text_label is not None:
            if self._compound == tkinter.LEFT or self._compound == "left":
                self._image_label.grid(row=0, column=0, sticky="e", rowspan=2, columnspan=1,
                                       padx=(max(self._apply_widget_scaling(self._corner_radius), self._apply_widget_scaling(self._border_width)), 2),
                                       pady=(self._apply_widget_scaling(self._border_width), self._apply_widget_scaling(self._border_width) + 1))
                self._text_label.grid(row=0, column=1, sticky="w", rowspan=2, columnspan=1,
                                      padx=(2, max(self._apply_widget_scaling(self._corner_radius), self._apply_widget_scaling(self._border_width))),
                                      pady=(self._apply_widget_scaling(self._border_width), self._apply_widget_scaling(self._border_width) + 1))
            elif self._compound == tkinter.TOP or self._compound == "top":
                self._image_label.grid(row=0, column=0, sticky="s", columnspan=2, rowspan=1,
                                       padx=max(self._apply_widget_scaling(self._corner_radius), self._apply_widget_scaling(self._border_width)),
                                       pady=(self._apply_widget_scaling(self._border_width), 2))
                self._text_label.grid(row=1, column=0, sticky="n", columnspan=2, rowspan=1,
                                      padx=max(self._apply_widget_scaling(self._corner_radius), self._apply_widget_scaling(self._border_width)),
                                      pady=(2, self._apply_widget_scaling(self._border_width)))
            elif self._compound == tkinter.RIGHT or self._compound == "right":
                self._image_label.grid(row=0, column=1, sticky="w", rowspan=2, columnspan=1,
                                       padx=(2, max(self._apply_widget_scaling(self._corner_radius), self._apply_widget_scaling(self._border_width))),
                                       pady=(self._apply_widget_scaling(self._border_width), self._apply_widget_scaling(self._border_width) + 1))
                self._text_label.grid(row=0, column=0, sticky="e", rowspan=2, columnspan=1,
                                      padx=(max(self._apply_widget_scaling(self._corner_radius), self._apply_widget_scaling(self._border_width)), 2),
                                      pady=(self._apply_widget_scaling(self._border_width), self._apply_widget_scaling(self._border_width) + 1))
            elif self._compound == tkinter.BOTTOM or self._compound == "bottom":
                self._image_label.grid(row=1, column=0, sticky="n", columnspan=2, rowspan=1,
                                       padx=max(self._apply_widget_scaling(self._corner_radius), self._apply_widget_scaling(self._border_width)),
                                       pady=(2, self._apply_widget_scaling(self._border_width)))
                self._text_label.grid(row=0, column=0, sticky="s", columnspan=2, rowspan=1,
                                      padx=max(self._apply_widget_scaling(self._corner_radius), self._apply_widget_scaling(self._border_width)),
                                      pady=(self._apply_widget_scaling(self._border_width), 2))

    def configure(self, require_redraw=False, **kwargs):
        if "text" in kwargs:
            self._text = kwargs.pop("text")
            if self._text_label is None:
                require_redraw = True  # text_label will be created in .draw()
            else:
                self._text_label.configure(text=self._text)

        if "font" in kwargs:
            self._font = kwargs.pop("font")
            if self._text_label is not None:
                self._text_label.configure(font=self._apply_font_scaling(self._font))

        if "state" in kwargs:
            self._state = kwargs.pop("state")
            self._set_cursor()
            require_redraw = True

        if "image" in kwargs:
            self._image = kwargs.pop("image")
            require_redraw = True

        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")
            require_redraw = True

        if "border_width" in kwargs:
            self._border_width = kwargs.pop("border_width")
            require_redraw = True

        if "compound" in kwargs:
            self._compound = kwargs.pop("compound")
            require_redraw = True

        if "fg_color" in kwargs:
            self._fg_color = kwargs.pop("fg_color")
            require_redraw = True

        if "border_color" in kwargs:
            self._border_color = kwargs.pop("border_color")
            require_redraw = True

        if "hover_color" in kwargs:
            self._hover_color = kwargs.pop("hover_color")
            require_redraw = True

        if "text_color" in kwargs:
            self._text_color = kwargs.pop("text_color")
            require_redraw = True

        if "command" in kwargs:
            self._command = kwargs.pop("command")

        if "textvariable" in kwargs:
            self._textvariable = kwargs.pop("textvariable")
            if self._text_label is not None:
                self._text_label.configure(textvariable=self._textvariable)

        if "background_corner_colors" in kwargs:
            self._background_corner_colors = kwargs.pop("background_corner_colors")
            require_redraw = True

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "corner_radius":
            return self._corner_radius
        elif attribute_name == "border_width":
            return self._border_width

        elif attribute_name == "fg_color":
            return self._fg_color
        elif attribute_name == "hover_color":
            return self._hover_color
        elif attribute_name == "border_color":
            return self._border_color
        elif attribute_name == "text_color":
            return self._text_color
        elif attribute_name == "text_color_disabled":
            return self._text_color_disabled
        elif attribute_name == "background_corner_colors":
            return self._background_corner_colors

        elif attribute_name == "text":
            return self._text
        elif attribute_name == "font":
            return self._font
        elif attribute_name == "textvariable":
            return self._textvariable
        elif attribute_name == "image":
            return self._image
        elif attribute_name == "state":
            return self._state
        elif attribute_name == "hover":
            return self._hover
        elif attribute_name == "command":
            return self._command
        elif attribute_name == "compound":
            return self._compound
        else:
            return super().cget(attribute_name)

    def _set_cursor(self):
        if Settings.cursor_manipulation_enabled:
            if self._state == tkinter.DISABLED:
                if sys.platform == "darwin" and self._command is not None and Settings.cursor_manipulation_enabled:
                    self.configure(cursor="arrow")
                elif sys.platform.startswith("win") and self._command is not None and Settings.cursor_manipulation_enabled:
                    self.configure(cursor="arrow")

            elif self._state == tkinter.NORMAL:
                if sys.platform == "darwin" and self._command is not None and Settings.cursor_manipulation_enabled:
                    self.configure(cursor="pointinghand")
                elif sys.platform.startswith("win") and self._command is not None and Settings.cursor_manipulation_enabled:
                    self.configure(cursor="hand2")

    def _on_enter(self, event=None):
        if self._hover is True and self._state == tkinter.NORMAL:
            if self._hover_color is None:
                inner_parts_color = self._fg_color
            else:
                inner_parts_color = self._hover_color

            # set color of inner button parts to hover color
            self._canvas.itemconfig("inner_parts",
                                    outline=ThemeManager.single_color(inner_parts_color, self._appearance_mode),
                                    fill=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

            # set text_label bg color to button hover color
            if self._text_label is not None:
                self._text_label.configure(bg=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

            # set image_label bg color to button hover color
            if self._image_label is not None:
                self._image_label.configure(bg=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

    def _on_leave(self, event=None):
        self._click_animation_running = False

        if self._hover is True:
            if self._fg_color is None:
                inner_parts_color = self._bg_color
            else:
                inner_parts_color = self._fg_color

            # set color of inner button parts
            self._canvas.itemconfig("inner_parts",
                                    outline=ThemeManager.single_color(inner_parts_color, self._appearance_mode),
                                    fill=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

            # set text_label bg color (label color)
            if self._text_label is not None:
                self._text_label.configure(bg=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

            # set image_label bg color (image bg color)
            if self._image_label is not None:
                self._image_label.configure(bg=ThemeManager.single_color(inner_parts_color, self._appearance_mode))

    def _click_animation(self):
        if self._click_animation_running:
            self._on_enter()

    def _clicked(self, event=None):
        if self._command is not None:
            if self._state != tkinter.DISABLED:

                # click animation: change color with .on_leave() and back to normal after 100ms with click_animation()
                self._on_leave()
                self._click_animation_running = True
                self.after(100, self._click_animation)

                self._command()

    def bind(self, sequence: str = None, command: Callable = None, add: str = None) -> str:
        """ called on the tkinter.Label and tkinter.Canvas """
        canvas_bind_return = self._canvas.bind(sequence, command, add)
        label_bind_return = self._text_label.bind(sequence, command, add)
        return canvas_bind_return + " + " + label_bind_return

    def unbind(self, sequence: str, funcid: str = None):
        """ called on the tkinter.Label and tkinter.Canvas """
        canvas_bind_return, label_bind_return = funcid.split(" + ")
        self._canvas.unbind(sequence, canvas_bind_return)
        self._text_label.unbind(sequence, label_bind_return)

    def focus(self):
        return self._text_label.focus()

    def focus_set(self):
        return self._text_label.focus_set()

    def focus_force(self):
        return self._text_label.focus_force()
