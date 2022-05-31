import tkinter

from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkEntry(CTkBaseClass):
    def __init__(self, *args,
                 bg_color=None,
                 fg_color="default_theme",
                 text_color="default_theme",
                 placeholder_text_color="default_theme",
                 text_font="default_theme",
                 placeholder_text=None,
                 corner_radius="default_theme",
                 border_width="default_theme",
                 border_color="default_theme",
                 width=140,
                 height=28,
                 state=tkinter.NORMAL,
                 **kwargs):

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        if "master" in kwargs:
            super().__init__(*args, bg_color=bg_color, width=width, height=height, master=kwargs["master"])
            del kwargs["master"]
        else:
            super().__init__(*args, bg_color=bg_color, width=width, height=height)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.fg_color = ThemeManager.theme["color"]["entry"] if fg_color == "default_theme" else fg_color
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.placeholder_text_color = ThemeManager.theme["color"]["entry_placeholder_text"] if placeholder_text_color == "default_theme" else placeholder_text_color
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font
        self.border_color = ThemeManager.theme["color"]["entry_border"] if border_color == "default_theme" else border_color

        self.placeholder_text = placeholder_text
        self.placeholder_text_active = False
        self.pre_placeholder_arguments = {}  # some set arguments of the entry will be changed for placeholder and then set back

        self.state = state

        self.corner_radius = ThemeManager.theme["shape"]["button_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = ThemeManager.theme["shape"]["entry_border_width"] if border_width == "default_theme" else border_width

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(self._current_width),
                                height=self.apply_widget_scaling(self._current_height))
        self.canvas.grid(column=0, row=0, sticky="we")
        self.draw_engine = DrawEngine(self.canvas)

        self.entry = tkinter.Entry(master=self,
                                   bd=0,
                                   width=1,
                                   highlightthickness=0,
                                   font=self.apply_font_scaling(self.text_font),
                                   state=self.state,
                                   **kwargs)
        self.entry.grid(column=0, row=0, sticky="we",
                        padx=self.apply_widget_scaling(self.corner_radius) if self.corner_radius >= 6 else self.apply_widget_scaling(6))

        super().bind('<Configure>', self.update_dimensions_event)
        self.entry.bind('<FocusOut>', self.set_placeholder)
        self.entry.bind('<FocusIn>', self.clear_placeholder)

        self.draw()
        self.set_placeholder()

    def set_scaling(self, *args, **kwargs):
        super().set_scaling( *args, **kwargs)

        self.entry.configure(font=self.apply_font_scaling(self.text_font))
        self.entry.grid(column=0, row=0, sticky="we",
                        padx=self.apply_widget_scaling(self.corner_radius) if self.corner_radius >= 6 else self.apply_widget_scaling(6))

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width), height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def set_dimensions(self, width=None, height=None):
        super().set_dimensions(width, height)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width),
                              height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def set_placeholder(self, event=None):
        if self.placeholder_text is not None:
            if not self.placeholder_text_active and self.entry.get() == "":
                self.placeholder_text_active = True
                self.pre_placeholder_arguments = {"show": self.entry.cget("show")}
                self.entry.config(fg=ThemeManager.single_color(self.placeholder_text_color, self._appearance_mode), show="")
                self.entry.delete(0, tkinter.END)
                self.entry.insert(0, self.placeholder_text)

    def clear_placeholder(self, event=None):
        if self.placeholder_text_active:
            self.placeholder_text_active = False
            self.entry.config(fg=ThemeManager.single_color(self.text_color, self._appearance_mode))
            self.entry.delete(0, tkinter.END)
            for argument, value in self.pre_placeholder_arguments.items():
                self.entry[argument] = value

    def draw(self, no_color_updates=False):
        self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border(self.apply_widget_scaling(self._current_width),
                                                                             self.apply_widget_scaling(self._current_height),
                                                                             self.apply_widget_scaling(self.corner_radius),
                                                                             self.apply_widget_scaling(self.border_width))

        if requires_recoloring or no_color_updates is False:
            if ThemeManager.single_color(self.fg_color, self._appearance_mode) is not None:
                self.canvas.itemconfig("inner_parts",
                                       fill=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.fg_color, self._appearance_mode))
                self.entry.configure(bg=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                     disabledbackground=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                     highlightcolor=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                     fg=ThemeManager.single_color(self.text_color, self._appearance_mode),
                                     disabledforeground=ThemeManager.single_color(self.text_color, self._appearance_mode),
                                     insertbackground=ThemeManager.single_color(self.text_color, self._appearance_mode))
            else:
                self.canvas.itemconfig("inner_parts",
                                       fill=ThemeManager.single_color(self.bg_color, self._appearance_mode),
                                       outline=ThemeManager.single_color(self.bg_color, self._appearance_mode))
                self.entry.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode),
                                     disabledbackground=ThemeManager.single_color(self.bg_color, self._appearance_mode),
                                     highlightcolor=ThemeManager.single_color(self.bg_color, self._appearance_mode),
                                     fg=ThemeManager.single_color(self.text_color, self._appearance_mode),
                                     disabledforeground=ThemeManager.single_color(self.text_color, self._appearance_mode),
                                     insertbackground=ThemeManager.single_color(self.text_color, self._appearance_mode))

            self.canvas.itemconfig("border_parts",
                                   fill=ThemeManager.single_color(self.border_color, self._appearance_mode),
                                   outline=ThemeManager.single_color(self.border_color, self._appearance_mode))

            if self.placeholder_text_active:
                self.entry.config(fg=ThemeManager.single_color(self.placeholder_text_color, self._appearance_mode))

    def bind(self, *args, **kwargs):
        self.entry.bind(*args, **kwargs)

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "state" in kwargs:
            self.state = kwargs["state"]
            self.entry.configure(state=self.state)
            del kwargs["state"]

        if "bg_color" in kwargs:
            if kwargs["bg_color"] is None:
                self.bg_color = self.detect_color_of_master()
            else:
                self.bg_color = kwargs["bg_color"]
            require_redraw = True
            del kwargs["bg_color"]

        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            del kwargs["fg_color"]
            require_redraw = True

        if "text_color" in kwargs:
            self.text_color = kwargs["text_color"]
            del kwargs["text_color"]
            require_redraw = True

        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
            del kwargs["border_color"]
            require_redraw = True

        if "corner_radius" in kwargs:
            self.corner_radius = kwargs["corner_radius"]

            if self.corner_radius * 2 > self._current_height:
                self.corner_radius = self._current_height / 2
            elif self.corner_radius * 2 > self._current_width:
                self.corner_radius = self._current_width / 2

            self.entry.grid(column=0, row=0, sticky="we", padx=self.apply_widget_scaling(self.corner_radius) if self.corner_radius >= 6 else self.apply_widget_scaling(6))
            del kwargs["corner_radius"]
            require_redraw = True

        if "width" in kwargs:
            self.set_dimensions(width=kwargs["width"])
            del kwargs["width"]

        if "height" in kwargs:
            self.set_dimensions(height=kwargs["height"])
            del kwargs["height"]

        if "placeholder_text" in kwargs:
            pass

        self.entry.configure(*args, **kwargs)

        if require_redraw is True:
            self.draw()

    def delete(self, *args, **kwargs):
        self.entry.delete(*args, **kwargs)
        self.set_placeholder()

    def insert(self, *args, **kwargs):
        self.clear_placeholder()
        return self.entry.insert(*args, **kwargs)

    def get(self):
        if self.placeholder_text_active:
            return ""
        else:
            return self.entry.get()
