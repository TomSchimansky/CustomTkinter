import tkinter
import sys
from typing import Union, Tuple, Callable, Optional

from .core_rendering import CTkCanvas
from .theme import ThemeManager
from .core_rendering import DrawEngine
from .core_widget_classes import CTkBaseClass
from .font import CTkFont
from .image import CTkImage


class CTkButton(CTkBaseClass):
    """
    Button with rounded corners, border, hover effect, image support, click command and textvariable.
    For detailed information check out the documentation.
    """

    _image_label_spacing: int = 6

    def __init__(self,
                 master: any,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,
                 border_spacing: int = 2,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 round_width_to_even_numbers: bool = True,
                 round_height_to_even_numbers: bool = True,

                 text: str = "CTkButton",
                 font: Optional[Union[tuple, CTkFont]] = None,
                 textvariable: Union[tkinter.Variable, None] = None,
                 image: Union[CTkImage, "ImageTk.PhotoImage", None] = None,
                 state: str = "normal",
                 hover: bool = True,
                 command: Union[Callable[[], None], None] = None,
                 compound: str = "left",
                 anchor: str = "center",
                 **kwargs):

        # transfer basic functionality (bg_color, size, appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

        # shape
        self._corner_radius: int = ThemeManager.theme["CTkButton"]["corner_radius"] if corner_radius is None else corner_radius
        self._corner_radius = min(self._corner_radius, round(self._current_height / 2))
        self._border_width: int = ThemeManager.theme["CTkButton"]["border_width"] if border_width is None else border_width
        self._border_spacing: int = border_spacing

        # color
        self._fg_color: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"]["fg_color"] if fg_color is None else self._check_color_type(fg_color, transparency=True)
        self._hover_color: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"]["hover_color"] if hover_color is None else self._check_color_type(hover_color)
        self._border_color: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"]["border_color"] if border_color is None else self._check_color_type(border_color)
        self._text_color: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"]["text_color"] if text_color is None else self._check_color_type(text_color)
        self._text_color_disabled: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"]["text_color_disabled"] if text_color_disabled is None else self._check_color_type(text_color_disabled)

        # rendering options
        self._background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = background_corner_colors  # rendering options for DrawEngine
        self._round_width_to_even_numbers: bool = round_width_to_even_numbers  # rendering options for DrawEngine
        self._round_height_to_even_numbers: bool = round_height_to_even_numbers  # rendering options for DrawEngine

        # text, font
        self._text = text
        self._text_label: Union[tkinter.Label, None] = None
        self._textvariable: tkinter.Variable = textvariable
        self._font: Union[tuple, CTkFont] = CTkFont() if font is None else self._check_font_type(font)
        if isinstance(self._font, CTkFont):
            self._font.add_size_configure_callback(self._update_font)

        # image
        self._image = self._check_image_type(image)
        self._image_label: Union[tkinter.Label, None] = None
        if isinstance(self._image, CTkImage):
            self._image.add_configure_callback(self._update_image)

        # other
        self._state: str = state
        self._hover: bool = hover
        self._command: Callable = command
        self._compound: str = compound
        self._anchor: str = anchor
        self._click_animation_running: bool = False

        # canvas and draw engine
        self._canvas = CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._desired_width),
                                 height=self._apply_widget_scaling(self._desired_height))
        self._canvas.grid(row=0, column=0, rowspan=5, columnspan=5, sticky="nsew")
        self._draw_engine = DrawEngine(self._canvas)
        self._draw_engine.set_round_to_even_numbers(self._round_width_to_even_numbers, self._round_height_to_even_numbers)  # rendering options

        # configure cursor and initial draw
        self._create_bindings()
        self._set_cursor()
        self._draw()

    def _create_bindings(self, sequence: Optional[str] = None):
        """ set necessary bindings for functionality of widget, will overwrite other bindings """

        if sequence is None or sequence == "<Enter>":
            self._canvas.bind("<Enter>", self._on_enter)

            if self._text_label is not None:
                self._text_label.bind("<Enter>", self._on_enter)
            if self._image_label is not None:
                self._image_label.bind("<Enter>", self._on_enter)

        if sequence is None or sequence == "<Leave>":
            self._canvas.bind("<Leave>", self._on_leave)

            if self._text_label is not None:
                self._text_label.bind("<Leave>", self._on_leave)
            if self._image_label is not None:
                self._image_label.bind("<Leave>", self._on_leave)

        if sequence is None or sequence == "<Button-1>":
            self._canvas.bind("<Button-1>", self._clicked)

            if self._text_label is not None:
                self._text_label.bind("<Button-1>", self._clicked)
            if self._image_label is not None:
                self._image_label.bind("<Button-1>", self._clicked)

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        self._create_grid()

        if self._text_label is not None:
            self._text_label.configure(font=self._apply_font_scaling(self._font))

        self._update_image()

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw(no_color_updates=True)

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        self._update_image()

    def _set_dimensions(self, width: int = None, height: int = None):
        super()._set_dimensions(width, height)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw()

    def _update_font(self):
        """ pass font to tkinter widgets with applied font scaling and update grid with workaround """
        if self._text_label is not None:
            self._text_label.configure(font=self._apply_font_scaling(self._font))

            # Workaround to force grid to be resized when text changes size.
            # Otherwise grid will lag and only resizes if other mouse action occurs.
            self._canvas.grid_forget()
            self._canvas.grid(row=0, column=0, rowspan=5, columnspan=5, sticky="nsew")

    def _update_image(self):
        if self._image_label is not None:
            if isinstance(self._image, CTkImage):
                self._image_label.configure(image=self._image.create_scaled_photo_image(self._get_widget_scaling(),
                                                                                        self._get_appearance_mode()))
            elif self._image is not None:
                self._image_label.configure(image=self._image)

    def destroy(self):
        if isinstance(self._font, CTkFont):
            self._font.remove_size_configure_callback(self._update_font)
        super().destroy()

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

        if self._background_corner_colors is not None:
            self._draw_engine.draw_background_corners(self._apply_widget_scaling(self._current_width),
                                                      self._apply_widget_scaling(self._current_height))
            self._canvas.itemconfig("background_corner_top_left", fill=self._apply_appearance_mode(self._background_corner_colors[0]))
            self._canvas.itemconfig("background_corner_top_right", fill=self._apply_appearance_mode(self._background_corner_colors[1]))
            self._canvas.itemconfig("background_corner_bottom_right", fill=self._apply_appearance_mode(self._background_corner_colors[2]))
            self._canvas.itemconfig("background_corner_bottom_left", fill=self._apply_appearance_mode(self._background_corner_colors[3]))
        else:
            self._canvas.delete("background_parts")

        requires_recoloring = self._draw_engine.draw_rounded_rect_with_border(self._apply_widget_scaling(self._current_width),
                                                                              self._apply_widget_scaling(self._current_height),
                                                                              self._apply_widget_scaling(self._corner_radius),
                                                                              self._apply_widget_scaling(self._border_width))

        if no_color_updates is False or requires_recoloring:

            self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))

            # set color for the button border parts (outline)
            self._canvas.itemconfig("border_parts",
                                    outline=self._apply_appearance_mode(self._border_color),
                                    fill=self._apply_appearance_mode(self._border_color))

            # set color for inner button parts
            if self._fg_color == "transparent":
                self._canvas.itemconfig("inner_parts",
                                        outline=self._apply_appearance_mode(self._bg_color),
                                        fill=self._apply_appearance_mode(self._bg_color))
            else:
                self._canvas.itemconfig("inner_parts",
                                        outline=self._apply_appearance_mode(self._fg_color),
                                        fill=self._apply_appearance_mode(self._fg_color))

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
                self._create_grid()

                self._text_label.bind("<Enter>", self._on_enter)
                self._text_label.bind("<Leave>", self._on_leave)
                self._text_label.bind("<Button-1>", self._clicked)
                self._text_label.bind("<Button-1>", self._clicked)

            if no_color_updates is False:
                # set text_label fg color (text color)
                self._text_label.configure(fg=self._apply_appearance_mode(self._text_color))

                if self._state == tkinter.DISABLED:
                    self._text_label.configure(fg=(self._apply_appearance_mode(self._text_color_disabled)))
                else:
                    self._text_label.configure(fg=self._apply_appearance_mode(self._text_color))

                if self._apply_appearance_mode(self._fg_color) == "transparent":
                    self._text_label.configure(bg=self._apply_appearance_mode(self._bg_color))
                else:
                    self._text_label.configure(bg=self._apply_appearance_mode(self._fg_color))

        else:
            # delete text_label if no text given
            if self._text_label is not None:
                self._text_label.destroy()
                self._text_label = None
                self._create_grid()

        # create image label if image given
        if self._image is not None:

            if self._image_label is None:
                self._image_label = tkinter.Label(master=self)
                self._update_image()  # set image
                self._create_grid()

                self._image_label.bind("<Enter>", self._on_enter)
                self._image_label.bind("<Leave>", self._on_leave)
                self._image_label.bind("<Button-1>", self._clicked)
                self._image_label.bind("<Button-1>", self._clicked)

            if no_color_updates is False:
                # set image_label bg color (background color of label)
                if self._apply_appearance_mode(self._fg_color) == "transparent":
                    self._image_label.configure(bg=self._apply_appearance_mode(self._bg_color))
                else:
                    self._image_label.configure(bg=self._apply_appearance_mode(self._fg_color))

        else:
            # delete text_label if no text given
            if self._image_label is not None:
                self._image_label.destroy()
                self._image_label = None
                self._create_grid()

    def _create_grid(self):
        """ configure grid system (5x5) """

        # Outer rows and columns have weight of 1000 to overpower the rows and columns of the label and image with weight 1.
        # Rows and columns of image and label need weight of 1 to collapse in case of missing space on the button,
        # so image and label need sticky option to stick together in the center, and therefore outer rows and columns
        # need weight of 100 in case of other anchor than center.
        n_padding_weight, s_padding_weight, e_padding_weight, w_padding_weight = 1000, 1000, 1000, 1000
        if self._anchor != "center":
            if "n" in self._anchor:
                n_padding_weight, s_padding_weight = 0, 1000
            if "s" in self._anchor:
                n_padding_weight, s_padding_weight = 1000, 0
            if "e" in self._anchor:
                e_padding_weight, w_padding_weight = 1000, 0
            if "w" in self._anchor:
                e_padding_weight, w_padding_weight = 0, 1000

        scaled_minsize_rows = self._apply_widget_scaling(max(self._border_width + 1, self._border_spacing))
        scaled_minsize_columns = self._apply_widget_scaling(max(self._corner_radius, self._border_width + 1, self._border_spacing))

        self.grid_rowconfigure(0, weight=n_padding_weight, minsize=scaled_minsize_rows)
        self.grid_rowconfigure(4, weight=s_padding_weight, minsize=scaled_minsize_rows)
        self.grid_columnconfigure(0, weight=e_padding_weight, minsize=scaled_minsize_columns)
        self.grid_columnconfigure(4, weight=w_padding_weight, minsize=scaled_minsize_columns)

        if self._compound in ("right", "left"):
            self.grid_rowconfigure(2, weight=1)
            if self._image_label is not None and self._text_label is not None:
                self.grid_columnconfigure(2, weight=0, minsize=self._apply_widget_scaling(self._image_label_spacing))
            else:
                self.grid_columnconfigure(2, weight=0)

            self.grid_rowconfigure((1, 3), weight=0)
            self.grid_columnconfigure((1, 3), weight=1)
        else:
            self.grid_columnconfigure(2, weight=1)
            if self._image_label is not None and self._text_label is not None:
                self.grid_rowconfigure(2, weight=0, minsize=self._apply_widget_scaling(self._image_label_spacing))
            else:
                self.grid_rowconfigure(2, weight=0)

            self.grid_columnconfigure((1, 3), weight=0)
            self.grid_rowconfigure((1, 3), weight=1)

        if self._compound == "right":
            if self._image_label is not None:
                self._image_label.grid(row=2, column=3, sticky="w")
            if self._text_label is not None:
                self._text_label.grid(row=2, column=1, sticky="e")
        elif self._compound == "left":
            if self._image_label is not None:
                self._image_label.grid(row=2, column=1, sticky="e")
            if self._text_label is not None:
                self._text_label.grid(row=2, column=3, sticky="w")
        elif self._compound == "top":
            if self._image_label is not None:
                self._image_label.grid(row=1, column=2, sticky="s")
            if self._text_label is not None:
                self._text_label.grid(row=3, column=2, sticky="n")
        elif self._compound == "bottom":
            if self._image_label is not None:
                self._image_label.grid(row=3, column=2, sticky="n")
            if self._text_label is not None:
                self._text_label.grid(row=1, column=2, sticky="s")

    def configure(self, require_redraw=False, **kwargs):
        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")
            self._create_grid()
            require_redraw = True

        if "border_width" in kwargs:
            self._border_width = kwargs.pop("border_width")
            self._create_grid()
            require_redraw = True

        if "border_spacing" in kwargs:
            self._border_spacing = kwargs.pop("border_spacing")
            self._create_grid()
            require_redraw = True

        if "fg_color" in kwargs:
            self._fg_color = self._check_color_type(kwargs.pop("fg_color"), transparency=True)
            require_redraw = True

        if "hover_color" in kwargs:
            self._hover_color = self._check_color_type(kwargs.pop("hover_color"))
            require_redraw = True

        if "border_color" in kwargs:
            self._border_color = self._check_color_type(kwargs.pop("border_color"))
            require_redraw = True

        if "text_color" in kwargs:
            self._text_color = self._check_color_type(kwargs.pop("text_color"))
            require_redraw = True

        if "text_color_disabled" in kwargs:
            self._text_color_disabled = self._check_color_type(kwargs.pop("text_color_disabled"))
            require_redraw = True

        if "background_corner_colors" in kwargs:
            self._background_corner_colors = kwargs.pop("background_corner_colors")
            require_redraw = True

        if "text" in kwargs:
            self._text = kwargs.pop("text")
            if self._text_label is None:
                require_redraw = True  # text_label will be created in .draw()
            else:
                self._text_label.configure(text=self._text)

        if "font" in kwargs:
            if isinstance(self._font, CTkFont):
                self._font.remove_size_configure_callback(self._update_font)
            self._font = self._check_font_type(kwargs.pop("font"))
            if isinstance(self._font, CTkFont):
                self._font.add_size_configure_callback(self._update_font)

            self._update_font()

        if "textvariable" in kwargs:
            self._textvariable = kwargs.pop("textvariable")
            if self._text_label is not None:
                self._text_label.configure(textvariable=self._textvariable)

        if "image" in kwargs:
            if isinstance(self._image, CTkImage):
                self._image.remove_configure_callback(self._update_image)
            self._image = self._check_image_type(kwargs.pop("image"))
            if isinstance(self._image, CTkImage):
                self._image.add_configure_callback(self._update_image)
            self._update_image()

        if "state" in kwargs:
            self._state = kwargs.pop("state")
            self._set_cursor()
            require_redraw = True

        if "hover" in kwargs:
            self._hover = kwargs.pop("hover")

        if "command" in kwargs:
            self._command = kwargs.pop("command")
            self._set_cursor()

        if "compound" in kwargs:
            self._compound = kwargs.pop("compound")
            require_redraw = True

        if "anchor" in kwargs:
            self._anchor = kwargs.pop("anchor")
            require_redraw = True

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "corner_radius":
            return self._corner_radius
        elif attribute_name == "border_width":
            return self._border_width
        elif attribute_name == "border_spacing":
            return self._border_spacing

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
        elif attribute_name == "anchor":
            return self._anchor
        else:
            return super().cget(attribute_name)

    def _set_cursor(self):
        if self._cursor_manipulation_enabled:
            if self._state == tkinter.DISABLED:
                if sys.platform == "darwin" and self._command is not None:
                    self.configure(cursor="arrow")
                elif sys.platform.startswith("win") and self._command is not None:
                    self.configure(cursor="arrow")

            elif self._state == tkinter.NORMAL:
                if sys.platform == "darwin" and self._command is not None:
                    self.configure(cursor="pointinghand")
                elif sys.platform.startswith("win") and self._command is not None:
                    self.configure(cursor="hand2")

    def _on_enter(self, event=None):
        if self._hover is True and self._state == "normal":
            if self._hover_color is None:
                inner_parts_color = self._fg_color
            else:
                inner_parts_color = self._hover_color

            # set color of inner button parts to hover color
            self._canvas.itemconfig("inner_parts",
                                    outline=self._apply_appearance_mode(inner_parts_color),
                                    fill=self._apply_appearance_mode(inner_parts_color))

            # set text_label bg color to button hover color
            if self._text_label is not None:
                self._text_label.configure(bg=self._apply_appearance_mode(inner_parts_color))

            # set image_label bg color to button hover color
            if self._image_label is not None:
                self._image_label.configure(bg=self._apply_appearance_mode(inner_parts_color))

    def _on_leave(self, event=None):
        self._click_animation_running = False

        if self._fg_color == "transparent":
            inner_parts_color = self._bg_color
        else:
            inner_parts_color = self._fg_color

        # set color of inner button parts
        self._canvas.itemconfig("inner_parts",
                                outline=self._apply_appearance_mode(inner_parts_color),
                                fill=self._apply_appearance_mode(inner_parts_color))

        # set text_label bg color (label color)
        if self._text_label is not None:
            self._text_label.configure(bg=self._apply_appearance_mode(inner_parts_color))

        # set image_label bg color (image bg color)
        if self._image_label is not None:
            self._image_label.configure(bg=self._apply_appearance_mode(inner_parts_color))

    def _click_animation(self):
        if self._click_animation_running:
            self._on_enter()

    def _clicked(self, event=None):
        if self._state != tkinter.DISABLED:

            # click animation: change color with .on_leave() and back to normal after 100ms with click_animation()
            self._on_leave()
            self._click_animation_running = True
            self.after(100, self._click_animation)

            if self._command is not None:
                self._command()

    def invoke(self):
        """ calls command function if button is not disabled """
        if self._state != tkinter.DISABLED:
            if self._command is not None:
                return self._command()

    def bind(self, sequence: str = None, command: Callable = None, add: Union[str, bool] = True):
        """ called on the tkinter.Canvas """
        if not (add == "+" or add is True):
            raise ValueError("'add' argument can only be '+' or True to preserve internal callbacks")
        self._canvas.bind(sequence, command, add=True)

        if self._text_label is not None:
            self._text_label.bind(sequence, command, add=True)
        if self._image_label is not None:
            self._image_label.bind(sequence, command, add=True)

    def unbind(self, sequence: str = None, funcid: str = None):
        """ called on the tkinter.Label and tkinter.Canvas """
        if funcid is not None:
            raise ValueError("'funcid' argument can only be None, because there is a bug in" +
                             " tkinter and its not clear whether the internal callbacks will be unbinded or not")
        self._canvas.unbind(sequence, None)

        if self._text_label is not None:
            self._text_label.unbind(sequence, None)
        if self._image_label is not None:
            self._image_label.unbind(sequence, None)

        self._create_bindings(sequence=sequence)  # restore internal callbacks for sequence

    def focus(self):
        return self._text_label.focus()

    def focus_set(self):
        return self._text_label.focus_set()

    def focus_force(self):
        return self._text_label.focus_force()
