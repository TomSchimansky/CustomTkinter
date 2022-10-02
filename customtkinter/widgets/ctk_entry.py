import tkinter
from typing import Union, Tuple

from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkEntry(CTkBaseClass):
    """
    Entry with rounded corners, border, textvariable support, focus and placeholder.
    For detailed information check out the documentation.
    """

    def __init__(self, *args,
                 bg_color: Union[str, Tuple[str, str], None] = None,
                 fg_color: Union[str, Tuple[str, str], None] = "default_theme",
                 text_color: Union[str, Tuple[str, str]] = "default_theme",
                 placeholder_text_color: Union[str, Tuple[str, str]] = "default_theme",
                 text_font: Union[str, Tuple[str, str]] = "default_theme",
                 placeholder_text: str = None,
                 corner_radius: int = "default_theme",
                 border_width: int = "default_theme",
                 border_color: Union[str, Tuple[str, str]] = "default_theme",
                 width: int = 140,
                 height: int = 28,
                 state: str = tkinter.NORMAL,
                 textvariable: tkinter.Variable = None,
                 **kwargs):

        # transfer basic functionality (_bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        if "master" in kwargs:
            super().__init__(*args, bg_color=bg_color, width=width, height=height, master=kwargs.pop("master"))
        else:
            super().__init__(*args, bg_color=bg_color, width=width, height=height)

        # configure grid system (1x1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # color
        self._fg_color = ThemeManager.theme["color"]["entry"] if fg_color == "default_theme" else fg_color
        self._text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self._placeholder_text_color = ThemeManager.theme["color"]["entry_placeholder_text"] if placeholder_text_color == "default_theme" else placeholder_text_color
        self._text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font
        self._border_color = ThemeManager.theme["color"]["entry_border"] if border_color == "default_theme" else border_color

        # shape
        self._corner_radius = ThemeManager.theme["shape"]["button_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self._border_width = ThemeManager.theme["shape"]["entry_border_width"] if border_width == "default_theme" else border_width

        # placeholder text
        self._is_focused: bool = True
        self._placeholder_text = placeholder_text
        self._placeholder_text_active = False
        self._pre_placeholder_arguments = {}  # some set arguments of the entry will be changed for placeholder and then set back

        # textvariable
        self._textvariable = textvariable
        self._state = state

        self._canvas = CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._current_width),
                                 height=self._apply_widget_scaling(self._current_height))
        self._canvas.grid(column=0, row=0, sticky="nswe")
        self._draw_engine = DrawEngine(self._canvas)

        self._entry = tkinter.Entry(master=self,
                                    bd=0,
                                    width=1,
                                    highlightthickness=0,
                                    font=self._apply_font_scaling(self._text_font),
                                    state=self._state,
                                    textvariable=self._textvariable,
                                    **kwargs)
        self._entry.grid(column=0, row=0, sticky="nswe",
                         padx=self._apply_widget_scaling(self._corner_radius) if self._corner_radius >= 6 else self._apply_widget_scaling(6),
                         pady=(self._apply_widget_scaling(self._border_width), self._apply_widget_scaling(self._border_width + 1)))

        super().bind('<Configure>', self._update_dimensions_event)
        self._entry.bind('<FocusOut>', self._entry_focus_out)
        self._entry.bind('<FocusIn>', self._entry_focus_in)

        self._activate_placeholder()
        self._draw()

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        self._entry.configure(font=self._apply_font_scaling(self._text_font))
        self._entry.grid(column=0, row=0, sticky="we",
                         padx=self._apply_widget_scaling(self._corner_radius) if self._corner_radius >= 6 else self._apply_widget_scaling(6))

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width), height=self._apply_widget_scaling(self._desired_height))
        self._draw()

    def _set_dimensions(self, width=None, height=None):
        super()._set_dimensions(width, height)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw()

    def _draw(self, no_color_updates=False):
        self._canvas.configure(bg=ThemeManager.single_color(self._bg_color, self._appearance_mode))

        requires_recoloring = self._draw_engine.draw_rounded_rect_with_border(self._apply_widget_scaling(self._current_width),
                                                                              self._apply_widget_scaling(self._current_height),
                                                                              self._apply_widget_scaling(self._corner_radius),
                                                                              self._apply_widget_scaling(self._border_width))

        if requires_recoloring or no_color_updates is False:
            if ThemeManager.single_color(self._fg_color, self._appearance_mode) is not None:
                self._canvas.itemconfig("inner_parts",
                                        fill=ThemeManager.single_color(self._fg_color, self._appearance_mode),
                                        outline=ThemeManager.single_color(self._fg_color, self._appearance_mode))
                self._entry.configure(bg=ThemeManager.single_color(self._fg_color, self._appearance_mode),
                                      disabledbackground=ThemeManager.single_color(self._fg_color, self._appearance_mode),
                                      highlightcolor=ThemeManager.single_color(self._fg_color, self._appearance_mode),
                                      fg=ThemeManager.single_color(self._text_color, self._appearance_mode),
                                      disabledforeground=ThemeManager.single_color(self._text_color, self._appearance_mode),
                                      insertbackground=ThemeManager.single_color(self._text_color, self._appearance_mode))
            else:
                self._canvas.itemconfig("inner_parts",
                                        fill=ThemeManager.single_color(self._bg_color, self._appearance_mode),
                                        outline=ThemeManager.single_color(self._bg_color, self._appearance_mode))
                self._entry.configure(bg=ThemeManager.single_color(self._bg_color, self._appearance_mode),
                                      disabledbackground=ThemeManager.single_color(self._bg_color, self._appearance_mode),
                                      highlightcolor=ThemeManager.single_color(self._bg_color, self._appearance_mode),
                                      fg=ThemeManager.single_color(self._text_color, self._appearance_mode),
                                      disabledforeground=ThemeManager.single_color(self._text_color, self._appearance_mode),
                                      insertbackground=ThemeManager.single_color(self._text_color, self._appearance_mode))

            self._canvas.itemconfig("border_parts",
                                    fill=ThemeManager.single_color(self._border_color, self._appearance_mode),
                                    outline=ThemeManager.single_color(self._border_color, self._appearance_mode))

            if self._placeholder_text_active:
                self._entry.config(fg=ThemeManager.single_color(self._placeholder_text_color, self._appearance_mode))

    def bind(self, *args, **kwargs):
        self._entry.bind(*args, **kwargs)

    def configure(self, require_redraw=False, **kwargs):
        if "state" in kwargs:
            self._state = kwargs.pop("state")
            self._entry.configure(state=self._state)

        if "fg_color" in kwargs:
            self._fg_color = kwargs.pop("fg_color")
            require_redraw = True

        if "text_color" in kwargs:
            self._text_color = kwargs.pop("text_color")
            require_redraw = True

        if "border_color" in kwargs:
            self._border_color = kwargs.pop("border_color")
            require_redraw = True

        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")

            if self._corner_radius * 2 > self._current_height:
                self._corner_radius = self._current_height / 2
            elif self._corner_radius * 2 > self._current_width:
                self._corner_radius = self._current_width / 2

            self._entry.grid(column=0, row=0, sticky="we", padx=self._apply_widget_scaling(self._corner_radius) if self._corner_radius >= 6 else self._apply_widget_scaling(6))
            require_redraw = True

        if "width" in kwargs:
            self._set_dimensions(width=kwargs.pop("width"))

        if "height" in kwargs:
            self._set_dimensions(height=kwargs.pop("height"))

        if "placeholder_text" in kwargs:
            self._placeholder_text = kwargs.pop("placeholder_text")
            if self._placeholder_text_active:
                self._entry.delete(0, tkinter.END)
                self._entry.insert(0, self._placeholder_text)
            else:
                self._activate_placeholder()

        if "placeholder_text_color" in kwargs:
            self._placeholder_text_color = kwargs.pop("placeholder_text_color")
            require_redraw = True

        if "textvariable" in kwargs:
            self._textvariable = kwargs.pop("textvariable")
            self._entry.configure(textvariable=self._textvariable)

        if "text_font" in kwargs:
            self._text_font = kwargs.pop("text_font")
            self._entry.configure(font=self._apply_font_scaling(self._text_font))

        if "show" in kwargs:
            if self._placeholder_text_active:
                self._pre_placeholder_arguments["show"] = kwargs.pop("show")
            else:
                self._entry.configure(show=kwargs.pop("show"))

        if "_bg_color" in kwargs:
            super().configure(bg_color=kwargs.pop("_bg_color"), require_redraw=require_redraw)
        else:
            super().configure(require_redraw=require_redraw)

        self._entry.configure(**kwargs)  # pass remaining kwargs to entry

    def _activate_placeholder(self):
        if self._entry.get() == "" and self._placeholder_text is not None and (self._textvariable is None or self._textvariable == ""):
            self._placeholder_text_active = True

            self._pre_placeholder_arguments = {"show": self._entry.cget("show")}
            self._entry.config(fg=ThemeManager.single_color(self._placeholder_text_color, self._appearance_mode), show="")
            self._entry.delete(0, tkinter.END)
            self._entry.insert(0, self._placeholder_text)

    def _deactivate_placeholder(self):
        if self._placeholder_text_active:
            self._placeholder_text_active = False

            self._entry.config(fg=ThemeManager.single_color(self._text_color, self._appearance_mode))
            self._entry.delete(0, tkinter.END)
            for argument, value in self._pre_placeholder_arguments.items():
                self._entry[argument] = value

    def _entry_focus_out(self, event=None):
        self._activate_placeholder()
        self._is_focused = False

    def _entry_focus_in(self, event=None):
        self._deactivate_placeholder()
        self._is_focused = True

    def delete(self, *args, **kwargs):
        self._entry.delete(*args, **kwargs)

        if not self._is_focused and self._entry.get() == "":
            self._activate_placeholder()

    def insert(self, *args, **kwargs):
        self._deactivate_placeholder()

        return self._entry.insert(*args, **kwargs)

    def get(self):
        if self._placeholder_text_active:
            return ""
        else:
            return self._entry.get()

    def focus(self):
        self._entry.focus()

    def focus_force(self):
        self._entry.focus_force()
