import tkinter

from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkEntry(tkinter.Frame):
    def __init__(self,
                 master=None,
                 bg_color=None,
                 fg_color=CTkColorManager.ENTRY,
                 text_color=CTkColorManager.TEXT,
                 corner_radius=10,
                 width=120,
                 height=25,
                 *args,
                 **kwargs):
        super().__init__(master=master)

        AppearanceModeTracker.add(self.change_appearance_mode)

        if bg_color is None:
            if isinstance(self.master, CTkFrame):
                self.bg_color = self.master.fg_color
            else:
                self.bg_color = self.master.cget("bg")
        else:
            self.bg_color = bg_color

        self.fg_color = fg_color
        self.text_color = text_color
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.width = width
        self.height = height
        self.corner_radius = corner_radius

        self.configure(width=self.width, height=self.height)

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     width=self.width,
                                     height=self.height)
        self.canvas.place(x=0, y=0)

        self.entry = tkinter.Entry(master=self,
                                   bd=0,
                                   highlightthicknes=0,
                                   *args, **kwargs)
        self.entry.place(relx=0.5, rely=0.5, relwidth=0.8, anchor=tkinter.CENTER)

        self.fg_parts = []

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.fg_parts = []

        # frame_border
        self.fg_parts.append(self.canvas.create_oval(0, 0,
                                                     self.corner_radius*2, self.corner_radius*2))
        self.fg_parts.append(self.canvas.create_oval(self.width-self.corner_radius*2, 0,
                                                     self.width, self.corner_radius*2))
        self.fg_parts.append(self.canvas.create_oval(0, self.height-self.corner_radius*2,
                                                     self.corner_radius*2, self.height))
        self.fg_parts.append(self.canvas.create_oval(self.width-self.corner_radius*2, self.height-self.corner_radius*2,
                                                     self.width, self.height))

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

    def delete(self, *args, **kwargs):
        return self.entry.delete(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.entry.insert(*args, **kwargs)

    def get(self):
        return self.entry.get()

