from typing import Union, Tuple, List


class CTkAppearanceModeBaseClass:
    def __init__(self):

    def _apply_appearance_mode(self, color: Union[str, Tuple[str, str], List[str]]) -> str:
        """ color can be either a single hex color string or a color name or it can be a
            tuple color with (light_color, dark_color). The functions returns
            always a single color string """

        if type(color) == tuple or type(color) == list:
            return color[self._appearance_mode]
        else:
            return color
