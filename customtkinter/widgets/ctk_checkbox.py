import tkinter
import sys

from .ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from ..settings import Settings
from ..draw_engine import DrawEngine
from .widget_base_class import CTkBaseClass


class CTkCheckBox(CTkBaseClass):
    """ tkinter custom checkbox with border, rounded corners and hover effect """

    def __init__(self, *args,
                 bg_color=None,
                 fg_color="default_theme",
                 hover_color="default_theme",
                 border_color="default_theme",
                 border_width="default_theme",
                 checkmark_color="default_theme",
                 width=24,
                 height=24,
                 corner_radius="default_theme",
                 text_font="default_theme",
                 text_color="default_theme",
                 text="CTkCheckBox",
                 text_color_disabled="default_theme",
                 hover=True,
                 command=None,
                 state=tkinter.NORMAL,
                 onvalue=1,
                 offvalue=0,
                 variable=None,
                 textvariable=None,
                 **kwargs):

        # transfer basic functionality (bg_color, size, appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=width, height=height, **kwargs)

        # color
        self.fg_color = ThemeManager.theme["color"]["button"] if fg_color == "default_theme" else fg_color
        self.hover_color = ThemeManager.theme["color"]["button_hover"] if hover_color == "default_theme" else hover_color
        self.border_color = ThemeManager.theme["color"]["checkbox_border"] if border_color == "default_theme" else border_color
        self.checkmark_color = ThemeManager.theme["color"]["checkmark"] if checkmark_color == "default_theme" else checkmark_color

        # shape
        self.corner_radius = ThemeManager.theme["shape"]["checkbox_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = ThemeManager.theme["shape"]["checkbox_border_width"] if border_width == "default_theme" else border_width

        # text
        self.text = text
        self.text_label = None
        self.text_color = ThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.text_color_disabled = ThemeManager.theme["color"]["text_disabled"] if text_color_disabled == "default_theme" else text_color_disabled
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font

        # callback and hover functionality
        self.function = command
        self.state = state
        self.hover = hover
        self.check_state = False
        self.onvalue = onvalue
        self.offvalue = offvalue
        self.variable: tkinter.Variable = variable
        self.variable_callback_blocked = False
        self.textvariable = textvariable
        self.variable_callback_name = None

        # configure grid system (1x3)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0, minsize=self.apply_widget_scaling(6))
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.bg_canvas = CTkCanvas(master=self,
                                   highlightthickness=0,
                                   width=self.apply_widget_scaling(self.desired_width),
                                   height=self.apply_widget_scaling(self.desired_height))
        self.bg_canvas.grid(row=0, column=0, padx=0, pady=0, columnspan=3, rowspan=1, sticky="nswe")

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.apply_widget_scaling(self.desired_width),
                                height=self.apply_widget_scaling(self.desired_height))
        self.canvas.grid(row=0, column=0, padx=0, pady=0, columnspan=1, rowspan=1)
        self.draw_engine = DrawEngine(self.canvas)

        if self.hover is True:
            self.canvas.bind("<Enter>", self.on_enter)
            self.canvas.bind("<Leave>", self.on_leave)

        self.canvas.bind("<Button-1>", self.toggle)
        self.canvas.bind("<Button-1>", self.toggle)

        # set select state according to variable
        if self.variable is not None:
            self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
            if self.variable.get() == self.onvalue:
                self.select(from_variable_callback=True)
            elif self.variable.get() == self.offvalue:
                self.deselect(from_variable_callback=True)

        self.set_cursor()
        self.draw()  # initial draw

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        self.grid_columnconfigure(1, weight=0, minsize=self.apply_widget_scaling(6))
        self.text_label.configure(font=self.apply_font_scaling(self.text_font))

        self.bg_canvas.configure(width=self.apply_widget_scaling(self.desired_width), height=self.apply_widget_scaling(self.desired_height))
        self.canvas.configure(width=self.apply_widget_scaling(self.desired_width), height=self.apply_widget_scaling(self.desired_height))
        self.draw()

    def destroy(self):
        if self.variable is not None:
            self.variable.trace_remove("write", self.variable_callback_name)

        super().destroy()

    def draw(self, no_color_updates=False):
        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border(self.apply_widget_scaling(self.current_width),
                                                                             self.apply_widget_scaling(self.current_height),
                                                                             self.apply_widget_scaling(self.corner_radius),
                                                                             self.apply_widget_scaling(self.border_width))

        if self.check_state is True:
            self.draw_engine.draw_checkmark(self.apply_widget_scaling(self.current_width),
                                            self.apply_widget_scaling(self.current_height),
                                            self.apply_widget_scaling(self.current_height * 0.58))
        else:
            self.canvas.delete("checkmark")

        self.bg_canvas.configure(bg=ThemeManager.single_color(self.bg_color, self.appearance_mode))
        self.canvas.configure(bg=ThemeManager.single_color(self.bg_color, self.appearance_mode))

        if self.check_state is True:
            self.canvas.itemconfig("inner_parts",
                                   outline=ThemeManager.single_color(self.fg_color, self.appearance_mode),
                                   fill=ThemeManager.single_color(self.fg_color, self.appearance_mode))
            self.canvas.itemconfig("border_parts",
                                   outline=ThemeManager.single_color(self.fg_color, self.appearance_mode),
                                   fill=ThemeManager.single_color(self.fg_color, self.appearance_mode))

            if "create_line" in self.canvas.gettags("checkmark"):
                self.canvas.itemconfig("checkmark", fill=ThemeManager.single_color(self.checkmark_color, self.appearance_mode))
            else:
                self.canvas.itemconfig("checkmark", fill=ThemeManager.single_color(self.checkmark_color, self.appearance_mode))
        else:
            self.canvas.itemconfig("inner_parts",
                                   outline=ThemeManager.single_color(self.bg_color, self.appearance_mode),
                                   fill=ThemeManager.single_color(self.bg_color, self.appearance_mode))
            self.canvas.itemconfig("border_parts",
                                   outline=ThemeManager.single_color(self.border_color, self.appearance_mode),
                                   fill=ThemeManager.single_color(self.border_color, self.appearance_mode))

        if self.text_label is None:
            self.text_label = tkinter.Label(master=self,
                                            bd=0,
                                            text=self.text,
                                            justify=tkinter.LEFT,
                                            font=self.apply_font_scaling(self.text_font))
            self.text_label.grid(row=0, column=2, padx=0, pady=0, sticky="w")
            self.text_label["anchor"] = "w"

        if self.state == tkinter.DISABLED:
            self.text_label.configure(fg=(ThemeManager.single_color(self.text_color_disabled, self.appearance_mode)))
        else:
            self.text_label.configure(fg=ThemeManager.single_color(self.text_color, self.appearance_mode))
        self.text_label.configure(bg=ThemeManager.single_color(self.bg_color, self.appearance_mode))

        self.set_text(self.text)

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw()

        if "text" in kwargs:
            self.set_text(kwargs["text"])
            del kwargs["text"]

        if "state" in kwargs:
            self.state = kwargs["state"]
            self.set_cursor()
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

        if "hover_color" in kwargs:
            self.hover_color = kwargs["hover_color"]
            require_redraw = True
            del kwargs["hover_color"]

        if "text_color" in kwargs:
            self.text_color = kwargs["text_color"]
            require_redraw = True
            del kwargs["text_color"]

        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
            require_redraw = True
            del kwargs["border_color"]

        if "command" in kwargs:
            self.function = kwargs["command"]
            del kwargs["command"]

        if "variable" in kwargs:
            if self.variable is not None:
                self.variable.trace_remove("write", self.variable_callback_name)

            self.variable = kwargs["variable"]

            if self.variable is not None and self.variable != "":
                self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
                if self.variable.get() == self.onvalue:
                    self.select(from_variable_callback=True)
                elif self.variable.get() == self.offvalue:
                    self.deselect(from_variable_callback=True)
            else:
                self.variable = None

            del kwargs["variable"]

        super().configure(*args, **kwargs)

        if require_redraw:
            self.draw()

    def set_cursor(self):
        if Settings.cursor_manipulation_enabled:
            if self.state == tkinter.DISABLED:
                if sys.platform == "darwin" and Settings.cursor_manipulation_enabled:
                    self.canvas.configure(cursor="arrow")
                elif sys.platform.startswith("win") and Settings.cursor_manipulation_enabled:
                    self.canvas.configure(cursor="arrow")

            elif self.state == tkinter.NORMAL:
                if sys.platform == "darwin" and Settings.cursor_manipulation_enabled:
                    self.canvas.configure(cursor="pointinghand")
                elif sys.platform.startswith("win") and Settings.cursor_manipulation_enabled:
                    self.canvas.configure(cursor="hand2")

    def set_text(self, text):
        self.text = text
        if self.text_label is not None:
            self.text_label.configure(text=self.text)
        else:
            sys.stderr.write("ERROR (CTkButton): Cant change text because checkbox has no text.")

    def on_enter(self, event=0):
        if self.hover is True and self.state == tkinter.NORMAL:
            if self.check_state is True:
                self.canvas.itemconfig("inner_parts",
                                       fill=ThemeManager.single_color(self.hover_color, self.appearance_mode),
                                       outline=ThemeManager.single_color(self.hover_color, self.appearance_mode))
                self.canvas.itemconfig("border_parts",
                                       fill=ThemeManager.single_color(self.hover_color, self.appearance_mode),
                                       outline=ThemeManager.single_color(self.hover_color, self.appearance_mode))
            else:
                self.canvas.itemconfig("inner_parts",
                                       fill=ThemeManager.single_color(self.hover_color, self.appearance_mode),
                                       outline=ThemeManager.single_color(self.hover_color, self.appearance_mode))

    def on_leave(self, event=0):
        if self.hover is True:
            if self.check_state is True:
                self.canvas.itemconfig("inner_parts",
                                       fill=ThemeManager.single_color(self.fg_color, self.appearance_mode),
                                       outline=ThemeManager.single_color(self.fg_color, self.appearance_mode))
                self.canvas.itemconfig("border_parts",
                                       fill=ThemeManager.single_color(self.fg_color, self.appearance_mode),
                                       outline=ThemeManager.single_color(self.fg_color, self.appearance_mode))
            else:
                self.canvas.itemconfig("inner_parts",
                                       fill=ThemeManager.single_color(self.bg_color, self.appearance_mode),
                                       outline=ThemeManager.single_color(self.bg_color, self.appearance_mode))
                self.canvas.itemconfig("border_parts",
                                       fill=ThemeManager.single_color(self.border_color, self.appearance_mode),
                                       outline=ThemeManager.single_color(self.border_color, self.appearance_mode))

    def variable_callback(self, var_name, index, mode):
        if not self.variable_callback_blocked:
            if self.variable.get() == self.onvalue:
                self.select(from_variable_callback=True)
            elif self.variable.get() == self.offvalue:
                self.deselect(from_variable_callback=True)

    def toggle(self, event=0):
        if self.state == tkinter.NORMAL:
            if self.check_state is True:
                self.check_state = False
                self.draw()
            else:
                self.check_state = True
                self.draw()

            if self.function is not None:
                self.function()

            if self.variable is not None:
                self.variable_callback_blocked = True
                self.variable.set(self.onvalue if self.check_state is True else self.offvalue)
                self.variable_callback_blocked = False

    def select(self, from_variable_callback=False):
        self.check_state = True
        self.draw()

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(self.onvalue)
            self.variable_callback_blocked = False

        if self.function is not None:
            try:
                self.function()
            except:
                pass

    def deselect(self, from_variable_callback=False):
        self.check_state = False
        self.draw()

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(self.offvalue)
            self.variable_callback_blocked = False

        if self.function is not None:
            try:
                self.function()
            except:
                pass

    def get(self):
        return self.onvalue if self.check_state is True else self.offvalue
