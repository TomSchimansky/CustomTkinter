from typing import Union, Tuple, List, Optional
import tkinter

from .ctk_frame import CTkFrame
from .ctk_scrollbar import CTkScrollbar


class CTkScrollableFrame(tkinter.Frame):

    _xscrollincrement = 4  # horizontal scrolling speed
    _yscrollincrement = 8  # vertical scrolling speed

    def __init__(self,
                 master: any,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,

                 activate_x_scrollbars: bool = False,
                 activate_y_scrollbars: bool = True):

        self._activate_x_scrollbars = activate_x_scrollbars
        self._activate_y_scrollbars = activate_y_scrollbars

        self.parent_frame = CTkFrame(master=master, width=width, height=height, corner_radius=corner_radius, border_width=border_width)
        self.parent_canvas = tkinter.Canvas(master=self.parent_frame, yscrollincrement=self._yscrollincrement, xscrollincrement=self._xscrollincrement)
        if self._activate_x_scrollbars:
            self.x_scrollbar = CTkScrollbar(master=self.parent_frame, orientation="horizontal", command=self.parent_canvas.xview)
            self.parent_canvas.configure(xscrollcommand=self.x_scrollbar.set)
        if self._activate_y_scrollbars:
            self.y_scrollbar = CTkScrollbar(master=self.parent_frame, orientation="vertical", command=self.parent_canvas.yview)
            self.parent_canvas.configure(yscrollcommand=self.y_scrollbar.set)
        self._create_grid()

        super().__init__(master=self.parent_canvas, width=0)

        self.bind("<Configure>", lambda e: self.parent_canvas.configure(scrollregion=self.parent_canvas.bbox("all")))
        self.bind_all("<MouseWheel>", self._mouse_wheel_all)
        self.bind_all("<KeyPress-Shift_L>", self._keyboard_shift_press_all)
        self.bind_all("<KeyPress-Shift_R>", self._keyboard_shift_press_all)
        self.bind_all("<KeyRelease-Shift_L>", self._keyboard_shift_release_all)
        self.bind_all("<KeyRelease-Shift_R>", self._keyboard_shift_release_all)
        self.parent_canvas.bind("<Configure>", self._parent_canvas_configure)
        self._create_window_id = self.parent_canvas.create_window(0, 0, window=self, anchor="nw")

        self._shift_pressed = False
        self.mouse_over_widget = False

    def _create_grid(self):
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)
        self.parent_canvas.grid(row=0, column=0, sticky="nsew")

        if self._activate_x_scrollbars:
            self.parent_frame.grid_rowconfigure(1, weight=0)
            self.x_scrollbar.grid(row=1, column=0, sticky="nsew")
        if self._activate_y_scrollbars:
            self.parent_frame.grid_columnconfigure(1, weight=0)
            self.y_scrollbar.grid(row=0, column=1, sticky="nsew")

    def _parent_canvas_configure(self, event):
        #self.parent_canvas.itemconfigure(self._create_window_id, width=event.width, height=event.height)
        pass

    def _mouse_wheel_all(self, event):
        if self.check_if_master_is_canvas(event.widget):
            if self._shift_pressed:
                self.parent_canvas.xview("scroll", -event.delta, "units")
            else:
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
