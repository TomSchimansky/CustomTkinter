import tkinter
from typing import Union, Tuple, Dict, List, Callable, Optional

from .theme import ThemeManager
from .ctk_frame import CTkFrame
from .core_rendering import CTkCanvas
from .core_rendering import DrawEngine
from .core_widget_classes import CTkBaseClass
from .ctk_segmented_button import CTkSegmentedButton


class CTkTabview(CTkBaseClass):
    """
    Tabview...
    For detailed information check out the documentation.
    """

    _top_spacing: int = 10  # px on top of the buttons
    _top_button_overhang: int = 8  # px
    _button_height: int = 26
    _segmented_button_border_width: int = 3

    def __init__(self,
                 master: any,
                 width: int = 300,
                 height: int = 250,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,

                 segmented_button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 segmented_button_selected_color: Optional[Union[str, Tuple[str, str]]] = None,
                 segmented_button_selected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 segmented_button_unselected_color: Optional[Union[str, Tuple[str, str]]] = None,
                 segmented_button_unselected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,

                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

                 command: Union[Callable, None] = None,
                 state: str = "normal",
                 **kwargs):

        # transfer some functionality to CTkFrame
        super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

        # color
        self._border_color = ThemeManager.theme["CTkFrame"]["border_color"] if border_color is None else self._check_color_type(border_color)

        # determine fg_color of frame
        if fg_color is None:
            if isinstance(self.master, (CTkFrame, CTkTabview)):
                if self.master.cget("fg_color") == ThemeManager.theme["CTkFrame"]["fg_color"]:
                    self._fg_color = ThemeManager.theme["CTkFrame"]["top_fg_color"]
                else:
                    self._fg_color = ThemeManager.theme["CTkFrame"]["fg_color"]
            else:
                self._fg_color = ThemeManager.theme["CTkFrame"]["fg_color"]
        else:
            self._fg_color = self._check_color_type(fg_color, transparency=True)

        # shape
        self._corner_radius = ThemeManager.theme["CTkFrame"]["corner_radius"] if corner_radius is None else corner_radius
        self._border_width = ThemeManager.theme["CTkFrame"]["border_width"] if border_width is None else border_width

        self._canvas = CTkCanvas(master=self,
                                 bg=self._apply_appearance_mode(self._bg_color),
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._desired_width),
                                 height=self._apply_widget_scaling(self._desired_height - self._top_spacing - self._top_button_overhang))
        self._draw_engine = DrawEngine(self._canvas)

        self._segmented_button = CTkSegmentedButton(self,
                                                    values=[],
                                                    height=self._button_height,
                                                    fg_color=segmented_button_fg_color,
                                                    selected_color=segmented_button_selected_color,
                                                    selected_hover_color=segmented_button_selected_hover_color,
                                                    unselected_color=segmented_button_unselected_color,
                                                    unselected_hover_color=segmented_button_unselected_hover_color,
                                                    text_color=text_color,
                                                    text_color_disabled=text_color_disabled,
                                                    corner_radius=corner_radius,
                                                    border_width=self._segmented_button_border_width,
                                                    command=self._segmented_button_callback,
                                                    state=state)
        self._configure_segmented_button_background_corners()
        self._configure_grid()
        self._set_grid_canvas()

        self._tab_dict: Dict[str, CTkFrame] = {}
        self._name_list: List[str] = []  # list of unique tab names in order of tabs
        self._current_name: str = ""
        self._command = command

        self._draw()

    def _segmented_button_callback(self, selected_name):
        self._set_grid_tab_by_name(selected_name)
        self._tab_dict[self._current_name].grid_forget()
        self._current_name = selected_name

        if self._command is not None:
            self._command()

    def winfo_children(self) -> List[any]:
        """
        winfo_children of CTkTabview without canvas and segmented button widgets,
        because it's not a child but part of the CTkTabview itself
        """

        child_widgets = super().winfo_children()
        try:
            child_widgets.remove(self._canvas)
            child_widgets.remove(self._segmented_button)
            return child_widgets
        except ValueError:
            return child_widgets

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height - self._top_spacing - self._top_button_overhang))
        self._configure_grid()
        self._draw(no_color_updates=True)

    def _set_dimensions(self, width=None, height=None):
        super()._set_dimensions(width, height)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height - self._top_spacing - self._top_button_overhang))
        self._draw()

    def _configure_segmented_button_background_corners(self):
        """ needs to be called for changes in fg_color, bg_color """

        if self._fg_color is not None:
            self._segmented_button.configure(background_corner_colors=(self._bg_color, self._bg_color, self._fg_color, self._fg_color))
        else:
            self._segmented_button.configure(background_corner_colors=(self._bg_color, self._bg_color, self._bg_color, self._bg_color))

    def _configure_tab_background_corners_by_name(self, name: str):
        """ needs to be called for changes in fg_color, bg_color, border_width """

        self._tab_dict[name].configure(background_corner_colors=None)

    def _configure_grid(self):
        """ create 3 x 4 grid system """

        self.grid_rowconfigure(0, weight=0, minsize=self._apply_widget_scaling(self._top_spacing))
        self.grid_rowconfigure(1, weight=0, minsize=self._apply_widget_scaling(self._top_button_overhang))
        self.grid_rowconfigure(2, weight=0, minsize=self._apply_widget_scaling(self._button_height - self._top_button_overhang))
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=1)

    def _set_grid_canvas(self):
        self._canvas.grid(row=2, rowspan=2, column=0, columnspan=1, sticky="nsew")

    def _set_grid_segmented_button(self):
        """ needs to be called for changes in corner_radius """
        self._segmented_button.grid(row=1, rowspan=2, column=0, columnspan=1, padx=self._apply_widget_scaling(self._corner_radius), sticky="ns")

    def _set_grid_tab_by_name(self, name: str):
        """ needs to be called for changes in corner_radius, border_width """
        self._tab_dict[name].grid(row=3, column=0, sticky="nsew",
                                  padx=self._apply_widget_scaling(max(self._corner_radius, self._border_width)),
                                  pady=self._apply_widget_scaling(max(self._corner_radius, self._border_width)))

    def _grid_forget_all_tabs(self):
        for frame in self._tab_dict.values():
            frame.grid_forget()

    def _create_tab(self) -> CTkFrame:
        new_tab = CTkFrame(self,
                           height=0,
                           width=0,
                           fg_color=self._fg_color,
                           border_width=0,
                           corner_radius=self._corner_radius)
        return new_tab

    def _draw(self, no_color_updates: bool = False):
        super()._draw(no_color_updates)

        if not self._canvas.winfo_exists():
            return

        requires_recoloring = self._draw_engine.draw_rounded_rect_with_border(self._apply_widget_scaling(self._current_width),
                                                                              self._apply_widget_scaling(self._current_height - self._top_spacing - self._top_button_overhang),
                                                                              self._apply_widget_scaling(self._corner_radius),
                                                                              self._apply_widget_scaling(self._border_width))

        if no_color_updates is False or requires_recoloring:
            if self._fg_color == "transparent":
                self._canvas.itemconfig("inner_parts",
                                        fill=self._apply_appearance_mode(self._bg_color),
                                        outline=self._apply_appearance_mode(self._bg_color))
            else:
                self._canvas.itemconfig("inner_parts",
                                        fill=self._apply_appearance_mode(self._fg_color),
                                        outline=self._apply_appearance_mode(self._fg_color))

            self._canvas.itemconfig("border_parts",
                                    fill=self._apply_appearance_mode(self._border_color),
                                    outline=self._apply_appearance_mode(self._border_color))
            self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))
            tkinter.Frame.configure(self, bg=self._apply_appearance_mode(self._bg_color))  # configure bg color of tkinter.Frame, cuase canvas does not fill frame

    def configure(self, require_redraw=False, **kwargs):
        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")
            require_redraw = True
        if "border_width" in kwargs:
            self._border_width = kwargs.pop("border_width")
            require_redraw = True

        if "fg_color" in kwargs:
            self._fg_color = self._check_color_type(kwargs.pop("fg_color"), transparency=True)
            require_redraw = True
        if "border_color" in kwargs:
            self._border_color = self._check_color_type(kwargs.pop("border_color"))
            require_redraw = True
        if "segmented_button_fg_color" in kwargs:
            self._segmented_button.configure(fg_color=kwargs.pop("segmented_button_fg_color"))
        if "segmented_button_selected_color" in kwargs:
            self._segmented_button.configure(selected_color=kwargs.pop("segmented_button_selected_color"))
        if "segmented_button_selected_hover_color" in kwargs:
            self._segmented_button.configure(selected_hover_color=kwargs.pop("segmented_button_selected_hover_color"))
        if "segmented_button_unselected_color" in kwargs:
            self._segmented_button.configure(unselected_color=kwargs.pop("segmented_button_unselected_color"))
        if "segmented_button_unselected_hover_color" in kwargs:
            self._segmented_button.configure(unselected_hover_color=kwargs.pop("segmented_button_unselected_hover_color"))
        if "text_color" in kwargs:
            self._segmented_button.configure(text_color=kwargs.pop("text_color"))
        if "text_color_disabled" in kwargs:
            self._segmented_button.configure(text_color_disabled=kwargs.pop("text_color_disabled"))

        if "command" in kwargs:
            self._command = kwargs.pop("command")
        if "state" in kwargs:
            self._segmented_button.configure(state=kwargs.pop("state"))

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str):
        if attribute_name == "corner_radius":
            return self._corner_radius
        elif attribute_name == "border_width":
            return self._border_width

        elif attribute_name == "fg_color":
            return self._fg_color
        elif attribute_name == "border_color":
            return self._border_color
        elif attribute_name == "segmented_button_fg_color":
            return self._segmented_button.cget(attribute_name)
        elif attribute_name == "segmented_button_selected_color":
            return self._segmented_button.cget(attribute_name)
        elif attribute_name == "segmented_button_selected_hover_color":
            return self._segmented_button.cget(attribute_name)
        elif attribute_name == "segmented_button_unselected_color":
            return self._segmented_button.cget(attribute_name)
        elif attribute_name == "segmented_button_unselected_hover_color":
            return self._segmented_button.cget(attribute_name)
        elif attribute_name == "text_color":
            return self._segmented_button.cget(attribute_name)
        elif attribute_name == "text_color_disabled":
            return self._segmented_button.cget(attribute_name)

        elif attribute_name == "command":
            return self._command
        elif attribute_name == "state":
            return self._segmented_button.cget(attribute_name)

        else:
            return super().cget(attribute_name)

    def tab(self, name: str) -> CTkFrame:
        """ returns reference to the tab with given name """

        if name in self._tab_dict:
            return self._tab_dict[name]
        else:
            raise ValueError(f"CTkTabview has no tab named '{name}'")

    def insert(self, index: int, name: str) -> CTkFrame:
        """ creates new tab with given name at position index """

        if name not in self._tab_dict:
            # if no tab exists, set grid for segmented button
            if len(self._tab_dict) == 0:
                self._set_grid_segmented_button()

            self._name_list.insert(index, name)
            self._tab_dict[name] = self._create_tab()
            self._segmented_button.insert(index, name)
            self._configure_tab_background_corners_by_name(name)

            # if created tab is only tab select this tab
            if len(self._tab_dict) == 1:
                self._current_name = name
                self._segmented_button.set(self._current_name)
                self._grid_forget_all_tabs()
                self._set_grid_tab_by_name(self._current_name)

            return self._tab_dict[name]
        else:
            raise ValueError(f"CTkTabview already has tab named '{name}'")

    def add(self, name: str) -> CTkFrame:
        """ appends new tab with given name """
        return self.insert(len(self._tab_dict), name)

    def move(self, new_index: int, name: str):
        if 0 <= new_index < len(self._name_list):
            if name in self._tab_dict:
                self._segmented_button.move(new_index, name)
            else:
                raise ValueError(f"CTkTabview has no name '{name}'")
        else:
            raise ValueError(f"CTkTabview new_index {new_index} not in range of name list with len {len(self._name_list)}")

    def delete(self, name: str):
        """ delete tab by name """

        if name in self._tab_dict:
            self._name_list.remove(name)
            self._tab_dict[name].grid_forget()
            self._tab_dict.pop(name)
            self._segmented_button.delete(name)

            # set current_name to '' and remove segmented button if no tab is left
            if len(self._name_list) == 0:
                self._current_name = ""
                self._segmented_button.grid_forget()

            # if only one tab left, select this tab
            elif len(self._name_list) == 1:
                self._current_name = self._name_list[0]
                self._segmented_button.set(self._current_name)
                self._grid_forget_all_tabs()
                self._set_grid_tab_by_name(self._current_name)

            # more tabs are left
            else:
                # if current_name is deleted tab, select first tab at position 0
                if self._current_name == name:
                    self.set(self._name_list[0])
        else:
            raise ValueError(f"CTkTabview has no tab named '{name}'")

    def set(self, name: str):
        """ select tab by name """

        if name in self._tab_dict:
            self._current_name = name
            self._segmented_button.set(name)
            self._grid_forget_all_tabs()
            self._set_grid_tab_by_name(name)
        else:
            raise ValueError(f"CTkTabview has no tab named '{name}'")

    def get(self) -> str:
        """ returns name of selected tab, returns empty string if no tab selected """
        return self._current_name
