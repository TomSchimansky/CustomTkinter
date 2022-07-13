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
    """ Base class of every CTk widget, handles the dimensions, bg_color,
        appearance_mode changes, scaling, bg changes of master if master is not a CTk widget """

    def __init__(self,
                 *args,
                 bg_color: Union[str, tuple] = None,
                 width: int,
                 height: int,
                 **kwargs):

        super().__init__(*args, width=width, height=height, **kwargs)  # set desired size of underlying tkinter.Frame

        # dimensions
        self._current_width = width  # _current_width and _current_height in pixel, represent current size of the widget
        self._current_height = height  # _current_width and _current_height are independent of the scale
        self._desired_width = width  # _desired_width and _desired_height, represent desired size set by width and height
        self._desired_height = height

        # scaling
        ScalingTracker.add_widget(self.set_scaling, self)  # add callback for automatic scaling changes
        self._widget_scaling = ScalingTracker.get_widget_scaling(self)
        self._spacing_scaling = ScalingTracker.get_spacing_scaling(self)

        super().configure(width=self.apply_widget_scaling(self._desired_width),
                          height=self.apply_widget_scaling(self._desired_height))

        # save latest geometry function and kwargs
        class GeometryCallDict(TypedDict):
            function: Callable
            kwargs: dict

        self._last_geometry_manager_call: Union[GeometryCallDict, None] = None

        # add set_appearance_mode method to callback list of AppearanceModeTracker for appearance mode changes
        AppearanceModeTracker.add(self.set_appearance_mode, self)
        self._appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        # background color
        self.bg_color = self.detect_color_of_master() if bg_color is None else bg_color

        super().configure(bg=ThemeManager.single_color(self.bg_color, self._appearance_mode))

        # overwrite configure methods of master when master is tkinter widget, so that bg changes get applied on child CTk widget as well
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
        self._last_geometry_manager_call = {"function": super().place, "kwargs": kwargs}
        super().place(**self.apply_argument_scaling(kwargs))

    def pack(self, **kwargs):
        self._last_geometry_manager_call = {"function": super().pack, "kwargs": kwargs}
        super().pack(**self.apply_argument_scaling(kwargs))

    def grid(self, **kwargs):
        self._last_geometry_manager_call = {"function": super().grid, "kwargs": kwargs}
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

    def configure(self, require_redraw=False, **kwargs):
        """ basic configure with bg_color support, to be overridden """

        if "bg_color" in kwargs:
            new_bg_color = kwargs.pop("bg_color")
            if new_bg_color is None:
                self.bg_color = self.detect_color_of_master()
            else:
                self.bg_color = new_bg_color
            require_redraw = True

        super().configure(**kwargs)

        if require_redraw:
            self.draw()

    def update_dimensions_event(self, event):
        # only redraw if dimensions changed (for performance), independent of scaling
        if round(self._current_width) != round(event.width / self._widget_scaling) or round(self._current_height) != round(event.height / self._widget_scaling):
            self._current_width = (event.width / self._widget_scaling)  # adjust current size according to new size given by event
            self._current_height = (event.height / self._widget_scaling)  # _current_width and _current_height are independent of the scale

            self.draw(no_color_updates=True)  # faster drawing without color changes

    def detect_color_of_master(self, master_widget=None):
        """ detect color of self.master widget to set correct bg_color """

        if master_widget is None:
            master_widget = self.master

        if isinstance(master_widget, (CTkBaseClass, CTk, CTkToplevel)) and hasattr(master_widget, "fg_color"):
            if master_widget.fg_color is not None:
                return master_widget.fg_color

            # if fg_color of master is None, try to retrieve fg_color from master of master
            elif hasattr(master_widget.master, "master"):
                return self.detect_color_of_master(self.master.master)

        elif isinstance(master_widget, (ttk.Frame, ttk.LabelFrame, ttk.Notebook, ttk.Label)):  # master is ttk widget
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
            self._appearance_mode = 1
        elif mode_string.lower() == "light":
            self._appearance_mode = 0

        self.draw()

    def set_scaling(self, new_widget_scaling, new_spacing_scaling, new_window_scaling):
        self._widget_scaling = new_widget_scaling
        self._spacing_scaling = new_spacing_scaling

        super().configure(width=self.apply_widget_scaling(self._desired_width),
                          height=self.apply_widget_scaling(self._desired_height))

        if self._last_geometry_manager_call is not None:
            self._last_geometry_manager_call["function"](**self.apply_argument_scaling(self._last_geometry_manager_call["kwargs"]))

    def set_dimensions(self, width=None, height=None):
        if width is not None:
            self._desired_width = width
        if height is not None:
            self._desired_height = height

        super().configure(width=self.apply_widget_scaling(self._desired_width),
                          height=self.apply_widget_scaling(self._desired_height))

    def apply_widget_scaling(self, value: Union[int, float, str]) -> Union[float, str]:
        if isinstance(value, (int, float)):
            return value * self._widget_scaling
        else:
            return value

    def apply_spacing_scaling(self, value: Union[int, float, str]) -> Union[float, str]:
        if isinstance(value, (int, float)):
            return value * self._spacing_scaling
        else:
            return value

    def apply_font_scaling(self, font):
        if type(font) == tuple or type(font) == list:
            font_list = list(font)
            for i in range(len(font_list)):
                if (type(font_list[i]) == int or type(font_list[i]) == float) and font_list[i] < 0:
                    font_list[i] = int(font_list[i] * self._widget_scaling)
            return tuple(font_list)

        elif type(font) == str:
            for negative_number in re.findall(r" -\d* ", font):
                font = font.replace(negative_number, f" {int(int(negative_number) * self._widget_scaling)} ")
            return font

        elif isinstance(font, tkinter.font.Font):
            new_font_object = copy.copy(font)
            if font.cget("size") < 0:
                new_font_object.config(size=int(font.cget("size") * self._widget_scaling))
            return new_font_object

        else:
            return font

    def draw(self, no_color_updates: bool = False):
        """ abstract of draw method to be overridden """
        pass
