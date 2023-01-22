from .widgets.theme.theme_manager import ThemeManager
from .ctk_toplevel import CTkToplevel
from .widgets.ctk_label import CTkLabel
from .widgets.appearance_mode.appearance_mode_tracker import AppearanceModeTracker
from typing import Union, Tuple


class CTkTooltip(CTkToplevel):
    # Mouse hover tooltips that can be attached to widgets
    def __init__(self, master,
                 text: str = 'CTk Tooltip',
                 delay: int = 500,
                 wrap_length: int = -1,
                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Union[str, Tuple[str, str]] = "default",
                 mouse_offset: Tuple[int, int] = (1, 1),
                 **kwargs):
        self.wait_time = delay  # milliseconds until tooltip appears
        self.wrap_length = wrap_length  # wrap length of the tooltip text
        self.master = master  # parent widget
        self.text = text  # text to display
        self.mouse_offset = mouse_offset  # offset from mouse position (x, y)
        self.master.bind("<Enter>", self._schedule, add="+")
        self.master.bind("<Leave>", self._leave, add="+")
        self.master.bind("<ButtonPress>", self._leave, add="+")
        self._id = None
        self.kwargs = kwargs
        self._visible = False

        # determine colors
        self.fg_color = ThemeManager.theme["CTkFrame"]["top_fg_color"] if fg_color == "default" else fg_color
        if bg_color == "transparent":
            if bg_color.startswith('#'):
                color_list = [int(fg_color[i:i + 2], 16) for i in range(1, len(fg_color), 2)]
                if not any(color == 255 for color in color_list):
                    for i in range(len(color_list)):
                        color_list[i] += 1
                else:
                    for i in range(len(color_list)):
                        color_list[i] -= 1

                self.bg_color = "#" + ''.join(['{:02x}'.format(x) for x in color_list])
            else:
                self.__appearance_mode = AppearanceModeTracker.get_mode()
                if self.__appearance_mode == 0:
                    self.bg_color = 'gray86' if self.fg_color != 'gray86' else 'gray84'
                else:
                    self.bg_color = 'gray17' if self.fg_color != 'gray17' else 'gray15'
        else:
            self.bg_color = bg_color

    def _leave(self, event=None):
        self._unschedule()
        if self._visible: self.hide()
        self._visible = False

    def _schedule(self, event=None):
        self._id = self.master.after(self.wait_time, self.show)

    def _unschedule(self):
        # Unschedule scheduled popups
        id = self._id
        self._id = None
        if id:
            self.master.after_cancel(id)

    def show(self, event=None):
        # Get the position the tooltip needs to appear at
        super().__init__(self.master)
        self._visible = True
        x = y = 0
        x, y, cx, cy = self.master.bbox("insert")
        # Has to be offset from mouse position, otherwise it will appear and disappear instantly because it left the parent widget
        x += self.master.winfo_pointerx() + self.mouse_offset[0]
        y += self.master.winfo_pointery() + self.mouse_offset[1]
        self.wm_attributes("-toolwindow", True)
        self.wm_overrideredirect(True)
        self.wm_geometry(f'+{x}+{y}')
        self.wm_attributes('-transparentcolor', self.bg_color)
        super().configure(bg_color=self.bg_color)
        label = CTkLabel(self, text=self.text, corner_radius=10, bg_color=self.bg_color, fg_color=self.fg_color, width=1, wraplength=self.wrap_length, **self.kwargs)
        label.pack()

    def hide(self):
        self._unschedule()
        self.withdraw()

    def configure(self, **kwargs):
        # Change attributes of the tooltip, and redraw if necessary
        require_redraw = False
        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            require_redraw = True
            del kwargs["fg_color"]
        if "bg_color" in kwargs:
            self.bg_color = kwargs["bg_color"]
            require_redraw = True
            del kwargs["bg_color"]
        if "text" in kwargs:
            self.text = kwargs["text"]
            require_redraw = True
            del kwargs["text"]
        if "delay" in kwargs:
            self.wait_time = kwargs["delay"]
            del kwargs["delay"]
        if "wrap_length" in kwargs:
            self.wrap_length = kwargs["wrap_length"]
            require_redraw = True
            del kwargs["wrap_length"]
        if "mouse_offset" in kwargs:
            self.mouse_offset = kwargs["mouse_offset"]
            require_redraw = True
            del kwargs["mouse_offset"]
        super().configure(**kwargs)
        if require_redraw:
            self.hide()
            self.show()
