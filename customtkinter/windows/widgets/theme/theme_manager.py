from __future__ import annotations

import json
import os
import sys
from typing import Any


class ThemeManager:
    theme: dict[str, Any] = {}  # contains all the theme data
    _built_in_themes: list[str] = ["blue", "green", "dark-blue", "sweetkind"]
    _currently_loaded_theme: str | None = None

    @classmethod
    def load_theme(cls, theme_name_or_path: str):
        script_directory = os.path.dirname(os.path.abspath(__file__))

        if theme_name_or_path in cls._built_in_themes:
            with open(os.path.join(script_directory, "../../../assets", "themes", f"{theme_name_or_path}.json")) as f:
                cls.theme = json.load(f)
        else:
            with open(theme_name_or_path) as f:
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

    @classmethod
    def save_theme(cls):
        if cls._currently_loaded_theme is not None:
            if cls._currently_loaded_theme not in cls._built_in_themes:
                with open(cls._currently_loaded_theme) as f:
                    json.dump(cls.theme, f, indent=2)
            else:
                raise ValueError(f"cannot modify builtin theme '{cls._currently_loaded_theme}'")
        else:
            raise ValueError("cannot save theme, no theme is loaded")
