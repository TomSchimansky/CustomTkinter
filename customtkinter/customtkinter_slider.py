import tkinter
import sys

from .customtkinter_tk import CTk
from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkSlider(tkinter.Frame):
    """ tkinter custom slider, always horizontal """

    def __init__(self, *args,
                 bg_color=None,
                 border_color=None,
                 fg_color="CTkColorManager",
                 progress_color="CTkColorManager",
                 button_color="CTkColorManager",
                 button_hover_color="CTkColorManager",
                 from_=0,
                 to=1,
                 number_of_steps=None,
                 width=160,
                 height=16,
                 border_width=5,
                 command=None,
                 variable=None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        # overwrite configure methods of master when master is tkinter widget, so that bg changes get applied on child CTk widget too
        if isinstance(self.master, (tkinter.Tk, tkinter.Frame)) and not isinstance(self.master, (CTk, CTkFrame)):
            master_old_configure = self.master.config

            def new_configure(*args, **kwargs):
                if "bg" in kwargs:
                    self.configure(bg_color=kwargs["bg"])
                elif "background" in kwargs:
                    self.configure(bg_color=kwargs["background"])

                # args[0] is dict when attribute gets changed by widget[<attribut>] syntax
                elif len(args) > 0 and type(args[0]) == dict:
                    if "bg" in args[0]:
                        self.configure(bg_color=args[0]["bg"])
                    elif "background" in args[0]:
                        self.configure(bg_color=args[0]["background"])
                master_old_configure(*args, **kwargs)

            self.master.config = new_configure
            self.master.configure = new_configure

        AppearanceModeTracker.add(self.change_appearance_mode, self)
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.bg_color = self.detect_color_of_master() if bg_color is None else bg_color
        self.border_color = border_color
        self.fg_color = CTkColorManager.SLIDER_BG if fg_color == "CTkColorManager" else fg_color
        self.progress_color = CTkColorManager.SLIDER_PROGRESS if progress_color == "CTkColorManager" else progress_color
        self.button_color = CTkColorManager.MAIN if button_color == "CTkColorManager" else button_color
        self.button_hover_color = CTkColorManager.MAIN_HOVER if button_hover_color == "CTkColorManager" else button_hover_color

        self.width = width
        self.height = self.calc_optimal_height(height)
        self.border_width = round(border_width)
        self.value = 0.5  # initial value of slider in percent
        self.hover_state = False
        self.from_ = from_
        self.to = to
        self.number_of_steps = number_of_steps
        self.output_value = self.from_ + (self.value * (self.to - self.from_))

        self.callback_function = command
        self.variable: tkinter.Variable = variable
        self.variable_callback_blocked = False
        self.variabel_callback_name = None

        self.configure(width=self.width, height=self.height)
        if sys.platform == "darwin":
            self.configure(cursor="pointinghand")

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthickness=0,
                                     width=self.width,
                                     height=self.height)
        self.canvas.place(x=0, y=0)

        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<B1-Motion>", self.clicked)

        self.draw()  # initial draw

        if self.variable is not None:
            self.variabel_callback_name = self.variable.trace_add("write", self.variable_callback)
            self.variable_callback_blocked = True
            self.set(self.variable.get(), from_variable_callback=True)
            self.variable_callback_blocked = False

    def destroy(self):
        # remove change_appearance_mode function from callback list of AppearanceModeTracker
        AppearanceModeTracker.remove(self.change_appearance_mode)

        # remove variabel_callback from variable callbacks if variable exists
        if self.variable is not None:
            self.variable.trace_remove("write", self.variabel_callback_name)

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

            if self.border_color is None:
                self.canvas.itemconfig("border_parts", fill=CTkColorManager.single_color(self.bg_color, self.appearance_mode))
            else:
                self.canvas.itemconfig("border_parts", fill=CTkColorManager.single_color(self.border_color, self.appearance_mode))

            self.canvas.itemconfig("inner_parts", fill=CTkColorManager.single_color(self.fg_color, self.appearance_mode))

            if self.progress_color is None:
                self.canvas.itemconfig("progress_parts", fill=CTkColorManager.single_color(self.fg_color, self.appearance_mode))
            else:
                self.canvas.itemconfig("progress_parts", fill=CTkColorManager.single_color(self.progress_color, self.appearance_mode))

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

        if self.progress_color != self.fg_color:
            if not self.canvas.find_withtag("progress_parts"):
                self.canvas.create_line((0, 0, 0, 0), tags=("inner_line_progress", "progress_parts"))
                self.canvas.tag_raise("button_parts")
        else:
            self.canvas.delete("progress_parts")

        self.canvas.coords("inner_line_1",
                           (((self.width + coordinate_shift - self.height) * self.value + self.height / 2),
                            self.height / 2,
                            self.width - self.height / 2 + coordinate_shift,
                            self.height / 2))

        if self.progress_color != self.fg_color:
            self.canvas.coords("inner_line_progress",
                               (self.height / 2,
                                self.height / 2,
                                ((self.width + coordinate_shift - self.height) * self.value + self.height / 2),
                                self.height / 2))

        self.canvas.itemconfig("inner_parts",
                               capstyle=tkinter.ROUND,
                               width=self.height - self.border_width * 2 + width_reduced)
        self.canvas.itemconfig("progress_parts",
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
            self.canvas.create_rectangle((0, 0, 0, 0), tags=("inner_rect_2", "inner_parts"), width=0)
            self.canvas.create_oval((0, 0, 0, 0), tags=("inner_oval_2", "inner_parts"), width=0)

        # progress parts
        if not self.canvas.find_withtag("inner_oval_1"):
            self.canvas.delete("inner_oval_1", "inner_rect_1")

            if self.progress_color != self.fg_color:
                self.canvas.create_oval((0, 0, 0, 0), tags=("inner_oval_1", "progress_parts"), width=0)
                self.canvas.create_rectangle((0, 0, 0, 0), tags=("inner_rect_1", "progress_parts"), width=0)
            else:
                self.canvas.create_oval((0, 0, 0, 0), tags=("inner_oval_1", "inner_parts"), width=0)

        if self.progress_color != self.fg_color:
            self.canvas.coords("inner_rect_1", (self.height / 2,
                                                self.border_width,
                                                (self.width - self.height) * self.value + (self.height / 2 + rect_bottom_right_shift),
                                                self.height - self.border_width + rect_bottom_right_shift))
            self.canvas.coords("inner_rect_2", ((self.width - self.height) * self.value + (self.height / 2 + rect_bottom_right_shift),
                                                self.border_width,
                                                self.width - (self.height / 2 + rect_bottom_right_shift),
                                                self.height - self.border_width + rect_bottom_right_shift))
        else:
            self.canvas.coords("inner_rect_2", (self.height/2,
                                                self.border_width,
                                                self.width-(self.height/2 + rect_bottom_right_shift),
                                                self.height-self.border_width + rect_bottom_right_shift))

        self.canvas.coords("inner_oval_1", (self.border_width,
                                            self.border_width,
                                            self.height - self.border_width + oval_bottom_right_shift,
                                            self.height - self.border_width + oval_bottom_right_shift))
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

        self.output_value = self.round_to_step_size(self.from_ + (self.value * (self.to - self.from_)))
        self.value = (self.output_value - self.from_) / (self.to - self.from_)

        self.draw(no_color_updates=True)

        if self.callback_function is not None:
            self.callback_function(self.output_value)

        if self.variable is not None:
            self.variable_callback_blocked = True
            self.variable.set(round(self.output_value) if isinstance(self.variable, tkinter.IntVar) else self.output_value)
            self.variable_callback_blocked = False

    def on_enter(self, event=0):
        self.hover_state = True
        self.canvas.itemconfig("button_parts", fill=CTkColorManager.single_color(self.button_hover_color, self.appearance_mode))

    def on_leave(self, event=0):
        self.hover_state = False
        self.canvas.itemconfig("button_parts", fill=CTkColorManager.single_color(self.button_color, self.appearance_mode))

    def round_to_step_size(self, value):
        if self.number_of_steps is not None:
            step_size = (self.to - self.from_) / self.number_of_steps
            value = self.to - (round((self.to - value) / step_size) * step_size)
            return value
        else:
            return value

    def get(self):
        return self.output_value

    def set(self, output_value, from_variable_callback=False):
        if output_value > self.to:
            output_value = self.to
        elif output_value < self.from_:
            output_value = self.from_

        self.output_value = self.round_to_step_size(output_value)
        self.value = (self.output_value - self.from_) / (self.to - self.from_)

        self.draw(no_color_updates=True)

        if self.callback_function is not None:
            self.callback_function(self.output_value)

        if self.variable is not None and not from_variable_callback:
            self.variable_callback_blocked = True
            self.variable.set(round(self.output_value) if isinstance(self.variable, tkinter.IntVar) else self.output_value)
            self.variable_callback_blocked = False

    def variable_callback(self, var_name, index, mode):
        if not self.variable_callback_blocked:
            self.set(self.variable.get(), from_variable_callback=True)

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            require_redraw = True
            del kwargs["fg_color"]

        if "bg_color" in kwargs:
            if kwargs["bg_color"] is None:
                self.bg_color = self.detect_color_of_master()
            else:
                self.bg_color = kwargs["bg_color"]
            require_redraw = True
            del kwargs["bg_color"]

        if "progress_color" in kwargs:
            if kwargs["progress_color"] is None:
                self.progress_color = self.fg_color
            else:
                self.progress_color = kwargs["progress_color"]
            require_redraw = True
            del kwargs["progress_color"]

        if "button_color" in kwargs:
            self.button_color = kwargs["button_color"]
            require_redraw = True
            del kwargs["button_color"]

        if "button_hover_color" in kwargs:
            self.button_hover_color = kwargs["button_hover_color"]
            require_redraw = True
            del kwargs["button_hover_color"]

        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
            require_redraw = True
            del kwargs["border_color"]

        if "border_width" in kwargs:
            self.border_width = kwargs["border_width"]
            require_redraw = True
            del kwargs["border_width"]

        if "from_" in kwargs:
            self.from_ = kwargs["from_"]
            del kwargs["from_"]

        if "to" in kwargs:
            self.to = kwargs["to"]
            del kwargs["to"]

        if "number_of_steps" in kwargs:
            self.number_of_steps = kwargs["number_of_steps"]
            del kwargs["number_of_steps"]

        if "command" in kwargs:
            self.callback_function = kwargs["command"]
            del kwargs["command"]

        if "variable" in kwargs:
            if self.variable is not None:
                self.variable.trace_remove("write", self.variabel_callback_name)

            self.variable = kwargs["variable"]

            if self.variable is not None and self.variable != "":
                self.variabel_callback_name = self.variable.trace_add("write", self.variable_callback)
                self.set(self.variable.get(), from_variable_callback=True)
            else:
                self.variable = None

            del kwargs["variable"]

        super().configure(*args, **kwargs)

        if require_redraw:
            self.draw()

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
