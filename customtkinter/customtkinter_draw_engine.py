import sys
import tkinter
from typing import Union
from .customtkinter_canvas import CTkCanvas


class CTkDrawEngine:
    """
    This is the core of the CustomTkinter library where all the drawing on the tkinter.Canvas happens.
    A year of experimenting and trying out different drawing methods have led to the current state of this
    class, and I don't think there's much I can do to make the rendering look better than this with the
    limited capabilities the tkinter.Canvas offers.

    Functions:
     - draw_rounded_rect_with_border()
     - draw_rounded_progress_bar_with_border()
     - draw_rounded_slider_with_border_and_button()
     - draw_checkmark()

    """

    def __init__(self, canvas: CTkCanvas, rendering_method: str):
        self._canvas = canvas
        self._rendering_method = rendering_method  # "polygon_shapes" (macOS), "font_shapes" (Windows, Linux), "circle_shapes" (backup without fonts)
        self._existing_tags = set()

    def _calc_optimal_corner_radius(self, user_corner_radius: Union[float, int]) -> Union[float, int]:
        # optimize for drawing with polygon shapes
        if self._rendering_method == "polygon_shapes":
            if sys.platform == "darwin":
                return user_corner_radius
            else:
                return round(user_corner_radius)

        # optimize forx drawing with antialiased font shapes
        elif self._rendering_method == "font_shapes":
            return round(user_corner_radius)

        # optimize for drawing with circles and rects
        elif self._rendering_method == "circle_shapes":
            user_corner_radius = 0.5 * round(user_corner_radius / 0.5)  # round to 0.5 steps

            # make sure the value is always with .5 at the end for smoother corners
            if user_corner_radius == 0:
                return 0
            elif user_corner_radius % 1 == 0:
                return user_corner_radius + 0.5
            else:
                return user_corner_radius

    def draw_rounded_rect_with_border(self, width: int, height: int, corner_radius: Union[float, int], border_width: Union[float, int]) -> bool:
        """ Draws a rounded rectangle with a corner_radius and border_width on the canvas. The border elements have a 'border_parts' tag,
            the main foreground elements have an 'inner_parts' tag to color the elements accordingly.

            returns bool if recoloring is necessary """

        if corner_radius > width / 2 or corner_radius > height / 2:  # restrict corner_radius if it's too larger
            corner_radius = min(width / 2, height / 2)

        border_width = round(border_width)
        corner_radius = self._calc_optimal_corner_radius(corner_radius)  # optimize corner_radius for different drawing methods (different rounding)

        if corner_radius >= border_width:
            inner_corner_radius = corner_radius - border_width
        else:
            inner_corner_radius = 0

        if self._rendering_method == "polygon_shapes":
            return self._draw_rounded_rect_with_border_polygon_shapes(width, height, corner_radius, border_width, inner_corner_radius)
        elif self._rendering_method == "font_shapes":
            return self._draw_rounded_rect_with_border_font_shapes(width, height, corner_radius, border_width, inner_corner_radius, ())
        elif self._rendering_method == "circle_shapes":
            return self._draw_rounded_rect_with_border_circle_shapes(width, height, corner_radius, border_width, inner_corner_radius)

    def _draw_rounded_rect_with_border_polygon_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int) -> bool:
        requires_recoloring = False

        # create border button parts (only if border exists)
        if border_width > 0:
            if not self._canvas.find_withtag("border_parts"):
                self._canvas.create_polygon((0, 0, 0, 0), tags=("border_line_1", "border_parts"))
                requires_recoloring = True

            self._canvas.coords("border_line_1",
                                (corner_radius,
                                corner_radius,
                                width - corner_radius,
                                corner_radius,
                                width - corner_radius,
                                height - corner_radius,
                                corner_radius,
                                height - corner_radius))
            self._canvas.itemconfig("border_line_1",
                                    joinstyle=tkinter.ROUND,
                                    width=corner_radius * 2)

        else:
            self._canvas.delete("border_parts")

        # create inner button parts
        if not self._canvas.find_withtag("inner_parts"):
            self._canvas.create_polygon((0, 0, 0, 0), tags=("inner_line_1", "inner_parts"), joinstyle=tkinter.ROUND)
            requires_recoloring = True

        if corner_radius <= border_width:
            bottom_right_shift = -1  # weird canvas rendering inaccuracy that has to be corrected in some cases
        else:
            bottom_right_shift = 0

        self._canvas.coords("inner_line_1",
                            border_width + inner_corner_radius,
                            border_width + inner_corner_radius,
                            width - (border_width + inner_corner_radius) + bottom_right_shift,
                            border_width + inner_corner_radius,
                            width - (border_width + inner_corner_radius) + bottom_right_shift,
                            height - (border_width + inner_corner_radius) + bottom_right_shift,
                            border_width + inner_corner_radius,
                            height - (border_width + inner_corner_radius) + bottom_right_shift)
        self._canvas.itemconfig("inner_line_1",
                                width=inner_corner_radius * 2)

        if requires_recoloring:  # new parts were added -> manage z-order
            self._canvas.tag_lower("inner_parts")
            self._canvas.tag_lower("border_parts")

        return requires_recoloring

    def _draw_rounded_rect_with_border_font_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int,
                                                   exclude_parts: tuple) -> bool:
        requires_recoloring = False

        # create border button parts
        if border_width > 0:
            if corner_radius > 0:
                # create canvas border corner parts if not already created, but only if needed, and delete if not needed
                if not self._canvas.find_withtag("border_oval_1_a") and "border_oval_1" not in exclude_parts:
                    self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_1_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
                    self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_1_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
                    requires_recoloring = True
                elif self._canvas.find_withtag("border_oval_1_a") and "border_oval_1" in exclude_parts:
                    self._canvas.delete("border_oval_1_a", "border_oval_1_b")

                if not self._canvas.find_withtag("border_oval_2_a") and width > 2 * corner_radius and "border_oval_2" not in exclude_parts:
                    self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_2_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
                    self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_2_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
                    requires_recoloring = True
                elif self._canvas.find_withtag("border_oval_2_a") and (not width > 2 * corner_radius or "border_oval_2" in exclude_parts):
                    self._canvas.delete("border_oval_2_a", "border_oval_2_b")

                if not self._canvas.find_withtag("border_oval_3_a") and height > 2 * corner_radius \
                        and width > 2 * corner_radius and "border_oval_3" not in exclude_parts:
                    self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_3_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
                    self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_3_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
                    requires_recoloring = True
                elif self._canvas.find_withtag("border_oval_3_a") and (not (height > 2 * corner_radius
                                                                            and width > 2 * corner_radius) or "border_oval_3" in exclude_parts):
                    self._canvas.delete("border_oval_3_a", "border_oval_3_b")

                if not self._canvas.find_withtag("border_oval_4_a") and height > 2 * corner_radius and "border_oval_4" not in exclude_parts:
                    self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_4_a", "border_corner_part", "border_parts"), anchor=tkinter.CENTER)
                    self._canvas.create_aa_circle(0, 0, 0, tags=("border_oval_4_b", "border_corner_part", "border_parts"), anchor=tkinter.CENTER, angle=180)
                    requires_recoloring = True
                elif self._canvas.find_withtag("border_oval_4_a") and (not height > 2 * corner_radius or "border_oval_4" in exclude_parts):
                    self._canvas.delete("border_oval_4_a", "border_oval_4_b")

                # change position of border corner parts
                self._canvas.coords("border_oval_1_a", corner_radius, corner_radius, corner_radius)
                self._canvas.coords("border_oval_1_b", corner_radius, corner_radius, corner_radius)
                self._canvas.coords("border_oval_2_a", width - corner_radius, corner_radius, corner_radius)
                self._canvas.coords("border_oval_2_b", width - corner_radius, corner_radius, corner_radius)
                self._canvas.coords("border_oval_3_a", width - corner_radius, height - corner_radius, corner_radius)
                self._canvas.coords("border_oval_3_b", width - corner_radius, height - corner_radius, corner_radius)
                self._canvas.coords("border_oval_4_a", corner_radius, height - corner_radius, corner_radius)
                self._canvas.coords("border_oval_4_b", corner_radius, height - corner_radius, corner_radius)

            else:
                self._canvas.delete("border_corner_part")  # delete border corner parts if not needed

            # create canvas border rectangle parts if not already created
            if not self._canvas.find_withtag("border_rectangle_1"):
                self._canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_1", "border_rectangle_part", "border_parts"), width=0)
                self._canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_2", "border_rectangle_part", "border_parts"), width=0)
                requires_recoloring = True

            # change position of border rectangle parts
            self._canvas.coords("border_rectangle_1", (0, corner_radius, width, height - corner_radius))
            self._canvas.coords("border_rectangle_2", (corner_radius, 0, width - corner_radius, height))

        else:
            self._canvas.delete("border_parts")

        # create inner button parts
        if inner_corner_radius > 0:

            # create canvas border corner parts if not already created, but only if they're needed and delete if not needed
            if not self._canvas.find_withtag("inner_oval_1_a") and "inner_oval_1" not in exclude_parts:
                self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_1_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
                self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_1_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
                requires_recoloring = True
            elif self._canvas.find_withtag("inner_oval_1_a") and "inner_oval_1" in exclude_parts:
                self._canvas.delete("inner_oval_1_a", "inner_oval_1_b")

            if not self._canvas.find_withtag("inner_oval_2_a") and width - (2 * border_width) > 2 * inner_corner_radius and "inner_oval_2" not in exclude_parts:
                self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_2_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
                self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_2_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
                requires_recoloring = True
            elif self._canvas.find_withtag("inner_oval_2_a") and (not width - (2 * border_width) > 2 * inner_corner_radius or "inner_oval_2" in exclude_parts):
                self._canvas.delete("inner_oval_2_a", "inner_oval_2_b")

            if not self._canvas.find_withtag("inner_oval_3_a") and height - (2 * border_width) > 2 * inner_corner_radius \
                    and width - (2 * border_width) > 2 * inner_corner_radius and "inner_oval_3" not in exclude_parts:
                self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_3_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
                self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_3_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
                requires_recoloring = True
            elif self._canvas.find_withtag("inner_oval_3_a") and (not (height - (2 * border_width) > 2 * inner_corner_radius
                    and width - (2 * border_width) > 2 * inner_corner_radius) or "inner_oval_3" in exclude_parts):
                self._canvas.delete("inner_oval_3_a", "inner_oval_3_b")

            if not self._canvas.find_withtag("inner_oval_4_a") and height - (2 * border_width) > 2 * inner_corner_radius and "inner_oval_4" not in exclude_parts:
                self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_4_a", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER)
                self._canvas.create_aa_circle(0, 0, 0, tags=("inner_oval_4_b", "inner_corner_part", "inner_parts"), anchor=tkinter.CENTER, angle=180)
                requires_recoloring = True
            elif self._canvas.find_withtag("inner_oval_4_a") and (not height - (2 * border_width) > 2 * inner_corner_radius or "inner_oval_4" in exclude_parts):
                self._canvas.delete("inner_oval_4_a", "inner_oval_4_b")

            # change position of border corner parts
            self._canvas.coords("inner_oval_1_a", border_width + inner_corner_radius, border_width + inner_corner_radius, inner_corner_radius)
            self._canvas.coords("inner_oval_1_b", border_width + inner_corner_radius, border_width + inner_corner_radius, inner_corner_radius)
            self._canvas.coords("inner_oval_2_a", width - border_width - inner_corner_radius, border_width + inner_corner_radius, inner_corner_radius)
            self._canvas.coords("inner_oval_2_b", width - border_width - inner_corner_radius, border_width + inner_corner_radius, inner_corner_radius)
            self._canvas.coords("inner_oval_3_a", width - border_width - inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)
            self._canvas.coords("inner_oval_3_b", width - border_width - inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)
            self._canvas.coords("inner_oval_4_a", border_width + inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)
            self._canvas.coords("inner_oval_4_b", border_width + inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)
        else:
            self._canvas.delete("inner_corner_part")  # delete inner corner parts if not needed

        # create canvas inner rectangle parts if not already created
        if not self._canvas.find_withtag("inner_rectangle_1"):
            self._canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_1", "inner_rectangle_part", "inner_parts"), width=0)
            requires_recoloring = True

        if not self._canvas.find_withtag("inner_rectangle_2") and inner_corner_radius * 2 < height - (border_width * 2):
            self._canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_2", "inner_rectangle_part", "inner_parts"), width=0)
            requires_recoloring = True

        elif self._canvas.find_withtag("inner_rectangle_2") and not inner_corner_radius * 2 < height - (border_width * 2):
            self._canvas.delete("inner_rectangle_2")

        # change position of inner rectangle parts
        self._canvas.coords("inner_rectangle_1", (border_width + inner_corner_radius,
                                                  border_width,
                                                  width - border_width - inner_corner_radius,
                                                  height - border_width))
        self._canvas.coords("inner_rectangle_2", (border_width,
                                                  border_width + inner_corner_radius,
                                                  width - border_width,
                                                  height - inner_corner_radius - border_width))

        if requires_recoloring:  # new parts were added -> manage z-order
            self._canvas.tag_lower("inner_parts")
            self._canvas.tag_lower("border_parts")

        return requires_recoloring

    def _draw_rounded_rect_with_border_circle_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int) -> bool:
        requires_recoloring = False

        # border button parts
        if border_width > 0:
            if corner_radius > 0:

                if not self._canvas.find_withtag("border_oval_1"):
                    self._canvas.create_oval(0, 0, 0, 0, tags=("border_oval_1", "border_corner_part", "border_parts"), width=0)
                    self._canvas.create_oval(0, 0, 0, 0, tags=("border_oval_2", "border_corner_part", "border_parts"), width=0)
                    self._canvas.create_oval(0, 0, 0, 0, tags=("border_oval_3", "border_corner_part", "border_parts"), width=0)
                    self._canvas.create_oval(0, 0, 0, 0, tags=("border_oval_4", "border_corner_part", "border_parts"), width=0)
                    self._canvas.tag_lower("border_parts")
                    requires_recoloring = True

                self._canvas.coords("border_oval_1", 0, 0, corner_radius * 2 - 1, corner_radius * 2 - 1)
                self._canvas.coords("border_oval_2", width - corner_radius * 2, 0, width - 1, corner_radius * 2 - 1)
                self._canvas.coords("border_oval_3", 0, height - corner_radius * 2, corner_radius * 2 - 1, height - 1)
                self._canvas.coords("border_oval_4", width - corner_radius * 2, height - corner_radius * 2, width - 1, height - 1)

            else:
                self._canvas.delete("border_corner_part")

            if not self._canvas.find_withtag("border_rectangle_1"):
                self._canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_1", "border_rectangle_part", "border_parts"), width=0)
                self._canvas.create_rectangle(0, 0, 0, 0, tags=("border_rectangle_2", "border_rectangle_part", "border_parts"), width=0)
                self._canvas.tag_lower("border_parts")
                requires_recoloring = True

            self._canvas.coords("border_rectangle_1", (0, corner_radius, width, height - corner_radius))
            self._canvas.coords("border_rectangle_2", (corner_radius, 0, width - corner_radius, height))

        else:
            self._canvas.delete("border_parts")

        # inner button parts
        if inner_corner_radius > 0:

            if not self._canvas.find_withtag("inner_oval_1"):
                self._canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_1", "inner_corner_part", "inner_parts"), width=0)
                self._canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_2", "inner_corner_part", "inner_parts"), width=0)
                self._canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_3", "inner_corner_part", "inner_parts"), width=0)
                self._canvas.create_oval(0, 0, 0, 0, tags=("inner_oval_4", "inner_corner_part", "inner_parts"), width=0)
                self._canvas.tag_raise("inner_parts")
                requires_recoloring = True

            self._canvas.coords("inner_oval_1", (border_width, border_width,
                                                 border_width + inner_corner_radius * 2 - 1, border_width + inner_corner_radius * 2 - 1))
            self._canvas.coords("inner_oval_2", (width - border_width - inner_corner_radius * 2, border_width,
                                                 width - border_width - 1, border_width + inner_corner_radius * 2 - 1))
            self._canvas.coords("inner_oval_3", (border_width, height - border_width - inner_corner_radius * 2,
                                                 border_width + inner_corner_radius * 2 - 1, height - border_width - 1))
            self._canvas.coords("inner_oval_4", (width - border_width - inner_corner_radius * 2, height - border_width - inner_corner_radius * 2,
                                                 width - border_width - 1, height - border_width - 1))
        else:
            self._canvas.delete("inner_corner_part")  # delete inner corner parts if not needed

        if not self._canvas.find_withtag("inner_rectangle_1"):
            self._canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_1", "inner_rectangle_part", "inner_parts"), width=0)
            self._canvas.create_rectangle(0, 0, 0, 0, tags=("inner_rectangle_2", "inner_rectangle_part", "inner_parts"), width=0)
            self._canvas.tag_raise("inner_parts")
            requires_recoloring = True

        self._canvas.coords("inner_rectangle_1", (border_width + inner_corner_radius,
                                                  border_width,
                                                  width - border_width - inner_corner_radius,
                                                  height - border_width))
        self._canvas.coords("inner_rectangle_2", (border_width,
                                                  border_width + inner_corner_radius,
                                                  width - border_width ,
                                                  height - inner_corner_radius - border_width))

        return requires_recoloring

    def draw_rounded_progress_bar_with_border(self, width: int, height: int, corner_radius: Union[float, int], border_width: Union[float, int],
                                              progress_value: float, orientation: str) -> bool:
        """ Draws a rounded bar on the canvas, which is split in half according to the argument 'progress_value' (0 - 1).
            The border elements get the 'border_parts' tag", the main elements get the 'inner_parts' tag and
            the progress elements get the 'progress_parts' tag. The 'orientation' argument defines from which direction the progress starts (n, w, s, e).

            returns bool if recoloring is necessary """

        if corner_radius > width / 2 or corner_radius > height / 2:  # restrict corner_radius if it's too larger
            corner_radius = min(width / 2, height / 2)

        border_width = round(border_width)
        corner_radius = self._calc_optimal_corner_radius(corner_radius)  # optimize corner_radius for different drawing methods (different rounding)

        if corner_radius >= border_width:
            inner_corner_radius = corner_radius - border_width
        else:
            inner_corner_radius = 0

        if self._rendering_method == "polygon_shapes" or self._rendering_method == "circle_shapes":
            return self._draw_rounded_progress_bar_with_border_polygon_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                              progress_value, orientation)
        elif self._rendering_method == "font_shapes":
            return self._draw_rounded_progress_bar_with_border_font_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                           progress_value, orientation)

    def _draw_rounded_progress_bar_with_border_polygon_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int,
                                                              progress_value: float, orientation: str) -> bool:

        requires_recoloring = self._draw_rounded_rect_with_border_polygon_shapes(width, height, corner_radius, border_width, inner_corner_radius)

        if corner_radius <= border_width:
            bottom_right_shift = 0  # weird canvas rendering inaccuracy that has to be corrected in some cases
        else:
            bottom_right_shift = 0

        # create progress parts
        if not self._canvas.find_withtag("progress_parts"):
            self._canvas.create_polygon((0, 0, 0, 0), tags=("progress_line_1", "progress_parts"), joinstyle=tkinter.ROUND)
            self._canvas.tag_raise("progress_parts", "inner_parts")
            requires_recoloring = True

        if orientation == "w":
            self._canvas.coords("progress_line_1",
                                border_width + inner_corner_radius,
                                border_width + inner_corner_radius,
                                border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value,
                                border_width + inner_corner_radius,
                                border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value,
                                height - (border_width + inner_corner_radius) + bottom_right_shift,
                                border_width + inner_corner_radius,
                                height - (border_width + inner_corner_radius) + bottom_right_shift)

        elif orientation == "s":
            self._canvas.coords("progress_line_1",
                                border_width + inner_corner_radius,
                                border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value),
                                width - (border_width + inner_corner_radius),
                                border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value),
                                width - (border_width + inner_corner_radius),
                                height - (border_width + inner_corner_radius) + bottom_right_shift,
                                border_width + inner_corner_radius,
                                height - (border_width + inner_corner_radius) + bottom_right_shift)

        self._canvas.itemconfig("progress_line_1", width=inner_corner_radius * 2)

        return requires_recoloring

    def _draw_rounded_progress_bar_with_border_font_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int,
                                                           progress_value: float, orientation: str) -> bool:

        requires_recoloring, requires_recoloring_2 = False, False

        if inner_corner_radius > 0:
            # create canvas border corner parts if not already created
            if not self._canvas.find_withtag("progress_oval_1_a"):
                self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_1_a", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER)
                self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_1_b", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER, angle=180)
                self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_2_a", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER)
                self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_2_b", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER, angle=180)
                requires_recoloring = True

            if not self._canvas.find_withtag("progress_oval_3_a") and round(inner_corner_radius) * 2 < height - 2 * border_width:
                self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_3_a", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER)
                self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_3_b", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER, angle=180)
                self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_4_a", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER)
                self._canvas.create_aa_circle(0, 0, 0, tags=("progress_oval_4_b", "progress_corner_part", "progress_parts"), anchor=tkinter.CENTER, angle=180)
                requires_recoloring = True
            elif self._canvas.find_withtag("progress_oval_3_a") and not round(inner_corner_radius) * 2 < height - 2 * border_width:
                self._canvas.delete("progress_oval_3_a", "progress_oval_3_b", "progress_oval_4_a", "progress_oval_4_b")

        if not self._canvas.find_withtag("progress_rectangle_1"):
            self._canvas.create_rectangle(0, 0, 0, 0, tags=("progress_rectangle_1", "progress_rectangle_part", "progress_parts"), width=0)
            requires_recoloring = True

        if not self._canvas.find_withtag("progress_rectangle_2") and inner_corner_radius * 2 < height - (border_width * 2):
            self._canvas.create_rectangle(0, 0, 0, 0, tags=("progress_rectangle_2", "progress_rectangle_part", "progress_parts"), width=0)
            requires_recoloring = True
        elif self._canvas.find_withtag("progress_rectangle_2") and not inner_corner_radius * 2 < height - (border_width * 2):
            self._canvas.delete("progress_rectangle_2")

        # horizontal orientation from the bottom
        if orientation == "w":
            requires_recoloring_2 = self._draw_rounded_rect_with_border_font_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                                    ("inner_oval_1", "inner_oval_4"))

            # set positions of progress corner parts
            self._canvas.coords("progress_oval_1_a", border_width + inner_corner_radius, border_width + inner_corner_radius, inner_corner_radius)
            self._canvas.coords("progress_oval_1_b", border_width + inner_corner_radius, border_width + inner_corner_radius, inner_corner_radius)
            self._canvas.coords("progress_oval_2_a", border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value,
                                border_width + inner_corner_radius, inner_corner_radius)
            self._canvas.coords("progress_oval_2_b", border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value,
                                border_width + inner_corner_radius, inner_corner_radius)
            self._canvas.coords("progress_oval_3_a",  border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value,
                                height - border_width - inner_corner_radius, inner_corner_radius)
            self._canvas.coords("progress_oval_3_b",  border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value,
                                height - border_width - inner_corner_radius, inner_corner_radius)
            self._canvas.coords("progress_oval_4_a", border_width + inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)
            self._canvas.coords("progress_oval_4_b", border_width + inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)

            # set positions of progress rect parts
            self._canvas.coords("progress_rectangle_1",
                                border_width + inner_corner_radius,
                                border_width,
                                border_width + inner_corner_radius + (width - 2 * border_width - 2 * inner_corner_radius) * progress_value,
                                height - border_width)
            self._canvas.coords("progress_rectangle_2",
                                border_width,
                                border_width + inner_corner_radius,
                                border_width + 2 * inner_corner_radius + (width - 2 * inner_corner_radius - 2 * border_width) * progress_value,
                                height - inner_corner_radius - border_width)

        # vertical orientation from the bottom
        if orientation == "s":
            requires_recoloring_2 = self._draw_rounded_rect_with_border_font_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                                    ("inner_oval_3", "inner_oval_4"))

            # set positions of progress corner parts
            self._canvas.coords("progress_oval_1_a", border_width + inner_corner_radius,
                                border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value), inner_corner_radius)
            self._canvas.coords("progress_oval_1_b", border_width + inner_corner_radius,
                                border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value), inner_corner_radius)
            self._canvas.coords("progress_oval_2_a", width - border_width - inner_corner_radius,
                                border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value), inner_corner_radius)
            self._canvas.coords("progress_oval_2_b", width - border_width - inner_corner_radius,
                                border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value), inner_corner_radius)
            self._canvas.coords("progress_oval_3_a", width - border_width - inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)
            self._canvas.coords("progress_oval_3_b", width - border_width - inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)
            self._canvas.coords("progress_oval_4_a", border_width + inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)
            self._canvas.coords("progress_oval_4_b", border_width + inner_corner_radius, height - border_width - inner_corner_radius, inner_corner_radius)

            # set positions of progress rect parts
            self._canvas.coords("progress_rectangle_1",
                                border_width + inner_corner_radius,
                                border_width + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value),
                                width - border_width - inner_corner_radius,
                                height - border_width)
            self._canvas.coords("progress_rectangle_2",
                                border_width,
                                border_width + inner_corner_radius + (height - 2 * border_width - 2 * inner_corner_radius) * (1 - progress_value),
                                width - border_width,
                                height - inner_corner_radius - border_width)

        return requires_recoloring or requires_recoloring_2

    def draw_rounded_slider_with_border_and_button(self, width: int, height: int, corner_radius: Union[float, int], border_width: Union[float, int],
                                                   button_length: Union[float, int], button_corner_radius: Union[float, int], slider_value: float,
                                                   orientation: str) -> bool:

        if corner_radius > width / 2 or corner_radius > height / 2:  # restrict corner_radius if it's too larger
            corner_radius = min(width / 2, height / 2)

        if button_corner_radius > width / 2 or button_corner_radius > height / 2:  # restrict button_corner_radius if it's too larger
            button_corner_radius = min(width / 2, height / 2)

        button_length = round(button_length)
        border_width = round(border_width)
        button_corner_radius = round(button_corner_radius)
        corner_radius = self._calc_optimal_corner_radius(corner_radius)  # optimize corner_radius for different drawing methods (different rounding)

        if corner_radius >= border_width:
            inner_corner_radius = corner_radius - border_width
        else:
            inner_corner_radius = 0

        if self._rendering_method == "polygon_shapes" or self._rendering_method == "circle_shapes":
            return self._draw_rounded_slider_with_border_and_button_polygon_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                                   button_length, button_corner_radius, slider_value, orientation)
        elif self._rendering_method == "font_shapes":
            return self._draw_rounded_slider_with_border_and_button_font_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                                button_length, button_corner_radius, slider_value, orientation)

    def _draw_rounded_slider_with_border_and_button_polygon_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int,
                                                                   button_length: int, button_corner_radius: int, slider_value: float, orientation: str) -> bool:

        # draw normal progressbar
        requires_recoloring = self._draw_rounded_progress_bar_with_border_polygon_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                                         slider_value, orientation)

        # create slider button part
        if not self._canvas.find_withtag("slider_parts"):
            self._canvas.create_polygon((0, 0, 0, 0), tags=("slider_line_1", "slider_parts"), joinstyle=tkinter.ROUND)
            self._canvas.tag_raise("slider_parts")  # manage z-order
            requires_recoloring = True

        if corner_radius <= border_width:
            bottom_right_shift = -1  # weird canvas rendering inaccuracy that has to be corrected in some cases
        else:
            bottom_right_shift = 0

        if orientation == "w":
            slider_x_position = corner_radius + (button_length / 2) + (width - 2 * corner_radius - button_length) * slider_value
            self._canvas.coords("slider_line_1",
                                slider_x_position - (button_length / 2), button_corner_radius,
                                slider_x_position + (button_length / 2), button_corner_radius,
                                slider_x_position + (button_length / 2), height - button_corner_radius,
                                slider_x_position - (button_length / 2), height - button_corner_radius)
            self._canvas.itemconfig("slider_line_1",
                                    width=button_corner_radius * 2)

        return requires_recoloring

    def _draw_rounded_slider_with_border_and_button_font_shapes(self, width: int, height: int, corner_radius: int, border_width: int, inner_corner_radius: int,
                                                                button_length: int, button_corner_radius: int, slider_value: float, orientation: str) -> bool:

        # draw normal progressbar
        requires_recoloring = self._draw_rounded_progress_bar_with_border_font_shapes(width, height, corner_radius, border_width, inner_corner_radius,
                                                                                      slider_value, orientation)

        # create 4 circles (if not needed, then less)
        if not self._canvas.find_withtag("slider_oval_1_a"):
            self._canvas.create_aa_circle(0, 0, 0, tags=("slider_oval_1_a", "slider_corner_part", "slider_parts"), anchor=tkinter.CENTER)
            self._canvas.create_aa_circle(0, 0, 0, tags=("slider_oval_1_b", "slider_corner_part", "slider_parts"), anchor=tkinter.CENTER, angle=180)
            requires_recoloring = True

        if not self._canvas.find_withtag("slider_oval_2_a") and button_length > 0:
            self._canvas.create_aa_circle(0, 0, 0, tags=("slider_oval_2_a", "slider_corner_part", "slider_parts"), anchor=tkinter.CENTER)
            self._canvas.create_aa_circle(0, 0, 0, tags=("slider_oval_2_b", "slider_corner_part", "slider_parts"), anchor=tkinter.CENTER, angle=180)
            requires_recoloring = True
        elif self._canvas.find_withtag("slider_oval_2_a") and not button_length > 0:
            self._canvas.delete("slider_oval_2_a", "slider_oval_2_b")

        if not self._canvas.find_withtag("slider_oval_4_a") and height > 2 * button_corner_radius:
            self._canvas.create_aa_circle(0, 0, 0, tags=("slider_oval_4_a", "slider_corner_part", "slider_parts"), anchor=tkinter.CENTER)
            self._canvas.create_aa_circle(0, 0, 0, tags=("slider_oval_4_b", "slider_corner_part", "slider_parts"), anchor=tkinter.CENTER, angle=180)
            requires_recoloring = True
        elif self._canvas.find_withtag("slider_oval_4_a") and not height > 2 * button_corner_radius:
            self._canvas.delete("slider_oval_4_a", "slider_oval_4_b")

        if not self._canvas.find_withtag("slider_oval_3_a") and button_length > 0 and height > 2 * button_corner_radius:
            self._canvas.create_aa_circle(0, 0, 0, tags=("slider_oval_3_a", "slider_corner_part", "slider_parts"), anchor=tkinter.CENTER)
            self._canvas.create_aa_circle(0, 0, 0, tags=("slider_oval_3_b", "slider_corner_part", "slider_parts"), anchor=tkinter.CENTER, angle=180)
            requires_recoloring = True
        elif self._canvas.find_withtag("border_oval_3_a") and not (button_length > 0 and height > 2 * button_corner_radius):
            self._canvas.delete("slider_oval_3_a", "slider_oval_3_b")

        # create the 2 rectangles (if needed)
        if not self._canvas.find_withtag("slider_rectangle_1") and button_length > 0:
            self._canvas.create_rectangle(0, 0, 0, 0, tags=("slider_rectangle_1", "slider_rectangle_part", "slider_parts"), width=0)
            requires_recoloring = True
        elif self._canvas.find_withtag("slider_rectangle_1") and not button_length > 0:
            self._canvas.delete("slider_rectangle_1")

        if not self._canvas.find_withtag("slider_rectangle_2") and height > 2 * button_corner_radius:
            self._canvas.create_rectangle(0, 0, 0, 0, tags=("slider_rectangle_2", "slider_rectangle_part", "slider_parts"), width=0)
            requires_recoloring = True
        elif self._canvas.find_withtag("slider_rectangle_2") and not height > 2 * button_corner_radius:
            self._canvas.delete("slider_rectangle_2")

        # set positions of circles and rectangles
        slider_x_position = corner_radius + (button_length / 2) + (width - 2 * corner_radius - button_length) * slider_value
        self._canvas.coords("slider_oval_1_a", slider_x_position - (button_length / 2), button_corner_radius, button_corner_radius)
        self._canvas.coords("slider_oval_1_b", slider_x_position - (button_length / 2), button_corner_radius, button_corner_radius)
        self._canvas.coords("slider_oval_2_a", slider_x_position + (button_length / 2), button_corner_radius, button_corner_radius)
        self._canvas.coords("slider_oval_2_b", slider_x_position + (button_length / 2), button_corner_radius, button_corner_radius)
        self._canvas.coords("slider_oval_3_a", slider_x_position + (button_length / 2), height - button_corner_radius, button_corner_radius)
        self._canvas.coords("slider_oval_3_b", slider_x_position + (button_length / 2), height - button_corner_radius, button_corner_radius)
        self._canvas.coords("slider_oval_4_a", slider_x_position - (button_length / 2), height - button_corner_radius, button_corner_radius)
        self._canvas.coords("slider_oval_4_b", slider_x_position - (button_length / 2), height - button_corner_radius, button_corner_radius)

        self._canvas.coords("slider_rectangle_1",
                            slider_x_position - (button_length / 2), 0,
                            slider_x_position + (button_length / 2), height)
        self._canvas.coords("slider_rectangle_2",
                            slider_x_position - (button_length / 2) - button_corner_radius, button_corner_radius,
                            slider_x_position + (button_length / 2) + button_corner_radius, height - button_corner_radius)

        if requires_recoloring:  # new parts were added -> manage z-order
            self._canvas.tag_raise("slider_parts")

        return requires_recoloring

    def draw_checkmark(self, width: int, height: int, size: Union[int, float]) -> bool:
        """ Draws a rounded rectangle with a corner_radius and border_width on the canvas. The border elements have a 'border_parts' tag,
            the main foreground elements have an 'inner_parts' tag to color the elements accordingly.

            returns bool if recoloring is necessary """

        size = round(size)
        requires_recoloring = False

        if self._rendering_method == "polygon_shapes" or self._rendering_method == "circle_shapes":
            x, y, radius = width / 2, height / 2, size / 2.8
            if not self._canvas.find_withtag("checkmark"):
                self._canvas.create_line(0, 0, 0, 0, tags=("checkmark", "create_line"), width=round(height / 8), joinstyle=tkinter.MITER, capstyle=tkinter.ROUND)
                self._canvas.tag_raise("checkmark")
                requires_recoloring = True

            self._canvas.coords("checkmark",
                                x + radius, y - radius,
                                x - radius / 4, y + radius * 0.8,
                                x - radius, y + radius / 6)
        elif self._rendering_method == "font_shapes":
            if not self._canvas.find_withtag("checkmark"):
                self._canvas.create_text(0, 0, text="Z", font=("CustomTkinter_shapes_font", -size), tags=("checkmark", "create_text"), anchor=tkinter.CENTER)
                self._canvas.tag_raise("checkmark")
                requires_recoloring = True

            self._canvas.coords("checkmark", round(width / 2), round(height / 2))

        return requires_recoloring
