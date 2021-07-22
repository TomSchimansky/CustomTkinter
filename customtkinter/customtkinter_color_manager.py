import sys


class CTkColorManager:
    MAIN = ("#1C94CF", "#1C94CF")
    MAIN_HOVER = ("#5FB4DD", "#5FB4DD")
    ENTRY = ("white", "#222222")
    TEXT = ("black", "white")
    SLIDER_BG = ("#6B6B6B", "#222222")
    PROGRESS_BG = ("#6B6B6B", "#222222")
    FRAME = ("#D4D5D6", "#3F3F3F")
    FRAME_2 = ("#BFBEC1", "#505050")

    DARKEN_COLOR_FACTOR = 0.8  # used for generate color for disabled button

    @staticmethod
    def rgb2hex(rgb_color):
        return "#{:02x}{:02x}{:02x}".format(round(rgb_color[0]), round(rgb_color[1]), round(rgb_color[2]))

    @staticmethod
    def hex2rgb(hex_color: str):
        return tuple(int(hex_color.strip("#")[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def darken_hex_color(hex_color):
        try:
            rgb_color = CTkColorManager.hex2rgb(hex_color)
            dark_rgb_color = (rgb_color[0] * CTkColorManager.DARKEN_COLOR_FACTOR,
                              rgb_color[1] * CTkColorManager.DARKEN_COLOR_FACTOR,
                              rgb_color[2] * CTkColorManager.DARKEN_COLOR_FACTOR)
            return CTkColorManager.rgb2hex(dark_rgb_color)
        except Exception as err:
            return hex_color

    @classmethod
    def set_theme_color(cls, hex_color, hex_color_hover):
        cls.MAIN = (hex_color, hex_color)
        cls.MAIN_HOVER = (hex_color_hover, hex_color_hover)

    @classmethod
    def set_theme(cls, main_color):
        if main_color.lower() == "green":
            cls.set_theme_color("#2EDEA4", "#82FCD4")

        elif main_color.lower() == "blue":
            cls.set_theme_color("#1C94CF", "#5FB4DD")

        else:
            sys.stderr.write("WARNING (CTkColorManager): No such color theme available: {}\n".format(main_color))
