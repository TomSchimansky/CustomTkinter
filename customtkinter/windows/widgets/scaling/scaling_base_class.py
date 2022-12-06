from typing import Union, Tuple
import copy
import re
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from .scaling_tracker import ScalingTracker
from ..font import CTkFont


class CTkScalingBaseClass:
    """
    Super-class that manages the scaling values and callbacks.
    Works for widgets and windows, type must be set in init method with
    scaling_type attribute. Methods:

    - _set_scaling() abstractmethod, gets called when scaling changes, must be overridden
    - destroy() must be called when sub-class is destroyed
    - _apply_widget_scaling()
    - _reverse_widget_scaling()
    - _apply_window_scaling()
    - _reverse_window_scaling()
    - _apply_font_scaling()
    - _apply_argument_scaling()
    - _apply_geometry_scaling()
    - _reverse_geometry_scaling()
    - _parse_geometry_string()

    """
    def __init__(self, scaling_type: Literal["widget", "window"] = "widget"):
        self.__scaling_type = scaling_type

        if self.__scaling_type == "widget":
            ScalingTracker.add_widget(self._set_scaling, self)  # add callback for automatic scaling changes
            self.__widget_scaling = ScalingTracker.get_widget_scaling(self)
        elif self.__scaling_type == "window":
            ScalingTracker.activate_high_dpi_awareness()  # make process DPI aware
            ScalingTracker.add_window(self._set_scaling, self)  # add callback for automatic scaling changes
            self.__window_scaling = ScalingTracker.get_window_scaling(self)

    def destroy(self):
        if self.__scaling_type == "widget":
            ScalingTracker.remove_widget(self._set_scaling, self)
        elif self.__scaling_type == "window":
            ScalingTracker.remove_window(self._set_scaling, self)

    def _set_scaling(self, new_widget_scaling, new_window_scaling):
        """ can be overridden, but super method must be called at the beginning """
        self.__widget_scaling = new_widget_scaling
        self.__window_scaling = new_window_scaling

    def _get_widget_scaling(self) -> float:
        return self.__widget_scaling

    def _get_window_scaling(self) -> float:
        return self.__window_scaling

    def _apply_widget_scaling(self, value: Union[int, float]) -> Union[float]:
        assert self.__scaling_type == "widget"
        return value * self.__widget_scaling

    def _reverse_widget_scaling(self, value: Union[int, float]) -> Union[float]:
        assert self.__scaling_type == "widget"
        return value / self.__widget_scaling

    def _apply_window_scaling(self, value: Union[int, float]) -> int:
        assert self.__scaling_type == "window"
        return int(value * self.__window_scaling)

    def _reverse_window_scaling(self, scaled_value: Union[int, float]) -> int:
        assert self.__scaling_type == "window"
        return int(scaled_value / self.__window_scaling)

    def _apply_font_scaling(self, font: Union[Tuple, CTkFont]) -> tuple:
        """ Takes CTkFont object and returns tuple font with scaled size, has to be called again for every change of font object """
        assert self.__scaling_type == "widget"

        if type(font) == tuple:
            if len(font) == 1:
                return font
            elif len(font) == 2:
                return font[0], -abs(round(font[1] * self.__widget_scaling))
            elif 3 <= len(font) <= 6:
                return font[0], -abs(round(font[1] * self.__widget_scaling)), font[2:]
            else:
                raise ValueError(f"Can not scale font {font}. font needs to be tuple of len 1, 2 or 3")

        elif isinstance(font, CTkFont):
            return font.create_scaled_tuple(self.__widget_scaling)
        else:
            raise ValueError(f"Can not scale font '{font}' of type {type(font)}. font needs to be tuple or instance of CTkFont")

    def _apply_argument_scaling(self, kwargs: dict) -> dict:
        assert self.__scaling_type == "widget"

        scaled_kwargs = copy.copy(kwargs)

        # scale padding values
        if "pady" in scaled_kwargs:
            if isinstance(scaled_kwargs["pady"], (int, float)):
                scaled_kwargs["pady"] = self._apply_widget_scaling(scaled_kwargs["pady"])
            elif isinstance(scaled_kwargs["pady"], tuple):
                scaled_kwargs["pady"] = tuple([self._apply_widget_scaling(v) for v in scaled_kwargs["pady"]])
        if "padx" in kwargs:
            if isinstance(scaled_kwargs["padx"], (int, float)):
                scaled_kwargs["padx"] = self._apply_widget_scaling(scaled_kwargs["padx"])
            elif isinstance(scaled_kwargs["padx"], tuple):
                scaled_kwargs["padx"] = tuple([self._apply_widget_scaling(v) for v in scaled_kwargs["padx"]])

        # scaled x, y values for place geometry manager
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
        assert self.__scaling_type == "window"

        width, height, x, y = self._parse_geometry_string(geometry_string)

        if x is None and y is None:  # no <x> and <y> in geometry_string
            return f"{round(width * self.__window_scaling)}x{round(height * self.__window_scaling)}"

        elif width is None and height is None:  # no <width> and <height> in geometry_string
            return f"+{x}+{y}"

        else:
            return f"{round(width * self.__window_scaling)}x{round(height * self.__window_scaling)}+{x}+{y}"

    def _reverse_geometry_scaling(self, scaled_geometry_string: str) -> str:
        assert self.__scaling_type == "window"

        width, height, x, y = self._parse_geometry_string(scaled_geometry_string)

        if x is None and y is None:  # no <x> and <y> in geometry_string
            return f"{round(width / self.__window_scaling)}x{round(height / self.__window_scaling)}"

        elif width is None and height is None:  # no <width> and <height> in geometry_string
            return f"+{x}+{y}"

        else:
            return f"{round(width / self.__window_scaling)}x{round(height / self.__window_scaling)}+{x}+{y}"
