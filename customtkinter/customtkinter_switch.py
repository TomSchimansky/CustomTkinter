import tkinter
import sys

from .customtkinter_tk import CTk
from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_theme_manager import CTkThemeManager
from .customtkinter_settings import CTkSettings
from .customtkinter_draw_engine import CTkDrawEngine
from .customtkinter_canvas import CTkCanvas


class CTkSwitch(tkinter.Frame):
    def __init__(self, *args,
                 text="CTkSwitch",
                 text_font="default_theme",
                 text_color="default_theme",
                 bg_color=None,
                 border_color=None,
                 fg_color="default_theme",
                 progress_color="default_theme",
                 button_color="default_theme",
                 button_hover_color="default_theme",
                 width=36,
                 height=18,
                 corner_radius="default_theme",
                 # button_corner_radius="default_theme",
                 border_width="default_theme",
                 button_length="default_theme",
                 command=None,
                 onvalue=1,
                 offvalue=0,
                 variable=None,
                 textvariable=None,
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
        self.border_color = border_color
        self.fg_color = CTkThemeManager.theme["color"]["switch"] if fg_color == "default_theme" else fg_color
        self.progress_color = CTkThemeManager.theme["color"]["switch_progress"] if progress_color == "default_theme" else progress_color
        self.button_color = CTkThemeManager.theme["color"]["switch_button"] if button_color == "default_theme" else button_color
        self.button_hover_color = CTkThemeManager.theme["color"]["switch_button_hover"] if button_hover_color == "default_theme" else button_hover_color
        self.text_color = CTkThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color

        self.text = text
        self.text_font = (CTkThemeManager.theme["text"]["font"], CTkThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font
        self.width = width
        self.height = height
        self.corner_radius = CTkThemeManager.theme["shape"]["switch_corner_radius"] if corner_radius == "default_theme" else corner_radius
        # self.button_corner_radius = CTkThemeManager.theme["shape"]["switch_button_corner_radius"] if button_corner_radius == "default_theme" else button_corner_radius
        self.border_width = CTkThemeManager.theme["shape"]["switch_border_width"] if border_width == "default_theme" else border_width
        self.button_length = CTkThemeManager.theme["shape"]["switch_button_length"] if button_length == "default_theme" else button_length
        self.hover_state = False
        self.check_state = False  # True if switch is activated
        self.onvalue = onvalue
        self.offvalue = offvalue

        #if self.corner_radius < self.button_corner_radius:
        #    self.corner_radius = self.button_corner_radius

        self.callback_function = command
        self.variable: tkinter.Variable = variable
        self.variable_callback_blocked = False
        self.variable_callback_name = None
        self.textvariable = textvariable

        # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=6)
        self.grid_columnconfigure(2, weight=0)

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.width,
                                height=self.height)
        self.canvas.grid(row=0, column=0, padx=0, pady=0, columnspan=1, sticky="nswe")

        self.draw_engine = CTkDrawEngine(self.canvas, CTkSettings.preferred_drawing_method)

        if sys.platform == "darwin" and CTkSettings.hand_cursor_enabled:
            self.canvas.configure(cursor="pointinghand")
        elif sys.platform.startswith("win") and CTkSettings.hand_cursor_enabled:
            self.canvas.configure(cursor="hand2")

        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.toggle)

        self.text_label = None

        self.draw()  # initial draw

        if self.variable is not None:
            self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
            if self.variable.get() == self.onvalue:
                self.select(from_variable_callback=True)
            elif self.variable.get() == self.offvalue:
                self.deselect(from_variable_callback=True)

    def destroy(self):
        # remove change_appearance_mode function from callback list of AppearanceModeTracker
        AppearanceModeTracker.remove(self.change_appearance_mode)

        # remove variable_callback from variable callbacks if variable exists
        if self.variable is not None:
            self.variable.trace_remove("write", self.variable_callback_name)

        super().destroy()

    def detect_color_of_master(self):
        if isinstance(self.master, CTkFrame):
            return self.master.fg_color
        else:
            return self.master.cget("bg")

    def draw(self, color_updates=True):

        if self.check_state is True:
            requires_recoloring = self.draw_engine.draw_rounded_slider_with_border_and_button(self.width, self.height, self.corner_radius, self.border_width,
                                                                                              self.button_length, self.corner_radius, 1, "w")
        else:
            requires_recoloring = self.draw_engine.draw_rounded_slider_with_border_and_button(self.width, self.height, self.corner_radius, self.border_width,
                                                                                              self.button_length, self.corner_radius, 0, "w")

        if color_updates or requires_recoloring:
            self.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))
            self.canvas.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))

            if self.border_color is None:
                self.canvas.itemconfig("border_parts", fill=CTkThemeManager.single_color(self.bg_color, self.appearance_mode),
                                       outline=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))
            else:
                self.canvas.itemconfig("border_parts", fill=CTkThemeManager.single_color(self.border_color, self.appearance_mode),
                                       outline=CTkThemeManager.single_color(self.border_color, self.appearance_mode))

            self.canvas.itemconfig("inner_parts", fill=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                                   outline=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))

            if self.progress_color is None:
                self.canvas.itemconfig("progress_parts", fill=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                                       outline=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))
            else:
                self.canvas.itemconfig("progress_parts", fill=CTkThemeManager.single_color(self.progress_color, self.appearance_mode),
                                       outline=CTkThemeManager.single_color(self.progress_color, self.appearance_mode))

            self.canvas.itemconfig("slider_parts", fill=CTkThemeManager.single_color(self.button_color, self.appearance_mode),
                                   outline=CTkThemeManager.single_color(self.button_color, self.appearance_mode))

        # self.canvas.configure(bg="red")

        if self.text_label is None:
            self.text_label = tkinter.Label(master=self,
                                            bd=0,
                                            text=self.text,
                                            justify=tkinter.LEFT,
                                            font=self.text_font)
            self.text_label.grid(row=0, column=2, padx=0, pady=0, sticky="w")
            self.text_label["anchor"] = "w"
            if self.textvariable is not None:
                self.text_label.configure(textvariable=self.textvariable)

        self.text_label.configure(fg=CTkThemeManager.single_color(self.text_color, self.appearance_mode))
        self.text_label.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))

        self.set_text(self.text)

    def set_text(self, text):
        self.text = text
        if self.text_label is not None:
            self.text_label.configure(text=self.text)
        else:
            sys.stderr.write("ERROR (CTkSwitch): Cant change text because checkbox has no text.")

    def toggle(self, event=None):
        if self.check_state is True:
            self.check_state = False
        else:
            self.check_state = True

        self.draw(color_updates=False)

        if self.callback_function is not None:
            self.callback_function()

        if self.variable is not None:
            self.variable_callback_blocked = True
            self.variable.set(self.onvalue if self.check_state is True else self.offvalue)
            self.variable_callback_blocked = False

    def select(self, from_variable_callback=False):
        self.check_state = True

        self.draw(color_updates=False)

        if self.callback_function is not None:
            self.callback_function()

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(self.onvalue)
            self.variable_callback_blocked = False

    def deselect(self, from_variable_callback=False):
        self.check_state = False

        self.draw(color_updates=False)

        if self.callback_function is not None:
            self.callback_function()

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(self.offvalue)
            self.variable_callback_blocked = False

    def get(self):
        return self.onvalue if self.check_state is True else self.offvalue

    def on_enter(self, event=0):
        self.hover_state = True
        self.canvas.itemconfig("slider_parts", fill=CTkThemeManager.single_color(self.button_hover_color, self.appearance_mode),
                               outline=CTkThemeManager.single_color(self.button_hover_color, self.appearance_mode))

    def on_leave(self, event=0):
        self.hover_state = False
        self.canvas.itemconfig("slider_parts", fill=CTkThemeManager.single_color(self.button_color, self.appearance_mode),
                               outline=CTkThemeManager.single_color(self.button_color, self.appearance_mode))

    def variable_callback(self, var_name, index, mode):
        if not self.variable_callback_blocked:
            if self.variable.get() == self.onvalue:
                self.select(from_variable_callback=True)
            elif self.variable.get() == self.offvalue:
                self.deselect(from_variable_callback=True)

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

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

        if "progress_color" in kwargs:
            if kwargs["progress_color"] is None:
                self.progress_color = self.fg_color
            else:
                self.progress_color = kwargs["progress_color"]
            require_redraw = True
            del kwargs["progress_color"]

        if "button_color" in kwargs:
            self.button_color = kwargs["button_color"]
            require_redraw = True
            del kwargs["button_color"]

        if "button_hover_color" in kwargs:
            self.button_hover_color = kwargs["button_hover_color"]
            require_redraw = True
            del kwargs["button_hover_color"]

        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
            require_redraw = True
            del kwargs["border_color"]

        if "border_width" in kwargs:
            self.border_width = kwargs["border_width"]
            require_redraw = True
            del kwargs["border_width"]

        if "command" in kwargs:
            self.callback_function = kwargs["command"]
            del kwargs["command"]

        if "textvariable" in kwargs:
            self.text_label.configure(textvariable=kwargs["textvariable"])
            del kwargs["textvariable"]

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
