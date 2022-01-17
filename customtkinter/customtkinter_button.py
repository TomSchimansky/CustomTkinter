import tkinter
import sys

from .customtkinter_tk import CTk
from .customtkinter_frame import CTkFrame
from .appearance_mode_tracker import AppearanceModeTracker
from .customtkinter_color_manager import CTkColorManager


class CTkButton(tkinter.Frame):
    """ tkinter custom button with border, rounded corners and hover effect """

    def __init__(self, *args,
                 bg_color=None,
                 fg_color="CTkColorManager",
                 hover_color="CTkColorManager",
                 border_color=None,
                 border_width=0,
                 command=None,
                 textvariable=None,
                 width=120,
                 height=30,
                 corner_radius=8,
                 text_font=None,
                 text_color="CTkColorManager",
                 text="CTkButton",
                 hover=True,
                 image=None,
                 compound=tkinter.LEFT,
                 state=tkinter.NORMAL,
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

                # args[0] is dict when attribute gets changed by widget[<attribute>] syntax
                elif len(args) > 0 and type(args[0]) == dict:
                    if "bg" in args[0]:
                        self.configure(bg_color=args[0]["bg"])
                    elif "background" in args[0]:
                        self.configure(bg_color=args[0]["background"])
                master_old_configure(*args, **kwargs)

            self.master.config = new_configure
            self.master.configure = new_configure

        AppearanceModeTracker.add(self.set_appearance_mode, self)
        self.appearance_mode = AppearanceModeTracker.get_mode()  # 0: "Light" 1: "Dark"

        self.configure_basic_grid()

        # color variables
        self.bg_color = self.detect_color_of_master() if bg_color is None else bg_color
        self.fg_color = CTkColorManager.MAIN if fg_color == "CTkColorManager" else fg_color
        self.hover_color = CTkColorManager.MAIN_HOVER if hover_color == "CTkColorManager" else hover_color
        self.border_color = border_color

        # shape and size
        self.width = width
        self.height = height
        self.configure(width=self.width, height=self.height)
        self.corner_radius = self.calc_optimal_corner_radius(corner_radius)  # optimise for less artifacts
        self.border_width = round(border_width)  # round border_width (inner parts not centered otherwise)

        if self.corner_radius * 2 > self.height:
            self.corner_radius = self.height / 2
        elif self.corner_radius * 2 > self.width:
            self.corner_radius = self.width / 2

        if self.corner_radius >= self.border_width:
            self.inner_corner_radius = self.corner_radius - self.border_width
        else:
            self.inner_corner_radius = 0

        # text and font and image
        self.image = image
        self.image_label = None
        self.text = text
        self.text_label = None
        self.text_color = CTkColorManager.TEXT if text_color == "CTkColorManager" else text_color
        if text_font is None:
            if sys.platform == "darwin":  # macOS
                self.text_font = ("Avenir", 13)
            elif "win" in sys.platform:  # Windows
                self.text_font = ("Century Gothic", 11)
            else:
                self.text_font = "TkDefaultFont"
        else:
            self.text_font = text_font

        # callback and hover functionality
        self.function = command
        self.textvariable = textvariable
        self.state = state
        self.hover = hover
        self.compound = compound
        self.click_animation_running = False

        if sys.platform == "darwin" and self.function is not None:
            self.configure(cursor="pointinghand")  # other cursor when hovering over button with command

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     width=self.width,
                                     height=self.height)
        self.canvas.grid(row=0, column=0, rowspan=2, columnspan=2)

        # event bindings
        if self.hover is True:
            self.canvas.bind("<Enter>", self.on_enter)
            self.canvas.bind("<Leave>", self.on_leave)

        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<Button-1>", self.clicked)

        # Each time an item is resized due to pack position mode, the binding Configure is called on the widget
        self.bind('<Configure>', self.update_dimensions)

        self.draw()  # initial draw

    def destroy(self):
        AppearanceModeTracker.remove(self.set_appearance_mode)
        super().destroy()

    def configure_basic_grid(self):
        # Configuration of a basic grid (2x2) in which all elements of CTkButtons are centered on one row and one column
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def update_dimensions(self, event):
        # only redraw if dimensions changed (for performance)
        if self.width != event.width or self.height != event.height:
            self.width = event.width
            self.height = event.height

            self.canvas.config(width=self.width, height=self.height)
            self.draw(no_color_updates=True)  # fast drawing without color changes

    def detect_color_of_master(self):
        if isinstance(self.master, CTkFrame):
            return self.master.fg_color
        else:
            return self.master.cget("bg")

    @staticmethod
    def calc_optimal_corner_radius(user_corner_radius):
        if sys.platform == "darwin":
            return user_corner_radius  # on macOS just use given value (canvas has Antialiasing)
        else:
            user_corner_radius = 0.5 * round(user_corner_radius / 0.5)  # round to 0.5 steps

            # make sure the value is always with .5 at the end for smoother corners
            if user_corner_radius == 0:
                return 0
            elif user_corner_radius % 1 == 0:
                return user_corner_radius + 0.5
            else:
                return user_corner_radius

    def draw(self, no_color_updates=False):
        self.canvas.configure(bg=CTkColorManager.single_color(self.bg_color, self.appearance_mode))

        # decide the drawing method
        if sys.platform == "darwin":
            # on macOS draw button with polygons (positions are more accurate, macOS has Antialiasing)
            self.draw_with_polygon_shapes()
        else:
            # on Windows and other draw with ovals (corner_radius can be optimised to look better than with polygons)
            self.draw_with_ovals_and_rects()

        if no_color_updates is False:

            # set color for the button border parts (outline)
            self.canvas.itemconfig("border_parts",
                                   outline=CTkColorManager.single_color(self.border_color, self.appearance_mode),
                                   fill=CTkColorManager.single_color(self.border_color, self.appearance_mode))

            # set color for inner button parts (depends on button state)
            if self.state == tkinter.DISABLED:
                if self.fg_color is None:
                    self.canvas.itemconfig("inner_parts",
                                           outline=CTkColorManager.darken_hex_color(CTkColorManager.single_color(self.bg_color, self.appearance_mode)),
                                           fill=CTkColorManager.darken_hex_color(CTkColorManager.single_color(self.bg_color, self.appearance_mode)))
                else:
                    self.canvas.itemconfig("inner_parts",
                                           outline=CTkColorManager.darken_hex_color(
                                                   CTkColorManager.single_color(self.fg_color, self.appearance_mode)),
                                           fill=CTkColorManager.darken_hex_color(
                                                   CTkColorManager.single_color(self.fg_color, self.appearance_mode)))

            else:
                if self.fg_color is None:
                    self.canvas.itemconfig("inner_parts",
                                           outline=CTkColorManager.single_color(self.bg_color, self.appearance_mode),
                                           fill=CTkColorManager.single_color(self.bg_color, self.appearance_mode))
                else:
                    self.canvas.itemconfig("inner_parts",
                                           outline=CTkColorManager.single_color(self.fg_color, self.appearance_mode),
                                           fill=CTkColorManager.single_color(self.fg_color, self.appearance_mode))

        # create text label if text given
        if self.text is not None and self.text != "":

            if self.text_label is None:
                self.text_label = tkinter.Label(master=self, font=self.text_font, textvariable=self.textvariable)

                self.text_label.bind("<Enter>", self.on_enter)
                self.text_label.bind("<Leave>", self.on_leave)
                self.text_label.bind("<Button-1>", self.clicked)
                self.text_label.bind("<Button-1>", self.clicked)

            if no_color_updates is False:
                # set text_label fg color (text color)
                self.text_label.configure(fg=CTkColorManager.single_color(self.text_color, self.appearance_mode))

                # set text_label bg color (label color)
                if self.state == tkinter.DISABLED:
                    if self.fg_color is None:
                        self.text_label.configure(
                                bg=CTkColorManager.darken_hex_color(CTkColorManager.single_color(self.bg_color, self.appearance_mode)))
                    else:
                        self.text_label.configure(
                                bg=CTkColorManager.darken_hex_color(CTkColorManager.single_color(self.fg_color, self.appearance_mode)))
                else:
                    if self.fg_color is None:
                        self.text_label.configure(bg=CTkColorManager.single_color(self.bg_color, self.appearance_mode))
                    else:
                        self.text_label.configure(bg=CTkColorManager.single_color(self.fg_color, self.appearance_mode))

            self.text_label.configure(text=self.text)  # set text

        else:
            # delete text_label if no text given
            if self.text_label is not None:
                self.text_label.destroy()
                self.text_label = None

        # create image label if image given
        if self.image is not None:

            if self.image_label is None:
                self.image_label = tkinter.Label(master=self)

                self.image_label.bind("<Enter>", self.on_enter)
                self.image_label.bind("<Leave>", self.on_leave)
                self.image_label.bind("<Button-1>", self.clicked)
                self.image_label.bind("<Button-1>", self.clicked)

            if no_color_updates is False:
                # set image_label bg color (background color of label)
                if self.state == tkinter.DISABLED:
                    self.image_label.configure(bg=CTkColorManager.darken_hex_color(CTkColorManager.single_color(self.fg_color, self.appearance_mode)))
                else:
                    self.image_label.configure(bg=CTkColorManager.single_color(self.fg_color, self.appearance_mode))

            self.image_label.configure(image=self.image)  # set image

        else:
            # delete text_label if no text given
            if self.image_label is not None:
                self.image_label.destroy()
                self.image_label = None

        # create grid layout with just an image given
        if self.image_label is not None and self.text_label is None:
            self.image_label.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="")

        # create grid layout with just text given
        if self.image_label is None and self.text_label is not None:
            self.text_label.grid(row=0, column=0, padx=self.corner_radius, pady=self.border_width, rowspan=2, columnspan=2, sticky="")

        # create grid layout of image and text label in 2x2 grid system with given compound
        if self.image_label is not None and self.text_label is not None:
            if self.compound == tkinter.LEFT or self.compound == "left":
                self.image_label.grid(row=0, column=0, padx=self.corner_radius, sticky="e", rowspan=2, columnspan=1)
                self.text_label.grid(row=0, column=1, padx=self.corner_radius, sticky="w", rowspan=2, columnspan=1, pady=self.border_width)
            elif self.compound == tkinter.TOP or self.compound == "top":
                self.image_label.grid(row=0, column=0, padx=self.corner_radius, sticky="s", columnspan=2, rowspan=1)
                self.text_label.grid(row=1, column=0, padx=self.corner_radius, sticky="n", columnspan=2, rowspan=1, pady=self.border_width)
            elif self.compound == tkinter.RIGHT or self.compound == "right":
                self.image_label.grid(row=0, column=1, padx=self.corner_radius, sticky="w", rowspan=2, columnspan=1)
                self.text_label.grid(row=0, column=0, padx=self.corner_radius, sticky="e", rowspan=2, columnspan=1, pady=self.border_width)
            elif self.compound == tkinter.BOTTOM or self.compound == "bottom":
                self.image_label.grid(row=1, column=0, padx=self.corner_radius, sticky="n", columnspan=2, rowspan=1)
                self.text_label.grid(row=0, column=0, padx=self.corner_radius, sticky="s", columnspan=2, rowspan=1, pady=self.border_width)

    def draw_with_polygon_shapes(self):
        """ draw the button parts with just two polygons that have a rounded border """

        # create border button parts (only if border exists)
        if self.border_width > 0:
            if not self.canvas.find_withtag("border_parts"):
                self.canvas.create_polygon((0, 0, 0, 0), tags=("border_line_1", "border_parts"))

            self.canvas.coords("border_line_1",
                               (self.corner_radius,
                                self.corner_radius,
                                self.width - self.corner_radius,
                                self.corner_radius,
                                self.width - self.corner_radius,
                                self.height - self.corner_radius,
                                self.corner_radius,
                                self.height - self.corner_radius))
            self.canvas.itemconfig("border_line_1",
                                   joinstyle=tkinter.ROUND,
                                   width=self.corner_radius * 2)

        # create inner button parts
        if not self.canvas.find_withtag("inner_parts"):
            self.canvas.create_polygon((0, 0, 0, 0), tags=("inner_line_1", "inner_parts"))

        if self.corner_radius <= self.border_width:
            bottom_right_shift = -1  # weird canvas rendering inaccuracy that has to be corrected in some cases
        else:
            bottom_right_shift = 0

        self.canvas.coords("inner_line_1",
                           (self.border_width + self.inner_corner_radius,
                            self.border_width + self.inner_corner_radius,
                            self.width - (self.border_width + self.inner_corner_radius) + bottom_right_shift,
                            self.border_width + self.inner_corner_radius,
                            self.width - (self.border_width + self.inner_corner_radius) + bottom_right_shift,
                            self.height - (self.border_width + self.inner_corner_radius) + bottom_right_shift,
                            self.border_width + self.inner_corner_radius,
                            self.height - (self.border_width + self.inner_corner_radius) + bottom_right_shift))
        self.canvas.itemconfig("inner_line_1",
                               joinstyle=tkinter.ROUND,
                               width=self.inner_corner_radius * 2)

    def draw_with_ovals_and_rects(self):
        """ draw the button parts with ovals at the corner and rectangles in the middle """

        if sys.platform == "darwin":
            oval_bottom_right_shift = 0
            rect_bottom_right_shift = 0
        else:
            # ovals and rects are always rendered too large on Windows and need to be made smaller by -1
            oval_bottom_right_shift = -1
            rect_bottom_right_shift = -1

        # create border button parts
        if self.border_width > 0:
            if self.corner_radius > 0:
                # create canvas border corner parts if not already created
                if not self.canvas.find_withtag("border_oval_1"):
                    self.canvas.create_oval(0, 0, 0, 0, tags=("border_oval_1", "border_corner_part", "border_parts"))
                    self.canvas.create_oval(0, 0, 0, 0, tags=("border_oval_2", "border_corner_part", "border_parts"))
                    self.canvas.create_oval(0, 0, 0, 0, tags=("border_oval_3", "border_corner_part", "border_parts"))
                    self.canvas.create_oval(0, 0, 0, 0, tags=("border_oval_4", "border_corner_part", "border_parts"))

                # change position of border corner parts
                self.canvas.coords("border_oval_1", (0,
                                                     0,
                                                     self.corner_radius * 2 + oval_bottom_right_shift,
                                                     self.corner_radius * 2 + oval_bottom_right_shift))
                self.canvas.coords("border_oval_2", (self.width - self.corner_radius * 2,
                                                     0,
                                                     self.width + oval_bottom_right_shift,
                                                     self.corner_radius * 2 + oval_bottom_right_shift))
                self.canvas.coords("border_oval_3", (0,
                                                     self.height - self.corner_radius * 2,
                                                     self.corner_radius * 2 + oval_bottom_right_shift,
                                                     self.height + oval_bottom_right_shift))
                self.canvas.coords("border_oval_4", (self.width - self.corner_radius * 2,
                                                     self.height - self.corner_radius * 2,
                                                     self.width + oval_bottom_right_shift,
                                                     self.height + oval_bottom_right_shift))
            else:
                self.canvas.delete("border_corner_part")  # delete border corner parts if not needed

            # create canvas border rectangle parts if not already created
            if not self.canvas.find_withtag("border_rectangle_1"):
                self.canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_1", "border_rectangle_part", "border_parts"))
                self.canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_2", "border_rectangle_part", "border_parts"))

            # change position of border rectangle parts
            self.canvas.coords("border_rectangle_1", (0,
                                                      self.corner_radius,
                                                      self.width + rect_bottom_right_shift,
                                                      self.height - self.corner_radius + rect_bottom_right_shift))
            self.canvas.coords("border_rectangle_2", (self.corner_radius,
                                                      0,
                                                      self.width - self.corner_radius + rect_bottom_right_shift,
                                                      self.height + rect_bottom_right_shift))

        # create inner button parts
        if self.inner_corner_radius > 0:

            # create canvas border corner parts if not already created
            if not self.canvas.find_withtag("inner_corner_part"):
                self.canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_1", "inner_corner_part", "inner_parts"))
                self.canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_2", "inner_corner_part", "inner_parts"))
                self.canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_3", "inner_corner_part", "inner_parts"))
                self.canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_4", "inner_corner_part", "inner_parts"))

            # change position of border corner parts
            self.canvas.coords("inner_oval_1", (self.border_width,
                                                self.border_width,
                                                self.border_width + self.inner_corner_radius * 2 + oval_bottom_right_shift,
                                                self.border_width + self.inner_corner_radius * 2 + oval_bottom_right_shift))
            self.canvas.coords("inner_oval_2", (self.width - self.border_width - self.inner_corner_radius * 2,
                                                self.border_width,
                                                self.width - self.border_width + oval_bottom_right_shift,
                                                self.border_width + self.inner_corner_radius * 2 + oval_bottom_right_shift))
            self.canvas.coords("inner_oval_3", (self.border_width,
                                                self.height - self.border_width - self.inner_corner_radius * 2,
                                                self.border_width + self.inner_corner_radius * 2 + oval_bottom_right_shift,
                                                self.height - self.border_width + oval_bottom_right_shift))
            self.canvas.coords("inner_oval_4", (self.width - self.border_width - self.inner_corner_radius * 2,
                                                self.height - self.border_width - self.inner_corner_radius * 2,
                                                self.width - self.border_width + oval_bottom_right_shift,
                                                self.height - self.border_width + oval_bottom_right_shift))
        else:
            self.canvas.delete("inner_corner_part")  # delete inner corner parts if not needed

        # create canvas inner rectangle parts if not already created
        if not self.canvas.find_withtag("inner_rectangle_part"):
            self.canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_1", "inner_rectangle_part", "inner_parts"))
            self.canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_2", "inner_rectangle_part", "inner_parts"))

        # change position of inner rectangle parts
        self.canvas.coords("inner_rectangle_1", (self.border_width + self.inner_corner_radius,
                                                 self.border_width,
                                                 self.width - self.border_width - self.inner_corner_radius + rect_bottom_right_shift,
                                                 self.height - self.border_width + rect_bottom_right_shift))
        self.canvas.coords("inner_rectangle_2", (self.border_width,
                                                 self.border_width + self.inner_corner_radius,
                                                 self.width - self.border_width + rect_bottom_right_shift,
                                                 self.height - self.inner_corner_radius - self.border_width + rect_bottom_right_shift))

    def config(self, *args, **kwargs):
        self.configure(*args, **kwargs)

    def configure(self, *args, **kwargs):
        require_redraw = False  # some attribute changes require a call of self.draw() at the end

        if "text" in kwargs:
            self.set_text(kwargs["text"])
            del kwargs["text"]

        if "state" in kwargs:
            self.set_state(kwargs["state"])
            del kwargs["state"]

        if "image" in kwargs:
            self.set_image(kwargs["image"])
            del kwargs["image"]

        if "compound" in kwargs:
            self.compound = kwargs["compound"]
            require_redraw = True
            del kwargs["compound"]

        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            require_redraw = True
            del kwargs["fg_color"]

        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
            require_redraw = True
            del kwargs["border_color"]

        if "bg_color" in kwargs:
            if kwargs["bg_color"] is None:
                self.bg_color = self.detect_color_of_master()
            else:
                self.bg_color = kwargs["bg_color"]
            require_redraw = True
            del kwargs["bg_color"]

        if "hover_color" in kwargs:
            self.hover_color = kwargs["hover_color"]
            require_redraw = True
            del kwargs["hover_color"]

        if "text_color" in kwargs:
            self.text_color = kwargs["text_color"]
            require_redraw = True
            del kwargs["text_color"]

        if "command" in kwargs:
            self.function = kwargs["command"]
            del kwargs["command"]

        if "textvariable" in kwargs:
            self.textvariable = kwargs["textvariable"]
            if self.text_label is not None:
                self.text_label.configure(textvariable=self.textvariable)
            del kwargs["textvariable"]

        super().configure(*args, **kwargs)

        if require_redraw:
            self.draw()

    def set_state(self, state):
        self.state = state

        if self.state == tkinter.DISABLED:
            self.hover = False
            if sys.platform == "darwin" and self.function is not None:
                self.configure(cursor="arrow")

        elif self.state == tkinter.NORMAL:
            self.hover = True
            if sys.platform == "darwin" and self.function is not None:
                self.configure(cursor="pointinghand")

        self.draw()

    def set_text(self, text):
        self.text = text
        self.draw()

    def set_image(self, image):
        self.image = image
        self.draw()

    def on_enter(self, event=0):
        if self.hover is True:
            if self.hover_color is None:
                inner_parts_color = self.fg_color
            else:
                inner_parts_color = self.hover_color

            # set color of inner button parts to hover color
            self.canvas.itemconfig("inner_parts",
                                   outline=CTkColorManager.single_color(inner_parts_color, self.appearance_mode),
                                   fill=CTkColorManager.single_color(inner_parts_color, self.appearance_mode))

            # set text_label bg color to button hover color
            if self.text_label is not None:
                self.text_label.configure(bg=CTkColorManager.single_color(inner_parts_color, self.appearance_mode))

            # set image_label bg color to button hover color
            if self.image_label is not None:
                self.image_label.configure(bg=CTkColorManager.single_color(inner_parts_color, self.appearance_mode))

    def on_leave(self, event=0):
        self.click_animation_running = False

        if self.hover is True:
            if self.fg_color is None:
                inner_parts_color = self.bg_color
            else:
                inner_parts_color = self.fg_color

            # set color of inner button parts
            self.canvas.itemconfig("inner_parts",
                                   outline=CTkColorManager.single_color(inner_parts_color, self.appearance_mode),
                                   fill=CTkColorManager.single_color(inner_parts_color, self.appearance_mode))

            # set text_label bg color (label color)
            if self.text_label is not None:
                self.text_label.configure(bg=CTkColorManager.single_color(inner_parts_color, self.appearance_mode))

            # set image_label bg color (image bg color)
            if self.image_label is not None:
                self.image_label.configure(bg=CTkColorManager.single_color(inner_parts_color, self.appearance_mode))

    def click_animation(self):
        if self.click_animation_running:
            self.on_enter()

    def clicked(self, event=0):
        if self.function is not None:
            if self.state is not tkinter.DISABLED:

                # click animation: change color with .on_leave() and back to normal after 100ms with click_animation()
                self.on_leave()
                self.click_animation_running = True
                self.after(100, self.click_animation)

                self.function()

    def set_appearance_mode(self, mode_string):
        if mode_string.lower() == "dark":
            self.appearance_mode = 1
        elif mode_string.lower() == "light":
            self.appearance_mode = 0

        if isinstance(self.master, (CTkFrame, CTk)):
            self.bg_color = self.master.fg_color
        else:
            self.bg_color = self.master.cget("bg")

        self.draw()
