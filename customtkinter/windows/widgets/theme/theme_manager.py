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
            with open(os.path.join(script_directory, "../../../assets", "themes", f"{theme_name_or_path}.json"), "r") as f:
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
