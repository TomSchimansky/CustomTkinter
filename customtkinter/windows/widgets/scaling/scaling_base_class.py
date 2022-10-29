from typing import Union, Tuple
from abc import ABC, abstractmethod
import copy
import re
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from .scaling_tracker import ScalingTracker
from ..font.ctk_font import CTkFont


class CTkScalingBaseClass(ABC):
    def __init__(self, scaling_type: Literal["widget", "window"] = "widget"):
        self._scaling_type = scaling_type

        if self._scaling_type == "widget":
            ScalingTracker.add_widget(self._set_scaling, self)  # add callback for automatic scaling changes
            self._widget_scaling = ScalingTracker.get_widget_scaling(self)
        elif self._scaling_type == "window":
            ScalingTracker.activate_high_dpi_awareness()  # make process DPI aware
            ScalingTracker.add_window(self._set_scaling, self)  # add callback for automatic scaling changes
            self._window_scaling = ScalingTracker.get_window_scaling(self)

    def destroy(self):
        if self._scaling_type == "widget":
            ScalingTracker.remove_widget(self._set_scaling, self)
        elif self._scaling_type == "window":
            ScalingTracker.remove_window(self._set_scaling, self)

    def _apply_widget_scaling(self, value: Union[int, float, str]) -> Union[float, str]:
        assert self._scaling_type == "widget"

        if isinstance(value, (int, float)):
            return value * self._widget_scaling
        else:
            return value

    def _apply_font_scaling(self, font: Union[Tuple, CTkFont]) -> tuple:
        """ Takes CTkFont object and returns tuple font with scaled size, has to be called again for every change of font object """
        assert self._scaling_type == "widget"

        if type(font) == tuple:
            if len(font) == 1:
                return font
            elif len(font) == 2:
                return font[0], -abs(round(font[1] * self._widget_scaling))
            elif len(font) == 3:
                return font[0], -abs(round(font[1] * self._widget_scaling)), font[2]
            else:
                raise ValueError(f"Can not scale font {font}. font needs to be tuple of len 1, 2 or 3")

        elif isinstance(font, CTkFont):
            return font.create_scaled_tuple(self._widget_scaling)
        else:
            raise ValueError(f"Can not scale font '{font}' of type {type(font)}. font needs to be tuple or instance of CTkFont")

    def _apply_argument_scaling(self, kwargs: dict) -> dict:
        assert self._scaling_type == "widget"

        scaled_kwargs = copy.copy(kwargs)

        if "pady" in scaled_kwargs:
            if isinstance(scaled_kwargs["pady"], (int, float, str)):
                scaled_kwargs["pady"] = self._apply_widget_scaling(scaled_kwargs["pady"])
            elif isinstance(scaled_kwargs["pady"], tuple):
                scaled_kwargs["pady"] = tuple([self._apply_widget_scaling(v) for v in scaled_kwargs["pady"]])
        if "padx" in kwargs:
            if isinstance(scaled_kwargs["padx"], (int, float, str)):
                scaled_kwargs["padx"] = self._apply_widget_scaling(scaled_kwargs["padx"])
            elif isinstance(scaled_kwargs["padx"], tuple):
                scaled_kwargs["padx"] = tuple([self._apply_widget_scaling(v) for v in scaled_kwargs["padx"]])

        if "x" in scaled_kwargs:
            scaled_kwargs["x"] = self._apply_widget_scaling(scaled_kwargs["x"])
        if "y" in scaled_kwargs:
            scaled_kwargs["y"] = self._apply_widget_scaling(scaled_kwargs["y"])

        return scaled_kwargs

    @staticmethod
    def _parse_geometry_string(geometry_string: str) -> tuple:
        #                 index:   1                   2           3          4             5       6
        # regex group structure: ('<width>x<height>', '<width>', '<height>', '+-<x>+-<y>', '-<x>', '-<y>')
        result = re.search(r"((\d+)x(\d+)){0,1}(\+{0,1}([+-]{0,1}\d+)\+{0,1}([+-]{0,1}\d+)){0,1}", geometry_string)

        width = int(result.group(2)) if result.group(2) is not None else None
        height = int(result.group(3)) if result.group(3) is not None else None
        x = int(result.group(5)) if result.group(5) is not None else None
        y = int(result.group(6)) if result.group(6) is not None else None

        return width, height, x, y

    def _apply_geometry_scaling(self, geometry_string: str) -> str:
        assert self._scaling_type == "window"

        width, height, x, y = self._parse_geometry_string(geometry_string)

        if x is None and y is None:  # no <x> and <y> in geometry_string
            return f"{round(width * self._window_scaling)}x{round(height * self._window_scaling)}"

        elif width is None and height is None:  # no <width> and <height> in geometry_string
            return f"+{x}+{y}"

        else:
            return f"{round(width * self._window_scaling)}x{round(height * self._window_scaling)}+{x}+{y}"

    def _reverse_geometry_scaling(self, scaled_geometry_string: str) -> str:
        assert self._scaling_type == "window"

        width, height, x, y = self._parse_geometry_string(scaled_geometry_string)

        if x is None and y is None:  # no <x> and <y> in geometry_string
            return f"{round(width / self._window_scaling)}x{round(height / self._window_scaling)}"

        elif width is None and height is None:  # no <width> and <height> in geometry_string
            return f"+{x}+{y}"

        else:
            return f"{round(width / self._window_scaling)}x{round(height / self._window_scaling)}+{x}+{y}"

    def _apply_window_scaling(self, value):
        assert self._scaling_type == "window"

        if isinstance(value, (int, float)):
            return int(value * self._window_scaling)
        else:
            return value

    @abstractmethod
    def _set_scaling(self, new_widget_scaling, new_window_scaling):
        return
