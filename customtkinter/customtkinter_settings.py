import sys
import platform


class CTkSettings:

    scaling_factor = 1
    circle_font_is_ready = False
    hand_cursor_enabled = True
    preferred_drawing_method = None

    radius_to_char_fine = None

    @classmethod
    def init_font_character_mapping(cls):
        radius_to_char_warped = {19: 'B', 18: 'B', 17: 'B', 16: 'B', 15: 'B', 14: 'B', 13: 'B', 12: 'B', 11: 'B', 10: 'B',
                                 9: 'C', 8: 'D', 7: 'C', 6: 'E', 5: 'F', 4: 'G', 3: 'H', 2: 'H', 1: 'H', 0: 'A'}

        radius_to_char_fine_windows_10 = {19: 'A', 18: 'A', 17: 'B', 16: 'B', 15: 'B', 14: 'B', 13: 'C', 12: 'C', 11: 'C', 10: 'C',
                                          9: 'D', 8: 'D', 7: 'D', 6: 'F', 5: 'D', 4: 'G', 3: 'G', 2: 'H', 1: 'H', 0: 'A'}

        radius_to_char_fine_windows_11 = {19: 'A', 18: 'A', 17: 'B', 16: 'B', 15: 'B', 14: 'B', 13: 'C', 12: 'C', 11: 'D', 10: 'D',
                                          9: 'E', 8: 'F', 7: 'C', 6: 'I', 5: 'E', 4: 'G', 3: 'P', 2: 'R', 1: 'R', 0: 'A'}

        if sys.platform.startswith("win"):
            if sys.getwindowsversion().build > 20000:  # Windows 11
                cls.radius_to_char_fine = radius_to_char_fine_windows_11
            else:  # < Windows 11
                cls.radius_to_char_fine = radius_to_char_fine_windows_10
        else:  # macOS and Linux
            cls.radius_to_char_fine = radius_to_char_fine_windows_10


    @classmethod
    def init_drawing_method(cls):
        """ possible: 'polygon_shapes', 'font_shapes', 'circle_shapes' """

        if sys.platform == "darwin":
            cls.preferred_drawing_method = "polygon_shapes"
        else:
            cls.preferred_drawing_method = "font_shapes"

    @classmethod
    def print_settings(cls):
        print(f"CTkSettings current values:")
        print(f"scaling_factor = {cls.scaling_factor}")
        print(f"circle_font_is_ready = {cls.circle_font_is_ready}")
        print(f"hand_cursor_enabled = {cls.hand_cursor_enabled}")
        print(f"preferred_drawing_method = {cls.preferred_drawing_method}")
        print(f"radius_to_char_fine = {cls.radius_to_char_fine}")


CTkSettings.init_font_character_mapping()
CTkSettings.init_drawing_method()
