import tkinter
import sys
from typing import Union, Tuple


class CTkCanvas(tkinter.Canvas):
    """
    Canvas with additional functionality to draw antialiased circles on Windows/Linux.

    Call .init_font_character_mapping() at program start to load the correct character
    dictionary according to the operating system. Characters (circle sizes) are optimised
    to look best for rendering CustomTkinter shapes on the different operating systems.

    - .create_aa_circle() creates antialiased circle and returns int identifier.
    - .coords() is modified to support the aa-circle shapes correctly like you would expect.
    - .itemconfig() is also modified to support aa-cricle shapes.

    The aa-circles are created by choosing a character from the custom created and loaded
    font 'CustomTkinter_shapes_font'. It contains circle shapes with different sizes filling
    either the whole character space or just pert of it (characters A to R). Circles with a smaller
    radius need a smaller circle character to look correct when rendered on the canvas.

    For an optimal result, the draw-engine creates two aa-circles on top of each other, while
    one is rotated by 90 degrees. This helps to make the circle look more symetric, which is
    not can be a problem when using only a single circle character.
    """

    radius_to_char_fine: dict = None  # dict to map radius to font circle character

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aa_circle_canvas_ids = set()

    @classmethod
    def init_font_character_mapping(cls):
        """ optimizations made for Windows 10, 11 only """

        radius_to_char_warped = {19: 'B', 18: 'B', 17: 'B', 16: 'B', 15: 'B', 14: 'B', 13: 'B', 12: 'B', 11: 'B',
                                 10: 'B',
                                 9: 'C', 8: 'D', 7: 'C', 6: 'E', 5: 'F', 4: 'G', 3: 'H', 2: 'H', 1: 'H', 0: 'A'}

        radius_to_char_fine_windows_10 = {19: 'A', 18: 'A', 17: 'B', 16: 'B', 15: 'B', 14: 'B', 13: 'C', 12: 'C',
                                          11: 'C', 10: 'C',
                                          9: 'D', 8: 'D', 7: 'D', 6: 'C', 5: 'D', 4: 'G', 3: 'G', 2: 'H', 1: 'H',
                                          0: 'A'}

        radius_to_char_fine_windows_11 = {19: 'A', 18: 'A', 17: 'B', 16: 'B', 15: 'B', 14: 'B', 13: 'C', 12: 'C',
                                          11: 'D', 10: 'D',
                                          9: 'E', 8: 'F', 7: 'C', 6: 'I', 5: 'E', 4: 'G', 3: 'P', 2: 'R', 1: 'R',
                                          0: 'A'}

        radius_to_char_fine_linux = {19: 'A', 18: 'A', 17: 'B', 16: 'B', 15: 'B', 14: 'B', 13: 'F', 12: 'C',
                                          11: 'F', 10: 'C',
                                          9: 'D', 8: 'G', 7: 'D', 6: 'F', 5: 'D', 4: 'G', 3: 'M', 2: 'H', 1: 'H',
                                          0: 'A'}

        if sys.platform.startswith("win"):
            if sys.getwindowsversion().build > 20000:  # Windows 11
                cls.radius_to_char_fine = radius_to_char_fine_windows_11
            else:  # < Windows 11
                cls.radius_to_char_fine = radius_to_char_fine_windows_10
        elif sys.platform.startswith("linux"):  # Optimized on Kali Linux
            cls.radius_to_char_fine = radius_to_char_fine_linux
        else:
            cls.radius_to_char_fine = radius_to_char_fine_windows_10

    def _get_char_from_radius(self, radius: int) -> str:
        if radius >= 20:
            return "A"
        else:
            return self.radius_to_char_fine[radius]

    def create_aa_circle(self, x_pos: int, y_pos: int, radius: int, angle: int = 0, fill: str = "white",
                         tags: Union[str, Tuple[str, ...]] = "", anchor: str = tkinter.CENTER) -> int:
        # create a circle with a font element
        circle_1 = self.create_text(x_pos, y_pos, text=self._get_char_from_radius(radius), anchor=anchor, fill=fill,
                                    font=("CustomTkinter_shapes_font", -radius * 2), tags=tags, angle=angle)
        self.addtag_withtag("ctk_aa_circle_font_element", circle_1)
        self._aa_circle_canvas_ids.add(circle_1)

        return circle_1

    def coords(self, tag_or_id, *args):

        if type(tag_or_id) == str and "ctk_aa_circle_font_element" in self.gettags(tag_or_id):
            coords_id = self.find_withtag(tag_or_id)[0]  # take the lowest id for the given tag
            super().coords(coords_id, *args[:2])

            if len(args) == 3:
                super().itemconfigure(coords_id, font=("CustomTkinter_shapes_font", -int(args[2]) * 2), text=self._get_char_from_radius(args[2]))

        elif type(tag_or_id) == int and tag_or_id in self._aa_circle_canvas_ids:
            super().coords(tag_or_id, *args[:2])

            if len(args) == 3:
                super().itemconfigure(tag_or_id, font=("CustomTkinter_shapes_font", -args[2] * 2), text=self._get_char_from_radius(args[2]))

        else:
            super().coords(tag_or_id, *args)

    def itemconfig(self, tag_or_id, *args, **kwargs):
        kwargs_except_outline = kwargs.copy()
        if "outline" in kwargs_except_outline:
            del kwargs_except_outline["outline"]

        if type(tag_or_id) == int:
            if tag_or_id in self._aa_circle_canvas_ids:
                super().itemconfigure(tag_or_id, *args, **kwargs_except_outline)
            else:
                super().itemconfigure(tag_or_id, *args, **kwargs)
        else:
            configure_ids = self.find_withtag(tag_or_id)
            for configure_id in configure_ids:
                if configure_id in self._aa_circle_canvas_ids:
                    super().itemconfigure(configure_id, *args, **kwargs_except_outline)
                else:
                    super().itemconfigure(configure_id, *args, **kwargs)
