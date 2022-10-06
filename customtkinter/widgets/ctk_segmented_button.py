import tkinter
from typing import Union, Tuple

from .widget_base_class import CTkBaseClass
from .ctk_button import CTkButton


class CTkSegmentedButton(CTkBaseClass):
    def __init__(self,
                 master: any = None,
                 bg_color: Union[str, Tuple[str, str], None] = None,
                 fg_color: Union[str, Tuple[str, str], None] = "default_theme",
                 hover_color: Union[str, Tuple[str, str]] = "default_theme",
                 text_color: Union[str, Tuple[str, str]] = "default_theme",
                 text_color_disabled: Union[str, Tuple[str, str]] = "default_theme",

                 values: list = None):
        super().__init__(master=master, )

