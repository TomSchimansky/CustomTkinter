import math
import tkinter
import sys
from typing import Union, Tuple, List, Callable

from . import aa_images


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

    If .aa_circles_as_images is True (drawing method 'image_shapes'), the aa-circles are image items
    with antialiased PNG images instead, see aa_images.py. The images are swapped when the radius
    or the fill color changes, and they are cached per window. The second, rotated circle is not
    needed for images, so it is created as an image item without an image.
    """

    _max_cached_images: int = 1000

    radius_to_char_fine: dict = None  # dict to map radius to font circle character

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aa_circle_canvas_ids = set()
        self.aa_circles_as_images: bool = False
        self._aa_image_items: dict = {}  # canvas id -> dict with radius or shape, fill color and current image

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
        if self.aa_circles_as_images:
            circle_1 = self.create_image(x_pos, y_pos, anchor=anchor, tags=tags)
            self.addtag_withtag("ctk_aa_circle_font_element", circle_1)
            self._aa_circle_canvas_ids.add(circle_1)
            # the rotated second circle of the font method is not needed, it stays an empty image item
            self._aa_image_items[circle_1] = {"radius": radius, "fill": fill, "image": None, "empty": angle != 0}
            self._update_aa_image(circle_1)
            return circle_1

        # create a circle with a font element
        circle_1 = self.create_text(x_pos, y_pos, text=self._get_char_from_radius(radius), anchor=anchor, fill=fill,
                                    font=("CustomTkinter_shapes_font", -radius * 2), tags=tags, angle=angle)
        self.addtag_withtag("ctk_aa_circle_font_element", circle_1)
        self._aa_circle_canvas_ids.add(circle_1)

        return circle_1

    def coords(self, tag_or_id, *args) -> List[float]:

        if type(tag_or_id) == str and "ctk_aa_circle_font_element" in self.gettags(tag_or_id):
            coords_id = self.find_withtag(tag_or_id)[0]  # take the lowest id for the given tag
            coords = super().coords(coords_id, *args[:2])

            if len(args) == 3:
                self._set_aa_circle_radius(coords_id, args[2])

        elif type(tag_or_id) == int and tag_or_id in self._aa_circle_canvas_ids:
            coords = super().coords(tag_or_id, *args[:2])

            if len(args) == 3:
                self._set_aa_circle_radius(tag_or_id, args[2])

        else:
            coords = super().coords(tag_or_id, *args)

        return coords

    def _set_aa_circle_radius(self, canvas_id: int, radius: Union[int, float]):
        if canvas_id in self._aa_image_items:
            item = self._aa_image_items[canvas_id]
            if item["radius"] != radius:
                item["radius"] = radius
                self._update_aa_image(canvas_id)
        else:
            super().itemconfigure(canvas_id, font=("CustomTkinter_shapes_font", -int(radius) * 2), text=self._get_char_from_radius(int(radius)))

    def create_aa_shape(self, kind: str, x_pos: float, y_pos: float, size: float, line_width: float, fill: str = "white",
                        tags: Union[str, Tuple[str, ...]] = "") -> int:
        """ creates an antialiased line shape ('checkmark' or 'dropdown_arrow') as image item, centered at x_pos, y_pos """
        canvas_id = self.create_image(0, 0, anchor=tkinter.NW, tags=tags)
        self._aa_image_items[canvas_id] = {"shape": None, "fill": fill, "image": None, "empty": False}
        self.set_aa_shape(canvas_id, kind, x_pos, y_pos, size, line_width)
        return canvas_id

    def set_aa_shape(self, tag_or_id: Union[str, int], kind: str, x_pos: float, y_pos: float, size: float, line_width: float):
        """ moves and resizes a shape created with create_aa_shape() """
        for canvas_id in self.find_withtag(tag_or_id):
            if canvas_id not in self._aa_image_items:
                continue
            image_size = aa_images.shape_image_size(kind, size, line_width)
            left, top = math.floor(x_pos), math.floor(y_pos)
            # fractional part of the position is drawn into the image, rounded to quarter pixels
            shape = (kind, size, line_width, round((x_pos - left) * 4) / 4, round((y_pos - top) * 4) / 4)
            super().coords(canvas_id, left - image_size // 2, top - image_size // 2)
            item = self._aa_image_items[canvas_id]
            if item["shape"] != shape:
                item["shape"] = shape
                self._update_aa_image(canvas_id)

    def _get_aa_image(self, key: tuple, fill: str, create_png: Callable[[Tuple[int, int, int]], bytes]) -> tkinter.PhotoImage:
        """ returns a cached image for key and color, the cache is shared by all canvases of a window """
        root = self._root()
        cache = root.__dict__.setdefault("_ctk_aa_image_cache", {})
        rgb_cache = root.__dict__.setdefault("_ctk_aa_rgb_cache", {})

        rgb = rgb_cache.get(fill)
        if rgb is None:
            rgb = tuple(value // 257 for value in self.winfo_rgb(fill))
            rgb_cache[fill] = rgb

        image = cache.get(key + (rgb,))
        if image is None:
            if len(cache) >= self._max_cached_images:
                cache.clear()  # images that are still in use are kept alive by the canvas items
            image = tkinter.PhotoImage(master=self, data=create_png(rgb))
            cache[key + (rgb,)] = image
        return image

    def _update_aa_image(self, canvas_id: int):
        item = self._aa_image_items[canvas_id]
        image = None

        if not item["empty"] and item["fill"]:
            if "radius" in item:
                radius = item["radius"]
                if radius > 0:
                    image = self._get_aa_image(("circle", radius), item["fill"], lambda rgb: aa_images.circle_png(radius, rgb))
            elif item["shape"] is not None:
                kind, size, line_width, offset_x, offset_y = item["shape"]
                image = self._get_aa_image(("shape",) + item["shape"], item["fill"],
                                           lambda rgb: aa_images.shape_png(kind, size, line_width, offset_x, offset_y, rgb))

        if image is not item["image"]:
            item["image"] = image  # reference keeps the image alive while it is used
            super().itemconfigure(canvas_id, image=image if image is not None else "")

    def _itemconfig_aa_image(self, canvas_id: int, kwargs: dict):
        item = self._aa_image_items[canvas_id]
        if "fill" in kwargs and kwargs["fill"] != item["fill"]:
            item["fill"] = kwargs["fill"]
            self._update_aa_image(canvas_id)
        image_item_kwargs = {key: value for key, value in kwargs.items() if key in ("state", "tags", "anchor")}
        if image_item_kwargs:
            super().itemconfigure(canvas_id, **image_item_kwargs)

    def delete(self, *args):
        if self._aa_image_items:
            for tag_or_id in args:
                for canvas_id in self.find_withtag(tag_or_id):
                    self._aa_image_items.pop(canvas_id, None)
                    self._aa_circle_canvas_ids.discard(canvas_id)
        super().delete(*args)

    def itemconfig(self, tag_or_id, *args, **kwargs):
        kwargs_except_outline = kwargs.copy()
        if "outline" in kwargs_except_outline:
            del kwargs_except_outline["outline"]

        if type(tag_or_id) == int:
            configure_ids = (tag_or_id,)
        else:
            configure_ids = self.find_withtag(tag_or_id)

        for configure_id in configure_ids:
            if configure_id in self._aa_image_items:
                self._itemconfig_aa_image(configure_id, kwargs)
            elif configure_id in self._aa_circle_canvas_ids:
                super().itemconfigure(configure_id, *args, **kwargs_except_outline)
            else:
                super().itemconfigure(configure_id, *args, **kwargs)
