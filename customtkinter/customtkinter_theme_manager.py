import sys
import os
import json


class CTkThemeManager:

    theme = {}  # contains all the theme data
    built_in_themes = ["blue", "green", "dark-blue"]

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

    @classmethod
    def initialize_color_theme(cls, theme_name):

        if sys.platform == "darwin":
            cls.TEXT_FONT_NAME = "Avenir"
        elif sys.platform.startswith("win"):
            cls.TEXT_FONT_NAME = "Roboto"
        else:
            cls.TEXT_FONT_NAME = "Roboto"

        cls.TEXT_FONT_SIZE = -14  # px height

        if theme_name.lower() == "blue":
            cls.WINDOW_BG_COLOR = ("#ECECEC", "#323232")  # macOS standard light and dark window bg colors
            cls.MAIN_COLOR = ("#64A1D2", "#1C94CF")
            cls.MAIN_HOVER_COLOR = ("#A7C2E0", "#5FB4DD")
            cls.ENTRY_COLOR = ("gray95", "#222222")
            cls.ENTRY_BORDER_COLOR = ("gray65", "gray40")
            cls.TEXT_COLOR = ("black", "white")
            cls.PLACEHOLDER_TEXT_COLOR = ("gray52", "gray62")
            cls.LABEL_BG_COLOR = ("white", "#626061")
            cls.SLIDER_BG_COLOR = ("#6B6B6B", "#222222")
            cls.SLIDER_PROGRESS_COLOR = ("#A5A6A5", "#555555")
            cls.PROGRESS_BG_COLOR = ("#6B6B6B", "#222222")
            cls.FRAME_COLOR = ("#D4D5D6", "#3F3F3F")
            cls.FRAME_2_COLOR = ("#BFBEC1", "#505050")
            cls.CHECKBOX_LINES_COLOR = ("black", "#ededed")
            cls.DARKEN_COLOR_FACTOR = 0.8  # used to generate color for disabled button

        elif theme_name.lower() == "green":
            cls.WINDOW_BG_COLOR = ("#ECECEC", "#323232")  # macOS standard light and dark window bg colors
            cls.MAIN_COLOR = ("#13C995", "#1ABE87")
            cls.MAIN_HOVER_COLOR = ("#6ACBA5", "#81E4B2")
            cls.ENTRY_COLOR = ("gray60", "#222223")
            cls.TEXT_COLOR = ("gray25", "gray92")
            cls.PLACEHOLDER_TEXT_COLOR = ("gray32", "gray55")
            cls.LABEL_BG_COLOR = ("white", "#626061")
            cls.SLIDER_BG_COLOR = ("#636363", "#0D1321")
            cls.SLIDER_PROGRESS_COLOR = ("white", "#727578")
            cls.PROGRESS_BG_COLOR = ("#636363", "#0D1321")
            cls.FRAME_COLOR = ("#D4D5D6", "#3F3F3F")
            cls.FRAME_2_COLOR = ("#BFBEC1", "#505050")
            cls.CHECKBOX_LINES_COLOR = ("#414141", "#EDEDED")
            cls.DARKEN_COLOR_FACTOR = 0.8  # used to generate color for disabled button

        elif theme_name.lower() == "dark-blue":
            cls.WINDOW_BG_COLOR = ("#F1F1F1", "#192026")  # macOS standard light and dark window bg colors
            cls.MAIN_COLOR = ("#608BD5", "#395E9C")
            cls.MAIN_HOVER_COLOR = ("#A4BDE6", "#748BB3")
            cls.ENTRY_COLOR = ("#FCFCFC", "#111116")
            cls.TEXT_COLOR = ("gray18", "gray75")
            cls.PLACEHOLDER_TEXT_COLOR = ("gray52", "gray60")
            cls.LABEL_BG_COLOR = ("white", "#444444")
            cls.SLIDER_BG_COLOR = ("#444444", "#444444")
            cls.SLIDER_PROGRESS_COLOR = ("white", "#AAAAAA")
            cls.PROGRESS_BG_COLOR = ("#636363", "#0D1321")
            cls.FRAME_COLOR = ("#DADADA", "#2B2C2E")
            cls.FRAME_2_COLOR = ("#C4C4C4", "#383838")
            cls.CHECKBOX_LINES_COLOR = ("#313131", "white")
            cls.DARKEN_COLOR_FACTOR = 0.8  # used to generate color for disabled button

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
    def darken_hex_color(cls, hex_color: str, darken_factor: float = None) -> str:
        if darken_factor is None:
            darken_factor = cls.DARKEN_COLOR_FACTOR

        try:
            rgb_color = CTkThemeManager.hex2rgb(hex_color)
            dark_rgb_color = (rgb_color[0] * darken_factor,
                              rgb_color[1] * darken_factor,
                              rgb_color[2] * darken_factor)
            return CTkThemeManager.rgb2hex(dark_rgb_color)
        except Exception as err:
            sys.stderr.write("ERROR (CTkColorManager): failed to darken the following color: " + str(hex_color) + " " + str(err))
            return hex_color

    @classmethod
    def set_main_color(cls, main_color, main_color_hover):
        cls.MAIN_COLOR = main_color
        cls.MAIN_HOVER_COLOR = main_color_hover


CTkThemeManager.load_theme("blue")
