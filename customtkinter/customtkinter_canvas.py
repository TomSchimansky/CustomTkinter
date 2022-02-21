import tkinter


class CTkCanvas(tkinter.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.aa_circle_canvas_ids = []

    def create_aa_circle(self, x_pos, y_pos, radius, angle=0, fill="white", tags="") -> str:
        circle_chars = ["A", "B", "C", "D", "E", "F"]

        # create a circle with a font element
        circle_1 = self.create_text(x_pos, y_pos, text=circle_chars[0], anchor=tkinter.CENTER, fill=fill,
                                    font=("TheCircle", -radius * 2), tags=tags, angle=angle)

        return circle_1
