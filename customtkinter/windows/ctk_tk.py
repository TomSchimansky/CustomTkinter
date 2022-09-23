import tkinter
from distutils.version import StrictVersion as Version
import sys
import os
import platform
import ctypes
import re
from typing import Union, Tuple

from ..appearance_mode_tracker import AppearanceModeTracker
from ..theme_manager import ThemeManager
from ..scaling_tracker import ScalingTracker
from ..settings import Settings


class CTk(tkinter.Tk):
    def __init__(self, *args,
                 fg_color="default_theme",
                 **kwargs):

        ScalingTracker.activate_high_dpi_awareness()  # make process DPI aware
        self.enable_macos_dark_title_bar()

        super().__init__(*args, **kwargs)

        # add set_appearance_mode method to callback list of AppearanceModeTracker for appearance mode changes
        AppearanceModeTracker.add(self.set_appearance_mode, self)
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        # add set_scaling method to callback list of ScalingTracker for automatic scaling changes
        ScalingTracker.add_widget(self.set_scaling, self)
        self.window_scaling = ScalingTracker.get_window_scaling(self)

        self.current_width = 600  # initial window size, always without scaling
        self.current_height = 500
        self.min_width: int = 0
        self.min_height: int = 0
        self.max_width: int = 1_000_000
        self.max_height: int = 1_000_000
        self.last_resizable_args: Union[Tuple[list, dict], None] = None  # (args, kwargs)

        self.fg_color = ThemeManager.theme["color"]["window_bg_color"] if fg_color == "default_theme" else fg_color

        if "bg" in kwargs:
            self.fg_color = kwargs["bg"]
            del kwargs["bg"]
        elif "background" in kwargs:
            self.fg_color = kwargs["background"]
            del kwargs["background"]

        super().configure(bg=ThemeManager.single_color(self.fg_color, self.appearance_mode))
        super().title("CTk")
        self.geometry(f"{self.current_width}x{self.current_height}")

        self.state_before_windows_set_titlebar_color = None
        self.window_exists = False  # indicates if the window is already shown through update() or mainloop() after init
        self.withdraw_called_before_window_exists = False  # indicates if withdraw() was called before window is first shown through update() or mainloop()
        self.iconify_called_before_window_exists = False  # indicates if iconify() was called before window is first shown through update() or mainloop()

        if sys.platform.startswith("win"):
            if self.appearance_mode == 1:
                self.windows_set_titlebar_color("dark")
            else:
                self.windows_set_titlebar_color("light")

        self.bind('<Configure>', self.update_dimensions_event)

        self.block_update_dimensions_event = False

    def update_dimensions_event(self, event=None):
        if not self.block_update_dimensions_event:
            detected_width = self.winfo_width()  # detect current window size
            detected_height = self.winfo_height()

            if self.current_width != round(detected_width / self.window_scaling) or self.current_height != round(detected_height / self.window_scaling):
                self.current_width = round(detected_width / self.window_scaling)  # adjust current size according to new size given by event
                self.current_height = round(detected_height / self.window_scaling)  # _current_width and _current_height are independent of the scale

    def set_scaling(self, new_widget_scaling, new_spacing_scaling, new_window_scaling):
        self.window_scaling = new_window_scaling

        # block update_dimensions_event to prevent current_width and current_height to get updated
        self.block_update_dimensions_event = True

        # force new dimensions on window by using min, max, and geometry
        super().minsize(self.apply_window_scaling(self.current_width), self.apply_window_scaling(self.current_height))
        super().maxsize(self.apply_window_scaling(self.current_width), self.apply_window_scaling(self.current_height))
        super().geometry(f"{self.apply_window_scaling(self.current_width)}x"+f"{self.apply_window_scaling(self.current_height)}")

        # set new scaled min and max with 400ms delay (otherwise it won't work for some reason)
        self.after(400, self.set_scaled_min_max)

        # release the blocking of update_dimensions_event after a small amount of time (slight delay is necessary)
        def set_block_update_dimensions_event_false():
            self.block_update_dimensions_event = False
        self.after(100, lambda: set_block_update_dimensions_event_false())

    def set_scaled_min_max(self):
        if self.min_width is not None or self.min_height is not None:
            super().minsize(self.apply_window_scaling(self.min_width), self.apply_window_scaling(self.min_height))
        if self.max_width is not None or self.max_height is not None:
            super().maxsize(self.apply_window_scaling(self.max_width), self.apply_window_scaling(self.max_height))

    def destroy(self):
        AppearanceModeTracker.remove(self.set_appearance_mode)
        ScalingTracker.remove_window(self.set_scaling, self)
        self.disable_macos_dark_title_bar()
        super().destroy()

    def withdraw(self):
        if self.window_exists is False:
            self.withdraw_called_before_window_exists = True
        super().withdraw()

    def iconify(self):
        if self.window_exists is False:
            self.iconify_called_before_window_exists = True
        super().iconify()

    def update(self):
        if self.window_exists is False:
            self.window_exists = True

            if sys.platform.startswith("win"):
                if not self.withdraw_called_before_window_exists and not self.iconify_called_before_window_exists:
                    # print("window dont exists -> deiconify in update")
                    self.deiconify()

        super().update()

    def mainloop(self, *args, **kwargs):
        if not self.window_exists:
            self.window_exists = True

            if sys.platform.startswith("win"):
                if not self.withdraw_called_before_window_exists and not self.iconify_called_before_window_exists:
                    # print("window dont exists -> deiconify in mainloop")
                    self.deiconify()

        super().mainloop(*args, **kwargs)

    def resizable(self, *args, **kwargs):
        super().resizable(*args, **kwargs)
        self.last_resizable_args = (args, kwargs)

        if sys.platform.startswith("win"):
            if self.appearance_mode == 1:
                self.windows_set_titlebar_color("dark")
            else:
                self.windows_set_titlebar_color("light")

    def minsize(self, width=None, height=None):
        self.min_width = width
        self.min_height = height
        if self.current_width < width: self.current_width = width
        if self.current_height < height: self.current_height = height
        super().minsize(self.apply_window_scaling(self.min_width), self.apply_window_scaling(self.min_height))

    def maxsize(self, width=None, height=None):
        self.max_width = width
        self.max_height = height
        if self.current_width > width: self.current_width = width
        if self.current_height > height: self.current_height = height
        super().maxsize(self.apply_window_scaling(self.max_width), self.apply_window_scaling(self.max_height))

    def geometry(self, geometry_string: str = None):
        if geometry_string is not None:
            super().geometry(self.apply_geometry_scaling(geometry_string))

            # update width and height attributes
            width, height, x, y = self.parse_geometry_string(geometry_string)
            if width is not None and height is not None:
                self.current_width = max(self.min_width, min(width, self.max_width))  # bound value between min and max
                self.current_height = max(self.min_height, min(height, self.max_height))
        else:
            return self.reverse_geometry_scaling(super().geometry())

    @staticmethod
    def parse_geometry_string(geometry_string: str) -> tuple:
        #                 index:   1                   2           3          4             5       6
        # regex group structure: ('<width>x<height>', '<width>', '<height>', '+-<x>+-<y>', '-<x>', '-<y>')
        result = re.search(r"((\d+)x(\d+)){0,1}(\+{0,1}([+-]{0,1}\d+)\+{0,1}([+-]{0,1}\d+)){0,1}", geometry_string)

        width = int(result.group(2)) if result.group(2) is not None else None
        height = int(result.group(3)) if result.group(3) is not None else None
        x = int(result.group(5)) if result.group(5) is not None else None
        y = int(result.group(6)) if result.group(6) is not None else None

        return width, height, x, y

    def apply_geometry_scaling(self, geometry_string: str) -> str:
        width, height, x, y = self.parse_geometry_string(geometry_string)

        if x is None and y is None:  # no <x> and <y> in geometry_string
            return f"{round(width * self.window_scaling)}x{round(height * self.window_scaling)}"

        elif width is None and height is None:  # no <width> and <height> in geometry_string
            return f"+{x}+{y}"

        else:
            return f"{round(width * self.window_scaling)}x{round(height * self.window_scaling)}+{x}+{y}"

    def reverse_geometry_scaling(self, scaled_geometry_string: str) -> str:
        width, height, x, y = self.parse_geometry_string(scaled_geometry_string)

        if x is None and y is None:  # no <x> and <y> in geometry_string
            return f"{round(width / self.window_scaling)}x{round(height / self.window_scaling)}"

        elif width is None and height is None:  # no <width> and <height> in geometry_string
            return f"+{x}+{y}"

        else:
            return f"{round(width / self.window_scaling)}x{round(height / self.window_scaling)}+{x}+{y}"

    def apply_window_scaling(self, value):
        if isinstance(value, (int, float)):
            return int(value * self.window_scaling)
        else:
            return value

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        bg_changed = False

        if "bg" in kwargs:
            self.fg_color = kwargs["bg"]
            bg_changed = True
            kwargs["bg"] = ThemeManager.single_color(self.fg_color, self.appearance_mode)
        elif "background" in kwargs:
            self.fg_color = kwargs["background"]
            bg_changed = True
            kwargs["background"] = ThemeManager.single_color(self.fg_color, self.appearance_mode)
        elif "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            kwargs["bg"] = ThemeManager.single_color(self.fg_color, self.appearance_mode)
            del kwargs["fg_color"]
            bg_changed = True

        elif len(args) > 0 and type(args[0]) == dict:
            if "bg" in args[0]:
                self.fg_color=args[0]["bg"]
                bg_changed = True
                args[0]["bg"] = ThemeManager.single_color(self.fg_color, self.appearance_mode)
            elif "background" in args[0]:
                self.fg_color=args[0]["background"]
                bg_changed = True
                args[0]["background"] = ThemeManager.single_color(self.fg_color, self.appearance_mode)

        if bg_changed:
            from ..widgets.widget_base_class import CTkBaseClass

            for child in self.winfo_children():
                if isinstance(child, CTkBaseClass):
                    child.configure(bg_color=self.fg_color)

        super().configure(*args, **kwargs)

    @staticmethod
    def enable_macos_dark_title_bar():
        if sys.platform == "darwin" and not Settings.deactivate_macos_window_header_manipulation:  # macOS
            if Version(platform.python_version()) < Version("3.10"):
                if Version(tkinter.Tcl().call("info", "patchlevel")) >= Version("8.6.9"):  # Tcl/Tk >= 8.6.9
                    os.system("defaults write -g NSRequiresAquaSystemAppearance -bool No")
                    # This command allows dark-mode for all programs

    @staticmethod
    def disable_macos_dark_title_bar():
        if sys.platform == "darwin" and not Settings.deactivate_macos_window_header_manipulation:  # macOS
            if Version(platform.python_version()) < Version("3.10"):
                if Version(tkinter.Tcl().call("info", "patchlevel")) >= Version("8.6.9"):  # Tcl/Tk >= 8.6.9
                    os.system("defaults delete -g NSRequiresAquaSystemAppearance")
                    # This command reverts the dark-mode setting for all programs.

    def windows_set_titlebar_color(self, color_mode: str):
        """
        Set the titlebar color of the window to light or dark theme on Microsoft Windows.

        Credits for this function:
        https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter/70724666#70724666

        MORE INFO:
        https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
        """

        if sys.platform.startswith("win") and not Settings.deactivate_windows_window_header_manipulation:

            if self.window_exists:
                self.state_before_windows_set_titlebar_color = self.state()
                # print("window_exists -> state_before_windows_set_titlebar_color: ", self.state_before_windows_set_titlebar_color)

                if self.state_before_windows_set_titlebar_color != "iconic" or self.state_before_windows_set_titlebar_color != "withdrawn":
                    super().withdraw()  # hide window so that it can be redrawn after the titlebar change so that the color change is visible
            else:
                # print("window dont exists -> withdraw and update")
                super().withdraw()
                super().update()

            if color_mode.lower() == "dark":
                value = 1
            elif color_mode.lower() == "light":
                value = 0
            else:
                return

            try:
                hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19

                # try with DWMWA_USE_IMMERSIVE_DARK_MODE
                if ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                                                              ctypes.byref(ctypes.c_int(value)),
                                                              ctypes.sizeof(ctypes.c_int(value))) != 0:

                    # try with DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20h1
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1,
                                                               ctypes.byref(ctypes.c_int(value)),
                                                               ctypes.sizeof(ctypes.c_int(value)))

            except Exception as err:
                print(err)

            if self.window_exists:
                # print("window_exists -> return to original state: ", self.state_before_windows_set_titlebar_color)
                if self.state_before_windows_set_titlebar_color == "normal":
                    self.deiconify()
                elif self.state_before_windows_set_titlebar_color == "iconic":
                    self.iconify()
                elif self.state_before_windows_set_titlebar_color == "zoomed":
                    self.state("zoomed")
                else:
                    self.state(self.state_before_windows_set_titlebar_color)  # other states
            else:
                pass  # wait for update or mainloop to be called

    def set_appearance_mode(self, mode_string):
        if mode_string.lower() == "dark":
            self.appearance_mode = 1
        elif mode_string.lower() == "light":
            self.appearance_mode = 0

        if sys.platform.startswith("win"):
            if self.appearance_mode == 1:
                self.windows_set_titlebar_color("dark")
            else:
                self.windows_set_titlebar_color("light")

        super().configure(bg=ThemeManager.single_color(self.fg_color, self.appearance_mode))
