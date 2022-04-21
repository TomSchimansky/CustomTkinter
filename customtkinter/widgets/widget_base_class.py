import tkinter
import tkinter.ttk as ttk
import copy
import re
import math

from .ctk_tk import CTk
from .ctk_toplevel import CTkToplevel
from ..appearance_mode_tracker import AppearanceModeTracker
from ..scaling_tracker import ScalingTracker
from ..theme_manager import CTkThemeManager


class CTkBaseClass(tkinter.Frame):
    def __init__(self, *args, bg_color=None, width, height, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)  # set desired size of underlying tkinter.Frame

        self.bg_color = self.detect_color_of_master() if bg_color is None else bg_color
        self.width = width  # width and height in pixel, represent current size of the widget (not the desired size by init)
        self.height = height  # width and height are independent of the scale

        # add set_scaling method to callback list of ScalingTracker for automatic scaling changes
        ScalingTracker.add_widget(self.set_scaling, self)
        self.scaling = ScalingTracker.get_widget_scaling(self)

        # add set_appearance_mode method to callback list of AppearanceModeTracker for appearance mode changes
        AppearanceModeTracker.add(self.set_appearance_mode, self)
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        super().configure(bg=CTkThemeManager.single_color(self.bg_color, self.appearance_mode))

        # overwrite configure methods of master when master is tkinter widget, so that bg changes get applied on child CTk widget too
        if isinstance(self.master, (tkinter.Tk, tkinter.Toplevel, tkinter.Frame)) and not isinstance(self.master, (CTkBaseClass, CTk, CTkToplevel)):
            master_old_configure = self.master.config

            def new_configure(*args, **kwargs):
                if "bg" in kwargs:
                    self.configure(bg_color=kwargs["bg"])
                elif "background" in kwargs:
                    self.configure(bg_color=kwargs["background"])

                # args[0] is dict when attribute gets changed by widget[<attribute>] syntax
                elif len(args) > 0 and type(args[0]) == dict:
                    if "bg" in args[0]:
                        self.configure(bg_color=args[0]["bg"])
                    elif "background" in args[0]:
                        self.configure(bg_color=args[0]["background"])
                master_old_configure(*args, **kwargs)

            self.master.config = new_configure
            self.master.configure = new_configure

    def destroy(self):
        AppearanceModeTracker.remove(self.set_appearance_mode)
        super().destroy()

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        """ basic configure with bg_color support, to be overridden """

        require_redraw = False

        if "bg_color" in kwargs:
            if kwargs["bg_color"] is None:
                self.bg_color = self.detect_color_of_master()
            else:
                self.bg_color = kwargs["bg_color"]
            require_redraw = True
            del kwargs["bg_color"]

        super().configure(*args, **kwargs)

        if require_redraw:
            self.draw()

    def update_dimensions_event(self, event):
        # only redraw if dimensions changed (for performance)
        if self.width != math.floor(event.width * self.scaling) or self.height != math.floor(event.height * self.scaling):
            self.width = event.width / self.scaling  # adjust current size according to new size given by event
            self.height = event.height / self.scaling  # width and height are independent of the scale

            self.draw(no_color_updates=True)  # faster drawing without color changes

    def detect_color_of_master(self):
        """ detect color of self.master widget to set correct bg_color """

        if isinstance(self.master, CTkBaseClass) and hasattr(self.master, "fg_color"):  # master is CTkFrame
            return self.master.fg_color

        elif isinstance(self.master, (ttk.Frame, ttk.LabelFrame, ttk.Notebook)):  # master is ttk widget
            try:
                ttk_style = ttk.Style()
                return ttk_style.lookup(self.master.winfo_class(), 'background')
            except Exception:
                return "#FFFFFF", "#000000"

        else:  # master is normal tkinter widget
            try:
                return self.master.cget("bg")  # try to get bg color by .cget() method
            except Exception:
                return "#FFFFFF", "#000000"

    def set_appearance_mode(self, mode_string):
        if mode_string.lower() == "dark":
            self.appearance_mode = 1
        elif mode_string.lower() == "light":
            self.appearance_mode = 0

        if isinstance(self.master, (CTkBaseClass, CTk)) and hasattr(self.master, "fg_color"):
            self.bg_color = self.master.fg_color
        else:
            self.bg_color = self.master.cget("bg")

        self.draw()

    def set_scaling(self, new_scaling):
        self.scaling = new_scaling

        super().configure(width=self.width * self.scaling, height=self.height * self.scaling)

    def apply_font_scaling(self, font):
        if type(font) == tuple or type(font) == list:
            font_list = list(font)
            for i in range(len(font_list)):
                if (type(font_list[i]) == int or type(font_list[i]) == float) and font_list[i] < 0:
                    font_list[i] = int(font_list[i] * self.scaling)
            return tuple(font_list)

        elif type(font) == str:
            for negative_number in re.findall(r" -\d* ", font):
                font = font.replace(negative_number, f" {int(int(negative_number) * self.scaling)} ")
            return font

        elif isinstance(font, tkinter.font.Font):
            new_font_object = copy.copy(font)
            if font.cget("size") < 0:
                new_font_object.config(size=int(font.cget("size") * self.scaling))
            return new_font_object

        else:
            return font

    def draw(self, no_color_updates=False):
        """ abstract of draw method to be overridden """
        pass


