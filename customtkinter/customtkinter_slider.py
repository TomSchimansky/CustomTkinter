import tkinter
import sys

from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkSlider(tkinter.Frame):
    def __init__(self,
                 bg_color=None,
                 border_color=None,
                 fg_color=CTkColorManager.SLIDER_BG,
                 button_color=CTkColorManager.MAIN,
                 button_hover_color=CTkColorManager.MAIN_HOVER,
                 width=160,
                 height=16,
                 border_width=5.5,
                 command=None,
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
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.width = width
        self.height = height
        self.border_width = border_width
        self.callback_function = command
        self.value = 0.5
        self.hover_state = False

        self.configure(width=self.width, height=self.height)
        if sys.platform == "darwin":
            self.configure(cursor="pointinghand")

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     width=self.width,
                                     height=self.height)
        self.canvas.place(x=0, y=0)

        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<B1-Motion>", self.clicked)

        self.border_parts = []
        self.fg_parts = []
        self.button_parts = []

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.border_parts = []
        self.fg_parts = []
        self.button_parts = []

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

        # button
        self.button_parts.append(self.canvas.create_oval(self.value*self.width - self.height/2, 0,
                                                         self.value*self.width + self.height/2, self.height))

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

        for part in self.button_parts:
            if type(self.button_color) == tuple:
                self.canvas.itemconfig(part, fill=self.button_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.button_color, width=0)

    def clicked(self, event=0):
        self.value = event.x / self.width

        if self.value > 1:
            self.value = 1
        if self.value < 0:
            self.value = 0

        self.update()

        if self.callback_function is not None:
            self.callback_function(self.value)

    def update(self):
        for part in self.button_parts:
            self.canvas.delete(part)

        self.button_parts.append(self.canvas.create_oval(self.value * (self.width-self.height), 0,
                                                         self.value * (self.width-self.height) + self.height, self.height))

        for part in self.button_parts:
            if self.hover_state is True:
                if type(self.button_hover_color) == tuple:
                    self.canvas.itemconfig(part, fill=self.button_hover_color[self.appearance_mode], width=0)
                else:
                    self.canvas.itemconfig(part, fill=self.button_hover_color, width=0)
            else:
                if type(self.button_color) == tuple:
                    self.canvas.itemconfig(part, fill=self.button_color[self.appearance_mode], width=0)
                else:
                    self.canvas.itemconfig(part, fill=self.button_color, width=0)

    def on_enter(self, event=0):
        self.hover_state = True
        for part in self.button_parts:
            if type(self.button_hover_color) == tuple:
                self.canvas.itemconfig(part, fill=self.button_hover_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.button_hover_color, width=0)

    def on_leave(self, event=0):
        self.hover_state = False
        for part in self.button_parts:
            if type(self.button_color) == tuple:
                self.canvas.itemconfig(part, fill=self.button_color[self.appearance_mode], width=0)
            else:
                self.canvas.itemconfig(part, fill=self.button_color, width=0)

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        self.update()

        if self.callback_function is not None:
            self.callback_function(self.value)

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

