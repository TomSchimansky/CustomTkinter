import os
import re
import subprocess
import tkinter
import sys
from typing import Callable, Union


class ScalingTracker:
    deactivate_automatic_dpi_awareness = False

    window_widgets_dict = {}  # contains window objects as keys with list of widget callbacks as elements
    window_dpi_scaling_dict = {}  # contains window objects as keys and corresponding scaling factors

    widget_scaling = 1  # user values which multiply to detected window scaling factor
    window_scaling = 1

    update_loop_running = False
    update_loop_interval = 100  # ms
    loop_pause_after_new_scaling = 1500  # ms

    _linux_xft_dpi_cache = {}  # X display name -> Xft.dpi value or None

    @classmethod
    def get_widget_scaling(cls, widget) -> float:
        window_root = cls.get_window_root_of_widget(widget)
        return cls.window_dpi_scaling_dict[window_root] * cls.widget_scaling

    @classmethod
    def get_window_scaling(cls, window) -> float:
        window_root = cls.get_window_root_of_widget(window)
        return cls.window_dpi_scaling_dict[window_root] * cls.window_scaling

    @classmethod
    def set_widget_scaling(cls, widget_scaling_factor: float):
        cls.widget_scaling = max(widget_scaling_factor, 0.4)
        cls.update_scaling_callbacks_all()

    @classmethod
    def set_window_scaling(cls, window_scaling_factor: float):
        cls.window_scaling = max(window_scaling_factor, 0.4)
        cls.update_scaling_callbacks_all()

    @classmethod
    def get_window_root_of_widget(cls, widget):
        current_widget = widget

        while isinstance(current_widget, tkinter.Tk) is False and\
                isinstance(current_widget, tkinter.Toplevel) is False:
            current_widget = current_widget.master

        return current_widget

    @classmethod
    def update_scaling_callbacks_all(cls):
        for window, callback_list in cls.window_widgets_dict.items():
            for set_scaling_callback in callback_list:
                if not cls.deactivate_automatic_dpi_awareness:
                    set_scaling_callback(cls.window_dpi_scaling_dict[window] * cls.widget_scaling,
                                         cls.window_dpi_scaling_dict[window] * cls.window_scaling)
                else:
                    set_scaling_callback(cls.widget_scaling,
                                         cls.window_scaling)

    @classmethod
    def update_scaling_callbacks_for_window(cls, window):
        for set_scaling_callback in cls.window_widgets_dict[window]:
            if not cls.deactivate_automatic_dpi_awareness:
                set_scaling_callback(cls.window_dpi_scaling_dict[window] * cls.widget_scaling,
                                     cls.window_dpi_scaling_dict[window] * cls.window_scaling)
            else:
                set_scaling_callback(cls.widget_scaling,
                                     cls.window_scaling)

    @classmethod
    def add_widget(cls, widget_callback: Callable, widget):
        window_root = cls.get_window_root_of_widget(widget)

        if window_root not in cls.window_widgets_dict:
            cls.window_widgets_dict[window_root] = [widget_callback]
        else:
            cls.window_widgets_dict[window_root].append(widget_callback)

        if window_root not in cls.window_dpi_scaling_dict:
            cls.window_dpi_scaling_dict[window_root] = cls.get_window_dpi_scaling(window_root)

        if not cls.update_loop_running:
            window_root.after(100, cls.check_dpi_scaling)
            cls.update_loop_running = True

    @classmethod
    def remove_widget(cls, widget_callback, widget):
        window_root = cls.get_window_root_of_widget(widget)
        try:
            cls.window_widgets_dict[window_root].remove(widget_callback)
        except:
            pass

    @classmethod
    def remove_window(cls, window_callback, window):
        try:
            del cls.window_widgets_dict[window]
        except:
            pass

    @classmethod
    def add_window(cls, window_callback, window):
        if window not in cls.window_widgets_dict:
            cls.window_widgets_dict[window] = [window_callback]
        else:
            cls.window_widgets_dict[window].append(window_callback)

        if window not in cls.window_dpi_scaling_dict:
            cls.window_dpi_scaling_dict[window] = cls.get_window_dpi_scaling(window)

    @classmethod
    def activate_high_dpi_awareness(cls):
        """ make process DPI aware, customtkinter elements will get scaled automatically,
            only gets activated when CTk object is created """

        if not cls.deactivate_automatic_dpi_awareness:
            if sys.platform == "darwin":
                pass  # high DPI scaling works automatically on macOS

            elif sys.platform.startswith("win"):
                import ctypes

                # Values for SetProcessDpiAwareness and SetProcessDpiAwarenessContext:
                # internal enum PROCESS_DPI_AWARENESS
                # {
                #     Process_DPI_Unaware = 0,
                #     Process_System_DPI_Aware = 1,
                #     Process_Per_Monitor_DPI_Aware = 2
                # }
                #
                # internal enum DPI_AWARENESS_CONTEXT
                # {
                #     DPI_AWARENESS_CONTEXT_UNAWARE = 16,
                #     DPI_AWARENESS_CONTEXT_SYSTEM_AWARE = 17,
                #     DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE = 18,
                #     DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = 34
                # }

                # ctypes.windll.user32.SetProcessDpiAwarenessContext(34)  # Non client area scaling at runtime (titlebar)
                # does not work with resizable(False, False), window starts growing on monitor with different scaling (weird tkinter bug...)
                # ctypes.windll.user32.EnableNonClientDpiScaling(hwnd) does not work for some reason (tested on Windows 11)

                # It's too bad, that these Windows API methods don't work properly with tkinter. But I tested days with multiple monitor setups,
                # and I don't think there is anything left to do. So this is the best option at the moment:

                ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Titlebar does not scale at runtime
            else:
                pass  # on Linux the scaling factor is detected with Xft.dpi in get_window_dpi_scaling()

    @classmethod
    def get_window_dpi_scaling(cls, window) -> float:
        if not cls.deactivate_automatic_dpi_awareness:
            if sys.platform == "darwin":
                return 1  # scaling works automatically on macOS

            elif sys.platform.startswith("win"):
                from ctypes import windll, pointer, wintypes

                DPI100pc = 96  # DPI 96 is 100% scaling
                DPI_type = 0  # MDT_EFFECTIVE_DPI = 0, MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2
                window_hwnd = wintypes.HWND(window.winfo_id())
                monitor_handle = windll.user32.MonitorFromWindow(window_hwnd, wintypes.DWORD(2))  # MONITOR_DEFAULTTONEAREST = 2
                x_dpi, y_dpi = wintypes.UINT(), wintypes.UINT()
                windll.shcore.GetDpiForMonitor(monitor_handle, DPI_type, pointer(x_dpi), pointer(y_dpi))
                return (x_dpi.value + y_dpi.value) / (2 * DPI100pc)

            else:
                return cls._get_linux_dpi_scaling(window)
        else:
            return 1

    @staticmethod
    def _read_xft_dpi(display_name: str) -> Union[float, None]:
        """ Returns the Xft.dpi value of the X resource database. GNOME, KDE and other desktops set it to 96 * scaling
            factor for X11 and XWayland apps. It's read with the libX11 that Tk already uses, or with 'xrdb -query'.
            Python builds of python-build-standalone (uv) link libX11 statically, loading the shared libX11 as
            a second copy into the process could crash it, so xrdb is used there. """
        resources = None
        try:
            with open("/proc/self/maps") as maps:
                libx11_loaded = "libX11.so" in maps.read()
        except OSError:
            libx11_loaded = False
        try:
            if not libx11_loaded:
                raise RuntimeError("libX11 is not loaded as a shared library")
            import ctypes
            import ctypes.util
            libx11 = ctypes.CDLL(ctypes.util.find_library("X11") or "libX11.so.6")
            libx11.XOpenDisplay.restype = ctypes.c_void_p
            libx11.XOpenDisplay.argtypes = [ctypes.c_char_p]
            libx11.XResourceManagerString.restype = ctypes.c_char_p
            libx11.XResourceManagerString.argtypes = [ctypes.c_void_p]
            libx11.XCloseDisplay.argtypes = [ctypes.c_void_p]
            display = libx11.XOpenDisplay(display_name.encode() if display_name else None)
            if display:
                try:
                    resources = (libx11.XResourceManagerString(display) or b"").decode(errors="replace")
                finally:
                    libx11.XCloseDisplay(display)
        except Exception:
            resources = None

        if resources is None:
            try:
                env = dict(os.environ, DISPLAY=display_name) if display_name else None
                resources = subprocess.run(["xrdb", "-query"], capture_output=True, text=True, timeout=1, env=env).stdout
            except Exception:
                return None

        match = re.search(r"^Xft\.dpi:\s*([\d.]+)", resources, re.MULTILINE)
        return float(match.group(1)) if match else None

    @classmethod
    def _get_linux_dpi_scaling(cls, window) -> float:
        """ Scaling factor on Linux, based on Xft.dpi (idea from PR #2877 by Ken Van Hoeylandt).
            X11 and XWayland apps have to scale themselves, the desktop only sets Xft.dpi.

            'tk scaling' is set to Xft.dpi as well, before any widgets are created. Tk 8.6 calculates it from the
            DPI of the X server (usually 96), but Xft renders point sizes with Xft.dpi. Since Tk 8.6.15 pixel sizes,
            like the ones of CTkFont, are converted to points with 'tk scaling', so without this, all text would be
            rendered too large compared to the rest of the widgets. Tk 9 already sets 'tk scaling' from Xft.dpi. """
        try:
            display_name = window.winfo_screen()
        except tkinter.TclError:
            return 1

        if display_name not in cls._linux_xft_dpi_cache:
            cls._linux_xft_dpi_cache[display_name] = cls._read_xft_dpi(display_name)
        xft_dpi = cls._linux_xft_dpi_cache[display_name]

        if xft_dpi is None or not 24 <= xft_dpi <= 960:
            try:
                return min(max(float(os.environ.get("GDK_SCALE", 1)), 0.5), 4)  # set for GTK apps on some systems
            except ValueError:
                return 1

        # set 'tk scaling' (pixels per point) once per Tk interpreter
        try:
            if not window.tk.call("info", "exists", "::ctk_tk_scaling_set"):
                window.tk.call("tk", "scaling", xft_dpi / 72)
                window.tk.call("set", "::ctk_tk_scaling_set", 1)
        except tkinter.TclError:
            pass

        return min(max(xft_dpi / 96, 0.5), 4)

    @classmethod
    def check_dpi_scaling(cls):
        new_scaling_detected = False

        # check for every window if scaling value changed
        for window in cls.window_widgets_dict:
            if window.winfo_exists() and not window.state() == "iconic":
                current_dpi_scaling_value = cls.get_window_dpi_scaling(window)
                if current_dpi_scaling_value != cls.window_dpi_scaling_dict[window]:
                    cls.window_dpi_scaling_dict[window] = current_dpi_scaling_value

                    if sys.platform.startswith("win"):
                        window.attributes("-alpha", 0.15)

                    window.block_update_dimensions_event()
                    cls.update_scaling_callbacks_for_window(window)
                    window.unblock_update_dimensions_event()

                    if sys.platform.startswith("win"):
                        window.attributes("-alpha", 1)

                    new_scaling_detected = True

        # find an existing tkinter object for the next call of .after()
        for app in cls.window_widgets_dict.keys():
            try:
                if new_scaling_detected:
                    app.after(cls.loop_pause_after_new_scaling, cls.check_dpi_scaling)
                else:
                    app.after(cls.update_loop_interval, cls.check_dpi_scaling)
                return
            except Exception:
                continue

        cls.update_loop_running = False
