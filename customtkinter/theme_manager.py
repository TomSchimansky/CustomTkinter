import sys
import os
import json


class ThemeManager:

    theme = {}  # contains all the theme data
    built_in_themes = ["blue", "green", "dark-blue", "sweetkind"]

    @classmethod
    def load_theme(cls, theme_name_or_path: str):
        script_directory = os.path.dirname(os.path.abspath(__file__))

        if theme_name_or_path in cls.built_in_themes:
            with open(os.path.join(script_directory, "assets", "themes", f"{theme_name_or_path}.json"), "r") as f:
                cls.theme = json.load(f)
        else:
            with open(theme_name_or_path, "r") as f:
                cls.theme = json.load(f)

        if sys.platform == "darwin":
            cls.theme["text"] = cls.theme["text"]["macOS"]
        elif sys.platform.startswith("win"):
            cls.theme["text"] = cls.theme["text"]["Windows"]
        else:
            cls.theme["text"] = cls.theme["text"]["Linux"]

    @staticmethod
    def single_color(color, appearance_mode: int) -> str:
        """ color can be either a single hex color string or a color name or it can be a
            tuple color with (light_color, dark_color). The functions then returns
            always a single color string """

        if type(color) == tuple or type(color) == list:
            return color[appearance_mode]
        else:
            return color

    @staticmethod
    def rgb2hex(rgb_color: tuple) -> str:
        return "#{:02x}{:02x}{:02x}".format(round(rgb_color[0]), round(rgb_color[1]), round(rgb_color[2]))

    @staticmethod
    def hex2rgb(hex_color: str) -> tuple:
        return tuple(int(hex_color.strip("#")[i:i+2], 16) for i in (0, 2, 4))

    @classmethod
    def linear_blend(cls, color_1: str, color_2: str, blend_factor: float) -> str:
        """ Blends two hex colors linear, where blend_factor of 0
            results in color_1 and blend_factor of 1 results in color_2. """

        if color_1 is None or color_2 is None:
            return None

        rgb_1 = cls.hex2rgb(color_1)
        rgb_2 = cls.hex2rgb(color_2)

        new_rgb = (rgb_1[0] + (rgb_2[0] - rgb_1[0]) * blend_factor,
                   rgb_1[1] + (rgb_2[1] - rgb_1[1]) * blend_factor,
                   rgb_1[2] + (rgb_2[2] - rgb_1[2]) * blend_factor)

        return cls.rgb2hex(new_rgb)

    @classmethod
    def get_minimal_darker(cls, color: str) -> str:
        if color.startswith("#"):
            color_rgb = cls.hex2rgb(color)
            if color_rgb[0] > 0:
                return cls.rgb2hex((color_rgb[0] - 1, color_rgb[1], color_rgb[2]))
            elif color_rgb[1] > 0:
                return cls.rgb2hex((color_rgb[0], color_rgb[1] - 1, color_rgb[2]))
            elif color_rgb[2] > 0:
                return cls.rgb2hex((color_rgb[0], color_rgb[1], color_rgb[2] - 1))
            else:
                return cls.rgb2hex((color_rgb[0] + 1, color_rgb[1], color_rgb[2] - 1))  # otherwise slightly lighter

    @classmethod
    def multiply_hex_color(cls, hex_color: str, factor: float = 1.0) -> str:
        try:
            rgb_color = ThemeManager.hex2rgb(hex_color)
            dark_rgb_color = (min(255, rgb_color[0] * factor),
                              min(255, rgb_color[1] * factor),
                              min(255, rgb_color[2] * factor))
            return ThemeManager.rgb2hex(dark_rgb_color)
        except Exception as err:
            # sys.stderr.write("ERROR (CTkColorManager): failed to darken the following color: " + str(hex_color) + " " + str(err))
            return hex_color

    @classmethod
    def set_main_color(cls, main_color, main_color_hover):
        cls.MAIN_COLOR = main_color
        cls.MAIN_HOVER_COLOR = main_color_hover
