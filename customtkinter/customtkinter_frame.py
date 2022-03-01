import tkinter

from .customtkinter_tk import CTk
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_theme_manager import CTkThemeManager
from .customtkinter_canvas import CTkCanvas
from .customtkinter_settings import CTkSettings
from .customtkinter_draw_engine import CTkDrawEngine


class CTkFrame(tkinter.Frame):
    def __init__(self, *args,
                 bg_color=None,
                 fg_color="default_theme",
                 border_color="default_theme",
                 border_width="default_theme",
                 corner_radius="default_theme",
                 width=200,
                 height=200,
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
        self.border_color = CTkThemeManager.theme["color"]["frame_border"] if border_color == "default_theme" else border_color

        if fg_color == "default_theme":
            if isinstance(self.master, CTkFrame):
                if self.master.fg_color == CTkThemeManager.theme["color"]["frame_low"]:
                    self.fg_color = CTkThemeManager.theme["color"]["frame_high"]
                else:
                    self.fg_color = CTkThemeManager.theme["color"]["frame_low"]
            else:
                self.fg_color = CTkThemeManager.theme["color"]["frame_low"]
        else:
            self.fg_color = fg_color

        self.width = width
        self.height = height
        self.configure(width=self.width, height=self.height)

        self.corner_radius = CTkThemeManager.theme["shape"]["frame_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = CTkThemeManager.theme["shape"]["frame_border_width"] if border_width == "default_theme" else border_width

        if self.corner_radius * 2 > self.height:
            self.corner_radius = self.height / 2
        elif self.corner_radius * 2 > self.width:
            self.corner_radius = self.width / 2

        if self.corner_radius >= self.border_width:
            self.inner_corner_radius = self.corner_radius - self.border_width
        else:
            self.inner_corner_radius = 0

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.width,
                                height=self.height)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.canvas.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))

        self.draw_engine = CTkDrawEngine(self.canvas, CTkSettings.preferred_drawing_method)

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

            self.draw()

    def draw(self):

        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border(self.width, self.height, self.corner_radius, self.border_width)

        self.canvas.itemconfig("inner_parts",
                               fill=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                               outline=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))
        self.canvas.itemconfig("border_parts",
                               fill=CTkThemeManager.single_color(self.border_color, self.appearance_mode),
                               outline=CTkThemeManager.single_color(self.border_color, self.appearance_mode))
        self.canvas.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))

        self.canvas.tag_lower("inner_parts")
        self.canvas.tag_lower("border_parts")

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            require_redraw = True
            del kwargs["fg_color"]

            # check if CTk widgets are children of the frame and change their bg_color to new frame fg_color
            from .customtkinter_slider import CTkSlider
            from .customtkinter_progressbar import CTkProgressBar
            from .customtkinter_label import CTkLabel
            from .customtkinter_entry import CTkEntry
            from customtkinter.customtkinter_checkbox import CTkCheckBox
            from .customtkinter_button import CTkButton

            for child in self.winfo_children():
                if isinstance(child, (CTkButton, CTkLabel, CTkSlider, CTkCheckBox, CTkEntry, CTkProgressBar, CTkFrame)):
                    child.configure(bg_color=self.fg_color)

        if "bg_color" in kwargs:
            if kwargs["bg_color"] is None:
                self.bg_color = self.detect_color_of_master()
            else:
                self.bg_color = kwargs["bg_color"]
            require_redraw = True

            del kwargs["bg_color"]

        if "corner_radius" in kwargs:
            self.corner_radius = kwargs["corner_radius"]
            require_redraw = True
            del kwargs["corner_radius"]

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
