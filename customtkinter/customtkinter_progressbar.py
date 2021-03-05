import tkinter

from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkProgressBar(tkinter.Frame):
    def __init__(self,
                 bg_color=None,
                 border_color=CTkColorManager.PROGRESS_BG,
                 fg_color=CTkColorManager.PROGRESS_BG,
                 progress_color=CTkColorManager.MAIN,
                 width=160,
                 height=10,
                 border_width=0,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        AppearanceModeTracker.add(self.change_appearance_mode)

        if bg_color is None:
            if isinstance(self.master, CTkFrame):
                self.bg_color = self.master.fg_color
            else:
                self.bg_color = self.master.cget("bg")
        else:
            self.bg_color = bg_color

        self.border_color = border_color
        self.fg_color = fg_color
        self.progress_color = progress_color
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.width = width
        self.height = height
        self.border_width = border_width
        self.value = 0.5

        self.configure(width=self.width, height=self.height)

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     width=self.width,
                                     height=self.height)
        self.canvas.place(x=0, y=0)

        self.border_parts = []
        self.fg_parts = []
        self.progress_parts = []

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.border_parts = []
        self.fg_parts = []
        self.progress_parts = []

        # frame_border
        self.border_parts.append(self.canvas.create_oval(0, 0,
                                                         self.height, self.height))
        self.border_parts.append(self.canvas.create_rectangle(self.height/2, 0,
                                                              self.width-(self.height/2), self.height))
        self.border_parts.append(self.canvas.create_oval(self.width-self.height, 0,
                                                         self.width, self.height))

        # foreground
        self.fg_parts.append(self.canvas.create_oval(self.border_width, self.border_width,
                                                     self.height-self.border_width, self.height-self.border_width))
        self.fg_parts.append(self.canvas.create_rectangle(self.height/2, self.border_width,
                                                          self.width-(self.height/2), self.height-self.border_width))
        self.fg_parts.append(self.canvas.create_oval(self.width-self.height+self.border_width, self.border_width,
                                                     self.width-self.border_width, self.height-self.border_width))

        if type(self.bg_color) == tuple:
            self.canvas.configure(bg=self.bg_color[self.appearance_mode])
        else:
            self.canvas.configure(bg=self.bg_color)

        for part in self.border_parts:
            if type(self.border_color) == tuple:
                self.canvas.itemconfig(part, fill=self.border_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.border_color, width=0)

        for part in self.fg_parts:
            if type(self.fg_color) == tuple:
                self.canvas.itemconfig(part, fill=self.fg_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.fg_color, width=0)

        self.set(self.value)

    def set(self, value):
        self.value = value

        if self.value > 1:
            self.value = 1
        elif self.value < 0:
            self.value = 0

        for part in self.progress_parts:
            self.canvas.delete(part)

        # progress
        self.progress_parts.append(self.canvas.create_oval(self.border_width,
                                                           self.border_width,
                                                           self.height - self.border_width,
                                                           self.height - self.border_width))

        self.progress_parts.append(self.canvas.create_rectangle(self.height / 2,
                                                                self.border_width,
                                                                self.height / 2 + (self.width - self.height) * self.value,
                                                                self.height - self.border_width))

        self.progress_parts.append(self.canvas.create_oval(self.height / 2 + (self.width - self.height) * self.value - (self.height) / 2 + self.border_width,
                                                           self.border_width,
                                                           self.height / 2 + (self.width - self.height) * self.value + (self.height) / 2 - self.border_width,
                                                           self.height - self.border_width))

        for part in self.progress_parts:
            if type(self.progress_color) == tuple:
                self.canvas.itemconfig(part, fill=self.progress_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.progress_color, width=0)

        self.canvas.update()
        self.canvas.update_idletasks()

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
