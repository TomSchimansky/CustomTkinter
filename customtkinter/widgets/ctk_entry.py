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
                 textvariable: tkinter.Variable = None,
                 **kwargs):

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        if "master" in kwargs:
            super().__init__(*args, bg_color=bg_color, width=width, height=height, master=kwargs.pop("master"))
        else:
            super().__init__(*args, bg_color=bg_color, width=width, height=height)

        # configure grid system (1x1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # color
        self.fg_color = ThemeManager.theme["color"]["entry"] if fg_color == "default_theme" else fg_color
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.placeholder_text_color = ThemeManager.theme["color"]["entry_placeholder_text"] if placeholder_text_color == "default_theme" else placeholder_text_color
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font
        self.border_color = ThemeManager.theme["color"]["entry_border"] if border_color == "default_theme" else border_color

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["button_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = ThemeManager.theme["shape"]["entry_border_width"] if border_width == "default_theme" else border_width

        # placeholder text
        self.placeholder_text = placeholder_text
        self.placeholder_text_active = False
        self.pre_placeholder_arguments = {}  # some set arguments of the entry will be changed for placeholder and then set back

        # textvariable
        self.textvariable = textvariable

        self.state = state

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(self._current_width),
                                height=self.apply_widget_scaling(self._current_height))
        self.canvas.grid(column=0, row=0, sticky="nswe")
        self.draw_engine = DrawEngine(self.canvas)

        self.entry = tkinter.Entry(master=self,
                                   bd=0,
                                   width=1,
                                   highlightthickness=0,
                                   font=self.apply_font_scaling(self.text_font),
                                   state=self.state,
                                   textvariable=self.textvariable,
                                   **kwargs)
        self.entry.grid(column=0, row=0, sticky="nswe",
                        padx=self.apply_widget_scaling(self.corner_radius) if self.corner_radius >= 6 else self.apply_widget_scaling(6),
                        pady=(self.apply_widget_scaling(self.border_width), self.apply_widget_scaling(self.border_width + 1)))

        super().bind('<Configure>', self.update_dimensions_event)
        self.entry.bind('<FocusOut>', self.entry_focus_out)
        self.entry.bind('<FocusIn>', self.entry_focus_in)

        self.activate_placeholder()
        self.draw()

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

    def configure(self, require_redraw=False, **kwargs):
        if "state" in kwargs:
            self.state = kwargs.pop("state")
            self.entry.configure(state=self.state)

        if "fg_color" in kwargs:
            self.fg_color = kwargs.pop("fg_color")
            require_redraw = True

        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")
            require_redraw = True

        if "border_color" in kwargs:
            self.border_color = kwargs.pop("border_color")
            require_redraw = True

        if "corner_radius" in kwargs:
            self.corner_radius = kwargs.pop("corner_radius")

            if self.corner_radius * 2 > self._current_height:
                self.corner_radius = self._current_height / 2
            elif self.corner_radius * 2 > self._current_width:
                self.corner_radius = self._current_width / 2

            self.entry.grid(column=0, row=0, sticky="we", padx=self.apply_widget_scaling(self.corner_radius) if self.corner_radius >= 6 else self.apply_widget_scaling(6))
            require_redraw = True

        if "width" in kwargs:
            self.set_dimensions(width=kwargs.pop("width"))

        if "height" in kwargs:
            self.set_dimensions(height=kwargs.pop("height"))

        if "placeholder_text" in kwargs:
            self.placeholder_text = kwargs.pop("placeholder_text")
            if self.placeholder_text_active:
                self.entry.delete(0, tkinter.END)
                self.entry.insert(0, self.placeholder_text)
            else:
                self.activate_placeholder()

        if "placeholder_text_color" in kwargs:
            self.placeholder_text_color = kwargs.pop("placeholder_text_color")
            require_redraw = True

        if "textvariable" in kwargs:
            self.textvariable = kwargs.pop("textvariable")
            self.entry.configure(textvariable=self.textvariable)

        if "text_font" in kwargs:
            self.text_font = kwargs.pop("text_font")
            self.entry.configure(font=self.apply_font_scaling(self.text_font))

        if "show" in kwargs:
            if self.placeholder_text_active:
                self.pre_placeholder_arguments["show"] = kwargs.pop("show")
            else:
                self.entry.configure(show=kwargs.pop("show"))

        if "bg_color" in kwargs:
            super().configure(bg_color=kwargs.pop("bg_color"), require_redraw=require_redraw)
        else:
            super().configure(require_redraw=require_redraw)

        self.entry.configure(**kwargs)  # pass remaining kwargs to entry

    def activate_placeholder(self):
        if self.entry.get() == "" and self.placeholder_text is not None and (self.textvariable is None or self.textvariable == ""):
            self.placeholder_text_active = True

            self.pre_placeholder_arguments = {"show": self.entry.cget("show")}
            self.entry.config(fg=ThemeManager.single_color(self.placeholder_text_color, self._appearance_mode), show="")
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, self.placeholder_text)

    def deactivate_placeholder(self):
        if self.placeholder_text_active:
            self.placeholder_text_active = False

            self.entry.config(fg=ThemeManager.single_color(self.text_color, self._appearance_mode))
            self.entry.delete(0, tkinter.END)
            for argument, value in self.pre_placeholder_arguments.items():
                self.entry[argument] = value

    def entry_focus_out(self, event=None):
        self.activate_placeholder()

    def entry_focus_in(self, event=None):
        self.deactivate_placeholder()

    def delete(self, *args, **kwargs):
        self.entry.delete(*args, **kwargs)

        if self.entry.get() == "":
            self.activate_placeholder()

    def insert(self, *args, **kwargs):
        self.deactivate_placeholder()

        return self.entry.insert(*args, **kwargs)

    def get(self):
        if self.placeholder_text_active:
            return ""
        else:
            return self.entry.get()

    def focus(self):
        self.entry.focus()

    def focus_force(self):
        self.entry.focus_force()
