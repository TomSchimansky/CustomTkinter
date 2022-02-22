import sys
import tkinter
from distutils.version import StrictVersion as Version
import darkdetect

if Version(darkdetect.__version__) < Version("0.3.1"):
    sys.stderr.write("WARNING: You have to update the darkdetect library: pip3 install --upgrade darkdetect\n")
    if sys.platform != "darwin":
        exit()


class AppearanceModeTracker:

    callback_list = []
    root_tk_list = []
    update_loop_running = False

    appearance_mode_set_by = "system"
    appearance_mode = 0  # Light (standard)

    @classmethod
    def init_appearance_mode(cls):
        if cls.appearance_mode_set_by == "system":
            new_appearance_mode = cls.detect_appearance_mode()

            if new_appearance_mode != cls.appearance_mode:
                cls.appearance_mode = new_appearance_mode
                cls.update_callbacks()

    @classmethod
    def add(cls, callback, widget=None):
        cls.callback_list.append(callback)

        if widget is not None:
            root_tk = cls.get_tk_root_of_widget(widget)
            if root_tk not in cls.root_tk_list:
                cls.root_tk_list.append(root_tk)

                if not cls.update_loop_running:
                    root_tk.after(500, cls.update)
                    cls.update_loop_running = True

    @classmethod
    def remove(cls, callback):
        cls.callback_list.remove(callback)

    @staticmethod
    def detect_appearance_mode():
        try:
            if darkdetect.theme() == "Dark":
                return 1  # Dark
            else:
                return 0  # Light
        except NameError:
            return 0  # Light

    @classmethod
    def get_tk_root_of_widget(cls, widget):
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
        for root_tk in cls.root_tk_list:
            try:
                root_tk.after(200, cls.update)
                return
            except Exception:
                continue

        cls.update_loop_running = False

    @classmethod
    def get_mode(cls):
        return cls.appearance_mode

    @classmethod
    def set_appearance_mode(cls, mode_string):
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


AppearanceModeTracker.init_appearance_mode()
