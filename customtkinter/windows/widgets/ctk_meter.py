import customtkinter as ctk
import math
from typing import Union, Tuple, Optional

class CTkMeter(ctk.CTkCanvas):
    CIRCLE = "CIRCLE"
    RING = "RING"

    def __init__(
        self,
        master: any,
        metersize: int = 400,
        value: int = 10,
        progress_thickness: int = 50,
        progress_color: Union[str, Tuple[str, str]] = "red",
        mid_circle_color: Union[str, Tuple[str, str]] = None,
        bg_color: Optional[Union[str, Tuple[str, str]]] = None,
        mid_text_font: Optional[Union[tuple]] = ("Times", 50),
        mid_text_color: Union[str, Tuple[str, str]] = None,
        max_amount: int = 100,
        border: bool = False,
        border_color: Union[str, Tuple[str, str]] = None,
        division: bool = False,
        no_of_divisions: int = 50,
        meter_label_text: str = None,
        meter_label_text_color: Union[str, Tuple[str, str]] = "green",
        meter_label_text_font: Union[tuple] = ("Times", 20),
        mode: str = CIRCLE,  # RING or CIRCLE
        prefix_text: str = None,
        prefix_text_color: Union[str, Tuple[str, str]] = "red",
        prefix_text_font: Union[tuple] = ("Times", 20),
        suffix_text: str = None,
        suffix_text_color: Union[str, Tuple[str, str]] = "red",
        suffix_text_font: Union[tuple] = ("Times", 20),
    ):
        """A Meter Widget that can be used to show progress

        Args:
            master (any): parent widget
            metersize (int, optional): size of the meter. Defaults to 400.
            value (int, optional): progress value. Defaults to 10.
            progress_thickness (int, optional): progresss thickness. Defaults to 50.
            progress_color (Union[str, Tuple[str, str]], optional): color of the progress. Defaults to 'red'.
            mid_circle_color (Union[str, Tuple[str, str]], optional): color of the circle in the middle for CIRCLE mode. Defaults to None.
            bg_color (Optional[Union[str, Tuple[str, str]]], optional): backgrounf color. Defaults to None.
            mid_text_font (Optional[Union[tuple]], optional): font of the middle text. Defaults to ('Times',50).
            mid_text_color (Union[str, Tuple[str, str]], optional): color of the middle text. Defaults to None.
            max_amount (int, optional): meter maximum value. Defaults to 100.
            border (bool, optional): border or the non progress part. Defaults to False.
            border_color (Union[str, Tuple[str, str]], optional): color of the border. Defaults to None.
            division (bool, optional): show the divisions. Defaults to False.
            no_of_divisions (int, optional): number of divisions. Defaults to 50.
            meter_label_text (str, optional): meter label. Defaults to None.
            meter_label_text_color (Union[str, Tuple[str, str]], optional): color of the meter label. Defaults to 'black'.
            meter_label_text_font (Union[tuple], optional): font of the meter label. Defaults to ('Times',20).
            mode (str, optional): CIRCLE or RING. Defaults to CIRCLE.
            prefix_text (str, optional): prefix text. Defaults to None.
            prefix_text_color (Union[str, Tuple[str, str]], optional): color of the prefix. Defaults to 'red'.
            prefix_text_font (Union[tuple], optional): font of the prefix. Defaults to ('Times',20).
            suffix_text (str, optional): suffix text. Defaults to None.
            suffix_text_color (Union[str, Tuple[str, str]], optional): color of the suffix. Defaults to 'red'.
            suffix_text_font (Union[tuple], optional): font of the suffix. Defaults to ('Times',20).
        """
        self.metersize = metersize
        self.value = value
        self.thickness = progress_thickness + metersize // 2
        self.color = progress_color
        self.mid_text_font = mid_text_font
        self.max_amount = max_amount
        self._top_circle_color = mid_circle_color
        self.border_color = border_color
        self._no_of_division = no_of_divisions
        self.division = division
        self._mode = mode

        # meter_label
        self.meter_label_text = meter_label_text
        self.meter_label_text_color = meter_label_text_color
        self.meter_label_text_font = meter_label_text_font

        # prefix
        self.prefix_text = prefix_text
        self.prefix_text_color = prefix_text_color
        self.prefix_text_font = prefix_text_font
        
        # suffix
        self.suffix_text = suffix_text
        self.suffix_text_color = suffix_text_color
        self.suffix_text_font = suffix_text_font

        if bg_color is None:
            if ctk.get_appearance_mode().lower() == "light":
                self._bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][0]
            elif ctk.get_appearance_mode().lower() == "dark":
                self._bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1]
        else:
            self._bg_color = bg_color

        if border_color is None:
            if ctk.get_appearance_mode().lower() == "light":
                self.border_color = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"][0]
            elif ctk.get_appearance_mode().lower() == "dark":
                self.border_color = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"][1]
        else:
            self.border_color = border_color

        if mid_circle_color is None:
            if ctk.get_appearance_mode().lower() == "light":
                self._top_circle_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1]
            elif ctk.get_appearance_mode().lower() == "dark":
                self._top_circle_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][0]
        else:
            self._top_circle_color = mid_circle_color

        if mid_text_color is None:
            if ctk.get_appearance_mode().lower() == "light":
                self.mid_text_color = "white"
            elif ctk.get_appearance_mode().lower() == "dark":
                self.mid_text_color = "black"
        else:
            self.mid_text_color = mid_text_color
        
        super().__init__(master, width=metersize, height=metersize, bg=self._bg_color, highlightthickness=0)

        if border:
            self.create_aa_circle(metersize // 2, metersize // 2, radius=metersize // 2 - 1, fill=self.border_color,tags='border')

        self.set_value(value)

    def _appearance_upadte(self,bg_color=None,
                           border_color=None,
                           mid_circle_color=None,
                           mid_text_color=None):
        if bg_color is None:
            if ctk.get_appearance_mode().lower() == "light":
                self._bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][0]
            elif ctk.get_appearance_mode().lower() == "dark":
                self._bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1]
        else:
            self._bg_color = bg_color

        if border_color is None:
            if ctk.get_appearance_mode().lower() == "light":
                self.border_color = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"][0]
            elif ctk.get_appearance_mode().lower() == "dark":
                self.border_color = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"][1]
        else:
            self.border_color = border_color

        if mid_circle_color is None:
            if ctk.get_appearance_mode().lower() == "light":
                self._top_circle_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1]
            elif ctk.get_appearance_mode().lower() == "dark":
                self._top_circle_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][0]
        else:
            self._top_circle_color = mid_circle_color

        if mid_text_color is None:
            if ctk.get_appearance_mode().lower() == "light":
                self.mid_text_color = "white"
            elif ctk.get_appearance_mode().lower() == "dark":
                self.mid_text_color = "black"
        else:
            self.mid_text_color = mid_text_color
        
        super().configure(bg=self._bg_color)
    
    def _draw_division(self):
        divisions = self._no_of_division
        angle_step = 360 / divisions
        center_x = self.metersize // 2
        center_y = self.metersize // 2
        radius = self.metersize // 2
        if self._mode == self.RING:
            col = self._top_circle_color
        elif self._mode == self.CIRCLE:
            col = self._bg_color
        for i in range(divisions):
            angle = i * angle_step
            end_x = center_x + radius * math.cos(math.radians(angle))
            end_y = center_y + radius * math.sin(math.radians(angle))
            self._divisions=self.create_line(
                center_x,
                center_y,
                end_x,
                end_y,
                smooth=True,
                fill=col,
                width=5,
            )

    def set_value(self, value: int):
        self.delete("fill_arc")
        self.delete("midd_circle")
        self.delete("text")

        start_angle = 90
        new_value = int((value / self.max_amount) * 100)
        end_angle = start_angle - new_value * 3.5999
        self.fill_arc = self.create_arc(
            0,
            0,
            self.metersize,
            self.metersize,
            start=start_angle,
            extent=end_angle - start_angle,
            outline="",
            fill=self.color,
            width=5,
            tags="fill_arc",
        )
        if self.division:
            self._draw_division()
        if self._mode == self.RING:
            self.create_aa_circle(
                self.metersize // 2,
                self.metersize // 2,
                radius=self.metersize - self.thickness,
                fill=self._bg_color,
                tags="midd_circle",
            )
        elif self._mode == self.CIRCLE:
            self._circle=self.create_aa_circle(
                self.metersize // 2,
                self.metersize // 2,
                radius=self.metersize - self.thickness,
                fill=self._top_circle_color,
                tags="midd_circle",
            )
        text_x = self.metersize // 2
        text_y = self.metersize // 2
        self.create_text(
            text_x, text_y, text=f"{value}", font=self.mid_text_font, fill=self.mid_text_color, tags="text"
        )
        self.lift("text")
        if self.suffix_text is not None:
            self.delete("suffix")
            mid_cord = self.bbox("text")
            self.create_text(
                mid_cord[2],
                text_y + (mid_cord[3] - mid_cord[1] - 20) // 2,
                text=f"{self.suffix_text}",
                anchor="sw",
                font=self.suffix_text_font,
                fill=self.suffix_text_color,
                tags="suffix",
            )
            self.lift("suffix")
        
        if self.prefix_text is not None:
            self.delete("prefix")
            mid_cord = self.bbox("text")
            self.create_text(
                mid_cord[0],
                text_y +(mid_cord[3] - mid_cord[1] - 20) // 2,
                text=f"{self.prefix_text}",
                anchor="se",
                font=self.prefix_text_font,
                fill=self.prefix_text_color,
                tags="prefix",
            )
            self.lift("prefix")

        if self.meter_label_text is not None:
            self.delete("meter_label")
            mid_cord = self.bbox("text")
            self.create_text(
                self.metersize // 2,
                text_y + (mid_cord[3] - mid_cord[1] - 20) // 2,
                text=f"{self.meter_label_text}",
                anchor="n",
                font=self.meter_label_text_font,
                fill=self.meter_label_text_color,
                tags="meter_label",
            )
            self.lift("meter_label")
