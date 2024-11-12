from typing import Union, Tuple, Optional

from .widgets import CTkLabel
from .widgets import CTkButton
from .widgets.theme import ThemeManager
from .ctk_toplevel import CTkToplevel
from .widgets.font import CTkFont


class CTkConfirmationDialog(CTkToplevel):
    """
    Dialog with a simple cancel and ok button.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_text_color: Optional[Union[str, Tuple[str, str]]] = None,

                 title: str = "Confirm",
                 font: Optional[Union[tuple, CTkFont]] = None,
                 message: str = "Are you sure?"):

        super().__init__(fg_color=fg_color)

        self._fg_color = ThemeManager.theme["CTkToplevel"]["fg_color"] if fg_color is None else self._check_color_type(fg_color)
        self._text_color = ThemeManager.theme["CTkLabel"]["text_color"] if text_color is None else self._check_color_type(button_hover_color)
        self._button_fg_color = ThemeManager.theme["CTkButton"]["fg_color"] if button_fg_color is None else self._check_color_type(button_fg_color)
        self._button_hover_color = ThemeManager.theme["CTkButton"]["hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)
        self._button_text_color = ThemeManager.theme["CTkButton"]["text_color"] if button_text_color is None else self._check_color_type(button_text_color)

        self._running: bool = False
        self._response = None
        self._title = title
        self._message = message
        self._font = font

        self.title(self._title)
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(10, self._create_widgets)  # create widgets with slight delay, to avoid white flickering of background
        self.resizable(False, False)

        self.grab_set()
        self.wait_window()

    def _create_widgets(self):
        # Message label
        self.label = CTkLabel(master=self,
                              width=300,
                              wraplength=300,
                              fg_color="transparent",
                              text_color=self._text_color,
                              text=self._message,
                              font=self._font)
        self.label.pack(pady=(20, 10))

        # OK and Cancel buttons
        self.ok_button = CTkButton(master=self,
                                   width=100,
                                   border_width=0,
                                   fg_color=self._button_fg_color,
                                   hover_color=self._button_hover_color,
                                   text_color=self._button_text_color,
                                   text='Ok',
                                   font=self._font,
                                   command=(lambda: self._set_response(True)))
        self.ok_button.pack(side="left", padx=(30, 10), pady=(10, 20))

        self.cancel_button = CTkButton(master=self,
                                       width=100,
                                       border_width=0,
                                       fg_color=self._button_fg_color,
                                       hover_color=self._button_hover_color,
                                       text_color=self._button_text_color,
                                       text='Cancel',
                                       font=self._font,
                                       command=(lambda: self._set_response(False)))
        self.cancel_button.pack(side="right", padx=(10, 30), pady=(10, 20))

    def _set_response(self, value):
        self._response = value
        self.destroy()

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def get_selection(self):
        return self._response
