import tkinter
import sys
import copy
import re
from typing import Union
from typing import Callable

from ..theme_manager import ThemeManager
from ..appearance_mode_tracker import AppearanceModeTracker
from ..scaling_tracker import ScalingTracker
from .widget_base_class import CTkBaseClass


class CTkMenu(tkinter.Menu, CTkBaseClass):

    def get_color_from_name(self, mode, name: str):
        color = ThemeManager.theme["color"][name][mode]
        return color

    def add_cascade(self, cnf={}, **kw):
        self.add('cascade', cnf or kw)

    def __init__(self, master: tkinter.Tk, text_font = "default_theme", cnf={}, **kw):
        
        super().__init__(cnf, kw)
        
        if isinstance(master, tkinter.Tk) or isinstance(master, CTkFrame) or isinstance(master, CTkToplevel):
            self.option_add('*tearOff', False)
        
        self.mode = AppearanceModeTracker.get_mode()
        ctk_bg =  self.get_color_from_name(self.mode, "frame_high")
        ctk_fg = self.get_color_from_name(self.mode, "text")
        ctk_hover_bg = self.get_color_from_name(self.mode, "button")
        self.text_font = (ThemeManager.theme["text"]["font"], ThemeManager.theme["text"]["size"]) if text_font == "default_theme" else text_font
        #self.font = CTkBaseClass.apply_font_scaling(self.text_font)
        self.configure(background=ctk_bg)
        self.configure(foreground=ctk_fg)
        self.configure(borderwidth=0)
        self.configure(activebackground=ctk_hover_bg)
        self.config(font=self.text_font)
