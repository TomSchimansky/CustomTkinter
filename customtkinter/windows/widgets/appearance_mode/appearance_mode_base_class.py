from typing import Union, Tuple, List

from .appearance_mode_tracker import AppearanceModeTracker


class CTkAppearanceModeBaseClass:
    """
    Super-class that manages the appearance mode. Methods:

    - destroy() must be called when sub-class is destroyed
    - _set_appearance_mode() abstractmethod, gets called when appearance mode changes, must be overridden
    - _apply_appearance_mode()

    """
    def __init__(self):
        AppearanceModeTracker.add(self._set_appearance_mode, self)
        self.__appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

    def destroy(self):
        AppearanceModeTracker.remove(self._set_appearance_mode)

    def _set_appearance_mode(self, mode_string: str):
        """ can be overridden but super method must be called at the beginning """
        if mode_string.lower() == "dark":
            self.__appearance_mode = 1
        elif mode_string.lower() == "light":
            self.__appearance_mode = 0

    def _get_appearance_mode(self) -> str:
        """ get appearance mode as a string, 'light' or 'dark' """
        if self.__appearance_mode == 0:
            return "light"
        else:
            return "dark"

    def _apply_appearance_mode(self, color: Union[str, Tuple[str, str], List[str]]) -> str:
        """
        color can be either a single hex color string or a color name or it can be a
        tuple color with (light_color, dark_color). The functions returns
        always a single color string
        """

        if isinstance(color, (tuple, list)):
            return color[self.__appearance_mode]
        else:
            return color

    @staticmethod
    def _check_color_type(color: any, transparency: bool = False):
        if color is None:
            raise ValueError(f"color is None, for transparency set color='transparent'")
        elif isinstance(color, (tuple, list)) and (color[0] == "transparent" or color[1] == "transparent"):
            raise ValueError(f"transparency is not allowed in tuple color {color}, use 'transparent'")
        elif color == "transparent" and transparency is False:
            raise ValueError(f"transparency is not allowed for this attribute")
        elif isinstance(color, str):
            return color
        elif isinstance(color, (tuple, list)) and len(color) == 2 and isinstance(color[0], str) and isinstance(color[1], str):
            return color
        else:
            raise ValueError(f"color {color} must be string ('transparent' or 'color-name' or 'hex-color') or tuple of two strings, not {type(color)}")
