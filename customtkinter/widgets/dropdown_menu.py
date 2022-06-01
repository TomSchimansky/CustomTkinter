import customtkinter
import tkinter
import sys
from typing import Union

from ..theme_manager import ThemeManager
from ..appearance_mode_tracker import AppearanceModeTracker
from ..scaling_tracker import ScalingTracker


class DropdownMenu(tkinter.Toplevel):
    def __init__(self, *args,
                 fg_color="#555555",
                 button_color="gray50",
                 button_hover_color="gray35",
                 text_color="black",
                 corner_radius=6,
                 button_corner_radius=3,
                 width=120,
                 button_height=24,
                 x_position=0,
                 y_position=0,
                 x_spacing=3,
                 y_spacing=3,
                 command=None,
                 values=None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        ScalingTracker.add_widget(self.set_scaling, self)
        self._widget_scaling = ScalingTracker.get_widget_scaling(self)
        self._spacing_scaling = ScalingTracker.get_spacing_scaling(self)

        self.values = values
        self.command = command

        # color
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"
        self.fg_color = fg_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.text_color = text_color

        # shape
        self.corner_radius = corner_radius
        self.button_corner_radius = button_corner_radius
        self.button_height = button_height
        self.width = width
        self.height = max(len(self.values), 1) * (self.button_height + self.apply_spacing_scaling(y_spacing)) + self.apply_spacing_scaling(y_spacing)

        self.geometry(f"{round(self.apply_widget_scaling(self.width))}x" +
                      f"{round(self.apply_widget_scaling(self.height))}+" +
                      f"{round(x_position)}+{round(y_position)}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        if sys.platform.startswith("darwin"):
            self.overrideredirect(True)  # remove title-bar
            self.overrideredirect(False)
            self.wm_attributes("-transparent", True)  # turn off window shadow
            self.config(bg='systemTransparent')  # transparent bg
            self.frame = customtkinter.CTkFrame(self,
                                                border_width=0,
                                                width=self.width,
                                                corner_radius=self.corner_radius,
                                                fg_color=ThemeManager.single_color(self.fg_color, self.appearance_mode))

        elif sys.platform.startswith("win"):
            self.overrideredirect(True)  # remove title-bar
            self.configure(bg="#010302")
            self.wm_attributes("-transparentcolor", "#010302")
            self.focus()
            self.frame = customtkinter.CTkFrame(self,
                                                border_width=0,
                                                width=self.width,
                                                corner_radius=self.corner_radius,
                                                fg_color=self.fg_color, overwrite_preferred_drawing_method="circle_shapes")
        else:
            self.overrideredirect(True)  # remove title-bar
            self.configure(bg="#010302")
            self.wm_attributes("-transparentcolor", "#010302")
            self.frame = customtkinter.CTkFrame(self,
                                                border_width=0,
                                                width=self.width,
                                                corner_radius=self.corner_radius,
                                                fg_color=self.fg_color, overwrite_preferred_drawing_method="circle_shapes")

        self.frame.grid(row=0, column=0, sticky="nsew", rowspan=1)
        self.frame.grid_rowconfigure(len(self.values) + 1, minsize=self.apply_spacing_scaling(y_spacing))  # add spacing at the bottom
        self.frame.grid_columnconfigure(0, weight=1)

        self.button_list = []
        for index, option in enumerate(self.values):
            button = customtkinter.CTkButton(self.frame,
                                             text=option,
                                             height=self.button_height,
                                             width=self.width - 2 * self.apply_widget_scaling(x_spacing),
                                             fg_color=self.button_color,
                                             text_color=self.text_color,
                                             hover_color=self.button_hover_color,
                                             corner_radius=self.button_corner_radius,
                                             command=lambda i=index: self.button_callback(i))
            button.text_label.configure(anchor="w")
            button.text_label.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="w")
            button.grid(row=index, column=0,
                        padx=self.apply_widget_scaling(x_spacing),
                        pady=(self.apply_widget_scaling(y_spacing), 0), sticky="ew")
            self.button_list.append(button)

        self.bind("<FocusOut>", self.focus_loss_event)
        self.frame.canvas.bind("<Button-1>", self.focus_loss_event)

    def apply_widget_scaling(self, value: Union[int, float, str]) -> Union[float, str]:
        if isinstance(value, (int, float)):
            return value * self._widget_scaling
        else:
            return value

    def apply_spacing_scaling(self, value: Union[int, float, str]) -> Union[float, str]:
        if isinstance(value, (int, float)):
            return value * self._spacing_scaling
        else:
            return value

    def set_scaling(self, new_widget_scaling, new_spacing_scaling, new_window_scaling):
        return

    def focus_loss_event(self, event):
        self.destroy()
        if sys.platform.startswith("darwin"):
            self.update()

    def button_callback(self, index):
        self.destroy()
        if sys.platform.startswith("darwin"):
            self.update()

        if self.command is not None:
            self.command(self.values[index])
