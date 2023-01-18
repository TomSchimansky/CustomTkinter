from typing import Optional, Union, Tuple

from .core_rendering import CTkCanvas
from .ctk_scrollbar import CTkScrollbar
from .ctk_frame import CTkFrame
from .appearance_mode import AppearanceModeTracker


class CTkScrollableFrame(CTkFrame):
    """
    A scrollable frame that allows you to add any kind of items (including frames with multiple widgets on it).
    all you have to do is inherit from this class. Example

    parent_scrollable = customtkinter.ScrollableFrame(parent)
    item = customtkinter.CTkFrame(master=parent_scrollable.scrollable_frame)
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.canvas = CTkCanvas(self, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nswe")
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)

        self.update_canvas_color()

        self.scrollbar = CTkScrollbar(self, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="nswe")

        self.scrollable_frame = CTkFrame(self.canvas, width=60000, height=50000) #scrollable frame is invisible. assuming it was stretched at max, the scroll upwards bug wont happen
        self.scrollable_frame.configure(fg_color='transparent')

        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.update_scrollable_frame_color()

        self._frame_id = self.canvas.create_window(0, 0, window=self.scrollable_frame,)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind("<Configure>", self.resize_frame)  # increase the items inside the canvas as the canvas grows

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.bind('<Enter>', lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind('<Leave>', lambda e: self.canvas.unbind_all('<MouseWheel>'))


    def resize_frame(self, e):
        self.canvas.itemconfig(self._frame_id, height=None,
                               width=e.width)  # height = None because otherwise wont scroll

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # self.canvas.yview_moveto(int(-1 * (event.delta / 120)))

    def get_appearance_mode(self) -> str:
        """ get current state of the appearance mode (light or dark) """
        if AppearanceModeTracker.appearance_mode == 0:
            return "Light"
        elif AppearanceModeTracker.appearance_mode == 1:
            return "Dark"
    def update_canvas_color(self):
        # because for some reason, Ctk canvas do not update automatically
        if self.get_appearance_mode() == "Light":
            self.canvas.configure(bg="#ffffff")
        if self.get_appearance_mode() == "Dark":
            self.canvas.configure(bg="#343638")

    def update_scrollable_frame_color(self):
        if self.get_appearance_mode() == "Light":
            self.scrollable_frame.configure(bg_color="#ffffff")
        if self.get_appearance_mode() == "Dark":
            self.scrollable_frame.configure(bg_color="#343638")
