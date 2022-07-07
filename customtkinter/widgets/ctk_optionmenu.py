import tkinter
import sys

from .dropdown_menu import DropdownMenu

from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..settings import Settings
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkOptionMenu(CTkBaseClass):
    def __init__(self, *args,
                 bg_color=None,
                 fg_color="default_theme",
                 button_color="default_theme",
                 button_hover_color="default_theme",
                 text_color="default_theme",
                 text_color_disabled="default_theme",
                 dropdown_color="default_theme",
                 dropdown_hover_color="default_theme",
                 dropdown_text_color="default_theme",
                 variable=None,
                 values=None,
                 command=None,
                 width=140,
                 height=28,
                 corner_radius="default_theme",
                 text_font="default_theme",
                 dropdown_text_font="default_theme",
                 hover=True,
                 state=tkinter.NORMAL,
                 dynamic_resizing=True,
                 **kwargs):

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=width, height=height, **kwargs)

        # color variables
        self.fg_color = ThemeManager.theme["color"]["button"] if fg_color == "default_theme" else fg_color
        self.button_color = ThemeManager.theme["color"]["optionmenu_button"] if button_color == "default_theme" else button_color
        self.button_hover_color = ThemeManager.theme["color"]["optionmenu_button_hover"] if button_hover_color == "default_theme" else button_hover_color

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["button_corner_radius"] if corner_radius == "default_theme" else corner_radius

        # text and font
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.text_color_disabled = ThemeManager.theme["color"]["text_button_disabled"] if text_color_disabled == "default_theme" else text_color_disabled
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font
        self.dropdown_text_font = dropdown_text_font

        # callback and hover functionality
        self.command = command
        self.variable = variable
        self.variable_callback_blocked = False
        self.variable_callback_name = None
        self.state = state
        self.hover = hover
        self.dynamic_resizing = dynamic_resizing

        if values is None:
            self.values = ["CTkOptionMenu"]
        else:
            self.values = values

        if len(self.values) > 0:
            self.current_value = self.values[0]
        else:
            self.current_value = "CTkOptionMenu"

        self.dropdown_menu = DropdownMenu(master=self,
                                          values=self.values,
                                          command=self.set,
                                          fg_color=dropdown_color,
                                          hover_color=dropdown_hover_color,
                                          text_color=dropdown_text_color,
                                          text_font=dropdown_text_font)

        # configure grid system (1x1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(self._desired_width),
                                height=self.apply_widget_scaling(self._desired_height))
        self.canvas.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew")
        self.draw_engine = DrawEngine(self.canvas)

        left_section_width = self._current_width - self._current_height
        self.text_label = tkinter.Label(master=self,
                                        font=self.apply_font_scaling(self.text_font),
                                        anchor="w",
                                        text=self.current_value)
        self.text_label.grid(row=0, column=0, sticky="w",
                             padx=(max(self.apply_widget_scaling(self.corner_radius), self.apply_widget_scaling(3)),
                                   max(self.apply_widget_scaling(self._current_width - left_section_width + 3), self.apply_widget_scaling(3))))

        if not self.dynamic_resizing:
            self.grid_propagate(0)

        if Settings.cursor_manipulation_enabled:
            if sys.platform == "darwin":
                self.configure(cursor="pointinghand")
            elif sys.platform.startswith("win"):
                self.configure(cursor="hand2")

        # event bindings
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<Button-1>", self.clicked)

        self.text_label.bind("<Enter>", self.on_enter)
        self.text_label.bind("<Leave>", self.on_leave)
        self.text_label.bind("<Button-1>", self.clicked)
        self.text_label.bind("<Button-1>", self.clicked)

        self.bind('<Configure>', self.update_dimensions_event)

        self.draw()  # initial draw

        if self.variable is not None:
            self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
            self.set(self.variable.get(), from_variable_callback=True)

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        # change label text size and grid padding
        left_section_width = self._current_width - self._current_height
        self.text_label.configure(font=self.apply_font_scaling(self.text_font))
        self.text_label.grid(row=0, column=0, sticky="w",
                             padx=(max(self.apply_widget_scaling(self.corner_radius), self.apply_widget_scaling(3)),
                                   max(self.apply_widget_scaling(self._current_width - left_section_width + 3), self.apply_widget_scaling(3))))

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width),
                              height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def set_dimensions(self, width: int = None, height: int = None):
        super().set_dimensions(width, height)

        self.canvas.configure(width=self.apply_widget_scaling(self._desired_width),
                              height=self.apply_widget_scaling(self._desired_height))
        self.draw()

    def draw(self, no_color_updates=False):
        left_section_width = self._current_width - self._current_height
        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border_vertical_split(self.apply_widget_scaling(self._current_width),
                                                                                            self.apply_widget_scaling(self._current_height),
                                                                                            self.apply_widget_scaling(self.corner_radius),
                                                                                            0,
                                                                                            self.apply_widget_scaling(left_section_width))

        requires_recoloring_2 = self.draw_engine.draw_dropdown_arrow(self.apply_widget_scaling(self._current_width - (self._current_height / 2)),
                                                                     self.apply_widget_scaling(self._current_height / 2),
                                                                     self.apply_widget_scaling(self._current_height / 3))

        if no_color_updates is False or requires_recoloring or requires_recoloring_2:

            self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

            self.canvas.itemconfig("inner_parts_left",
                                   outline=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.fg_color, self._appearance_mode))
            self.canvas.itemconfig("inner_parts_right",
                                   outline=ThemeManager.single_color(self.button_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.button_color, self._appearance_mode))

            self.text_label.configure(fg=ThemeManager.single_color(self.text_color, self._appearance_mode))

            if self.state == tkinter.DISABLED:
                self.text_label.configure(fg=(ThemeManager.single_color(self.text_color_disabled, self._appearance_mode)))
                self.canvas.itemconfig("dropdown_arrow",
                                       fill=ThemeManager.single_color(self.text_color_disabled, self._appearance_mode))
            else:
                self.text_label.configure(fg=ThemeManager.single_color(self.text_color, self._appearance_mode))
                self.canvas.itemconfig("dropdown_arrow",
                                       fill=ThemeManager.single_color(self.text_color, self._appearance_mode))

            self.text_label.configure(bg=ThemeManager.single_color(self.fg_color, self._appearance_mode))

        self.canvas.update_idletasks()

    def open_dropdown_menu(self):
        self.dropdown_menu.open(self.winfo_rootx(),
                                self.winfo_rooty() + self.apply_widget_scaling(self._current_height + 0))

    def configure(self, require_redraw=False, **kwargs):
        if "state" in kwargs:
            self.state = kwargs.pop("state")
            require_redraw = True

        if "fg_color" in kwargs:
            self.fg_color = kwargs.pop("fg_color")
            require_redraw = True

        if "button_color" in kwargs:
            self.button_color = kwargs.pop("button_color")
            require_redraw = True

        if "button_hover_color" in kwargs:
            self.button_hover_color = kwargs.pop("button_hover_color")
            require_redraw = True

        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")
            require_redraw = True

        if "command" in kwargs:
            self.command = kwargs.pop("command")

        if "variable" in kwargs:
            if self.variable is not None:  # remove old callback
                self.variable.trace_remove("write", self.variable_callback_name)

            self.variable = kwargs.pop("variable")

            if self.variable is not None and self.variable != "":
                self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
                self.set(self.variable.get(), from_variable_callback=True)
            else:
                self.variable = None

        if "width" in kwargs:
            self.set_dimensions(width=kwargs.pop("width"))

        if "height" in kwargs:
            self.set_dimensions(height=kwargs.pop("height"))

        if "values" in kwargs:
            self.values = kwargs.pop("values")
            self.dropdown_menu.configure(values=self.values)

        if "dropdown_color" in kwargs:
            self.dropdown_menu.configure(fg_color=kwargs.pop("dropdown_color"))

        if "dropdown_hover_color" in kwargs:
            self.dropdown_menu.configure(hover_color=kwargs.pop("dropdown_hover_color"))

        if "dropdown_text_color" in kwargs:
            self.dropdown_menu.configure(text_color=kwargs.pop("dropdown_text_color"))

        if "dropdown_text_font" in kwargs:
            self.dropdown_menu.configure(text_font=kwargs.pop("dropdown_text_font"))

        if "dynamic_resizing" in kwargs:
            self.dynamic_resizing = kwargs.pop("dynamic_resizing")
            if not self.dynamic_resizing:
                self.grid_propagate(0)
            else:
                self.grid_propagate(1)

        super().configure(require_redraw=require_redraw, **kwargs)

    def on_enter(self, event=0):
        if self.hover is True and self.state == tkinter.NORMAL and len(self.values) > 0:
            # set color of inner button parts to hover color
            self.canvas.itemconfig("inner_parts_right",
                                   outline=ThemeManager.single_color(self.button_hover_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.button_hover_color, self._appearance_mode))

    def on_leave(self, event=0):
        if self.hover is True:
            # set color of inner button parts
            self.canvas.itemconfig("inner_parts_right",
                                   outline=ThemeManager.single_color(self.button_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.button_color, self._appearance_mode))

    def variable_callback(self, var_name, index, mode):
        if not self.variable_callback_blocked:
            self.set(self.variable.get(), from_variable_callback=True)

    def set(self, value: str, from_variable_callback: bool = False):
        self.current_value = value

        self.text_label.configure(text=self.current_value)

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(self.current_value)
            self.variable_callback_blocked = False

        if not from_variable_callback:
            if self.command is not None:
                self.command(self.current_value)

    def get(self) -> str:
        return self.current_value

    def clicked(self, event=0):
        if self.state is not tkinter.DISABLED and len(self.values) > 0:
            self.open_dropdown_menu()
