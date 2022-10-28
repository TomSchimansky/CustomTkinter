import sys
import tkinter
import tkinter.ttk as ttk
import copy
from typing import Union, Callable, Tuple

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

from ...windows.ctk_tk import CTk
from ...windows.ctk_toplevel import CTkToplevel
from ...appearance_mode_tracker import AppearanceModeTracker
from ...scaling_tracker import ScalingTracker
from ...theme_manager import ThemeManager
from ..font.ctk_font import CTkFont
from ..image.ctk_image import CTkImage

from ...utility.utility_functions import pop_from_dict_by_set, check_kwargs_empty


class CTkBaseClass(tkinter.Frame):
    """ Base class of every CTk widget, handles the dimensions, _bg_color,
        appearance_mode changes, scaling, bg changes of master if master is not a CTk widget """

    # attributes that are passed to and managed by the tkinter frame only:
    _valid_tk_frame_attributes: set = {"cursor"}

    _cursor_manipulation_enabled: bool = True

    def __init__(self,
                 master: any = None,
                 width: int = 0,
                 height: int = 0,

                 bg_color: Union[str, Tuple[str, str], None] = None,
                 **kwargs):

        super().__init__(master=master, width=width, height=height, **pop_from_dict_by_set(kwargs, self._valid_tk_frame_attributes))

        # check if kwargs is empty, if not raise error for unsupported arguments
        check_kwargs_empty(kwargs, raise_error=True)

        # dimensions
        self._current_width = width  # _current_width and _current_height in pixel, represent current size of the widget
        self._current_height = height  # _current_width and _current_height are independent of the scale
        self._desired_width = width  # _desired_width and _desired_height, represent desired size set by width and height
        self._desired_height = height

        # scaling
        ScalingTracker.add_widget(self._set_scaling, self)  # add callback for automatic scaling changes
        self._widget_scaling = ScalingTracker.get_widget_scaling(self)

        super().configure(width=self._apply_widget_scaling(self._desired_width),
                          height=self._apply_widget_scaling(self._desired_height))

        # save latest geometry function and kwargs
        class GeometryCallDict(TypedDict):
            function: Callable
            kwargs: dict

        self._last_geometry_manager_call: Union[GeometryCallDict, None] = None

        # add set_appearance_mode method to callback list of AppearanceModeTracker for appearance mode changes
        AppearanceModeTracker.add(self._set_appearance_mode, self)
        self._appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        # background color
        self._bg_color:  Union[str, Tuple[str, str]] = self._detect_color_of_master() if bg_color is None else bg_color

        super().configure(bg=ThemeManager.single_color(self._bg_color, self._appearance_mode))
        super().bind('<Configure>', self._update_dimensions_event)

        # overwrite configure methods of master when master is tkinter widget, so that bg changes get applied on child CTk widget as well
        if isinstance(self.master, (tkinter.Tk, tkinter.Toplevel, tkinter.Frame)) and not isinstance(self.master, (CTkBaseClass, CTk, CTkToplevel)):
            master_old_configure = self.master.config

            def new_configure(*args, **kwargs):
                if "bg" in kwargs:
                    self.configure(bg_color=kwargs["bg"])
                elif "background" in kwargs:
                    self.configure(bg_color=kwargs["background"])

                # args[0] is dict when attribute gets changed by widget[<attribute>] syntax
                elif len(args) > 0 and type(args[0]) == dict:
                    if "bg" in args[0]:
                        self.configure(bg_color=args[0]["bg"])
                    elif "background" in args[0]:
                        self.configure(bg_color=args[0]["background"])
                master_old_configure(*args, **kwargs)

            self.master.config = new_configure
            self.master.configure = new_configure

    def _draw(self, no_color_updates: bool = False):
        """ abstract of draw method to be overridden """
        pass

    def config(self, *args, **kwargs):
        raise AttributeError("'config' is not implemented for CTk widgets. For consistency, always use 'configure' instead.")

    def configure(self, require_redraw=False, **kwargs):
        """ basic configure with bg_color, width, height support, calls configure of tkinter.Frame, updates in the end """

        if "width" in kwargs:
            self._set_dimensions(width=kwargs.pop("width"))

        if "height" in kwargs:
            self._set_dimensions(height=kwargs.pop("height"))

        if "bg_color" in kwargs:
            new_bg_color = kwargs.pop("bg_color")
            if new_bg_color is None:
                self._bg_color = self._detect_color_of_master()
            else:
                self._bg_color = new_bg_color
            require_redraw = True

        super().configure(**pop_from_dict_by_set(kwargs, self._valid_tk_frame_attributes))  # configure tkinter.Frame

        # if there are still items in the kwargs dict, raise ValueError
        check_kwargs_empty(kwargs, raise_error=True)

        if require_redraw:
            self._draw()

    def cget(self, attribute_name: str):
        """ basic cget with bg_color, width, height support, calls cget of tkinter.Frame """

        if attribute_name == "bg_color":
            return self._bg_color
        elif attribute_name == "width":
            return self._desired_width
        elif attribute_name == "height":
            return self._desired_height

        elif attribute_name in self._valid_tk_frame_attributes:
            return super().cget(attribute_name)  # cget of tkinter.Frame
        else:
            raise ValueError(f"'{attribute_name}' is not a supported argument. Look at the documentation for supported arguments.")

    @staticmethod
    def _check_font_type(font: any):
        if isinstance(font, CTkFont):
            return font

        elif type(font) == tuple and len(font) == 1:
            sys.stderr.write(f"Warning: font {font} given without size, will be extended with default text size of current theme\n")
            return font[0], ThemeManager.theme["text"]["size"]

        elif type(font) == tuple and 2 <= len(font) <= 3:
            return font

        else:
            raise ValueError(f"Wrong font type {type(font)}\n" +
                             f"For consistency, Customtkinter requires the font argument to be a tuple of len 2 or 3 or an instance of CTkFont.\n" +
                             f"\nUsage example:\n" +
                             f"font=customtkinter.CTkFont(family='<name>', size=<size in px>)\n" +
                             f"font=('<name>', <size in px>)\n")

    def _update_dimensions_event(self, event):
        # only redraw if dimensions changed (for performance), independent of scaling
        if round(self._current_width) != round(event.width / self._widget_scaling) or round(self._current_height) != round(event.height / self._widget_scaling):
            self._current_width = (event.width / self._widget_scaling)  # adjust current size according to new size given by event
            self._current_height = (event.height / self._widget_scaling)  # _current_width and _current_height are independent of the scale

            self._draw(no_color_updates=True)  # faster drawing without color changes

    def _detect_color_of_master(self, master_widget=None) -> Union[str, Tuple[str, str]]:
        """ detect color of self.master widget to set correct _bg_color """

        if master_widget is None:
            master_widget = self.master

        if isinstance(master_widget, (CTkBaseClass, CTk, CTkToplevel)) and hasattr(master_widget, "_fg_color"):
            if master_widget.cget("fg_color") is not None:
                return master_widget.cget("fg_color")

            # if fg_color of master is None, try to retrieve fg_color from master of master
            elif hasattr(master_widget.master, "master"):
                return self._detect_color_of_master(master_widget.master)

        elif isinstance(master_widget, (ttk.Frame, ttk.LabelFrame, ttk.Notebook, ttk.Label)):  # master is ttk widget
            try:
                ttk_style = ttk.Style()
                return ttk_style.lookup(master_widget.winfo_class(), 'background')
            except Exception:
                return "#FFFFFF", "#000000"

        else:  # master is normal tkinter widget
            try:
                return master_widget.cget("bg")  # try to get bg color by .cget() method
            except Exception:
                return "#FFFFFF", "#000000"

    def _set_appearance_mode(self, mode_string):
        if mode_string.lower() == "dark":
            self._appearance_mode = 1
        elif mode_string.lower() == "light":
            self._appearance_mode = 0

        super().configure(bg=ThemeManager.single_color(self._bg_color, self._appearance_mode))
        self._draw()

    def _set_scaling(self, new_widget_scaling, new_window_scaling):
        self._widget_scaling = new_widget_scaling

        super().configure(width=self._apply_widget_scaling(self._desired_width),
                          height=self._apply_widget_scaling(self._desired_height))

        if self._last_geometry_manager_call is not None:
            self._last_geometry_manager_call["function"](**self._apply_argument_scaling(self._last_geometry_manager_call["kwargs"]))

    def _set_dimensions(self, width=None, height=None):
        if width is not None:
            self._desired_width = width
        if height is not None:
            self._desired_height = height

        super().configure(width=self._apply_widget_scaling(self._desired_width),
                          height=self._apply_widget_scaling(self._desired_height))

    def _apply_widget_scaling(self, value: Union[int, float, str]) -> Union[float, str]:
        if isinstance(value, (int, float)):
            return value * self._widget_scaling
        else:
            return value

    def _apply_font_scaling(self, font: Union[Tuple, CTkFont]) -> tuple:
        """ Takes CTkFont object and returns tuple font with scaled size, has to be called again for every change of font object """
        if type(font) == tuple:
            if len(font) == 1:
                return font
            elif len(font) == 2:
                return font[0], -abs(round(font[1] * self._widget_scaling))
            elif len(font) == 3:
                return font[0], -abs(round(font[1] * self._widget_scaling)), font[2]
            else:
                raise ValueError(f"Can not scale font {font}. font needs to be tuple of len 1, 2 or 3")

        elif isinstance(font, CTkFont):
            return font.create_scaled_tuple(self._widget_scaling)
        else:
            raise ValueError(f"Can not scale font '{font}' of type {type(font)}. font needs to be tuple or instance of CTkFont")

    def _apply_argument_scaling(self, kwargs: dict) -> dict:
        scaled_kwargs = copy.copy(kwargs)

        if "pady" in scaled_kwargs:
            if isinstance(scaled_kwargs["pady"], (int, float, str)):
                scaled_kwargs["pady"] = self._apply_widget_scaling(scaled_kwargs["pady"])
            elif isinstance(scaled_kwargs["pady"], tuple):
                scaled_kwargs["pady"] = tuple([self._apply_widget_scaling(v) for v in scaled_kwargs["pady"]])
        if "padx" in kwargs:
            if isinstance(scaled_kwargs["padx"], (int, float, str)):
                scaled_kwargs["padx"] = self._apply_widget_scaling(scaled_kwargs["padx"])
            elif isinstance(scaled_kwargs["padx"], tuple):
                scaled_kwargs["padx"] = tuple([self._apply_widget_scaling(v) for v in scaled_kwargs["padx"]])

        if "x" in scaled_kwargs:
            scaled_kwargs["x"] = self._apply_widget_scaling(scaled_kwargs["x"])
        if "y" in scaled_kwargs:
            scaled_kwargs["y"] = self._apply_widget_scaling(scaled_kwargs["y"])

        return scaled_kwargs

    def destroy(self):
        """ Destroy this and all descendants widgets. """
        AppearanceModeTracker.remove(self._set_appearance_mode)
        ScalingTracker.remove_widget(self._set_scaling, self)
        super().destroy()

    def place(self, **kwargs):
        """
        Place a widget in the parent widget. Use as options:
        in=master - master relative to which the widget is placed
        in_=master - see 'in' option description
        x=amount - locate anchor of this widget at position x of master
        y=amount - locate anchor of this widget at position y of master
        relx=amount - locate anchor of this widget between 0.0 and 1.0 relative to width of master (1.0 is right edge)
        rely=amount - locate anchor of this widget between 0.0 and 1.0 relative to height of master (1.0 is bottom edge)
        anchor=NSEW (or subset) - position anchor according to given direction
        width=amount - width of this widget in pixel
        height=amount - height of this widget in pixel
        relwidth=amount - width of this widget between 0.0 and 1.0 relative to width of master (1.0 is the same width as the master)
        relheight=amount - height of this widget between 0.0 and 1.0 relative to height of master (1.0 is the same height as the master)
        bordermode="inside" or "outside" - whether to take border width of master widget into account
        """
        self._last_geometry_manager_call = {"function": super().place, "kwargs": kwargs}
        return super().place(**self._apply_argument_scaling(kwargs))

    def place_forget(self):
        """ Unmap this widget. """
        self._last_geometry_manager_call = None
        return super().place_forget()

    def pack(self, **kwargs):
        """
        Pack a widget in the parent widget. Use as options:
        after=widget - pack it after you have packed widget
        anchor=NSEW (or subset) - position widget according to given direction
        before=widget - pack it before you will pack widget
        expand=bool - expand widget if parent size grows
        fill=NONE or X or Y or BOTH - fill widget if widget grows
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        side=TOP or BOTTOM or LEFT or RIGHT -  where to add this widget.
        """
        self._last_geometry_manager_call = {"function": super().pack, "kwargs": kwargs}
        return super().pack(**self._apply_argument_scaling(kwargs))

    def pack_forget(self):
        """ Unmap this widget and do not use it for the packing order. """
        self._last_geometry_manager_call = None
        return super().pack_forget()

    def grid(self, **kwargs):
        """
        Position a widget in the parent widget in a grid. Use as options:
        column=number - use cell identified with given column (starting with 0)
        columnspan=number - this widget will span several columns
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        row=number - use cell identified with given row (starting with 0)
        rowspan=number - this widget will span several rows
        sticky=NSEW - if cell is larger on which sides will this widget stick to the cell boundary
        """
        self._last_geometry_manager_call = {"function": super().grid, "kwargs": kwargs}
        return super().grid(**self._apply_argument_scaling(kwargs))

    def grid_forget(self):
        """ Unmap this widget. """
        self._last_geometry_manager_call = None
        return super().grid_forget()
