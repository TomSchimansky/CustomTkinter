import tkinter
import time
from typing import Union, Tuple

from ..widgets.ctk_label import CTkLabel
from ..widgets.ctk_entry import CTkEntry
from ..widgets.ctk_frame import CTkFrame
from ..windows.ctk_toplevel import CTkToplevel
from ..widgets.ctk_button import CTkButton
from ..appearance_mode_tracker import AppearanceModeTracker
from ..theme_manager import ThemeManager


class CTkInputDialog:
    """
    Dialog with extra window, message, entry widget, cancel and ok button.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 master: any = None,
                 title: str = "CTkDialog",
                 text: str = "CTkDialog",
                 fg_color: Union[str, Tuple[str, str]] = "default_theme",
                 hover_color: Union[str, Tuple[str, str]] = "default_theme",
                 border_color: Union[str, Tuple[str, str]] = "default_theme"):

        self._appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"
        self.master = master

        self._window_bg_color = ThemeManager.theme["color"]["window_bg_color"]
        self._fg_color = ThemeManager.theme["color"]["button"] if fg_color == "default_theme" else fg_color
        self._hover_color = ThemeManager.theme["color"]["button_hover"] if hover_color == "default_theme" else hover_color
        self._border_color = ThemeManager.theme["color"]["button_hover"] if border_color == "default_theme" else border_color

        self._user_input: Union[str, None] = None
        self._running: bool = False
        self._height: int = len(text.split("\n")) * 20 + 150
        self._text = text

        self._toplevel_window = CTkToplevel()
        self._toplevel_window.geometry(f"{280}x{self._height}")
        self._toplevel_window.minsize(280, self._height)
        self._toplevel_window.maxsize(280, self._height)
        self._toplevel_window.title(title)
        self._toplevel_window.lift()
        self._toplevel_window.focus_force()
        self._toplevel_window.grab_set()
        self._toplevel_window.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._toplevel_window.after(10, self._create_widgets)  # create widgets with slight delay, to avoid white flickering of background

    def _create_widgets(self):
        self._label_frame = CTkFrame(master=self._toplevel_window,
                                     corner_radius=0,
                                     fg_color=self._window_bg_color,
                                     width=300,
                                     height=self._height-100)
        self._label_frame.place(relx=0.5, rely=0, anchor=tkinter.N)

        self._button_and_entry_frame = CTkFrame(master=self._toplevel_window,
                                                corner_radius=0,
                                                fg_color=self._window_bg_color,
                                                width=300,
                                                height=100)
        self._button_and_entry_frame.place(relx=0.5, rely=1, anchor=tkinter.S)

        self._myLabel = CTkLabel(master=self._label_frame,
                                 text=self._text,
                                 width=300,
                                 fg_color=None,
                                 height=self._height-100)
        self._myLabel.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self._entry = CTkEntry(master=self._button_and_entry_frame,
                               width=230)
        self._entry.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self._ok_button = CTkButton(master=self._button_and_entry_frame,
                                    text='Ok',
                                    width=100,
                                    command=self._ok_event,
                                    fg_color=self._fg_color,
                                    hover_color=self._hover_color,
                                    border_color=self._border_color)
        self._ok_button.place(relx=0.28, rely=0.65, anchor=tkinter.CENTER)

        self._cancel_button = CTkButton(master=self._button_and_entry_frame,
                                        text='Cancel',
                                        width=100,
                                        command=self._cancel_event,
                                        fg_color=self._fg_color,
                                        hover_color=self._hover_color,
                                        border_color=self._border_color)
        self._cancel_button.place(relx=0.72, rely=0.65, anchor=tkinter.CENTER)

        self._entry.focus_force()
        self._entry.bind("<Return>", self._ok_event)

    def _ok_event(self, event=None):
        self._user_input = self._entry.get()
        self._running = False

    def _on_closing(self):
        self._running = False

    def _cancel_event(self):
        self._running = False

    def get_input(self):
        self._running = True

        while self._running:
            try:
                self._toplevel_window.update()
            except Exception:
                return self._user_input
            finally:
                time.sleep(0.01)

        time.sleep(0.05)
        self._toplevel_window.destroy()
        return self._user_input
