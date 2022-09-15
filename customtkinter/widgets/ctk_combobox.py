import tkinter
import sys

from .dropdown_menu import DropdownMenu
from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..settings import Settings
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkComboBox(CTkBaseClass):
    def __init__(self, *args,
                 bg_color=None,
                 fg_color="default_theme",
                 border_color="default_theme",
                 button_color="default_theme",
                 button_hover_color="default_theme",
                 dropdown_color="default_theme",
                 dropdown_hover_color="default_theme",
                 dropdown_text_color="default_theme",
                 variable=None,
                 values=None,
                 command=None,
                 width=140,
                 height=28,
                 corner_radius="default_theme",
                 border_width="default_theme",
                 text_font="default_theme",
                 dropdown_text_font="default_theme",
                 text_color="default_theme",
                 text_color_disabled="default_theme",
                 hover=True,
                 state=tkinter.NORMAL,
                 **kwargs):

        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=width, height=height, **kwargs)

        # color variables
        self.fg_color = ThemeManager.theme["color"]["entry"] if fg_color == "default_theme" else fg_color
        self.border_color = ThemeManager.theme["color"]["combobox_border"] if border_color == "default_theme" else border_color
        self.button_color = ThemeManager.theme["color"]["combobox_border"] if button_color == "default_theme" else button_color
        self.button_hover_color = ThemeManager.theme["color"]["combobox_button_hover"] if button_hover_color == "default_theme" else button_hover_color

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["button_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = ThemeManager.theme["shape"]["entry_border_width"] if border_width == "default_theme" else border_width

        # text and font
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.text_color_disabled = ThemeManager.theme["color"]["text_button_disabled"] if text_color_disabled == "default_theme" else text_color_disabled
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font

        # callback and hover functionality
        self.command = command
        self.textvariable = variable
        self.state = state
        self.hover = hover

        if values is None:
            self.values = ["CTkComboBox"]
        else:
            self.values = values

        self.dropdown_menu = DropdownMenu(master=self,
                                          values=self.values,
                                          command=self.dropdown_callback,
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

        self.entry = tkinter.Entry(master=self,
                                   state=self.state,
                                   width=1,
                                   bd=0,
                                   highlightthickness=0,
                                   font=self.apply_font_scaling(self.text_font))
        left_section_width = self._current_width - self._current_height
        self.entry.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="ew",
                        padx=(max(self.apply_widget_scaling(self.corner_radius), self.apply_widget_scaling(3)),
                              max(self.apply_widget_scaling(self._current_width - left_section_width + 3), self.apply_widget_scaling(3))))

        # insert default value
        if len(self.values) > 0:
            self.entry.insert(0, self.values[0])
        else:
            self.entry.insert(0, "CTkComboBox")

        self.draw()  # initial draw

        # event bindings
        self.canvas.tag_bind("right_parts", "<Enter>", self.on_enter)
        self.canvas.tag_bind("dropdown_arrow", "<Enter>", self.on_enter)
        self.canvas.tag_bind("right_parts", "<Leave>", self.on_leave)
        self.canvas.tag_bind("dropdown_arrow", "<Leave>", self.on_leave)
        self.canvas.tag_bind("right_parts", "<Button-1>", self.clicked)
        self.canvas.tag_bind("dropdown_arrow", "<Button-1>", self.clicked)
        self.bind('<Configure>', self.update_dimensions_event)

        if self.textvariable is not None:
            self.entry.configure(textvariable=self.textvariable)

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        # change entry font size and grid padding
        left_section_width = self._current_width - self._current_height
        self.entry.configure(font=self.apply_font_scaling(self.text_font))
        self.entry.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="ew",
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
                                                                                            self.apply_widget_scaling(self.border_width),
                                                                                            self.apply_widget_scaling(left_section_width))

        requires_recoloring_2 = self.draw_engine.draw_dropdown_arrow(self.apply_widget_scaling(self._current_width - (self._current_height / 2)),
                                                                     self.apply_widget_scaling(self._current_height / 2),
                                                                     self.apply_widget_scaling(self._current_height / 3))

        if no_color_updates is False or requires_recoloring or requires_recoloring_2:

            self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

            self.canvas.itemconfig("inner_parts_left",
                                   outline=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.fg_color, self._appearance_mode))
            self.canvas.itemconfig("border_parts_left",
                                   outline=ThemeManager.single_color(self.border_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.border_color, self._appearance_mode))
            self.canvas.itemconfig("inner_parts_right",
                                   outline=ThemeManager.single_color(self.border_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.border_color, self._appearance_mode))
            self.canvas.itemconfig("border_parts_right",
                                   outline=ThemeManager.single_color(self.border_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.border_color, self._appearance_mode))

            self.entry.configure(bg=ThemeManager.single_color(self.fg_color, self._appearance_mode),
                                 fg=ThemeManager.single_color(self.text_color, self._appearance_mode),
                                 disabledforeground=ThemeManager.single_color(self.text_color_disabled, self._appearance_mode),
                                 disabledbackground=ThemeManager.single_color(self.fg_color, self._appearance_mode))

            if self.state == tkinter.DISABLED:
                self.canvas.itemconfig("dropdown_arrow",
                                       fill=ThemeManager.single_color(self.text_color_disabled, self._appearance_mode))
            else:
                self.canvas.itemconfig("dropdown_arrow",
                                       fill=ThemeManager.single_color(self.text_color, self._appearance_mode))

    def open_dropdown_menu(self):
        self.dropdown_menu.open(self.winfo_rootx(),
                                self.winfo_rooty() + self.apply_widget_scaling(self._current_height + 0))

    def configure(self, require_redraw=False, **kwargs):
        if "state" in kwargs:
            self.state = kwargs.pop("state")
            self.entry.configure(state=self.state)
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

        if "text_font" in kwargs:
            self.text_font = kwargs.pop("text_font")
            self.entry.configure(font=self.apply_font_scaling(self.text_font))

        if "command" in kwargs:
            self.command = kwargs.pop("command")

        if "variable" in kwargs:
            self.textvariable = kwargs.pop("variable")
            self.entry.configure(textvariable=self.textvariable)

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

        super().configure(require_redraw=require_redraw, **kwargs)

    def on_enter(self, event=0):
        if self.hover is True and self.state == tkinter.NORMAL and len(self.values) > 0:
            if sys.platform == "darwin" and len(self.values) > 0 and Settings.cursor_manipulation_enabled:
                self.canvas.configure(cursor="pointinghand")
            elif sys.platform.startswith("win") and len(self.values) > 0 and Settings.cursor_manipulation_enabled:
                self.canvas.configure(cursor="hand2")

            # set color of inner button parts to hover color
            self.canvas.itemconfig("inner_parts_right",
                                   outline=ThemeManager.single_color(self.button_hover_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.button_hover_color, self._appearance_mode))
            self.canvas.itemconfig("border_parts_right",
                                   outline=ThemeManager.single_color(self.button_hover_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.button_hover_color, self._appearance_mode))

    def on_leave(self, event=0):
        if self.hover is True:
            if sys.platform == "darwin" and len(self.values) > 0 and Settings.cursor_manipulation_enabled:
                self.canvas.configure(cursor="arrow")
            elif sys.platform.startswith("win") and len(self.values) > 0 and Settings.cursor_manipulation_enabled:
                self.canvas.configure(cursor="arrow")

            # set color of inner button parts
            self.canvas.itemconfig("inner_parts_right",
                                   outline=ThemeManager.single_color(self.button_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.button_color, self._appearance_mode))
            self.canvas.itemconfig("border_parts_right",
                                   outline=ThemeManager.single_color(self.button_color, self._appearance_mode),
                                   fill=ThemeManager.single_color(self.button_color, self._appearance_mode))

    def dropdown_callback(self, value: str):
        if self.state == "readonly":
            self.entry.configure(state="normal")
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, value)
            self.entry.configure(state="readonly")
        else:
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, value)

        if self.command is not None:
            self.command(value)

    def set(self, value: str):
        if self.state == "readonly":
            self.entry.configure(state="normal")
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, value)
            self.entry.configure(state="readonly")
        else:
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, value)

    def get(self) -> str:
        return self.entry.get()

    def clicked(self, event=0):
        if self.state is not tkinter.DISABLED and len(self.values) > 0:
            self.open_dropdown_menu()
