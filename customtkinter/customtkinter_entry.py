import tkinter
import sys

from .customtkinter_tk import CTk
from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkEntry(tkinter.Frame):
    def __init__(self, *args,
                 master=None,
                 bg_color=None,
                 fg_color="CTkColorManager",
                 text_color="CTkColorManager",
                 corner_radius=8,
                 width=120,
                 height=30,
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

        self.configure_basic_grid()

        self.bg_color = self.detect_color_of_master() if bg_color is None else bg_color
        self.fg_color = CTkColorManager.ENTRY if fg_color == "CTkColorManager" else fg_color
        self.text_color = CTkColorManager.TEXT if text_color == "CTkColorManager" else text_color

        self.width = width
        self.height = height

        self.corner_radius = self.calc_optimal_corner_radius(corner_radius)  # optimise for less artifacts

        if self.corner_radius*2 > self.height:
            self.corner_radius = self.height/2
        elif self.corner_radius*2 > self.width:
            self.corner_radius = self.width/2

        super().configure(width=self.width, height=self.height)

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     width=self.width,
                                     height=self.height)
        self.canvas.grid(column=0, row=0)

        self.entry = tkinter.Entry(master=self,
                                   bd=0,
                                   width=1,
                                   highlightthicknes=0,
                                   **kwargs)
        self.entry.grid(column=0, row=0, sticky="we", padx=self.corner_radius if self.corner_radius >= 6 else 6)

        self.fg_parts = []

        self.bind('<Configure>', self.update_dimensions)
        self.draw()

    def destroy(self):
        AppearanceModeTracker.remove(self.change_appearance_mode)
        super().destroy()

    def configure_basic_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

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

        for part in self.fg_parts:
            if type(self.fg_color) == tuple:
                self.canvas.itemconfig(part, fill=self.fg_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.fg_color, width=0)

        if type(self.bg_color) == tuple:
            self.canvas.configure(bg=self.bg_color[self.appearance_mode])
        else:
            self.canvas.configure(bg=self.bg_color)

        if type(self.fg_color) == tuple:
            self.entry.configure(bg=self.fg_color[self.appearance_mode],
                                 highlightcolor=self.fg_color[self.appearance_mode])
        else:
            self.entry.configure(bg=self.fg_color,
                                 highlightcolor=self.fg_color)

        if type(self.text_color) == tuple:
            self.entry.configure(fg=self.text_color[self.appearance_mode],
                                 insertbackground=self.text_color[self.appearance_mode])
        else:
            self.entry.configure(fg=self.text_color,
                                 insertbackground=self.text_color)

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

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

        if "text_color" in kwargs:
            self.text_color = kwargs["text_color"]
            del kwargs["text_color"]
            require_redraw = True

        if "corner_radius" in kwargs:
            self.corner_radius = self.calc_optimal_corner_radius(kwargs["corner_radius"])  # optimise for less artifacts

            if self.corner_radius * 2 > self.height:
                self.corner_radius = self.height / 2
            elif self.corner_radius * 2 > self.width:
                self.corner_radius = self.width / 2

            self.entry.grid(column=0, row=0, sticky="we", padx=self.corner_radius if self.corner_radius >= 6 else 6)
            del kwargs["corner_radius"]
            require_redraw = True

        self.entry.configure(*args, **kwargs)

        if require_redraw is True:
            self.draw()

    def delete(self, *args, **kwargs):
        return self.entry.delete(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.entry.insert(*args, **kwargs)

    def get(self):
        return self.entry.get()

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
