import sys
import tkinter

from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkProgressBar(tkinter.Frame):
    """ tkinter custom progressbar, always horizontal, values are from 0 to 1 """

    def __init__(self,
                 bg_color=None,
                 border_color=CTkColorManager.PROGRESS_BG,
                 fg_color=CTkColorManager.PROGRESS_BG,
                 progress_color=CTkColorManager.MAIN,
                 width=160,
                 height=10,
                 border_width=0,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        AppearanceModeTracker.add(self.change_appearance_mode)
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.bg_color = self.detect_color_of_master() if bg_color is None else bg_color
        self.border_color = border_color
        self.fg_color = fg_color
        self.progress_color = CTkColorManager.MAIN if progress_color is None else progress_color

        self.width = width
        self.height = self.calc_optimal_height(height)
        self.border_width = round(border_width)
        self.value = 0.5

        self.configure(width=self.width, height=self.height)

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     width=self.width,
                                     height=self.height)
        self.canvas.place(x=0, y=0)

        self.draw()

        # set progress
        self.set(self.value)

    def destroy(self):
        AppearanceModeTracker.remove(self.change_appearance_mode)
        super().destroy()

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
            self.canvas.itemconfig("border_parts", fill=CTkColorManager.single_color(self.border_color, self.appearance_mode))
            self.canvas.itemconfig("inner_parts", fill=CTkColorManager.single_color(self.fg_color, self.appearance_mode))
            self.canvas.itemconfig("progress_parts", fill=CTkColorManager.single_color(self.progress_color, self.appearance_mode))

    def draw_with_polygon_shapes(self):
        """ draw the progress bar parts with just three polygons that have a rounded border """

        coordinate_shift = -1
        width_reduced = -1

        # create border button parts (only if border exists)
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

        # progress parts
        if not self.canvas.find_withtag("progress_parts"):
            self.canvas.create_line((0, 0, 0, 0), tags=("progress_line_1", "progress_parts"))

        self.canvas.coords("progress_line_1",
                           (self.height / 2,
                            self.height / 2,
                            self.height / 2 + (self.width + coordinate_shift - self.height) * self.value,
                            self.height / 2))
        self.canvas.itemconfig("progress_line_1",
                               capstyle=tkinter.ROUND,
                               width=self.height - self.border_width * 2 + width_reduced)

    def draw_with_ovals_and_rects(self):
        """ draw the progress bar parts with ovals and rectangles """

        if sys.platform == "darwin":
            oval_bottom_right_shift = 0
            rect_bottom_right_shift = 0
        else:
            # ovals and rects are always rendered too large on Windows and need to be made smaller by -1
            oval_bottom_right_shift = -1
            rect_bottom_right_shift = -0

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
        if not self.canvas.find_withtag("progress_parts"):
            self.canvas.create_oval((0, 0, 0, 0), tags=("progress_oval_1", "progress_parts"), width=0)
            self.canvas.create_rectangle((0, 0, 0, 0), tags=("progress_rect_1", "progress_parts"), width=0)
            self.canvas.create_oval((0, 0, 0, 0), tags=("progress_oval_2", "progress_parts"), width=0)

        self.canvas.coords("progress_oval_1", (self.border_width,
                                               self.border_width,
                                               self.height - self.border_width + oval_bottom_right_shift,
                                               self.height - self.border_width + oval_bottom_right_shift))
        self.canvas.coords("progress_rect_1", (self.height / 2,
                                               self.border_width,
                                               self.height / 2 + (self.width - self.height) * self.value + rect_bottom_right_shift,
                                               self.height - self.border_width + rect_bottom_right_shift))
        self.canvas.coords("progress_oval_2",
                           (self.height / 2 + (self.width - self.height) * self.value - self.height / 2 + self.border_width,
                            self.border_width,
                            self.height / 2 + (self.width - self.height) * self.value + self.height / 2 - self.border_width + oval_bottom_right_shift,
                            self.height - self.border_width + oval_bottom_right_shift))

    def set(self, value):
        self.value = value

        if self.value > 1:
            self.value = 1
        elif self.value < 0:
            self.value = 0

        self.draw(no_color_updates=True)

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
