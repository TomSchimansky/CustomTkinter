from typing import Union, Tuple

from ..widgets.ctk_label import CTkLabel
from ..widgets.ctk_entry import CTkEntry
from ..windows.ctk_toplevel import CTkToplevel
from ..widgets.ctk_button import CTkButton
from ..appearance_mode_tracker import AppearanceModeTracker
from ..theme_manager import ThemeManager


class CTkInputDialog:
    """
    Dialog with extra window, message, entry widget, cancel and ok button.
    For detailed information check out the documentation.
    """

    def __init__(self, *args,
                 fg_color: Union[str, Tuple[str, str]] = "default_theme",
                 hover_color: Union[str, Tuple[str, str]] = "default_theme",
                 border_color: Union[str, Tuple[str, str]] = "default_theme",

                 master: any = None,
                 title: str = "CTkDialog",
                 text: str = "CTkDialog"):

        self._appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        if len(args) > 0 and master is None:
            self.master = args[0]
        elif master is not None:
            self.master = master
        else:
            raise ValueError("master argument is missing")

        self._window_bg_color = ThemeManager.theme["color"]["window_bg_color"]
        self._fg_color = ThemeManager.theme["color"]["button"] if fg_color == "default_theme" else fg_color
        self._hover_color = ThemeManager.theme["color"]["button_hover"] if hover_color == "default_theme" else hover_color
        self._border_color = ThemeManager.theme["color"]["button_hover"] if border_color == "default_theme" else border_color

        self._user_input: Union[str, None] = None
        self._running: bool = False
        self._height: int = len(text.split("\n")) * 20 + 150
        self._text = text

        self._toplevel_window = CTkToplevel(self.master)
        self._toplevel_window.geometry(f"{280}x{self._height}")
        self._toplevel_window.minsize(280, self._height)
        self._toplevel_window.maxsize(280, self._height)
        self._toplevel_window.title(title)
        self._toplevel_window.focus_force()
        self._toplevel_window.grab_set()  # make other windows not clickable
        self._toplevel_window.lift()  # lift window on top
        self._toplevel_window.attributes("-topmost", True)  # stay on top
        self._toplevel_window.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._toplevel_window.after(10, self._create_widgets)  # create widgets with slight delay, to avoid white flickering of background

    def _create_widgets(self):

        self._toplevel_window.grid_columnconfigure((0, 1), weight=1)
        self._toplevel_window.rowconfigure(0, weight=1)

        self._myLabel = CTkLabel(master=self._toplevel_window,
                                 text=self._text,
                                 width=300,
                                 fg_color=None,
                                 height=self._height-100)
        self._myLabel.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        self._entry = CTkEntry(master=self._toplevel_window,
                               width=230)
        self._entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        self._ok_button = CTkButton(master=self._toplevel_window,
                                    text='Ok',
                                    width=100,
                                    command=self._ok_event,
                                    fg_color=self._fg_color,
                                    hover_color=self._hover_color,
                                    border_color=self._border_color)
        self._ok_button.grid(row=2, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky="ew")

        self._cancel_button = CTkButton(master=self._toplevel_window,
                                        text='Cancel',
                                        width=100,
                                        command=self._cancel_event,
                                        fg_color=self._fg_color,
                                        hover_color=self._hover_color,
                                        border_color=self._border_color)
        self._cancel_button.grid(row=2, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky="ew")

        self._entry.focus_force()
        self._entry.bind("<Return>", self._ok_event)

    def _ok_event(self, event=None):
        self._user_input = self._entry.get()
        self._toplevel_window.grab_release()
        self._toplevel_window.destroy()

    def _on_closing(self):
        self._toplevel_window.grab_release()
        self._toplevel_window.destroy()

    def _cancel_event(self):
        self._toplevel_window.grab_release()
        self._toplevel_window.destroy()

    def get_input(self):
        self.master.wait_window(self._toplevel_window)
        return self._user_input
