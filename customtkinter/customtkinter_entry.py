import tkinter

from .customtkinter_tk import CTk
from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_theme_manager import CTkThemeManager
from .customtkinter_canvas import CTkCanvas
from .customtkinter_settings import CTkSettings
from .customtkinter_draw_engine import CTkDrawEngine


class CTkEntry(tkinter.Frame):
    def __init__(self, *args,
                 master=None,
                 bg_color=None,
                 fg_color="default_theme",
                 text_color="default_theme",
                 placeholder_text_color="default_theme",
                 text_font="default_theme",
                 placeholder_text=None,
                 corner_radius="default_theme",
                 border_width="default_theme",
                 border_color="default_theme",
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
        self.fg_color = CTkThemeManager.theme["color"]["entry"] if fg_color == "default_theme" else fg_color
        self.text_color = CTkThemeManager.theme["color"]["text"] if text_color == "default_theme" else text_color
        self.placeholder_text_color = CTkThemeManager.theme["color"]["entry_placeholder_text"] if placeholder_text_color == "default_theme" else placeholder_text_color
        self.text_font = (CTkThemeManager.theme["text"]["font"], CTkThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font
        self.border_color = CTkThemeManager.theme["color"]["entry_border"] if border_color == "default_theme" else border_color

        self.placeholder_text = placeholder_text
        self.placeholder_text_active = False
        self.pre_placeholder_arguments = {}  # some set arguments of the entry will be changed for placeholder and then set back

        self.width = width
        self.height = height
        self.corner_radius = CTkThemeManager.theme["shape"]["button_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self.border_width = CTkThemeManager.theme["shape"]["entry_border_width"] if border_width == "default_theme" else border_width

        if self.corner_radius*2 > self.height:
            self.corner_radius = self.height/2
        elif self.corner_radius*2 > self.width:
            self.corner_radius = self.width/2

        super().configure(width=self.width, height=self.height)

        self.canvas = CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self.width,
                                height=self.height)
        self.canvas.grid(column=0, row=0, sticky="we")

        self.entry = tkinter.Entry(master=self,
                                   bd=0,
                                   width=1,
                                   highlightthickness=0,
                                   font=self.text_font,
                                   **kwargs)
        self.entry.grid(column=0, row=0, sticky="we", padx=self.corner_radius if self.corner_radius >= 6 else 6)

        self.draw_engine = CTkDrawEngine(self.canvas, CTkSettings.preferred_drawing_method)

        super().bind('<Configure>', self.update_dimensions)
        self.entry.bind('<FocusOut>', self.set_placeholder)
        self.entry.bind('<FocusIn>', self.clear_placeholder)

        self.draw()
        self.set_placeholder()

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
            try:
                return self.master.cget("bg")
            except:
                pass

    def update_dimensions(self, event):
        # only redraw if dimensions changed (for performance)
        if self.width != event.width or self.height != event.height:
            # print(event.x, event.width, self.width)
            self.width = event.width
            self.height = event.height

            self.draw()

    def set_placeholder(self, event=None):
        if self.placeholder_text is not None:
            if not self.placeholder_text_active and self.entry.get() == "":
                self.placeholder_text_active = True
                self.pre_placeholder_arguments = {"show": self.entry.cget("show")}
                self.entry.config(fg=CTkThemeManager.single_color(self.placeholder_text_color, self.appearance_mode), show="")
                self.entry.delete(0, tkinter.END)
                self.entry.insert(0, self.placeholder_text)

    def clear_placeholder(self, event=None):
        if self.placeholder_text_active:
            self.placeholder_text_active = False
            self.entry.config(fg=CTkThemeManager.single_color(self.text_color, self.appearance_mode))
            self.entry.delete(0, tkinter.END)
            for argument, value in self.pre_placeholder_arguments.items():
                self.entry[argument] = value

    def draw(self):
        self.canvas.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))

        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border(self.width, self.height, self.corner_radius, self.border_width)

        if CTkThemeManager.single_color(self.fg_color, self.appearance_mode) is not None:
            self.canvas.itemconfig("inner_parts",
                                   fill=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                                   outline=CTkThemeManager.single_color(self.fg_color, self.appearance_mode))
            self.entry.configure(bg=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                                 highlightcolor=CTkThemeManager.single_color(self.fg_color, self.appearance_mode),
                                 fg=CTkThemeManager.single_color(self.text_color, self.appearance_mode),
                                 insertbackground=CTkThemeManager.single_color(self.text_color, self.appearance_mode))
        else:
            self.canvas.itemconfig("inner_parts",
                                   fill=CTkThemeManager.single_color(self.bg_color, self.appearance_mode),
                                   outline=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))
            self.entry.configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode),
                                 highlightcolor=CTkThemeManager.single_color(self.bg_color, self.appearance_mode),
                                 fg=CTkThemeManager.single_color(self.text_color, self.appearance_mode),
                                 insertbackground=CTkThemeManager.single_color(self.text_color, self.appearance_mode))

        self.canvas.itemconfig("border_parts",
                               fill=CTkThemeManager.single_color(self.border_color, self.appearance_mode),
                               outline=CTkThemeManager.single_color(self.border_color, self.appearance_mode))

        if self.placeholder_text_active:
            self.entry.config(fg=CTkThemeManager.single_color(self.placeholder_text_color, self.appearance_mode))

    def bind(self, *args, **kwargs):
        self.entry.bind(*args, **kwargs)

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
            self.corner_radius = kwargs["corner_radius"]

            if self.corner_radius * 2 > self.height:
                self.corner_radius = self.height / 2
            elif self.corner_radius * 2 > self.width:
                self.corner_radius = self.width / 2

            self.entry.grid(column=0, row=0, sticky="we", padx=self.corner_radius if self.corner_radius >= 6 else 6)
            del kwargs["corner_radius"]
            require_redraw = True

        if "placeholder_text" in kwargs:
            pass

        self.entry.configure(*args, **kwargs)

        if require_redraw is True:
            self.draw()

    def delete(self, *args, **kwargs):
        self.entry.delete(*args, **kwargs)
        self.set_placeholder()
        return

    def insert(self, *args, **kwargs):
        self.clear_placeholder()
        return self.entry.insert(*args, **kwargs)

    def get(self):
        if self.placeholder_text_active:
            return ""
        else:
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
