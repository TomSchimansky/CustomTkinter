import tkinter
from typing import Union
from .customtkinter_canvas import CTkCanvas


class DrawEngine:
    def __init__(self, canvas: CTkCanvas, rendering_method: str):
        self.canvas = canvas
        self.rendering_method = rendering_method

    def calc_optimal_corner_radius(self, user_corner_radius: Union[float, int]) -> Union[float, int]:
        # optimize for drawing with polygon shapes
        if self.rendering_method == "polygon_shapes":
            return user_corner_radius

        # optimize forx drawing with antialiased font shapes
        elif self.rendering_method == "font_shapes":
            return round(user_corner_radius)

        # optimize for drawing with circles and rects
        elif self.rendering_method == "circle_shapes":
            user_corner_radius = 0.5 * round(user_corner_radius / 0.5)  # round to 0.5 steps

            # make sure the value is always with .5 at the end for smoother corners
            if user_corner_radius == 0:
                return 0
            elif user_corner_radius % 1 == 0:
                return user_corner_radius + 0.5
            else:
                return user_corner_radius

    def draw_rounded_rect_with_border(self, width: int, height: int, corner_radius: Union[float, int], border_width: Union[float, int]) -> bool:
        """ returns bool if recoloring is necessary """

        border_width = round(border_width)
        corner_radius = self.calc_optimal_corner_radius(corner_radius)  # optimize corner_radius for different drawing methods (different rounding)

        if corner_radius >= border_width:
            inner_corner_radius = corner_radius - border_width
        else:
            inner_corner_radius = 0

        if self.rendering_method == "polygon_shapes":
            return self._draw_rounded_rect_with_border_polygon_shapes(width, height, corner_radius, border_width, inner_corner_radius)
        elif self.rendering_method == "font_shapes":
            return self._draw_rounded_rect_with_border_font_shapes(width, height, corner_radius, border_width, inner_corner_radius)
        elif self.rendering_method == "circle_shapes":
            return self._draw_rounded_rect_with_border_circle_shapes(width, height, corner_radius, border_width, inner_corner_radius)

    def _draw_rounded_rect_with_border_polygon_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int) -> bool:
        requires_recoloring = False

        # create border button parts (only if border exists)
        if border_width > 0:
            if not self.canvas.find_withtag("border_parts"):
                self.canvas.create_polygon((0, 0, 0, 0), tags=("border_line_1", "border_parts"))
                self.canvas.tag_lower("border_parts")
                requires_recoloring = True

            self.canvas.coords("border_line_1",
                               (corner_radius,
                                corner_radius,
                                width - corner_radius,
                                corner_radius,
                                width - corner_radius,
                                height - corner_radius,
                                corner_radius,
                                height - corner_radius))
            self.canvas.itemconfig("border_line_1",
                                   joinstyle=tkinter.ROUND,
                                   width=corner_radius * 2)

        else:
            self.canvas.delete("border_parts")

        # create inner button parts
        if not self.canvas.find_withtag("inner_parts"):
            self.canvas.create_polygon((0, 0, 0, 0), tags=("inner_line_1", "inner_parts"))
            self.canvas.tag_raise("inner_parts")
            requires_recoloring = True

        if corner_radius <= border_width:
            bottom_right_shift = -1  # weird canvas rendering inaccuracy that has to be corrected in some cases
        else:
            bottom_right_shift = 0

        self.canvas.coords("inner_line_1",
                           (border_width + inner_corner_radius,
                            border_width + inner_corner_radius,
                            width - (border_width + inner_corner_radius) + bottom_right_shift,
                            border_width + inner_corner_radius,
                            width - (border_width + inner_corner_radius) + bottom_right_shift,
                            height - (border_width + inner_corner_radius) + bottom_right_shift,
                            border_width + inner_corner_radius,
                            height - (border_width + inner_corner_radius) + bottom_right_shift))
        self.canvas.itemconfig("inner_line_1",
                               joinstyle=tkinter.ROUND,
                               width=inner_corner_radius * 2)

        return requires_recoloring

    def _draw_rounded_rect_with_border_font_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int) -> bool:
        requires_recoloring = False

        # create border button parts
        if border_width > 0:
            if corner_radius > 0:
                # create canvas border corner parts if not already created
                if not self.canvas.find_withtag("border_oval_1_a"):
                    self.canvas.create_aa_circle(0, 0, 0, tags=("border_oval_1_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
                    self.canvas.create_aa_circle(0, 0, 0, tags=("border_oval_1_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
                    self.canvas.create_aa_circle(0, 0, 0, tags=("border_oval_2_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
                    self.canvas.create_aa_circle(0, 0, 0, tags=("border_oval_2_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
                    self.canvas.tag_lower("border_corner_part")
                    requires_recoloring = True

                if not self.canvas.find_withtag("border_oval_3_a") and round(corner_radius) * 2 < height:
                    self.canvas.create_aa_circle(0, 0, 0, tags=("border_oval_3_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
                    self.canvas.create_aa_circle(0, 0, 0, tags=("border_oval_3_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
                    self.canvas.create_aa_circle(0, 0, 0, tags=("border_oval_4_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
                    self.canvas.create_aa_circle(0, 0, 0, tags=("border_oval_4_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
                    self.canvas.tag_lower("border_corner_part")
                    requires_recoloring = True

                elif self.canvas.find_withtag("border_oval_3_a") and not round(corner_radius) * 2 < height:
                    self.canvas.delete(["border_oval_3_a", "border_oval_3_b", "border_oval_4_a", "border_oval_4_b"])

                # change position of border corner parts
                self.canvas.coords("border_oval_1_a", corner_radius, corner_radius, corner_radius)
                self.canvas.coords("border_oval_1_b", corner_radius, corner_radius, corner_radius)
                self.canvas.coords("border_oval_2_a", width - corner_radius, corner_radius, corner_radius)
                self.canvas.coords("border_oval_2_b", width - corner_radius, corner_radius, corner_radius)
                self.canvas.coords("border_oval_3_a", width - corner_radius, height - corner_radius, corner_radius)
                self.canvas.coords("border_oval_3_b", width - corner_radius, height - corner_radius, corner_radius)
                self.canvas.coords("border_oval_4_a", corner_radius, height - corner_radius, corner_radius)
                self.canvas.coords("border_oval_4_b", corner_radius, height - corner_radius, corner_radius)

            else:
                self.canvas.delete("border_corner_part")  # delete border corner parts if not needed

            # create canvas border rectangle parts if not already created
            if not self.canvas.find_withtag("border_rectangle_1"):
                self.canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_1", "border_rectangle_part", "border_parts"), width=0)
                self.canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_2", "border_rectangle_part", "border_parts"), width=0)
                self.canvas.tag_lower("border_rectangle_part")
                requires_recoloring = True

            # change position of border rectangle parts
            self.canvas.coords("border_rectangle_1", (0, corner_radius, width, height - corner_radius))
            self.canvas.coords("border_rectangle_2", (corner_radius, 0, width - corner_radius, height))

        else:
            self.canvas.delete("border_parts")

        # create inner button parts
        if inner_corner_radius > 0:

            # create canvas border corner parts if not already created
            if not self.canvas.find_withtag("inner_oval_1_a"):
                self.canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_1_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
                self.canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_1_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
                self.canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_2_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
                self.canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_2_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
                self.canvas.tag_raise("inner_corner_part")
                requires_recoloring = True

            if not self.canvas.find_withtag("inner_oval_3_a") and round(inner_corner_radius) * 2 < height - (2 * border_width):
                self.canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_3_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
                self.canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_3_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
                self.canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_4_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
                self.canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_4_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
                self.canvas.tag_raise("inner_corner_part")
                requires_recoloring = True

            elif self.canvas.find_withtag("inner_oval_3_a") and not round(inner_corner_radius) * 2 < height - (2 * border_width):
                self.canvas.delete(["inner_oval_3_a", "inner_oval_3_b", "inner_oval_4_a", "inner_oval_4_b"])

            # change position of border corner parts
            self.canvas.coords("inner_oval_1_a", border_width + inner_corner_radius, border_width + inner_corner_radius, inner_corner_radius)
            self.canvas.coords("inner_oval_1_b", border_width + inner_corner_radius, border_width + inner_corner_radius, inner_corner_radius)
            self.canvas.coords("inner_oval_2_a", width - border_width - inner_corner_radius, border_width + inner_corner_radius, inner_corner_radius)
            self.canvas.coords("inner_oval_2_b", width - border_width - inner_corner_radius, border_width + inner_corner_radius, inner_corner_radius)
            self.canvas.coords("inner_oval_3_a", width - border_width - inner_corner_radius,  height - border_width - inner_corner_radius, inner_corner_radius)
            self.canvas.coords("inner_oval_3_b", width - border_width - inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)
            self.canvas.coords("inner_oval_4_a", border_width + inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)
            self.canvas.coords("inner_oval_4_b", border_width + inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)
        else:
            self.canvas.delete("inner_corner_part")  # delete inner corner parts if not needed

        # create canvas inner rectangle parts if not already created
        if not self.canvas.find_withtag("inner_rectangle_1"):
            self.canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_1", "inner_rectangle_part", "inner_parts"), width=0)
            self.canvas.tag_raise("inner_rectangle_part")
            requires_recoloring = True

        if not self.canvas.find_withtag("inner_rectangle_2") and inner_corner_radius * 2 < height - (border_width * 2):
            self.canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_2", "inner_rectangle_part", "inner_parts"), width=0)
            self.canvas.tag_raise("inner_rectangle_part")
            requires_recoloring = True

        elif self.canvas.find_withtag("inner_rectangle_2") and not inner_corner_radius * 2 < height - (border_width * 2):
            self.canvas.delete("inner_rectangle_2")

        # change position of inner rectangle parts
        self.canvas.coords("inner_rectangle_1", (border_width + inner_corner_radius,
                                                 border_width,
                                                 width - border_width - inner_corner_radius,
                                                 height - border_width))
        self.canvas.coords("inner_rectangle_2", (border_width,
                                                 border_width + inner_corner_radius,
                                                 width - border_width,
                                                 height - inner_corner_radius - border_width))

        return requires_recoloring

    def _draw_rounded_rect_with_border_circle_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int) -> bool:
        requires_recoloring = False

        # border button parts
        if border_width > 0:
            if corner_radius > 0:

                if not self.canvas.find_withtag("border_oval_1"):
                    self.canvas.create_oval(0, 0, 0, 0, tags=("border_oval_1", "border_corner_part", "border_parts"), width=0)
                    self.canvas.create_oval(0, 0, 0, 0, tags=("border_oval_2", "border_corner_part", "border_parts"), width=0)
                    self.canvas.create_oval(0, 0, 0, 0, tags=("border_oval_3", "border_corner_part", "border_parts"), width=0)
                    self.canvas.create_oval(0, 0, 0, 0, tags=("border_oval_4", "border_corner_part", "border_parts"), width=0)
                    self.canvas.tag_lower("border_parts")
                    requires_recoloring = True

                self.canvas.coords("border_oval_1", 0, 0, corner_radius * 2 - 1, corner_radius * 2 - 1)
                self.canvas.coords("border_oval_2", width - corner_radius * 2, 0, width - 1, corner_radius * 2 - 1)
                self.canvas.coords("border_oval_3", 0, height - corner_radius * 2, corner_radius * 2 - 1, height - 1)
                self.canvas.coords("border_oval_4", width - corner_radius * 2, height - corner_radius * 2, width - 1, height - 1)

            else:
                self.canvas.delete("border_corner_part")

            if not self.canvas.find_withtag("border_rectangle_1"):
                self.canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_1", "border_rectangle_part", "border_parts"), width=0)
                self.canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_2", "border_rectangle_part", "border_parts"), width=0)
                self.canvas.tag_lower("border_parts")
                requires_recoloring = True

            self.canvas.coords("border_rectangle_1", (0, corner_radius, width, height - corner_radius ))
            self.canvas.coords("border_rectangle_2", (corner_radius, 0, width - corner_radius, height ))

        else:
            self.canvas.delete("border_parts")

        # inner button parts
        if inner_corner_radius > 0:

            if not self.canvas.find_withtag("inner_oval_1"):
                self.canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_1", "inner_corner_part", "inner_parts"), width=0)
                self.canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_2", "inner_corner_part", "inner_parts"), width=0)
                self.canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_3", "inner_corner_part", "inner_parts"), width=0)
                self.canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_4", "inner_corner_part", "inner_parts"), width=0)
                self.canvas.tag_raise("inner_parts")
                requires_recoloring = True

            self.canvas.coords("inner_oval_1", (border_width, border_width,
                                                border_width + inner_corner_radius * 2 - 1, border_width + inner_corner_radius * 2 - 1))
            self.canvas.coords("inner_oval_2", (width - border_width - inner_corner_radius * 2, border_width,
                                                width - border_width - 1, border_width + inner_corner_radius * 2 - 1))
            self.canvas.coords("inner_oval_3", (border_width, height - border_width - inner_corner_radius * 2,
                                                border_width + inner_corner_radius * 2 - 1, height - border_width - 1))
            self.canvas.coords("inner_oval_4", (width - border_width - inner_corner_radius * 2, height - border_width - inner_corner_radius * 2,
                                                width - border_width - 1, height - border_width - 1))
        else:
            self.canvas.delete("inner_corner_part")  # delete inner corner parts if not needed

        if not self.canvas.find_withtag("inner_rectangle_1"):
            self.canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_1", "inner_rectangle_part", "inner_parts"), width=0)
            self.canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_2", "inner_rectangle_part", "inner_parts"), width=0)
            self.canvas.tag_raise("inner_parts")
            requires_recoloring = True

        self.canvas.coords("inner_rectangle_1", (border_width + inner_corner_radius,
                                                 border_width,
                                                 width - border_width - inner_corner_radius,
                                                 height - border_width))
        self.canvas.coords("inner_rectangle_2", (border_width,
                                                 border_width + inner_corner_radius,
                                                 width - border_width ,
                                                 height - inner_corner_radius - border_width))

        return requires_recoloring

    def draw_rounded_bar_with_border(self, width: int, height: int, corner_radius: Union[float, int], border_width: Union[float, int]) -> bool:
        pass

    def draw_rounded_button(self, canvas, width, height):
        pass
