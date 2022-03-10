import tkinter
import sys

from customtkinter.customtkinter_tk import CTk
from customtkinter.customtkinter_frame import CTkFrame
from customtkinter.appearance_mode_tracker import AppearanceModeTracker
from customtkinter.customtkinter_theme_manager import CTkThemeManager
from customtkinter.customtkinter_canvas import CTkCanvas
from customtkinter.customtkinter_settings import CTkSettings
from customtkinter.customtkinter_draw_engine import CTkDrawEngine


class CTkCheckBox(tkinter.Frame):
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

        AppearanceModeTracker.add(self.set_appearance_mode, self)
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.bg_color = self.detect_color_of_master() if bg_color is None else bg_color
        self.fg_color = CTkThemeManager.theme["color"]["button"] if fg_color == "default_theme" else fg_color
        self.hover_color = CTkThemeManager.theme["color"]["button_hover"] if hover_color == "default_theme" else hover_color
        self.border_color = CTkThemeManager.theme["color"]["checkbox_border"] if border_color == "default_theme" else border_color
        self.checkmark_color = CTkThemeManager.theme["color"]["checkmark"] if checkmark_color == "default_theme" else checkmark_color

        self.width = width
        self.height = height
        self.corner_radius = CTkThemeManager.theme["shape"]["checkbox_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = CTkThemeManager.theme["shape"]["checkbox_border_width"] if border_width == "default_theme" else border_width

        if self.corner_radius*2 > self.height:
            self.corner_radius = self.height/2
        elif self.corner_radius*2 > self.width:
            self.corner_radius = self.width/2

        if self.corner_radius >= self.border_width:
            self.inner_corner_radius = self.corner_radius - self.border_width
        else:
            self.inner_corner_radius = 0

        self.text = text
        self.text_color = CTkThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.text_color_disabled = CTkThemeManager.theme["color"]["text_disabled"] if text_color_disabled == "default_theme" else text_color_disabled
        self.text_font = (CTkThemeManager.theme["text"]["font"], CTkThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font

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

        # configure grid system
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0, minsize=6)
        self.grid_columnconfigure(2, weight=1)

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.width,
                                height=self.height)
        self.canvas.grid(row=0, column=0, padx=0, pady=0, columnspan=1)

        self.draw_engine = CTkDrawEngine(self.canvas, CTkSettings.preferred_drawing_method)

        if self.hover is True:
            self.canvas.bind("<Enter>", self.on_enter)
            self.canvas.bind("<Leave>", self.on_leave)

        self.canvas.bind("<Button-1>", self.toggle)
        self.canvas.bind("<Button-1>", self.toggle)

        self.text_label = None

        self.set_cursor()
        self.draw()  # initial draw

        if self.variable is not None:
            self.variable_callback_name = self.variable.trace_add("write", self.variable_callback)
            if self.variable.get() == self.onvalue:
                self.select(from_variable_callback=True)
            elif self.variable.get() == self.offvalue:
                self.deselect(from_variable_callback=True)

    def destroy(self):
        AppearanceModeTracker.remove(self.set_appearance_mode)

        if self.variable is not None:
            self.variable.trace_remove("write", self.variable_callback_name)

        super().destroy()

    def detect_color_of_master(self):
        if isinstance(self.master, CTkFrame):
            return self.master.fg_color
        else:
            return self.master.cget("bg")

    def draw(self):
        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border(self.width, self.height, self.corner_radius, self.border_width)

        if self.check_state is True:
            self.draw_engine.draw_checkmark(self.width, self.height, self.height * 0.58)
        else:
            self.canvas.delete("checkmark")

        self.canvas.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))
        self.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))

        if self.check_state is True:
            self.canvas.itemconfig("inner_parts",
                                   outline=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                                   fill=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))
            self.canvas.itemconfig("border_parts",
                                   outline=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                                   fill=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))

            if "create_line" in self.canvas.gettags("checkmark"):
                self.canvas.itemconfig("checkmark", fill=CTkThemeManager.single_color(self.checkmark_color, self.appearance_mode))
            else:
                self.canvas.itemconfig("checkmark", fill=CTkThemeManager.single_color(self.checkmark_color, self.appearance_mode))
        else:
            self.canvas.itemconfig("inner_parts",
                                   outline=CTkThemeManager.single_color(self.bg_color, self.appearance_mode),
                                   fill=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))
            self.canvas.itemconfig("border_parts",
                                   outline=CTkThemeManager.single_color(self.border_color, self.appearance_mode),
                                   fill=CTkThemeManager.single_color(self.border_color, self.appearance_mode))

        if self.text_label is None:
            self.text_label = tkinter.Label(master=self,
                                            bd=0,
                                            text=self.text,
                                            justify=tkinter.LEFT,
                                            font=self.text_font)
            self.text_label.grid(row=0, column=2, padx=0, pady=0, sticky="w")
            self.text_label["anchor"] = "w"

        if self.state == tkinter.DISABLED:
            self.text_label.configure(fg=(CTkThemeManager.single_color(self.text_color_disabled, self.appearance_mode)))
        else:
            self.text_label.configure(fg=CTkThemeManager.single_color(self.text_color, self.appearance_mode))
        self.text_label.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))

        self.set_text(self.text)

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

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
        if self.state == tkinter.DISABLED:
            if sys.platform == "darwin" and CTkSettings.hand_cursor_enabled:
                self.canvas.configure(cursor="arrow")
            elif sys.platform.startswith("win") and CTkSettings.hand_cursor_enabled:
                self.canvas.configure(cursor="arrow")

        elif self.state == tkinter.NORMAL:
            if sys.platform == "darwin" and CTkSettings.hand_cursor_enabled:
                self.canvas.configure(cursor="pointinghand")
            elif sys.platform.startswith("win") and CTkSettings.hand_cursor_enabled:
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
                                       fill=CTkThemeManager.single_color(self.hover_color, self.appearance_mode),
                                       outline=CTkThemeManager.single_color(self.hover_color, self.appearance_mode))
                self.canvas.itemconfig("border_parts",
                                       fill=CTkThemeManager.single_color(self.hover_color, self.appearance_mode),
                                       outline=CTkThemeManager.single_color(self.hover_color, self.appearance_mode))
            else:
                self.canvas.itemconfig("inner_parts",
                                       fill=CTkThemeManager.single_color(self.hover_color, self.appearance_mode),
                                       outline=CTkThemeManager.single_color(self.hover_color, self.appearance_mode))

    def on_leave(self, event=0):
        if self.hover is True:
            if self.check_state is True:
                self.canvas.itemconfig("inner_parts",
                                       fill=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                                       outline=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))
                self.canvas.itemconfig("border_parts",
                                       fill=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                                       outline=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))
            else:
                self.canvas.itemconfig("inner_parts",
                                       fill=CTkThemeManager.single_color(self.bg_color, self.appearance_mode),
                                       outline=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))
                self.canvas.itemconfig("border_parts",
                                       fill=CTkThemeManager.single_color(self.border_color, self.appearance_mode),
                                       outline=CTkThemeManager.single_color(self.border_color, self.appearance_mode))

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

        if self.function is not None:
            self.function()

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(self.onvalue)
            self.variable_callback_blocked = False

    def deselect(self, from_variable_callback=False):
        self.check_state = False
        self.draw()

        if self.function is not None:
            self.function()

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(self.offvalue)
            self.variable_callback_blocked = False

    def get(self):
        return self.onvalue if self.check_state is True else self.offvalue

    def set_appearance_mode(self, mode_string):
        if mode_string.lower() == "dark":
            self.appearance_mode = 1
        elif mode_string.lower() == "light":
            self.appearance_mode = 0

        if isinstance(self.master, (CTkFrame, CTk)):
            self.bg_color = self.master.fg_color
        else:
            self.bg_color = self.master.cget("bg")

        self.draw()
