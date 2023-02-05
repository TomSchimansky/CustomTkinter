from typing import Union, Tuple, Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import tkinter
import sys

from .ctk_frame import CTkFrame
from .ctk_scrollbar import CTkScrollbar
from .appearance_mode import CTkAppearanceModeBaseClass
from .core_widget_classes import CTkBaseClass


class CTkScrollableFrame(tkinter.Frame, CTkAppearanceModeBaseClass):
    def __init__(self,
                 master: any,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,

                 orientation: Literal["vertical", "horizontal"] = "vertical"):

        self._orientation = orientation

        self.parent_frame = CTkFrame(master=master, width=width, height=height, corner_radius=corner_radius,
                                     border_width=border_width, bg_color=bg_color, fg_color=fg_color, border_color=border_color)
        self.parent_frame.grid_propagate(0)
        self.parent_canvas = tkinter.Canvas(master=self.parent_frame, highlightthickness=0, width=0, height=0)
        self._set_scroll_increments()

        if self._orientation == "horizontal":
            self.scrollbar = CTkScrollbar(master=self.parent_frame, orientation="horizontal", command=self.parent_canvas.xview)
            self.parent_canvas.configure(xscrollcommand=self.scrollbar.set)
        elif self._orientation == "vertical":
            self.scrollbar = CTkScrollbar(master=self.parent_frame, orientation="vertical", command=self.parent_canvas.yview)
            self.parent_canvas.configure(yscrollcommand=self.scrollbar.set)
        self._create_grid()

        tkinter.Frame.__init__(self, master=self.parent_canvas, highlightthickness=0)
        CTkAppearanceModeBaseClass.__init__(self)

        self.bind("<Configure>", lambda e: self.parent_canvas.configure(scrollregion=self.parent_canvas.bbox("all")))
        self.parent_canvas.bind("<Configure>", self._fit_frame_dimensions_to_canvas)
        self.bind_all("<MouseWheel>", self._mouse_wheel_all)
        self.bind_all("<KeyPress-Shift_L>", self._keyboard_shift_press_all)
        self.bind_all("<KeyPress-Shift_R>", self._keyboard_shift_press_all)
        self.bind_all("<KeyRelease-Shift_L>", self._keyboard_shift_release_all)
        self.bind_all("<KeyRelease-Shift_R>", self._keyboard_shift_release_all)
        self._create_window_id = self.parent_canvas.create_window(0, 0, window=self, anchor="nw")

        tkinter.Frame.configure(self, bg=self._apply_appearance_mode(self.parent_frame.cget("fg_color")))

        self._shift_pressed = False

    def destroy(self):
        tkinter.Frame.destroy(self)
        CTkAppearanceModeBaseClass.destroy(self)

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        tkinter.Frame.configure(self, bg=self._apply_appearance_mode(self.parent_frame.cget("fg_color")))

    def configure(self, **kwargs):
        if "fg_color" in kwargs:
            self.parent_frame.configure(fg_color=kwargs.pop("fg_color"))
            tkinter.Frame.configure(self, bg=self._apply_appearance_mode(self.parent_frame.cget("fg_color")))

            for child in self.winfo_children():
                if isinstance(child, CTkBaseClass):
                    child.configure(bg_color=self.parent_frame.cget("fg_color"))

        if "corner_radius" in kwargs:
            self.parent_frame.configure(corner_radius=kwargs.pop("corner_radius"))
            self._create_grid()

        if "border_width" in kwargs:
            self.parent_frame.configure(border_width=kwargs.pop("border_width"))
            self._create_grid()

        self.parent_frame.configure(**kwargs)

    def _fit_frame_dimensions_to_canvas(self, event):
        if self._orientation == "horizontal":
            self.parent_canvas.itemconfigure(self._create_window_id, height=self.parent_canvas.winfo_height())
        elif self._orientation == "vertical":
            self.parent_canvas.itemconfigure(self._create_window_id, width=self.parent_canvas.winfo_width())

    def _set_scroll_increments(self):
        if sys.platform.startswith("win"):
            self.parent_canvas.configure(xscrollincrement=1, yscrollincrement=1)
        elif sys.platform == "darwin":
            self.parent_canvas.configure(xscrollincrement=4, yscrollincrement=8)

    def _create_grid(self):
        border_spacing = self.parent_frame.cget("corner_radius") + self.parent_frame.cget("border_width")
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        if self._orientation == "horizontal":
            self.parent_frame.grid_rowconfigure(1, weight=0)
            self.parent_canvas.grid(row=0, column=0, sticky="nsew",
                                    padx=border_spacing, pady=(border_spacing, 0))
            self.scrollbar.grid(row=1, column=0, sticky="nsew",
                                padx=border_spacing)
        elif self._orientation == "vertical":
            self.parent_frame.grid_columnconfigure(1, weight=0)
            self.parent_canvas.grid(row=0, column=0, sticky="nsew",
                                    pady=border_spacing, padx=(border_spacing, 0))
            self.scrollbar.grid(row=0, column=1, sticky="nsew",
                                pady=border_spacing)

    def _mouse_wheel_all(self, event):
        if self.check_if_master_is_canvas(event.widget):
            if sys.platform.startswith("win"):
                if self._shift_pressed:
                    if self.parent_canvas.xview() != (0.0, 1.0):
                        self.parent_canvas.xview("scroll", -int(event.delta/6), "units")
                else:
                    if self.parent_canvas.yview() != (0.0, 1.0):
                        self.parent_canvas.yview("scroll", -int(event.delta/6), "units")
            elif sys.platform == "darwin":
                if self._shift_pressed:
                    if self.parent_canvas.xview() != (0.0, 1.0):
                        self.parent_canvas.xview("scroll", -event.delta, "units")
                else:
                    if self.parent_canvas.yview() != (0.0, 1.0):
                        self.parent_canvas.yview("scroll", -event.delta, "units")
            else:
                if self._shift_pressed:
                    if self.parent_canvas.xview() != (0.0, 1.0):
                        self.parent_canvas.xview("scroll", -event.delta, "units")
                else:
                    if self.parent_canvas.yview() != (0.0, 1.0):
                        self.parent_canvas.yview("scroll", -event.delta, "units")

    def _keyboard_shift_press_all(self, event):
        self._shift_pressed = True

    def _keyboard_shift_release_all(self, event):
        self._shift_pressed = False

    def check_if_master_is_canvas(self, widget):
        if widget == self.parent_canvas:
            return True
        elif widget.master is not None:
            return self.check_if_master_is_canvas(widget.master)
        else:
            return False

    def pack(self, **kwargs):
        self.parent_frame.pack(**kwargs)

    def place(self, **kwargs):
        self.parent_frame.place(**kwargs)

    def grid(self, **kwargs):
        self.parent_frame.grid(**kwargs)

    def pack_forget(self):
        self.parent_frame.pack_forget()

    def place_forget(self, **kwargs):
        self.parent_frame.place_forget()

    def grid_forget(self, **kwargs):
        self.parent_frame.grid_forget()

    def grid_remove(self, **kwargs):
        self.parent_frame.grid_remove()

    def grid_propagate(self, **kwargs):
        self.parent_frame.grid_propagate()

    def grid_info(self, **kwargs):
        self.parent_frame.grid_info()

    def lift(self, aboveThis=None):
        self.parent_frame.lift(aboveThis)

    def lower(self, belowThis=None):
        self.parent_frame.lower(belowThis)
