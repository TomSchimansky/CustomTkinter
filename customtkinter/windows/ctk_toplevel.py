import tkinter
from distutils.version import StrictVersion as Version
import sys
import os
import platform
import ctypes
from typing import Union, Tuple, Optional

from .widgets.theme import ThemeManager
from .widgets.scaling import CTkScalingBaseClass
from .widgets.appearance_mode import CTkAppearanceModeBaseClass

from customtkinter.windows.widgets.utility.utility_functions import pop_from_dict_by_set, check_kwargs_empty


class CTkToplevel(tkinter.Toplevel, CTkAppearanceModeBaseClass, CTkScalingBaseClass):
    """
    Toplevel window with dark titlebar on Windows and macOS.
    For detailed information check out the documentation.
    """

    _valid_tk_toplevel_arguments: set = {"bd", "borderwidth", "class", "container", "cursor", "height",
                                         "highlightbackground", "highlightthickness", "menu", "relief",
                                         "screen", "takefocus", "use", "visual", "width"}

    _deactivate_macos_window_header_manipulation: bool = False
    _deactivate_windows_window_header_manipulation: bool = False

    def __init__(self, *args,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 **kwargs):

        self._enable_macos_dark_title_bar()

        # call init methods of super classes
        super().__init__(*args, **pop_from_dict_by_set(kwargs, self._valid_tk_toplevel_arguments))
        CTkAppearanceModeBaseClass.__init__(self)
        CTkScalingBaseClass.__init__(self, scaling_type="window")
        check_kwargs_empty(kwargs, raise_error=True)

        try:
            # Set Windows titlebar icon
            if sys.platform.startswith("win"):
                customtkinter_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                self.after(200, lambda: self.iconbitmap(os.path.join(customtkinter_directory, "assets", "icons", "CustomTkinter_icon_Windows.ico")))
        except Exception:
            pass

        self._current_width = 200  # initial window size, always without scaling
        self._current_height = 200
        self._min_width: int = 0
        self._min_height: int = 0
        self._max_width: int = 1_000_000
        self._max_height: int = 1_000_000
        self._last_resizable_args: Union[Tuple[list, dict], None] = None  # (args, kwargs)

        self._fg_color = ThemeManager.theme["CTkToplevel"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)

        # set bg color of tkinter.Toplevel
        super().configure(bg=self._apply_appearance_mode(self._fg_color))

        # set title of tkinter.Toplevel
        super().title("CTkToplevel")

        # indicator variables
        self._iconbitmap_method_called = True
        self._state_before_windows_set_titlebar_color = None
        self._windows_set_titlebar_color_called = False  # indicates if windows_set_titlebar_color was called, stays True until revert_withdraw_after_windows_set_titlebar_color is called
        self._withdraw_called_after_windows_set_titlebar_color = False  # indicates if withdraw() was called after windows_set_titlebar_color
        self._iconify_called_after_windows_set_titlebar_color = False  # indicates if iconify() was called after windows_set_titlebar_color
        self._block_update_dimensions_event = False

        # set CustomTkinter titlebar icon (Windows only)
        if sys.platform.startswith("win"):
            self.after(200, self._windows_set_titlebar_icon)

        # set titlebar color (Windows only)
        if sys.platform.startswith("win"):
            self._windows_set_titlebar_color(self._get_appearance_mode())

        self.bind('<Configure>', self._update_dimensions_event)
        self.bind('<FocusIn>', self._focus_in_event)

    def destroy(self):
        self._disable_macos_dark_title_bar()

        # call destroy methods of super classes
        tkinter.Toplevel.destroy(self)
        CTkAppearanceModeBaseClass.destroy(self)
        CTkScalingBaseClass.destroy(self)

    def _focus_in_event(self, event):
        # sometimes window looses jumps back on macOS if window is selected from Mission Control, so has to be lifted again
        if sys.platform == "darwin":
            self.lift()

    def _update_dimensions_event(self, event=None):
        if not self._block_update_dimensions_event:
            detected_width = self.winfo_width()  # detect current window size
            detected_height = self.winfo_height()

            if self._current_width != self._reverse_window_scaling(detected_width) or self._current_height != self._reverse_window_scaling(detected_height):
                self._current_width = self._reverse_window_scaling(detected_width)  # adjust current size according to new size given by event
                self._current_height = self._reverse_window_scaling(detected_height)  # _current_width and _current_height are independent of the scale

    def _set_scaling(self, new_widget_scaling, new_window_scaling):
        super()._set_scaling(new_widget_scaling, new_window_scaling)

        # Force new dimensions on window by using min, max, and geometry. Without min, max it won't work.
        super().minsize(self._apply_window_scaling(self._current_width), self._apply_window_scaling(self._current_height))
        super().maxsize(self._apply_window_scaling(self._current_width), self._apply_window_scaling(self._current_height))

        super().geometry(f"{self._apply_window_scaling(self._current_width)}x{self._apply_window_scaling(self._current_height)}")

        # set new scaled min and max with delay (delay prevents weird bug where window dimensions snap to unscaled dimensions when mouse releases window)
        self.after(1000, self._set_scaled_min_max)  # Why 1000ms delay? Experience! (Everything tested on Windows 11)

    def block_update_dimensions_event(self):
        self._block_update_dimensions_event = False

    def unblock_update_dimensions_event(self):
        self._block_update_dimensions_event = False

    def _set_scaled_min_max(self):
        if self._min_width is not None or self._min_height is not None:
            super().minsize(self._apply_window_scaling(self._min_width), self._apply_window_scaling(self._min_height))
        if self._max_width is not None or self._max_height is not None:
            super().maxsize(self._apply_window_scaling(self._max_width), self._apply_window_scaling(self._max_height))

    def geometry(self, geometry_string: str = None):
        if geometry_string is not None:
            super().geometry(self._apply_geometry_scaling(geometry_string))

            # update width and height attributes
            width, height, x, y = self._parse_geometry_string(geometry_string)
            if width is not None and height is not None:
                self._current_width = max(self._min_width, min(width, self._max_width))  # bound value between min and max
                self._current_height = max(self._min_height, min(height, self._max_height))
        else:
            return self._reverse_geometry_scaling(super().geometry())

    def withdraw(self):
        if self._windows_set_titlebar_color_called:
            self._withdraw_called_after_windows_set_titlebar_color = True
        super().withdraw()

    def iconify(self):
        if self._windows_set_titlebar_color_called:
            self._iconify_called_after_windows_set_titlebar_color = True
        super().iconify()

    def resizable(self, width: bool = None, height: bool = None):
        current_resizable_values = super().resizable(width, height)
        self._last_resizable_args = ([], {"width": width, "height": height})

        if sys.platform.startswith("win"):
            self.after(10, lambda: self._windows_set_titlebar_color(self._get_appearance_mode()))

        return current_resizable_values

    def minsize(self, width=None, height=None):
        self._min_width = width
        self._min_height = height
        if self._current_width < width:
            self._current_width = width
        if self._current_height < height:
            self._current_height = height
        super().minsize(self._apply_window_scaling(self._min_width), self._apply_window_scaling(self._min_height))

    def maxsize(self, width=None, height=None):
        self._max_width = width
        self._max_height = height
        if self._current_width > width:
            self._current_width = width
        if self._current_height > height:
            self._current_height = height
        super().maxsize(self._apply_window_scaling(self._max_width), self._apply_window_scaling(self._max_height))

    def configure(self, **kwargs):
        if "fg_color" in kwargs:
            self._fg_color = self._check_color_type(kwargs.pop("fg_color"))
            super().configure(bg=self._apply_appearance_mode(self._fg_color))

            for child in self.winfo_children():
                try:
                    child.configure(bg_color=self._fg_color)
                except Exception:
                    pass

        super().configure(**pop_from_dict_by_set(kwargs, self._valid_tk_toplevel_arguments))
        check_kwargs_empty(kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "fg_color":
            return self._fg_color
        else:
            return super().cget(attribute_name)

    def wm_iconbitmap(self, bitmap=None, default=None):
        self._iconbitmap_method_called = True
        super().wm_iconbitmap(bitmap, default)

    def _windows_set_titlebar_icon(self):
        try:
            # if not the user already called iconbitmap method, set icon
            if not self._iconbitmap_method_called:
                customtkinter_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                self.iconbitmap(os.path.join(customtkinter_directory, "assets", "icons", "CustomTkinter_icon_Windows.ico"))
        except Exception:
            pass

    @classmethod
    def _enable_macos_dark_title_bar(cls):
        if sys.platform == "darwin" and not cls._deactivate_macos_window_header_manipulation:  # macOS
            if Version(platform.python_version()) < Version("3.10"):
                if Version(tkinter.Tcl().call("info", "patchlevel")) >= Version("8.6.9"):  # Tcl/Tk >= 8.6.9
                    os.system("defaults write -g NSRequiresAquaSystemAppearance -bool No")

    @classmethod
    def _disable_macos_dark_title_bar(cls):
        if sys.platform == "darwin" and not cls._deactivate_macos_window_header_manipulation:  # macOS
            if Version(platform.python_version()) < Version("3.10"):
                if Version(tkinter.Tcl().call("info", "patchlevel")) >= Version("8.6.9"):  # Tcl/Tk >= 8.6.9
                    os.system("defaults delete -g NSRequiresAquaSystemAppearance")
                    # This command reverts the dark-mode setting for all programs.

    def _windows_set_titlebar_color(self, color_mode: str):
        """
        Set the titlebar color of the window to light or dark theme on Microsoft Windows.

        Credits for this function:
        https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter/70724666#70724666

        MORE INFO:
        https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
        """

        if sys.platform.startswith("win") and not self._deactivate_windows_window_header_manipulation:

            self._state_before_windows_set_titlebar_color = self.state()
            super().withdraw()  # hide window so that it can be redrawn after the titlebar change so that the color change is visible
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

            self._windows_set_titlebar_color_called = True
            self.after(5, self._revert_withdraw_after_windows_set_titlebar_color)

    def _revert_withdraw_after_windows_set_titlebar_color(self):
        """ if in a short time (5ms) after """
        if self._windows_set_titlebar_color_called:

            if self._withdraw_called_after_windows_set_titlebar_color:
                pass  # leave it withdrawed
            elif self._iconify_called_after_windows_set_titlebar_color:
                super().iconify()
            else:
                if self._state_before_windows_set_titlebar_color == "normal":
                    self.deiconify()
                elif self._state_before_windows_set_titlebar_color == "iconic":
                    self.iconify()
                elif self._state_before_windows_set_titlebar_color == "zoomed":
                    self.state("zoomed")
                else:
                    self.state(self._state_before_windows_set_titlebar_color)  # other states

            self._windows_set_titlebar_color_called = False
            self._withdraw_called_after_windows_set_titlebar_color = False
            self._iconify_called_after_windows_set_titlebar_color = False

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)

        if sys.platform.startswith("win"):
            self._windows_set_titlebar_color(mode_string)

        super().configure(bg=self._apply_appearance_mode(self._fg_color))
