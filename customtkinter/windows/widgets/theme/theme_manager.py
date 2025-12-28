import sys
import os
import pathlib
import json
from typing import List, Union


class ThemeManager:

    theme: dict = {}  # contains all the theme data
    _built_in_themes: List[str] = ["blue", "green", "dark-blue", "sweetkind"]
    _currently_loaded_theme: Union[str, None] = None

    @classmethod
    def load_theme(cls, theme_name_or_path: str):
        script_directory = os.path.dirname(os.path.abspath(__file__))

        if theme_name_or_path in cls._built_in_themes:
            customtkinter_path = pathlib.Path(script_directory).parent.parent.parent
            with open(os.path.join(customtkinter_path, "assets", "themes", f"{theme_name_or_path}.json"), "r") as f:
                cls.theme = json.load(f)
        else:
            with open(theme_name_or_path, "r") as f:
                cls.theme = json.load(f)

        # store theme path for saving
        cls._currently_loaded_theme = theme_name_or_path

        # filter theme values for platform
        for key in cls.theme.keys():
            # check if values for key differ on platforms
            if "macOS" in cls.theme[key].keys():
                if sys.platform == "darwin":
                    cls.theme[key] = cls.theme[key]["macOS"]
                elif sys.platform.startswith("win"):
                    cls.theme[key] = cls.theme[key]["Windows"]
                else:
                    cls.theme[key] = cls.theme[key]["Linux"]

        # fix name inconsistencies
        if "CTkCheckbox" in cls.theme.keys():
            cls.theme["CTkCheckBox"] = cls.theme.pop("CTkCheckbox")
        if "CTkRadiobutton" in cls.theme.keys():
            cls.theme["CTkRadioButton"] = cls.theme.pop("CTkRadiobutton")

    @classmethod
    def save_theme(cls):
        if cls._currently_loaded_theme is not None:
            if cls._currently_loaded_theme not in cls._built_in_themes:
                with open(cls._currently_loaded_theme, "r") as f:
                    json.dump(cls.theme, f, indent=2)
            else:
                raise ValueError(f"cannot modify builtin theme '{cls._currently_loaded_theme}'")
        else:
            raise ValueError(f"cannot save theme, no theme is loaded")
