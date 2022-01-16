import tkinter
import sys

from .customtkinter_tk import CTk
from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkCheckBox(tkinter.Frame):
    """ tkinter custom checkbox with border, rounded corners and hover effect """

    def __init__(self, *args,
                 bg_color=None,
                 fg_color="CTkColorManager",
                 hover_color="CTkColorManager",
                 border_color="CTkColorManager",
                 border_width=3,
                 width=25,
                 height=25,
                 corner_radius=4,
                 text_font=None,
                 text_color="CTkColorManager",
                 text="CTkCheckBox",
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
        self.fg_color = CTkColorManager.MAIN if fg_color == "CTkColorManager" else fg_color
        self.hover_color = CTkColorManager.MAIN_HOVER if hover_color == "CTkColorManager" else hover_color
        self.border_color = CTkColorManager.CHECKBOX_LINES if border_color == "CTkColorManager" else border_color

        self.width = width
        self.height = height
        self.corner_radius = self.calc_optimal_corner_radius(corner_radius)  # optimise for less artifacts

        if self.corner_radius*2 > self.height:
            self.corner_radius = self.height/2
        elif self.corner_radius*2 > self.width:
            self.corner_radius = self.width/2

        self.border_width = round(border_width)

        if self.corner_radius >= self.border_width:
            self.inner_corner_radius = self.corner_radius - self.border_width
        else:
            self.inner_corner_radius = 0

        self.text = text
        self.text_color = CTkColorManager.TEXT if text_color == "CTkColorManager" else text_color
        if text_font is None:
            if sys.platform == "darwin":  # macOS
                self.text_font = ("Avenir", 13)
            elif "win" in sys.platform:  # Windows
                self.text_font = ("Century Gothic", 11)
            else:
                self.text_font = ("TkDefaultFont")
        else:
            self.text_font = text_font

        self.function = command
        self.state = state
        self.hover = hover
        self.check_state = False
        self.onvalue = onvalue
        self.offvalue = offvalue
        self.variable: tkinter.Variable = variable
        self.variable_callback_blocked = False
        self.textvariable = textvariable
        self.variabel_callback_name = None

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     width=self.width,
                                     height=self.height)
        self.canvas.pack(side='left')

        if sys.platform == "darwin" and self.state == tkinter.NORMAL:
            self.canvas.configure(cursor="pointinghand")

        if self.hover is True:
            self.canvas.bind("<Enter>", self.on_enter)
            self.canvas.bind("<Leave>", self.on_leave)

        self.canvas.bind("<Button-1>", self.toggle)
        self.canvas.bind("<Button-1>", self.toggle)

        self.canvas_fg_parts = []
        self.canvas_border_parts = []
        self.canvas_check_parts = []
        self.text_label = None

        self.draw()  # initial draw

        if self.variable is not None:
            self.variabel_callback_name = self.variable.trace_add("write", self.variable_callback)
            if self.variable.get() == self.onvalue:
                self.select(from_variable_callback=True)
            elif self.variable.get() == self.offvalue:
                self.deselect(from_variable_callback=True)

    def destroy(self):
        AppearanceModeTracker.remove(self.set_appearance_mode)

        if self.variable is not None:
            self.variable.trace_remove("write", self.variabel_callback_name)

        super().destroy()

    def detect_color_of_master(self):
        if isinstance(self.master, CTkFrame):
            return self.master.fg_color
        else:
            return self.master.cget("bg")

    @staticmethod
    def calc_optimal_corner_radius(user_corner_radius):
        if sys.platform == "darwin":
            return user_corner_radius  # on macOS just use given value (canvas has Antialiasing)
        else:
            user_corner_radius = 0.5 * round(user_corner_radius / 0.5)  # round to 0.5 steps

            # make sure the value is always with .5 at the end for smoother corners
            if user_corner_radius == 0:
                return 0
            elif user_corner_radius % 1 == 0:
                return user_corner_radius + 0.5
            else:
                return user_corner_radius

    def draw(self):
        self.canvas.delete("all")
        self.canvas_fg_parts = []
        self.canvas_border_parts = []
        self.canvas_check_parts = []

        if type(self.bg_color) == tuple and len(self.bg_color) == 2:
            self.canvas.configure(bg=self.bg_color[self.appearance_mode])
        else:
            self.canvas.configure(bg=self.bg_color)

        if sys.platform == "darwin":
            oval_size_corr_br = 0
        else:
            oval_size_corr_br = -1

        # border button parts
        if self.border_width > 0:

            if self.corner_radius > 0:
                self.canvas_border_parts.append(self.canvas.create_oval(0,
                                                                        0,
                                                                        self.corner_radius * 2 + oval_size_corr_br,
                                                                        self.corner_radius * 2 + oval_size_corr_br))
                self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2,
                                                                        0,
                                                                        self.width + oval_size_corr_br,
                                                                        self.corner_radius * 2 + oval_size_corr_br))
                self.canvas_border_parts.append(self.canvas.create_oval(0,
                                                                        self.height - self.corner_radius * 2,
                                                                        self.corner_radius * 2 + oval_size_corr_br,
                                                                        self.height + oval_size_corr_br))
                self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2,
                                                                        self.height - self.corner_radius * 2,
                                                                        self.width + oval_size_corr_br,
                                                                        self.height + oval_size_corr_br))

            self.canvas_border_parts.append(self.canvas.create_rectangle(0,
                                                                         self.corner_radius,
                                                                         self.width,
                                                                         self.height - self.corner_radius))
            self.canvas_border_parts.append(self.canvas.create_rectangle(self.corner_radius,
                                                                         0,
                                                                         self.width - self.corner_radius,
                                                                         self.height))

        # inner button parts

        if self.corner_radius > 0:
            self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width,
                                                                self.border_width,
                                                                self.border_width + self.inner_corner_radius * 2 + oval_size_corr_br,
                                                                self.border_width + self.inner_corner_radius * 2 + oval_size_corr_br))
            self.canvas_fg_parts.append(self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2,
                                                                self.border_width,
                                                                self.width - self.border_width + oval_size_corr_br,
                                                                self.border_width + self.inner_corner_radius * 2 + oval_size_corr_br))
            self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width,
                                                                self.height - self.border_width - self.inner_corner_radius * 2,
                                                                self.border_width + self.inner_corner_radius * 2 + oval_size_corr_br,
                                                                self.height-self.border_width + oval_size_corr_br))
            self.canvas_fg_parts.append(self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2,
                                                                self.height - self.border_width - self.inner_corner_radius * 2,
                                                                self.width - self.border_width + oval_size_corr_br,
                                                                self.height - self.border_width + oval_size_corr_br))

        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width + self.inner_corner_radius,
                                                                 self.border_width,
                                                                 self.width - self.border_width - self.inner_corner_radius,
                                                                 self.height - self.border_width))
        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width,
                                                                 self.border_width + self.inner_corner_radius,
                                                                 self.width - self.border_width,
                                                                 self.height - self.inner_corner_radius - self.border_width))

        if self.check_state is False:
            for part in self.canvas_fg_parts:
                if type(self.bg_color) == tuple and len(self.bg_color) == 2:
                        self.canvas.itemconfig(part, fill=self.bg_color[self.appearance_mode], width=0)
                else:
                        self.canvas.itemconfig(part, fill=self.bg_color, outline=self.bg_color, width=0)
        else:
            for part in self.canvas_fg_parts:
                if type(self.fg_color) == tuple and len(self.fg_color) == 2:
                        self.canvas.itemconfig(part, fill=self.fg_color[self.appearance_mode], width=0)
                else:
                        self.canvas.itemconfig(part, fill=self.fg_color, outline=self.bg_color, width=0)

        for part in self.canvas_border_parts:
            if type(self.border_color) == tuple and len(self.border_color) == 2:
                self.canvas.itemconfig(part, fill=self.border_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.border_color, outline=self.border_color, width=0)

        if self.text_label is not None:
            self.text_label.pack_forget()

        self.text_label = tkinter.Label(master=self,
                                        text=self.text,
                                        font=self.text_font)
        self.text_label.pack(side='right', padx="4")

        if type(self.text_color) == tuple and len(self.text_color) == 2:
            self.text_label.configure(fg=self.text_color[self.appearance_mode])
        else:
            self.text_label.configure(fg=self.text_color)

        if type(self.bg_color) == tuple and len(self.bg_color) == 2:
            self.configure(bg=self.bg_color[self.appearance_mode])
            self.text_label.configure(bg=self.bg_color[self.appearance_mode])
        else:
            self.configure(bg=self.bg_color)
            self.text_label.configure(bg=self.bg_color)

        self.set_text(self.text)

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw()

        if "text" in kwargs:
            self.set_text(kwargs["text"])
            del kwargs["text"]

        if "state" in kwargs:
            self.set_state(kwargs["state"])
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
                self.variable.trace_remove("write", self.variabel_callback_name)

            self.variable = kwargs["variable"]

            if self.variable is not None and self.variable != "":
                self.variabel_callback_name = self.variable.trace_add("write", self.variable_callback)
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

    def set_state(self, state):
        self.state = state

        if self.state == tkinter.DISABLED:
            self.hover = False
            if sys.platform == "darwin":
                self.canvas.configure(cursor="arrow")

        elif self.state == tkinter.NORMAL:
            self.hover = True
            if sys.platform == "darwin":
                self.canvas.configure(cursor="pointinghand")

        self.draw()

    def set_text(self, text):
        self.text = text
        if self.text_label is not None:
            self.text_label.configure(text=self.text, width=len(self.text))
        else:
            sys.stderr.write("ERROR (CTkButton): Cant change text because button has no text.")

    def on_enter(self, event=0):
        if self.hover is True:
            for part in self.canvas_fg_parts:
                if type(self.hover_color) == tuple and len(self.hover_color) == 2:
                    self.canvas.itemconfig(part, fill=self.hover_color[self.appearance_mode], width=0)
                else:
                    self.canvas.itemconfig(part, fill=self.hover_color, width=0)

    def on_leave(self, event=0):
        if self.hover is True:
            if self.check_state == True:
                for part in self.canvas_fg_parts:
                    if type(self.fg_color) == tuple and len(self.fg_color) == 2:
                        self.canvas.itemconfig(part, fill=self.fg_color[self.appearance_mode], width=0)
                    else:
                        self.canvas.itemconfig(part, fill=self.fg_color, width=0)
            else:
                for part in self.canvas_fg_parts:
                    if type(self.bg_color) == tuple and len(self.bg_color) == 2:
                        self.canvas.itemconfig(part, fill=self.bg_color[self.appearance_mode], width=0)
                    else:
                        self.canvas.itemconfig(part, fill=self.bg_color, width=0)

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
                for part in self.canvas_fg_parts:
                    if type(self.bg_color) == tuple and len(self.bg_color) == 2:
                        self.canvas.itemconfig(part, fill=self.bg_color[self.appearance_mode], width=0)
                    else:
                        self.canvas.itemconfig(part, fill=self.bg_color, width=0)
            else:
                self.check_state = True
                for part in self.canvas_fg_parts:
                    if type(self.fg_color) == tuple and len(self.fg_color) == 2:
                        self.canvas.itemconfig(part, fill=self.fg_color[self.appearance_mode], width=0)
                    else:
                        self.canvas.itemconfig(part, fill=self.fg_color, width=0)

            if self.function is not None:
                self.function()

            if self.variable is not None:
                self.variable_callback_blocked = True
                self.variable.set(self.onvalue if self.check_state is True else self.offvalue)
                self.variable_callback_blocked = False

    def select(self, from_variable_callback=False):
        self.check_state = True
        for part in self.canvas_fg_parts:
            if type(self.fg_color) == tuple and len(self.fg_color) == 2:
                self.canvas.itemconfig(part, fill=self.fg_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.fg_color, width=0)

        if self.function is not None:
            self.function()

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(self.onvalue)
            self.variable_callback_blocked = False

    def deselect(self, from_variable_callback=False):
        self.check_state = False
        for part in self.canvas_fg_parts:
            if type(self.bg_color) == tuple and len(self.bg_color) == 2:
                self.canvas.itemconfig(part, fill=self.bg_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.bg_color, width=0)

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
