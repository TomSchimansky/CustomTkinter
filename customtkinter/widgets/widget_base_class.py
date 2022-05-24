import tkinter
import tkinter.ttk as ttk
import copy
import re
from typing import Callable, Union

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

from ..windows.ctk_tk import CTk
from ..windows.ctk_toplevel import CTkToplevel
from ..appearance_mode_tracker import AppearanceModeTracker
from ..scaling_tracker import ScalingTracker
from ..theme_manager import ThemeManager


class CTkBaseClass(tkinter.Frame):
    def __init__(self, *args, bg_color=None, width, height, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)  # set desired size of underlying tkinter.Frame

        self.bg_color = self.detect_color_of_master() if bg_color is None else bg_color

        self.current_width = width  # current_width and current_height in pixel, represent current size of the widget (not the desired size by init)
        self.current_height = height  # current_width and current_height are independent of the scale
        self.desired_width = width
        self.desired_height = height

        # add set_scaling method to callback list of ScalingTracker for automatic scaling changes
        ScalingTracker.add_widget(self.set_scaling, self)
        self.widget_scaling = ScalingTracker.get_widget_scaling(self)
        self.spacing_scaling = ScalingTracker.get_spacing_scaling(self)

        super().configure(width=self.apply_widget_scaling(self.desired_width),
                          height=self.apply_widget_scaling(self.desired_height))

        # save latest geometry function and kwargs
        class GeometryCallDict(TypedDict):
            function: Callable
            kwargs: dict

        self.last_geometry_manager_call: Union[GeometryCallDict, None] = None

        # add set_appearance_mode method to callback list of AppearanceModeTracker for appearance mode changes
        AppearanceModeTracker.add(self.set_appearance_mode, self)
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        super().configure(bg=ThemeManager.single_color(self.bg_color, self.appearance_mode))

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

    def place(self, **kwargs):
        self.last_geometry_manager_call = {"function": super().place, "kwargs": kwargs}
        super().place(**self.apply_argument_scaling(kwargs))

    def pack(self, **kwargs):
        self.last_geometry_manager_call = {"function": super().pack, "kwargs": kwargs}
        super().pack(**self.apply_argument_scaling(kwargs))

    def grid(self, **kwargs):
        self.last_geometry_manager_call = {"function": super().grid, "kwargs": kwargs}
        super().grid(**self.apply_argument_scaling(kwargs))

    def apply_argument_scaling(self, kwargs: dict) -> dict:
        scaled_kwargs = copy.copy(kwargs)

        if "pady" in scaled_kwargs:
            if isinstance(scaled_kwargs["pady"], (int, float, str)):
                scaled_kwargs["pady"] = self.apply_spacing_scaling(scaled_kwargs["pady"])
            elif isinstance(scaled_kwargs["pady"], tuple):
                scaled_kwargs["pady"] = tuple([self.apply_spacing_scaling(v) for v in scaled_kwargs["pady"]])
        if "padx" in kwargs:
            if isinstance(scaled_kwargs["padx"], (int, float, str)):
                scaled_kwargs["padx"] = self.apply_spacing_scaling(scaled_kwargs["padx"])
            elif isinstance(scaled_kwargs["padx"], tuple):
                scaled_kwargs["padx"] = tuple([self.apply_spacing_scaling(v) for v in scaled_kwargs["padx"]])

        if "x" in scaled_kwargs:
            scaled_kwargs["x"] = self.apply_spacing_scaling(scaled_kwargs["x"])
        if "y" in scaled_kwargs:
            scaled_kwargs["y"] = self.apply_spacing_scaling(scaled_kwargs["y"])

        return scaled_kwargs

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
        if round(self.current_width) != round(event.width / self.widget_scaling) or round(self.current_height) != round(event.height / self.widget_scaling):
            self.current_width = (event.width / self.widget_scaling)  # adjust current size according to new size given by event
            self.current_height = (event.height / self.widget_scaling)  # current_width and current_height are independent of the scale

            self.draw(no_color_updates=True)  # faster drawing without color changes

    def detect_color_of_master(self, master_widget=None):
        """ detect color of self.master widget to set correct bg_color """

        if master_widget is None:
            master_widget = self.master

        if isinstance(master_widget, CTkBaseClass) and hasattr(master_widget, "fg_color"):  # master is CTkFrame
            if master_widget.fg_color is not None:
                return master_widget.fg_color

            # if fg_color of master is None, try to retrieve fg_color from master of master
            elif hasattr(master_widget.master, "master"):
                return self.detect_color_of_master(self.master.master)

        elif isinstance(master_widget, (ttk.Frame, ttk.LabelFrame, ttk.Notebook)):  # master is ttk widget
            try:
                ttk_style = ttk.Style()
                return ttk_style.lookup(master_widget.winfo_class(), 'background')
            except Exception:
                return "#FFFFFF", "#000000"

        else:  # master is normal tkinter widget
            try:
                return master_widget.cget("bg")  # try to get bg color by .cget() method
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

    def set_scaling(self, new_widget_scaling, new_spacing_scaling, new_window_scaling):
        self.widget_scaling = new_widget_scaling
        self.spacing_scaling = new_spacing_scaling

        super().configure(width=self.apply_widget_scaling(self.desired_width),
                          height=self.apply_widget_scaling(self.desired_height))

        if self.last_geometry_manager_call is not None:
            self.last_geometry_manager_call["function"](**self.apply_argument_scaling(self.last_geometry_manager_call["kwargs"]))

    def set_dimensions(self, width=None, height=None):
        if width is not None:
            self.desired_width = width
        if height is not None:
            self.desired_height = height

        super().configure(width=self.apply_widget_scaling(self.desired_width),
                          height=self.apply_widget_scaling(self.desired_height))

    def apply_widget_scaling(self, value):
        if isinstance(value, (int, float)):
            return value * self.widget_scaling
        else:
            return value

    def apply_spacing_scaling(self, value):
        if isinstance(value, (int, float)):
            return value * self.spacing_scaling
        else:
            return value

    def apply_font_scaling(self, font):
        if type(font) == tuple or type(font) == list:
            font_list = list(font)
            for i in range(len(font_list)):
                if (type(font_list[i]) == int or type(font_list[i]) == float) and font_list[i] < 0:
                    font_list[i] = int(font_list[i] * self.widget_scaling)
            return tuple(font_list)

        elif type(font) == str:
            for negative_number in re.findall(r" -\d* ", font):
                font = font.replace(negative_number, f" {int(int(negative_number) * self.widget_scaling)} ")
            return font

        elif isinstance(font, tkinter.font.Font):
            new_font_object = copy.copy(font)
            if font.cget("size") < 0:
                new_font_object.config(size=int(font.cget("size") * self.widget_scaling))
            return new_font_object

        else:
            return font

    def draw(self, no_color_updates=False):
        """ abstract of draw method to be overridden """
        pass


