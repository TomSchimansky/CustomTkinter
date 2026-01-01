__version__ = "5.2.2"

from typing import Optional
import os
import sys
from tkinter import Variable, StringVar, IntVar, DoubleVar, BooleanVar
from tkinter.constants import *
import tkinter.filedialog as filedialog

# import manager classes
from .windows.widgets.appearance_mode import AppearanceModeTracker
from .windows.widgets.font import FontManager
from .windows.widgets.scaling import ScalingTracker
from .windows.widgets.theme import ThemeManager
from .windows.widgets.core_rendering import DrawEngine

# import base widgets
from .windows.widgets.core_rendering import CTkCanvas
from .windows.widgets.core_widget_classes import CTkBaseClass

# import widgets
from .windows.widgets import CTkButton
from .windows.widgets import CTkCheckBox
from .windows.widgets import CTkComboBox
from .windows.widgets import CTkEntry
from .windows.widgets import CTkFrame
from .windows.widgets import CTkLabel
from .windows.widgets import CTkOptionMenu
from .windows.widgets import CTkProgressBar
from .windows.widgets import CTkRadioButton
from .windows.widgets import CTkScrollbar
from .windows.widgets import CTkSegmentedButton
from .windows.widgets import CTkSlider
from .windows.widgets import CTkSwitch
from .windows.widgets import CTkTabview
from .windows.widgets import CTkTextbox
from .windows.widgets import CTkScrollableFrame

# import windows
from .windows import CTk
from .windows import CTkToplevel
from .windows import CTkInputDialog

# import font classes
from .windows.widgets.font import CTkFont

# import image classes
from .windows.widgets.image import CTkImage

from .windows import ctk_tk

_ = Variable, StringVar, IntVar, DoubleVar, BooleanVar, CENTER, filedialog  # prevent IDE from removing unused imports


def set_appearance_mode(mode_string: str):
    """ possible values: light, dark, system """
    AppearanceModeTracker.set_appearance_mode(mode_string)


def get_appearance_mode() -> str:
    """ get current state of the appearance mode (light or dark) """
    if AppearanceModeTracker.appearance_mode == 0:
        return "Light"
    elif AppearanceModeTracker.appearance_mode == 1:
        return "Dark"


def set_default_color_theme(color_string: str):
    """ set color theme or load custom theme file by passing the path """
    ThemeManager.load_theme(color_string)


def set_widget_scaling(scaling_value: float):
    """ set scaling for the widget dimensions """
    ScalingTracker.set_widget_scaling(scaling_value)


def set_window_scaling(scaling_value: float):
    """ set scaling for window dimensions """
    ScalingTracker.set_window_scaling(scaling_value)


def deactivate_automatic_dpi_awareness():
    """ deactivate DPI awareness of current process (windll.shcore.SetProcessDpiAwareness(0)) """
    ScalingTracker.deactivate_automatic_dpi_awareness = True


def set_ctk_parent_class(ctk_parent_class):
    ctk_tk.CTK_PARENT_CLASS = ctk_parent_class
def run_showroom() -> None:
    set_appearance_mode("Light")

    new_theme: Optional[str] = "blue"
    while new_theme:
        set_default_color_theme(new_theme)

        app = _Showroom()
        app.mainloop()
        new_theme = app.new_theme


class _Showroom(CTk):
    SPACING = 20

    def __init__(self) -> None:
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        self.new_theme: Optional[str] = None

        # create sidebar frame with widgets
        self.sidebar_frame = CTkFrame(self, width=140, corner_radius=0)
        self.logo_label = CTkLabel(self.sidebar_frame, text="CustomTkinter", font=CTkFont(size=20, weight="bold"))
        self.theme_label = CTkLabel(self.sidebar_frame, text="Theme:", anchor="w")
        self.theme_optionmenu = CTkOptionMenu(self.sidebar_frame, values=ThemeManager._built_in_themes,
                                              command=self._change_theme_event)
        self.theme_optionmenu.set(ThemeManager._currently_loaded_theme)
        self.appearance_mode_label = CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_optionemenu = CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                         command=self._change_appearance_mode_event)
        self.appearance_mode_optionemenu.set(get_appearance_mode())
        self.scaling_label = CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_optionmenu = CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                command=self._change_scaling_event)
        self.scaling_optionmenu.set("100%")

        self.sidebar_frame.pack(side="left", fill="y")
        self.logo_label.pack(side="top", fill="x", padx=5, pady=5)
        self.theme_label.pack(side="top", fill="x", padx=20, pady=(20, 5))
        self.theme_optionmenu.pack(side="top", fill="x", padx=20, pady=(0, 10))
        self.appearance_mode_label.pack(side="top", fill="x", padx=20, pady=(20, 5))
        self.appearance_mode_optionemenu.pack(side="top", fill="x", padx=20, pady=(0, 10))
        self.scaling_label.pack(side="top", fill="x", padx=20, pady=(20, 5))
        self.scaling_optionmenu.pack(side="top", fill="x", padx=20, pady=(0, 10))

        # create main tabview
        self.main_tabview = CTkTabview(self)

        self.main_tabview.pack(side="left", fill="both", expand=True, padx=5, pady=(0, 5))

        # buttons
        self.buttons_frame = self.main_tabview.add("Buttons")

        self.button_1 = CTkButton(self.buttons_frame)
        self.button_2 = CTkButton(self.buttons_frame, hover=False, text="No Hover")
        self.button_3 = CTkButton(self.buttons_frame, state="disabled", text="disabled")

        self.button_1.pack(padx=20, pady=(self.SPACING, 5))
        self.button_2.pack(padx=20, pady=(0, 5))
        self.button_3.pack(padx=20, pady=(0, 5))

        # choices
        self.choices_frame = self.main_tabview.add("Choices")
        self.combobox_1 = CTkComboBox(self.choices_frame,
                                      values=["CTkComboBox", "Value 2", "Value 3", "User can also", "write any text"])
        self.combobox_1.set("CTkComboBox")
        self.combobox_2 = CTkComboBox(self.choices_frame, state="readonly",
                                      values=["readonly", "Value 2", "Value 3", "User can only", "choose a value"])
        self.combobox_2.set("readonly")
        self.optionmenu = CTkOptionMenu(self.choices_frame, dynamic_resizing=False,
                                        values=["CTkOptionMenu", "Value 2", "Value 3"])
        self.seg_button = CTkSegmentedButton(self.choices_frame, values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button.set("CTkSegmentedButton")

        self.combobox_1.pack(padx=20, pady=(self.SPACING, 5))
        self.combobox_2.pack(padx=20, pady=(0, 5))
        self.optionmenu.pack(padx=20, pady=(self.SPACING, 5))
        self.seg_button.pack(padx=20, pady=(self.SPACING, 5))

        # text
        self.text_frame = self.main_tabview.add("Text")
        self.label = CTkLabel(self.text_frame, text="CTkLabel", height=1)
        self.entry = CTkEntry(self.text_frame, placeholder_text="CTkEntry")
        self.textbox = CTkTextbox(self.text_frame, width=400)
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

        self.label.pack(padx=20, pady=(self.SPACING, 5))
        self.entry.pack(padx=20, pady=(self.SPACING, 5))
        self.textbox.pack(padx=20, pady=(self.SPACING, 5))

        # boolean
        self.boolean_frame = self.main_tabview.add("Boolean")
        self.radio_var = IntVar(value=0)
        self.radio_button_1 = CTkRadioButton(self.boolean_frame, variable=self.radio_var, value=0, width=130)
        self.radio_button_2 = CTkRadioButton(self.boolean_frame, variable=self.radio_var, value=1, hover=False, text="No Hover", width=130)
        self.radio_button_3 = CTkRadioButton(self.boolean_frame, variable=self.radio_var, value=2, state="disabled", text="Disabled", width=130)
        self.checkbox_var = BooleanVar(value=True)
        self.checkbox_1 = CTkCheckBox(self.boolean_frame, variable=self.checkbox_var, width=130)
        self.checkbox_2 = CTkCheckBox(self.boolean_frame, hover=False, text="No Hover", width=130)
        self.checkbox_3 = CTkCheckBox(self.boolean_frame, state="disabled", text="Disabled", width=130)
        self.switch_var = BooleanVar(value=True)
        self.switch_1 = CTkSwitch(self.boolean_frame, variable=self.switch_var, width=130)
        self.switch_2 = CTkSwitch(self.boolean_frame, hover=False, text="No Hover", width=130)
        self.switch_3 = CTkSwitch(self.boolean_frame, state="disabled", text="Disabled", width=130)

        self.radio_button_1.pack(padx=20, pady=(self.SPACING, 5))
        self.radio_button_2.pack(padx=20, pady=(0, 5))
        self.radio_button_3.pack(padx=20, pady=(0, 5))
        self.checkbox_1.pack(padx=20, pady=(self.SPACING, 5))
        self.checkbox_2.pack(padx=20, pady=(0, 5))
        self.checkbox_3.pack(padx=20, pady=(0, 5))
        self.switch_1.pack(padx=20, pady=(self.SPACING, 5))
        self.switch_2.pack(padx=20, pady=(0, 5))
        self.switch_3.pack(padx=20, pady=(0, 5))

        # bars
        self.bars_frame = self.main_tabview.add("Bars")
        self.label_progbar_1 = CTkLabel(self.bars_frame, text="CTkProgressBar - determinate", height=1)
        self.progressbar_1 = CTkProgressBar(self.bars_frame, mode="determinate", determinate_speed=0.5)
        self.label_progbar_2 = CTkLabel(self.bars_frame, text="CTkProgressBar - indeterminate", height=1)
        self.progressbar_2 = CTkProgressBar(self.bars_frame, mode="indeterminate", indeterminate_speed=0.5)
        self.label_slider_1 = CTkLabel(self.bars_frame, text="CTkSlider - with steps", height=1)
        self.slider_1 = CTkSlider(self.bars_frame, from_=0, to=1, number_of_steps=4)
        self.label_slider_2 = CTkLabel(self.bars_frame, text="CTkSlider - continuous", height=1)
        self.slider_2 = CTkSlider(self.bars_frame, from_=10, to=100)
        self.label_scrollbar_1 = CTkLabel(self.bars_frame, text="CTkScrollbar", height=1)
        self.scrollbar_1 = CTkScrollbar(self.bars_frame, orientation="horizontal")
        self.scrollbar_1.set(0, 0.3)

        self.label_vertical = CTkLabel(self.bars_frame, text="vertical", height=1)
        self.frame_vertical = CTkFrame(self.bars_frame)
        self.progressbar_3 = CTkProgressBar(self.frame_vertical, orientation="vertical")
        self.slider_3 = CTkSlider(self.frame_vertical, orientation="vertical")
        self.scrollbar_2 = CTkScrollbar(self.frame_vertical, orientation="vertical")
        self.scrollbar_2.set(0, 0.3)

        self.progressbar_1.start()
        self.progressbar_2.start()
        self.slider_3.configure(command = self.progressbar_3.set)

        self.label_progbar_1.pack(padx=20, pady=(self.SPACING, 5))
        self.progressbar_1.pack(padx=20, pady=(0, 5))
        self.label_progbar_2.pack(padx=20, pady=(0, 5))
        self.progressbar_2.pack(padx=20, pady=(0, 5))
        self.label_slider_1.pack(padx=20, pady=(self.SPACING, 5))
        self.slider_1.pack(padx=20, pady=(0, 5))
        self.label_slider_2.pack(padx=20, pady=(0, 5))
        self.slider_2.pack(padx=20, pady=(0, 5))
        self.label_scrollbar_1.pack(padx=20, pady=(self.SPACING, 5))
        self.scrollbar_1.pack(padx=20, pady=(0, 5))

        self.label_vertical.pack(padx=20, pady=(self.SPACING, 5))
        self.frame_vertical.pack(padx=20, pady=(0, 5))
        self.progressbar_3.pack(side="left", padx=20)
        self.slider_3.pack(side="left", padx=20)
        self.scrollbar_2.pack(side="left", padx=20)

        # frames
        self.frames_frame = self.main_tabview.add("Frames")
        self.scrollable_frame = CTkScrollableFrame(self.frames_frame, label_text="CTkScrollableFrame",
                                                   fg_color=ThemeManager.theme["CTk"]["fg_color"])
        self.tabview = CTkTabview(self.frames_frame,
                                  fg_color=ThemeManager.theme["CTk"]["fg_color"])
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")

        for i in range(100):
            switch = CTkSwitch(self.scrollable_frame, text=f"CTkSwitch {i+1}")
            switch.pack(padx=20, pady=5)

        self.scrollable_frame.pack(padx=20, pady=(self.SPACING, 5))
        self.tabview.pack(padx=20, pady=(self.SPACING, 5))

        # windows
        self.windows_frame = self.main_tabview.add("Windows")
        self.open_toplevel = CTkButton(self.windows_frame, text="Open CTkToplevel", command=self._open_ctktoplevel_event)
        self.open_dialog = CTkButton(self.windows_frame, text="Open CTkInputDialog", command=self._open_input_dialog_event)

        self.open_toplevel.pack(padx=20, pady=(self.SPACING, 5))
        self.open_dialog.pack(padx=20, pady=(self.SPACING, 5))


    def _open_ctktoplevel_event(self) -> None:
        toplevel = CTkToplevel(self)
        toplevel.geometry(f"{500}x{250}")
        toplevel.resizable(True, True)
        toplevel.title("CTkToplevel")

    def _open_input_dialog_event(self) -> None:
        dialog = CTkInputDialog(title="CTkInputDialog", text="Description of requested input")
        dialog.get_input()

    def _change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        set_appearance_mode(new_appearance_mode)

    def _change_scaling_event(self, new_scaling: str) -> None:
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        set_widget_scaling(new_scaling_float)

    def _change_theme_event(self, new_theme: str) -> None:
        self.new_theme = new_theme
        self.destroy()
