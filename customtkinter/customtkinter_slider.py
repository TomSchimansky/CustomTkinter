import tkinter
import sys

from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkSlider(tkinter.Frame):
    """ tkinter custom slider, always horizontal """

    def __init__(self,
                 bg_color=None,
                 border_color=None,
                 fg_color=CTkColorManager.SLIDER_BG,
                 button_color=CTkColorManager.MAIN,
                 button_hover_color=CTkColorManager.MAIN_HOVER,
                 from_=0,
                 to=1,
                 width=160,
                 height=16,
                 border_width=5,
                 command=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        AppearanceModeTracker.add(self.change_appearance_mode)
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.bg_color = self.detect_color_of_master() if bg_color is None else bg_color
        self.border_color = self.bg_color if border_color is None else border_color
        self.fg_color = fg_color
        self.button_color = self.bg_color if button_color is None else button_color
        self.button_hover_color = self.bg_color if button_hover_color is None else button_hover_color

        self.width = width
        self.height = self.calc_optimal_height(height)
        self.border_width = round(border_width)
        self.callback_function = command
        self.value = 0.5  # initial value of slider in percent
        self.hover_state = False
        self.from_ = from_
        self.to = to
        self.output_value = self.from_ + (self.value * (self.to - self.from_))

        self.configure(width=self.width, height=self.height)
        if sys.platform == "darwin":
            self.configure(cursor="pointinghand")

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     width=self.width,
                                     height=self.height)
        self.canvas.place(x=0, y=0)

        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<B1-Motion>", self.clicked)

        self.draw()

    def detect_color_of_master(self):
        if isinstance(self.master, CTkFrame):
            return self.master.fg_color
        else:
            return self.master.cget("bg")

    @staticmethod
    def calc_optimal_height(user_height):
        if sys.platform == "darwin":
            return user_height  # on macOS just use given value (canvas has Antialiasing)
        else:
            # make sure the value is always with uneven for better rendering of the ovals
            if user_height == 0:
                return 0
            elif user_height % 2 == 0:
                return user_height + 1
            else:
                return user_height

    def draw(self, no_color_updates=False):

        # decide the drawing method
        if sys.platform == "darwin":
            # on macOS draw button with polygons (positions are more accurate, macOS has Antialiasing)
            self.draw_with_polygon_shapes()
        else:
            # on Windows and other draw with ovals (corner_radius can be optimised to look better than with polygons)
            self.draw_with_ovals_and_rects()

        if no_color_updates is False:
            self.canvas.configure(bg=CTkColorManager.single_color(self.bg_color, self.appearance_mode))
            print(self.border_color)
            self.canvas.itemconfig("border_parts", fill=CTkColorManager.single_color(self.border_color, self.appearance_mode))
            self.canvas.itemconfig("inner_parts", fill=CTkColorManager.single_color(self.fg_color, self.appearance_mode))
            self.canvas.itemconfig("button_parts", fill=CTkColorManager.single_color(self.button_color, self.appearance_mode))

    def draw_with_polygon_shapes(self):
        """ draw the slider parts with just three polygons that have a rounded border """

        coordinate_shift = -1
        width_reduced = -1

        # create border parts
        if self.border_width > 0:
            if not self.canvas.find_withtag("border_parts"):
                self.canvas.create_line((0, 0, 0, 0), tags=("border_line_1", "border_parts"))

            self.canvas.coords("border_line_1",
                               (self.height / 2,
                                self.height / 2,
                                self.width - self.height / 2 + coordinate_shift,
                                self.height / 2))
            self.canvas.itemconfig("border_line_1",
                                   capstyle=tkinter.ROUND,
                                   width=self.height + width_reduced)

        # create inner button parts
        if not self.canvas.find_withtag("inner_parts"):
            self.canvas.create_line((0, 0, 0, 0), tags=("inner_line_1", "inner_parts"))

        self.canvas.coords("inner_line_1",
                           (self.height / 2,
                            self.height / 2,
                            self.width - self.height / 2 + coordinate_shift,
                            self.height / 2))
        self.canvas.itemconfig("inner_line_1",
                               capstyle=tkinter.ROUND,
                               width=self.height - self.border_width * 2 + width_reduced)

        # button parts
        if not self.canvas.find_withtag("button_parts"):
            self.canvas.create_line((0, 0, 0, 0), tags=("button_line_1", "button_parts"))

        self.canvas.coords("button_line_1",
                           (self.height / 2 + (self.width + coordinate_shift - self.height) * self.value,
                            self.height / 2,
                            self.height / 2 + (self.width + coordinate_shift - self.height) * self.value,
                            self.height / 2))
        self.canvas.itemconfig("button_line_1",
                               capstyle=tkinter.ROUND,
                               width=self.height + width_reduced)

    def draw_with_ovals_and_rects(self):
        """ draw the progress bar parts with ovals and rectangles """

        # ovals and rects are always rendered too large and need to be made smaller by -1
        oval_bottom_right_shift = -1
        rect_bottom_right_shift = 0

        # frame_border
        if self.border_width > 0:
            if not self.canvas.find_withtag("border_parts"):
                self.canvas.create_oval((0, 0, 0, 0), tags=("border_oval_1", "border_parts"), width=0)
                self.canvas.create_rectangle((0, 0, 0, 0), tags=("border_rect_1", "border_parts"), width=0)
                self.canvas.create_oval((0, 0, 0, 0), tags=("border_oval_2", "border_parts"), width=0)

            self.canvas.coords("border_oval_1", (0,
                                                 0,
                                                 self.height + oval_bottom_right_shift,
                                                 self.height + oval_bottom_right_shift))
            self.canvas.coords("border_rect_1", (self.height/2,
                                                 0,
                                                 self.width-(self.height/2) + rect_bottom_right_shift,
                                                 self.height + rect_bottom_right_shift))
            self.canvas.coords("border_oval_2", (self.width-self.height,
                                                 0,
                                                 self.width + oval_bottom_right_shift,
                                                 self.height + oval_bottom_right_shift))

        # foreground
        if not self.canvas.find_withtag("inner_parts"):
            self.canvas.create_oval((0, 0, 0, 0), tags=("inner_oval_1", "inner_parts"), width=0)
            self.canvas.create_rectangle((0, 0, 0, 0), tags=("inner_rect_1", "inner_parts"), width=0)
            self.canvas.create_oval((0, 0, 0, 0), tags=("inner_oval_2", "inner_parts"), width=0)

        self.canvas.coords("inner_oval_1", (self.border_width,
                                            self.border_width,
                                            self.height-self.border_width + oval_bottom_right_shift,
                                            self.height-self.border_width + oval_bottom_right_shift))
        self.canvas.coords("inner_rect_1", (self.height/2,
                                            self.border_width,
                                            self.width-(self.height/2 + rect_bottom_right_shift),
                                            self.height-self.border_width + rect_bottom_right_shift))
        self.canvas.coords("inner_oval_2", (self.width-self.height+self.border_width,
                                            self.border_width,
                                            self.width-self.border_width + oval_bottom_right_shift,
                                            self.height-self.border_width + oval_bottom_right_shift))

        # progress parts
        if not self.canvas.find_withtag("button_parts"):
            self.canvas.create_oval((0, 0, 0, 0), tags=("button_oval_1", "button_parts"), width=0)

        self.canvas.coords("button_oval_1",
                           ((self.width - self.height) * self.value,
                            0,
                            self.height + (self.width - self.height) * self.value + oval_bottom_right_shift,
                            self.height + oval_bottom_right_shift))

    def clicked(self, event=None):
        self.value = event.x / self.width

        if self.value > 1:
            self.value = 1
        if self.value < 0:
            self.value = 0

        self.output_value = self.from_ + (self.value * (self.to - self.from_))

        self.draw(no_color_updates=True)

        if self.callback_function is not None:
            self.callback_function(self.output_value)

    def on_enter(self, event=0):
        self.hover_state = True
        self.canvas.itemconfig("button_parts", fill=CTkColorManager.single_color(self.button_hover_color, self.appearance_mode))

    def on_leave(self, event=0):
        self.hover_state = False
        self.canvas.itemconfig("button_parts", fill=CTkColorManager.single_color(self.button_color, self.appearance_mode))

    def get(self):
        return self.output_value

    def set(self, output_value):
        self.output_value = output_value
        self.value = (self.output_value - self.from_) / (self.to - self.from_)

        self.draw(no_color_updates=True)

        if self.callback_function is not None:
            self.callback_function(self.output_value)

    def change_appearance_mode(self, mode_string):
        if mode_string.lower() == "dark":
            self.appearance_mode = 1
        elif mode_string.lower() == "light":
            self.appearance_mode = 0

        if isinstance(self.master, CTkFrame):
            self.bg_color = self.master.fg_color
        else:
            self.bg_color = self.master.cget("bg")

        self.draw()

