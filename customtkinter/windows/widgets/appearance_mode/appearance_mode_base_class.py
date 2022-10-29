from typing import Union, Tuple, List
from abc import ABC, abstractmethod

from .appearance_mode_tracker import AppearanceModeTracker


class CTkAppearanceModeBaseClass(ABC):
    def __init__(self):
        AppearanceModeTracker.add(self._set_appearance_mode, self)
        self._appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

    def destroy(self):
        AppearanceModeTracker.remove(self._set_appearance_mode)

    def _apply_appearance_mode(self, color: Union[str, Tuple[str, str], List[str]]) -> str:
        """ color can be either a single hex color string or a color name or it can be a
            tuple color with (light_color, dark_color). The functions returns
            always a single color string """

        if type(color) == tuple or type(color) == list:
            return color[self._appearance_mode]
        else:
            return color

    @abstractmethod
    def _set_appearance_mode(self, mode_string: str):
        return
