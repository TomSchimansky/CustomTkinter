import tkinter
import sys
from typing import Union

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
        self.dropdown_color = ThemeManager.theme["color"]["dropdown_color"] if dropdown_color == "default_theme" else dropdown_color
        self.dropdown_hover_color = ThemeManager.theme["color"]["dropdown_hover"] if dropdown_hover_color == "default_theme" else dropdown_hover_color
        self.dropdown_text_color = ThemeManager.theme["color"]["dropdown_text"] if dropdown_text_color == "default_theme" else dropdown_text_color

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["button_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = ThemeManager.theme["shape"]["entry_border_width"] if border_width == "default_theme" else border_width

        # text and font
        self.text_label = None
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.text_color_disabled = ThemeManager.theme["color"]["text_button_disabled"] if text_color_disabled == "default_theme" else text_color_disabled
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font

        # callback and hover functionality
        self.function = command
        self.variable = variable
        self.state = state
        self.hover = hover
        self.click_animation_running = False

        if values is None:
            self.values = ["CTkComboBox"]
        else:
            self.values = values

        if len(self.values) > 0:
            self.current_value = self.values[0]
        else:
            self.current_value = "CTkComboBox"

        self.dropdown_menu: Union[DropdownMenu, None] = None

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
                        padx=(self.apply_widget_scaling(max(self.corner_radius, 3)),
                              self.apply_widget_scaling(max(self._current_width - left_section_width + 3, 3))))

        self.draw()  # initial draw

        # event bindings
        self.canvas.tag_bind("right_parts", "<Enter>", self.on_enter)
        self.canvas.tag_bind("dropdown_arrow", "<Enter>", self.on_enter)
        self.canvas.tag_bind("right_parts", "<Leave>", self.on_leave)
        self.canvas.tag_bind("dropdown_arrow", "<Leave>", self.on_leave)
        self.canvas.tag_bind("right_parts", "<Button-1>", self.clicked)
        self.canvas.tag_bind("dropdown_arrow", "<Button-1>", self.clicked)
        self.bind('<Configure>', self.update_dimensions_event)

        if self.variable is not None:
            self.entry.configure(textvariable=self.variable)

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

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

        if self.current_value is not None:
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, self.current_value)

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

            self.entry.configure(fg=ThemeManager.single_color(self.text_color, self._appearance_mode))
            self.entry.configure(bg=ThemeManager.single_color(self.fg_color, self._appearance_mode))

            if self.state == tkinter.DISABLED:
                self.entry.configure(fg=(ThemeManager.single_color(self.text_color_disabled, self._appearance_mode)))
                self.canvas.itemconfig("dropdown_arrow",
                                       fill=ThemeManager.single_color(self.text_color_disabled, self._appearance_mode))
            else:
                self.entry.configure(fg=ThemeManager.single_color(self.text_color, self._appearance_mode))
                self.canvas.itemconfig("dropdown_arrow",
                                       fill=ThemeManager.single_color(self.text_color, self._appearance_mode))

    def open_dropdown_menu(self):
        self.dropdown_menu = DropdownMenu(x_position=self.winfo_rootx(),
                                          y_position=self.winfo_rooty() + self.apply_widget_scaling(self._current_height + 4),
                                          width=self._current_width,
                                          values=self.values,
                                          command=self.set,
                                          fg_color=self.dropdown_color,
                                          button_hover_color=self.dropdown_hover_color,
                                          button_color=self.dropdown_color,
                                          text_color=self.dropdown_text_color)

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "state" in kwargs:
            self.state = kwargs["state"]
            self.entry.configure(state=self.state)
            require_redraw = True
            del kwargs["state"]

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

        if "button_color" in kwargs:
            self.button_color = kwargs["button_color"]
            require_redraw = True
            del kwargs["button_color"]

        if "button_hover_color" in kwargs:
            self.button_hover_color = kwargs["button_hover_color"]
            require_redraw = True
            del kwargs["button_hover_color"]

        if "text_color" in kwargs:
            self.text_color = kwargs["text_color"]
            require_redraw = True
            del kwargs["text_color"]

        if "command" in kwargs:
            self.function = kwargs["command"]
            del kwargs["command"]

        if "variable" in kwargs:
            self.variable = kwargs["variable"]
            self.entry.configure(textvariable=self.variable)
            del kwargs["variable"]

        if "width" in kwargs:
            self.set_dimensions(width=kwargs["width"])
            del kwargs["width"]

        if "height" in kwargs:
            self.set_dimensions(height=kwargs["height"])
            del kwargs["height"]

        if "values" in kwargs:
            self.values = kwargs["values"]
            del kwargs["values"]

        super().configure(*args, **kwargs)

        if require_redraw:
            self.draw()

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
        self.click_animation_running = False

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

    def click_animation(self):
        if self.click_animation_running:
            self.on_enter()

    def set(self, value: str, from_variable_callback: bool = False):
        self.current_value = value

        self.entry.delete(0, tkinter.END)
        self.entry.insert(0, self.current_value)

        if not from_variable_callback:
            if self.function is not None:
                self.function(self.current_value)

    def get(self) -> str:
        return self.entry.get()

    def clicked(self, event=0):
        if self.state is not tkinter.DISABLED and len(self.values) > 0:
            self.open_dropdown_menu()

            # click animation: change color with .on_leave() and back to normal after 100ms with click_animation()
            self.on_leave()
            self.click_animation_running = True
            self.after(100, self.click_animation)
