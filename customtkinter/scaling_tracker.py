import tkinter
import sys

from .ctk_settings import CTkSettings


class ScalingTracker:

    window_widgets_dict = {}  # contains window objects as keys with list of widget callbacks as elements

    window_dpi_scaling_dict = {}  # contains window objects as keys and corresponding scaling factors

    widget_scaling = 1  # user values which multiply to detected window scaling factor
    window_scaling = 1
    spacing_scaling = 1

    update_loop_running = False

    @classmethod
    def get_widget_scaling(cls, widget):
        window_root = cls.get_window_root_of_widget(widget)
        return cls.window_dpi_scaling_dict[window_root] * cls.widget_scaling

    @classmethod
    def get_spacing_scaling(cls, widget):
        window_root = cls.get_window_root_of_widget(widget)
        return cls.window_dpi_scaling_dict[window_root] * cls.spacing_scaling

    @classmethod
    def get_window_scaling(cls, window):
        window_root = cls.get_window_root_of_widget(window)
        return cls.window_dpi_scaling_dict[window_root] * cls.window_scaling

    @classmethod
    def set_widget_scaling(cls, widget_scaling_factor):
        cls.widget_scaling = max(widget_scaling_factor, 0.4)
        cls.update_scaling_callbacks()

    @classmethod
    def set_spacing_scaling(cls, spacing_scaling_factor):
        cls.spacing_scaling = max(spacing_scaling_factor, 0.4)
        cls.update_scaling_callbacks()

    @classmethod
    def set_window_scaling(cls, window_scaling_factor):
        cls.window_scaling = max(window_scaling_factor, 0.4)
        cls.update_scaling_callbacks()

    @classmethod
    def get_window_root_of_widget(cls, widget):
        current_widget = widget

        while isinstance(current_widget, tkinter.Tk) is False and\
                isinstance(current_widget, tkinter.Toplevel) is False:
            current_widget = current_widget.master

        return current_widget

    @classmethod
    def update_scaling_callbacks(cls):
        for window, callback_list in cls.window_widgets_dict.items():
            for callback in callback_list:
                if not CTkSettings.deactivate_automatic_dpi_awareness:
                    callback(cls.window_dpi_scaling_dict[window] * cls.widget_scaling,
                             cls.window_dpi_scaling_dict[window] * cls.spacing_scaling,
                             cls.window_dpi_scaling_dict[window] * cls.window_scaling)
                else:
                    callback(cls.widget_scaling,
                             cls.spacing_scaling,
                             cls.window_scaling)

    @classmethod
    def add_widget(cls, widget_callback, widget):
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
    def add_window(cls, window_callback, window):
        if window not in cls.window_widgets_dict:
            cls.window_widgets_dict[window] = [window_callback]
        else:
            cls.window_widgets_dict[window].append(window_callback)

        if window not in cls.window_dpi_scaling_dict:
            cls.window_dpi_scaling_dict[window] = cls.get_window_dpi_scaling(window)

    @classmethod
    def activate_high_dpi_awareness(cls):
        """ make process DPI aware, customtkinter elemets will get scaled automatically,
            only gets activated when CTk object is created """

        if not CTkSettings.deactivate_automatic_dpi_awareness:
            if sys.platform == "darwin":
                pass  # high DPI scaling works automatically on macOS

            elif sys.platform.startswith("win"):
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(2)
                # Microsoft Docs: https://docs.microsoft.com/en-us/windows/win32/api/shellscalingapi/ne-shellscalingapi-process_dpi_awareness

            else:
                pass  # DPI awareness on Linux not implemented

    @classmethod
    def get_window_dpi_scaling(cls, window):
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
            return 1  # DPI awareness on Linux not implemented

    @classmethod
    def check_dpi_scaling(cls):
        # find an existing tkinter object for the next call of .after()
        for root_tk in cls.window_widgets_dict.keys():
            try:
                root_tk.after(500, cls.check_dpi_scaling)
                return
            except Exception:
                continue

        cls.update_loop_running = False
