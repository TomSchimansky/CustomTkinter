from __future__ import annotations

import sys
import tkinter
from distutils.version import StrictVersion as Version
from typing import Callable, TYPE_CHECKING

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if TYPE_CHECKING:
    from customtkinter.windows.ctk_tk import CTk

try:
    import darkdetect   # type: ignore

    if Version(darkdetect.__version__) < Version("0.3.1"):
        sys.stderr.write("WARNING: You have to upgrade the darkdetect library: pip3 install --upgrade darkdetect\n")
        if sys.platform != "darwin":
            exit()
except ImportError as err:
    raise err
except Exception:
    sys.stderr.write("customtkinter.appearance_mode_tracker warning: failed to import darkdetect")


class AppearanceModeTracker:

    callback_list: list[Callable[[str], None]] = []
    app_list: list[CTk] = []
    update_loop_running = False
    update_loop_interval = 30  # milliseconds

    appearance_mode_set_by: Literal["system", "user"] = "system"
    appearance_mode: Literal[0, 1] = 0  # 0 = Light, 1 = Dark

    @classmethod
    def init_appearance_mode(cls):
        if cls.appearance_mode_set_by == "system":
            new_appearance_mode = cls.detect_appearance_mode()

            if new_appearance_mode != cls.appearance_mode:
                cls.appearance_mode = new_appearance_mode
                cls.update_callbacks()

    @classmethod
    def add(cls, callback: Callable[[str], None], widget: CTk | None = None):
        cls.callback_list.append(callback)

        if widget is not None:
            app = cls.get_tk_root_of_widget(widget)
            if app not in cls.app_list:
                cls.app_list.append(app)

                if not cls.update_loop_running:
                    app.after(cls.update_loop_interval, cls.update)
                    cls.update_loop_running = True

    @classmethod
    def remove(cls, callback: Callable[[str], None]):
        try:
            cls.callback_list.remove(callback)
        except ValueError:
            return

    @staticmethod
    def detect_appearance_mode() -> Literal[0, 1]:
        try:
            if darkdetect.theme() == "Dark":    # type: ignore
                return 1  # Dark
            else:
                return 0  # Light
        except NameError:
            return 0  # Light

    @classmethod
    def get_tk_root_of_widget(cls, widget: CTk) -> CTk:
        current_widget = widget

        while isinstance(current_widget, tkinter.Tk) is False:
            current_widget = current_widget.master

        return current_widget

    @classmethod
    def update_callbacks(cls):
        if cls.appearance_mode == 0:
            for callback in cls.callback_list:
                try:
                    callback("Light")
                except Exception:
                    continue

        elif cls.appearance_mode == 1:
            for callback in cls.callback_list:
                try:
                    callback("Dark")
                except Exception:
                    continue

    @classmethod
    def update(cls):
        if cls.appearance_mode_set_by == "system":
            new_appearance_mode = cls.detect_appearance_mode()

            if new_appearance_mode != cls.appearance_mode:
                cls.appearance_mode = new_appearance_mode
                cls.update_callbacks()

        # find an existing tkinter.Tk object for the next call of .after()
        for app in cls.app_list:
            try:
                app.after(cls.update_loop_interval, cls.update)
                return
            except Exception:
                continue

        cls.update_loop_running = False

    @classmethod
    def get_mode(cls) -> int:
        return cls.appearance_mode

    @classmethod
    def set_appearance_mode(cls, mode_string: str):
        if mode_string.lower() == "dark":
            cls.appearance_mode_set_by = "user"
            new_appearance_mode = 1

            if new_appearance_mode != cls.appearance_mode:
                cls.appearance_mode = new_appearance_mode
                cls.update_callbacks()

        elif mode_string.lower() == "light":
            cls.appearance_mode_set_by = "user"
            new_appearance_mode = 0

            if new_appearance_mode != cls.appearance_mode:
                cls.appearance_mode = new_appearance_mode
                cls.update_callbacks()

        elif mode_string.lower() == "system":
            cls.appearance_mode_set_by = "system"
