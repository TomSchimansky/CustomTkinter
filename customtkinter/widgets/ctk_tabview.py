import tkinter
from typing import Union, Tuple, List

from ..theme_manager import ThemeManager
from .widget_base_class import CTkBaseClass
from .ctk_frame import CTkFrame


class CTkTab:
    def __init__(self, master=None, identifier: str = None, text: str = "CTkTab", index: int = 0):
        self.text: str = text
        self.frame: tkinter.Frame = tkinter.Frame(master, width=0, height=0)
        self.identifier = str(id(self.frame)) if identifier is None else identifier
        self.visible: bool = True
        self.index = index


class CTkTabview(CTkBaseClass):
    """
    Tabview...
    For detailed information check out the documentation.
    """

    _top_spacing = 10  # px on top of the buttons
    _top_button_overhang = 8  # px
    _button_size = 24

    def __init__(self,
                 master: any = None,
                 width: int = 300,
                 height: int = 250,
                 corner_radius: Union[int, str] = "default_theme",
                 border_width: Union[int, str] = "default_theme",

                 bg_color: Union[str, Tuple[str, str], None] = None,
                 fg_color: Union[str, Tuple[str, str], None] = "default_theme",

                 button_frame_color: Union[str, Tuple[str, str]] = "default_theme",
                 button_color: Union[str, Tuple[str, str]] = "default_theme",
                 button_hover_color: Union[str, Tuple[str, str]] = "default_theme",
                 border_color: Union[str, Tuple[str, str]] = "default_theme",

                 **kwargs):

        # transfer basic functionality (bg_color, size, appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

        # determine fg_color
        if fg_color == "default_theme":
            if isinstance(self.master, (CTkFrame, CTkTabview)):
                if self.master.cget("fg_color") == ThemeManager.theme["color"]["frame_low"]:
                    self._fg_color = ThemeManager.theme["color"]["frame_high"]
                else:
                    self._fg_color = ThemeManager.theme["color"]["frame_low"]
            else:
                self._fg_color = ThemeManager.theme["color"]["frame_low"]
        else:
            self._fg_color = fg_color

        self._border_color = ThemeManager.theme["color"]["frame_border"] if border_color == "default_theme" else border_color
        self._button_frame_color = ThemeManager.theme["color"]["tabview_button_frame"] if button_frame_color == "default_theme" else button_frame_color
        self._button_color = ThemeManager.theme["color"]["tabview_button"] if button_color == "default_theme" else button_color
        self._button_hover_color = ThemeManager.theme["color"]["tabview_button_hover"] if button_hover_color == "default_theme" else button_hover_color

        # shape
        self._corner_radius = ThemeManager.theme["shape"]["frame_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self._border_width = ThemeManager.theme["shape"]["frame_border_width"] if border_width == "default_theme" else border_width

        self._main_frame = CTkFrame(self,
                                    width=width,
                                    height=height - (self._top_spacing + self._top_button_overhang),
                                    bg_color=self._bg_color,
                                    fg_color=self._fg_color,
                                    border_color=self._border_color,
                                    border_width=self._border_width)
        self._button_frame = CTkFrame(self,
                                      width=0,
                                      height=0,
                                      bg_color=self._fg_color,
                                      fg_color=self._button_frame_color,
                                      border_color=self._border_color,
                                      border_width=self._border_width)
        self._create_grid_for_frames()

        self._tab_list: List[CTkTab] = []

    def _create_grid_for_frames(self):
        """ create 3 x 4 grid system """

        self.grid_rowconfigure(0, weight=0, minsize=self._apply_widget_scaling(self._top_spacing))
        self.grid_rowconfigure(1, weight=0, minsize=self._apply_widget_scaling(self._top_button_overhang))
        self.grid_rowconfigure(2, weight=0, minsize=self._apply_widget_scaling(self._button_size - self._top_button_overhang))
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure((0, 2), weight=1, minsize=self._apply_widget_scaling(self._corner_radius))
        self.grid_columnconfigure(1, weight=0, minsize=self._apply_widget_scaling(self._corner_radius))

        self._main_frame.grid(row=2, column=0, rowspan=2, columnspan=3, sticky="nsew")
        self._button_frame.grid(row=1, column=1, rowspan=2, columnspan=1, sticky="nsew")

    def _get_tab_by_identifier(self, identifier: str):
        for tab in self._tab_list:
            if tab.identifier == identifier:
                return tab

    def create_tab(self, identifier=None, text="CTkTabview"):
        new_tab = CTkTab(master=self, identifier=identifier, text=text)
        self._tab_list.append(new_tab)
        return new_tab.identifier

    def select_tab(self, identifier: str):
        selected_tab = self._get_tab_by_identifier(identifier)
        for tab in self._tab_list:
            if tab != selected_tab:
                tab.frame.grid_forget()

        selected_tab.frame.grid(row=3, column=0, rowspan=1, columnspan=3, sticky="nsew")

    def get_tab(self, identifier):
        pass

