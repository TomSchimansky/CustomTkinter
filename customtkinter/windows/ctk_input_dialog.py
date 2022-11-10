from typing import Union, Tuple

from .widgets.ctk_label import CTkLabel
from .widgets.ctk_entry import CTkEntry
from .widgets.ctk_button import CTkButton
from .widgets.theme.theme_manager import ThemeManager
from .ctk_toplevel import CTkToplevel


class CTkInputDialog(CTkToplevel):
    """
    Dialog with extra window, message, entry widget, cancel and ok button.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 master: any = None,
                 fg_color: Union[str, Tuple[str, str]] = "default",
                 button_fg_color: Union[str, Tuple[str, str]] = "default",
                 button_hover_color: Union[str, Tuple[str, str]] = "default",
                 text_color: Union[str, Tuple[str, str]] = "default",

                 title: str = "CTkDialog",
                 text: str = "CTkDialog"):

        super().__init__(master=master, fg_color=fg_color)

        self._fg_color = ThemeManager.theme["color"]["window"] if fg_color == "default" else fg_color
        self._button_fg_color = ThemeManager.theme["color"]["button"] if button_fg_color == "default" else button_fg_color
        self._button_hover_color = ThemeManager.theme["color"]["button_hover"] if button_hover_color == "default" else button_hover_color
        self._text_color = ThemeManager.theme["color"]["text"] if button_hover_color == "default" else button_hover_color
        self._user_input: Union[str, None] = None
        self._running: bool = False
        self._height: int = len(text.split("\n")) * 20 + 150
        self._text = text

        self.geometry(f"{280}x{self._height}")
        self.minsize(280, self._height)
        self.maxsize(280, self._height)
        self.title(title)
        self.focus_force()
        self.grab_set()  # make other windows not clickable
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(10, self._create_widgets)  # create widgets with slight delay, to avoid white flickering of background

    def _create_widgets(self):

        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self._myLabel = CTkLabel(master=self,
                                 text=self._text,
                                 width=300,
                                 fg_color=None,
                                 height=self._height-100)
        self._myLabel.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        self._entry = CTkEntry(master=self,
                               width=230)
        self._entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        self._ok_button = CTkButton(master=self,
                                    text='Ok',
                                    width=100,
                                    command=self._ok_event,
                                    fg_color=self._fg_color,
                                    hover_color=self._hover_color,
                                    border_width=0)
        self._ok_button.grid(row=2, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky="ew")

        self._cancel_button = CTkButton(master=self,
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
        self.grab_release()
        self.destroy()

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self._user_input
