import tkinter
import sys

from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkLabel(tkinter.Frame):
    def __init__(self,
                 master=None,
                 bg_color=None,
                 fg_color=None,
                 text_color=CTkColorManager.TEXT,
                 corner_radius=8,
                 width=120,
                 height=25,
                 text="CTkLabel",
                 text_font=None,
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

        if fg_color is None:
            self.fg_color = self.bg_color
        else:
            self.fg_color = fg_color
        self.text_color = text_color
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.text = text

        if text_font is None:
            if sys.platform == "darwin":  # macOS
                self.text_font = ("Avenir", 13)
            elif "win" in sys.platform:  # Windows
                self.text_font = ("Century Gothic", 11)
            else:
                self.text_font = ("TkDefaultFont", 11)
        else:
            self.text_font = text_font
        self.configure(width=self.width, height=self.height)

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
                                        *args, **kwargs)
        self.text_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

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

        if type(self.bg_color) == tuple:
            self.canvas.configure(bg=self.bg_color[self.appearance_mode])
        else:
            self.canvas.configure(bg=self.bg_color)

        for part in self.fg_parts:
            if type(self.fg_color) == tuple:
                self.canvas.itemconfig(part, fill=self.fg_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.fg_color, width=0)

        if type(self.text_color) == tuple:
            self.text_label.configure(fg=self.text_color[self.appearance_mode])
        else:
            self.text_label.configure(fg=self.text_color)

        if type(self.fg_color) == tuple:
            self.text_label.configure(bg=self.fg_color[self.appearance_mode])
        else:
            self.text_label.configure(bg=self.fg_color)

    def configure_color(self, bg_color=None, fg_color=None, text_color=None):
        if bg_color is not None:
            self.bg_color = bg_color

        if fg_color is not None:
            self.fg_color = fg_color

        if text_color is not None:
            self.text_color = text_color

        self.draw()

    def set_text(self, text):
        self.text_label.configure(text=text, width=len(self.text))

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
