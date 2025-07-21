import sys
import os
import shutil
from typing import Union
import subprocess


class FontManager:
    linux_font_paths = [
        os.path.expanduser("~/.fonts/"),  # Default path
        os.path.expanduser("~/.local/share/fonts/"),  # Fallback path
    ]

    @classmethod
    def init_font_manager(cls):
        """
        Initialize font manager by ensuring the required font directories exist.
        """
        if sys.platform.startswith("linux"):
            try:
                for path in cls.linux_font_paths:
                    if not os.path.isdir(path):
                        os.makedirs(path, exist_ok=True)
                return True
            except Exception as err:
                sys.stderr.write(f"FontManager error (init): {err}\n")
                return False
        else:
            return True

    @classmethod
    def windows_load_font(cls, font_path: Union[str, bytes], private: bool = True, enumerable: bool = False) -> bool:
        """ Function taken from: https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter/30631309#30631309 """

        from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

        FR_PRIVATE = 0x10
        FR_NOT_ENUM = 0x20

        if isinstance(font_path, bytes):
            path_buffer = create_string_buffer(font_path)
            add_font_resource_ex = windll.gdi32.AddFontResourceExA
        elif isinstance(font_path, str):
            path_buffer = create_unicode_buffer(font_path)
            add_font_resource_ex = windll.gdi32.AddFontResourceExW
        else:
            raise TypeError('font_path must be of type bytes or str')

        flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
        num_fonts_added = add_font_resource_ex(byref(path_buffer), flags, 0)
        return bool(min(num_fonts_added, 1))

    @classmethod
    def load_font(cls, font_path: str) -> bool:
        """
        Load a font into the system for different platforms.
        """
        # Check if the font file exists
        if not os.path.isfile(font_path):
            sys.stderr.write(f"FontManager error: Font file '{font_path}' does not exist.\n")
            return False

        # Windows
        if sys.platform.startswith("win"):
            return cls.windows_load_font(font_path, private=True, enumerable=False)

        # Linux
        elif sys.platform.startswith("linux"):
            for path in cls.linux_font_paths:
                try:
                    dest_path = os.path.join(path, os.path.basename(font_path))
                    if not os.path.isfile(dest_path):  # Avoid redundant copying
                        shutil.copy(font_path, dest_path)
                        cls.refresh_font_cache(path)  # Refresh the font cache
                    return True
                except Exception as err:
                    sys.stderr.write(f"FontManager error (Linux): {err}\n")
            return False

        # macOS and others
        else:
            sys.stderr.write("FontManager warning: Font loading is not supported on this platform.\n")
            return False

    @staticmethod
    def refresh_font_cache(directory: str):
        """
        Refresh the font cache on Linux using fc-cache.
        """
        try:
            subprocess.run(["fc-cache", "-fv", directory], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as err:
            sys.stderr.write(f"FontManager error (fc-cache): {err}\n")
