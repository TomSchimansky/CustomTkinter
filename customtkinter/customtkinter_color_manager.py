import sys


class CTkColorManager:

    WINDOW_BG = None
    MAIN = None
    MAIN_HOVER = None
    ENTRY = None
    TEXT = None
    LABEL_BG = None
    SLIDER_BG = None
    SLIDER_PROGRESS = None
    PROGRESS_BG = None
    FRAME = None
    FRAME_2 = None
    CHECKBOX_LINES = None
    DARKEN_COLOR_FACTOR = None

    @classmethod
    def initialize_color_theme(cls, theme_name):

        if theme_name.lower() == "blue":
            cls.WINDOW_BG = ("#ECECEC", "#323232")  # macOS standard light and dark window bg colors
            cls.MAIN = ("#1C94CF", "#1C94CF")
            cls.MAIN_HOVER = ("#5FB4DD", "#5FB4DD")
            cls.ENTRY = ("white", "#222222")
            cls.TEXT = ("black", "white")
            cls.LABEL_BG = ("white", "#626061")
            cls.SLIDER_BG = ("#6B6B6B", "#222222")
            cls.SLIDER_PROGRESS = ("#A5A6A5", "#555555")
            cls.PROGRESS_BG = ("#6B6B6B", "#222222")
            cls.FRAME = ("#D4D5D6", "#3F3F3F")
            cls.FRAME_2 = ("#BFBEC1", "#505050")
            cls.CHECKBOX_LINES = ("black", "#ededed")
            cls.DARKEN_COLOR_FACTOR = 0.8  # used to generate color for disabled button

        elif theme_name.lower() == "green":
            cls.WINDOW_BG = ("#ECECEC", "#323232")  # macOS standard light and dark window bg colors
            cls.MAIN = ("#29B57E", "#29B57E")
            cls.MAIN_HOVER = ("#6ACBA5", "#6ACBA5")
            cls.ENTRY = ("gray60", "#222223")
            cls.TEXT = ("black", "white")
            cls.LABEL_BG = ("white", "#626061")
            cls.SLIDER_BG = ("#636363", "#0D1321")
            cls.SLIDER_PROGRESS = ("white", "#727578")
            cls.PROGRESS_BG = ("#636363", "#0D1321")
            cls.FRAME = ("#D4D5D6", "#3F3F3F")
            cls.FRAME_2 = ("#BFBEC1", "#505050")
            cls.CHECKBOX_LINES = ("#414141", "#EDEDED")
            cls.DARKEN_COLOR_FACTOR = 0.8  # used to generate color for disabled button

        elif theme_name.lower() == "dark-blue":
            cls.WINDOW_BG = ("#F1F1F1", "#192026")  # macOS standard light and dark window bg colors
            cls.MAIN = ("#608BD5", "#395E9C")
            cls.MAIN_HOVER = ("#A4BDE6", "#748BB3")
            cls.ENTRY = ("#FCFCFC", "#111116")
            cls.TEXT = ("black", "white")
            cls.LABEL_BG = ("white", "#444444")
            cls.SLIDER_BG = ("#444444", "#444444")
            cls.SLIDER_PROGRESS = ("white", "#AAAAAA")
            cls.PROGRESS_BG = ("#636363", "#0D1321")
            cls.FRAME = ("#DADADA", "#2B2C2E")
            cls.FRAME_2 = ("#C4C4C4", "#383838")
            cls.CHECKBOX_LINES = ("#313131", "white")
            cls.DARKEN_COLOR_FACTOR = 0.8  # used to generate color for disabled button

    @staticmethod
    def single_color(color, appearance_mode: int) -> str:
        """ color can be either a single hex color string or a color name or it can be a
            tuple color with (light_color, dark_color). The functions then returns
            always a single color string """

        if type(color) == tuple:
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
            rgb_color = CTkColorManager.hex2rgb(hex_color)
            dark_rgb_color = (rgb_color[0] * darken_factor,
                              rgb_color[1] * darken_factor,
                              rgb_color[2] * darken_factor)
            return CTkColorManager.rgb2hex(dark_rgb_color)
        except Exception as err:
            sys.stderr.write("ERROR (CTkColorManager): failed to darken the following color: " + str(hex_color) + " " + str(err))
            return hex_color

    @classmethod
    def set_main_color(cls, main_color, main_color_hover):
        cls.MAIN = main_color
        cls.MAIN_HOVER = main_color_hover


CTkColorManager.initialize_color_theme("blue")
