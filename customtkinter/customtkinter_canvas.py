import tkinter
from .customtkinter_settings import CTkSettings


class CTkCanvas(tkinter.Canvas):

    # This dict maps a corner_radius of a circle to a specific font character, which is circle shape which fills the space
    # of one monospace character to a specific amount from 100% to 90% (A to I).
    radius_to_char = {19: 'B', 18: 'B', 17: 'B', 16: 'B', 15: 'B', 14: 'B', 13: 'B', 12: 'B', 11: 'B', 10: 'B',
                      9: 'C', 8: 'D', 7: 'C', 6: 'E', 5: 'F', 4: 'G', 3: 'H', 2: 'H', 1: 'H', 0: 'A'}

    radius_to_char_fine = {19: 'A', 18: 'A', 17: 'B', 16: 'B', 15: 'B', 14: 'B', 13: 'C', 12: 'C', 11: 'C', 10: 'C',
                           9: 'D', 8: 'D', 7: 'D', 6: 'F', 5: 'D', 4: 'G', 3: 'G', 2: 'H', 1: 'H', 0: 'A'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.aa_circle_canvas_ids = set()

    def get_char_from_radius(self, radius):
        if CTkSettings.scaling_factor == 1:
            if radius >= 20:
                return "A"
            else:
                return self.radius_to_char_fine[radius]

    def create_aa_circle(self, x_pos, y_pos, radius, angle=0, fill="white", tags="", anchor=tkinter.CENTER) -> str:
        # create a circle with a font element
        circle_1 = self.create_text(x_pos, y_pos, text=self.get_char_from_radius(radius), anchor=anchor, fill=fill,
                                    font=("CustomTkinter_shapes_font", -radius * 2), tags=tags, angle=angle)
        self.addtag_withtag("ctk_aa_circle_font_element", circle_1)
        self.aa_circle_canvas_ids.add(circle_1)

        return circle_1

    def coords(self, tag_or_id, *args):

        if type(tag_or_id) == str and "ctk_aa_circle_font_element" in self.gettags(tag_or_id):
            coords_id = self.find_withtag(tag_or_id)[0]  # take the lowest id for the given tag
            super().coords(coords_id, *args[:2])

            if len(args) == 3:
                super().itemconfigure(coords_id, font=("CustomTkinter_shapes_font", -int(args[2]) * 2), text=self.get_char_from_radius(args[2]))

        elif type(tag_or_id) == int and tag_or_id in self.aa_circle_canvas_ids:
            super().coords(tag_or_id, *args[:2])

            if len(args) == 3:
                super().itemconfigure(tag_or_id, font=("CustomTkinter_shapes_font", -args[2] * 2), text=self.get_char_from_radius(args[2]))

        else:
            super().coords(tag_or_id, *args)

    def itemconfig(self, tag_or_id, *args, **kwargs):
        kwargs_except_outline = kwargs.copy()
        if "outline" in kwargs_except_outline:
            del kwargs_except_outline["outline"]

        if type(tag_or_id) == int:
            if tag_or_id in self.aa_circle_canvas_ids:
                super().itemconfigure(tag_or_id, *args, **kwargs_except_outline)
            else:
                super().itemconfigure(tag_or_id, *args, **kwargs)
        else:
            configure_ids = self.find_withtag(tag_or_id)
            for configure_id in configure_ids:
                if configure_id in self.aa_circle_canvas_ids:
                    super().itemconfigure(configure_id, *args, **kwargs_except_outline)
                else:
                    super().itemconfigure(configure_id, *args, **kwargs)


