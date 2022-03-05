import sys
import tkinter

from .customtkinter_tk import CTk
from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_theme_manager import CTkThemeManager
from .customtkinter_canvas import CTkCanvas
from .customtkinter_draw_engine import CTkDrawEngine
from .customtkinter_settings import CTkSettings


class CTkProgressBar(tkinter.Frame):
    """ tkinter custom progressbar, always horizontal, values are from 0 to 1 """

    def __init__(self, *args,
                 variable=None,
                 bg_color=None,
                 border_color="default_theme",
                 fg_color="default_theme",
                 progress_color="default_theme",
                 corner_radius="default_theme",
                 width=200,
                 height=8,
                 border_width="default_theme",
                 **kwargs):
        super().__init__(*args, **kwargs)

        # overwrite configure methods of master when master is tkinter widget, so that bg changes get applied on child CTk widget too
        if isinstance(self.master, (tkinter.Tk, tkinter.Frame)) and not isinstance(self.master, (CTk, CTkFrame)):
            master_old_configure = self.master.config

            def new_configure(*args, **kwargs):
                if "bg" in kwargs:
                    self.configure(bg_color=kwargs["bg"])
                elif "background" in kwargs:
                    self.configure(bg_color=kwargs["background"])

                # args[0] is dict when attribute gets changed by widget[<attribut>] syntax
                elif len(args) > 0 and type(args[0]) == dict:
                    if "bg" in args[0]:
                        self.configure(bg_color=args[0]["bg"])
                    elif "background" in args[0]:
                        self.configure(bg_color=args[0]["background"])
                master_old_configure(*args, **kwargs)

            self.master.config = new_configure
            self.master.configure = new_configure

        AppearanceModeTracker.add(self.change_appearance_mode, self)
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.bg_color = self.detect_color_of_master() if bg_color is None else bg_color
        self.border_color = CTkThemeManager.theme["color"]["progressbar_border"] if border_color == "default_theme" else border_color
        self.fg_color = CTkThemeManager.theme["color"]["progressbar"] if fg_color == "default_theme" else fg_color
        self.progress_color = CTkThemeManager.theme["color"]["progressbar_progress"] if progress_color == "default_theme" else progress_color

        self.variable = variable
        self.variable_callback_blocked = False
        self.variable_callback_name = None

        self.width = width
        self.height = height
        self.corner_radius = CTkThemeManager.theme["shape"]["progressbar_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = CTkThemeManager.theme["shape"]["progressbar_border_width"] if border_width == "default_theme" else border_width
        self.value = 0.5

        self.configure(width=self.width, height=self.height)

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.width,
                                height=self.height)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.draw_engine = CTkDrawEngine(self.canvas, CTkSettings.preferred_drawing_method)

        # Each time an item is resized due to pack position mode, the binding Configure is called on the widget
        self.bind('<Configure>', self.update_dimensions)

        self.draw()  # initial draw

        if self.variable is not None:
            self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
            self.variable_callback_blocked = True
            self.set(self.variable.get(), from_variable_callback=True)
            self.variable_callback_blocked = False

    def destroy(self):
        AppearanceModeTracker.remove(self.change_appearance_mode)

        if self.variable is not None:
            self.variable.trace_remove("write", self.variable_callback_name)

        super().destroy()

    def detect_color_of_master(self):
        if isinstance(self.master, CTkFrame):
            return self.master.fg_color
        else:
            return self.master.cget("bg")

    @staticmethod
    def calc_optimal_height(user_height):
        if sys.platform == "darwin":
            return user_height  # on macOS just use given value (canvas has Antialiasing)
        else:
            # make sure the value is always with uneven for better rendering of the ovals
            if user_height == 0:
                return 0
            elif user_height % 2 == 0:
                return user_height + 1
            else:
                return user_height

    def update_dimensions(self, event):
        # only redraw if dimensions changed (for performance)
        if self.width != event.width or self.height != event.height:
            self.width = event.width
            self.height = event.height

            self.draw()

    def draw(self, no_color_updates=False):

        requires_recoloring = self.draw_engine.draw_rounded_progress_bar_with_border(self.width, self.height, self.corner_radius, self.border_width, self.value, "w")

        if no_color_updates is False or requires_recoloring:
            self.canvas.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))
            self.canvas.itemconfig("border_parts",
                                   fill=CTkThemeManager.single_color(self.border_color, self.appearance_mode),
                                   outline=CTkThemeManager.single_color(self.border_color, self.appearance_mode))
            self.canvas.itemconfig("inner_parts",
                                   fill=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                                   outline=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))
            self.canvas.itemconfig("progress_parts",
                                   fill=CTkThemeManager.single_color(self.progress_color, self.appearance_mode),
                                   outline=CTkThemeManager.single_color(self.progress_color, self.appearance_mode))

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "bg_color" in kwargs:
            self.bg_color = kwargs["bg_color"]
            del kwargs["bg_color"]
            require_redraw = True

        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            del kwargs["fg_color"]
            require_redraw = True

        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
            del kwargs["border_color"]
            require_redraw = True

        if "progress_color" in kwargs:
            self.progress_color = kwargs["progress_color"]
            del kwargs["progress_color"]
            require_redraw = True

        if "border_width" in kwargs:
            self.border_width = kwargs["border_width"]
            del kwargs["border_width"]
            require_redraw = True

        if "variable" in kwargs:
            if self.variable is not None:
                self.variable.trace_remove("write", self.variable_callback_name)

            self.variable = kwargs["variable"]

            if self.variable is not None and self.variable != "":
                self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
                self.set(self.variable.get(), from_variable_callback=True)
            else:
                self.variable = None

            del kwargs["variable"]

        super().configure(*args, **kwargs)

        if require_redraw is True:
            self.draw()

    def variable_callback(self, var_name, index, mode):
        if not self.variable_callback_blocked:
            self.set(self.variable.get(), from_variable_callback=True)

    def set(self, value, from_variable_callback=False):
        self.value = value

        if self.value > 1:
            self.value = 1
        elif self.value < 0:
            self.value = 0

        self.draw(no_color_updates=True)

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(round(self.value) if isinstance(self.variable, tkinter.IntVar) else self.value)
            self.variable_callback_blocked = False

    def change_appearance_mode(self, mode_string):
        if mode_string.lower() == "dark":
            self.appearance_mode = 1
        elif mode_string.lower() == "light":
            self.appearance_mode = 0

        if isinstance(self.master, CTkFrame):
            self.bg_color = self.master.fg_color
        else:
            self.bg_color = self.master.cget("bg")

        self.draw()
