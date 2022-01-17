import tkinter
import sys

from .customtkinter_tk import CTk
from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkLabel(tkinter.Frame):
    def __init__(self, *args,
                 master=None,
                 bg_color=None,
                 fg_color="CTkColorManager",
                 text_color="CTkColorManager",
                 corner_radius=8,
                 width=120,
                 height=25,
                 text="CTkLabel",
                 text_font=None,
                 **kwargs):
        if master is None:
            super().__init__(*args)
        else:
            super().__init__(*args, master=master)

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
        self.fg_color = CTkColorManager.LABEL_BG if fg_color == "CTkColorManager" else fg_color
        self.text_color = CTkColorManager.TEXT if text_color == "CTkColorManager" else text_color

        self.width = width
        self.height = height

        self.corner_radius = self.calc_optimal_corner_radius(corner_radius)  # optimise for less artifacts

        if self.corner_radius * 2 > self.height:
            self.corner_radius = self.height / 2
        elif self.corner_radius * 2 > self.width:
            self.corner_radius = self.width / 2

        self.text = text

        if text_font is None:
            if sys.platform == "darwin":  # macOS
                self.text_font = ("Avenir", 13)
            elif "win" in sys.platform:  # Windows
                self.text_font = ("Century Gothic", 10)
            else:
                self.text_font = ("TkDefaultFont", 10)
        else:
            self.text_font = text_font

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     width=self.width,
                                     height=self.height)
        self.canvas.place(relx=0, rely=0, anchor=tkinter.NW)

        self.text_label = tkinter.Label(master=self,
                                        highlightthicknes=0,
                                        bd=0,
                                        text=self.text,
                                        font=self.text_font,
                                        **kwargs)
        self.text_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.fg_parts = []

        super().configure(width=self.width, height=self.height)

        self.bind('<Configure>', self.update_dimensions)
        self.draw()

    def destroy(self):
        AppearanceModeTracker.remove(self.change_appearance_mode)
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

    def update_dimensions(self, event):
        # only redraw if dimensions changed (for performance)
        if self.width != event.width or self.height != event.height:
            self.width = event.width
            self.height = event.height

            self.canvas.config(width=self.width, height=self.height)
            self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.fg_parts = []

        if sys.platform == "darwin":
            oval_size_corr_br = 0
        else:
            oval_size_corr_br = -1  # correct canvas oval draw size on bottom and right by 1 pixel (too large otherwise)

        # frame_border
        self.fg_parts.append(self.canvas.create_oval(0,
                                                     0,
                                                     self.corner_radius*2 + oval_size_corr_br,
                                                     self.corner_radius*2 + oval_size_corr_br))
        self.fg_parts.append(self.canvas.create_oval(self.width-self.corner_radius*2,
                                                     0,
                                                     self.width + oval_size_corr_br,
                                                     self.corner_radius*2 + oval_size_corr_br))
        self.fg_parts.append(self.canvas.create_oval(0,
                                                     self.height-self.corner_radius*2,
                                                     self.corner_radius*2 + oval_size_corr_br,
                                                     self.height + oval_size_corr_br))
        self.fg_parts.append(self.canvas.create_oval(self.width-self.corner_radius*2,
                                                     self.height-self.corner_radius*2,
                                                     self.width + oval_size_corr_br,
                                                     self.height + oval_size_corr_br))

        self.fg_parts.append(self.canvas.create_rectangle(0, self.corner_radius,
                                                          self.width, self.height-self.corner_radius))
        self.fg_parts.append(self.canvas.create_rectangle(self.corner_radius, 0,
                                                          self.width-self.corner_radius, self.height))

        if type(self.bg_color) == tuple:
            self.canvas.configure(bg=self.bg_color[self.appearance_mode])
        else:
            self.canvas.configure(bg=self.bg_color)

        if self.fg_color is None:
            new_fg_color = self.bg_color
        else:
            new_fg_color = self.fg_color

        for part in self.fg_parts:
            if type(new_fg_color) == tuple:
                self.canvas.itemconfig(part, fill=new_fg_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=new_fg_color, width=0)

        if type(self.text_color) == tuple:
            self.text_label.configure(fg=self.text_color[self.appearance_mode])
        else:
            self.text_label.configure(fg=self.text_color)

        if type(new_fg_color) == tuple:
            self.text_label.configure(bg=new_fg_color[self.appearance_mode])
        else:
            self.text_label.configure(bg=new_fg_color)

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "text" in kwargs:
            self.set_text(kwargs["text"])
            del kwargs["text"]

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

        if "text_color" in kwargs:
            self.text_color = kwargs["text_color"]
            require_redraw = True
            del kwargs["text_color"]

        self.text_label.configure(*args, **kwargs)

        if require_redraw:
            self.draw()

    def set_text(self, text):
        self.text = text
        self.text_label.configure(text=self.text, width=len(self.text))

    def change_appearance_mode(self, mode_string):
        if mode_string.lower() == "dark":
            self.appearance_mode = 1
        elif mode_string.lower() == "light":
            self.appearance_mode = 0

        if isinstance(self.master, (CTkFrame, CTk)):
            self.bg_color = self.master.fg_color
        else:
            self.bg_color = self.master.cget("bg")

        self.draw()
