import tkinter
import sys

from .customtkinter_tk import CTk
from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_theme_manager import CTkThemeManager
from .customtkinter_canvas import CTkCanvas
from .customtkinter_settings import CTkSettings
from .customtkinter_draw_engine import CTkDrawEngine


class CTkLabel(tkinter.Frame):
    def __init__(self, *args,
                 master=None,
                 bg_color=None,
                 fg_color="default_theme",
                 text_color="default_theme",
                 corner_radius="default_theme",
                 width=120,
                 height=25,
                 text="CTkLabel",
                 text_font="default_theme",
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
        self.fg_color = CTkThemeManager.theme["color"]["label"] if fg_color == "default_theme" else fg_color
        if self.fg_color is None:
            self.fg_color = self.bg_color
        self.text_color = CTkThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color

        self.width = width
        self.height = height
        self.corner_radius = CTkThemeManager.theme["shape"]["label_corner_radius"] if corner_radius == "default_theme" else corner_radius

        if self.corner_radius * 2 > self.height:
            self.corner_radius = self.height / 2
        elif self.corner_radius * 2 > self.width:
            self.corner_radius = self.width / 2

        self.text = text
        self.text_font = (CTkThemeManager.theme["text"]["font"], CTkThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.width,
                                height=self.height)
        self.canvas.grid(row=0, column=0, sticky="nswe")

        self.text_label = tkinter.Label(master=self,
                                        highlightthickness=0,
                                        bd=0,
                                        text=self.text,
                                        font=self.text_font,
                                        **kwargs)
        self.text_label.grid(row=0, column=0, padx=self.corner_radius)

        self.draw_engine = CTkDrawEngine(self.canvas, CTkSettings.preferred_drawing_method)

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

    def update_dimensions(self, event):
        # only redraw if dimensions changed (for performance)
        if self.width != event.width or self.height != event.height:
            self.width = event.width
            self.height = event.height

            # self.canvas.config(width=self.width, height=self.height)
            self.draw()

    def draw(self):
        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border(self.width, self.height, self.corner_radius, 0)

        self.canvas.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))

        if CTkThemeManager.single_color(self.fg_color, self.appearance_mode) is not None:
            self.canvas.itemconfig("inner_parts",
                                   fill=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                                   outline=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))

            self.text_label.configure(fg=CTkThemeManager.single_color(self.text_color, self.appearance_mode),
                                      bg=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))
        else:
            self.canvas.itemconfig("inner_parts",
                                   fill=CTkThemeManager.single_color(self.bg_color, self.appearance_mode),
                                   outline=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))

            self.text_label.configure(fg=CTkThemeManager.single_color(self.text_color, self.appearance_mode),
                                      bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))

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
