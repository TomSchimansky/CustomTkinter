import sys


class CTkSettings:

    scaling_factor = 1
    circle_font_is_ready = False
    hand_cursor_enabled = True
    preferred_drawing_method = None

    @classmethod
    def init_drawing_method(cls):
        """ possible: 'polygon_shapes', 'font_shapes', 'circle_shapes' """

        if sys.platform == "darwin":
            cls.preferred_drawing_method = "polygon_shapes"
        else:
            cls.preferred_drawing_method = "font_shapes"


CTkSettings.init_drawing_method()
