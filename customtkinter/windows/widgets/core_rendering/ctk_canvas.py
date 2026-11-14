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
        # Python-side registry of the item tags, so that the draw engine doesn't need a Tcl call to check whether
        # an item exists or which items have a tag. Kept up to date in _create() and delete(), other tag changes
        # (addtag, dtag, itemconfigure with tags) mark it as invalid and it gets rebuilt from Tcl when needed.
        self._tag_ids: dict = {}  # tag -> list of canvas ids in creation order
        self._id_tags: dict = {}  # canvas id -> tuple of tags
        self._tag_registry_valid: bool = True
        self._coords_cache: dict = {}  # canvas id -> last coordinates set with coords(), to skip unchanged ones

        super().__init__(*args, **kwargs)
        self._aa_circle_canvas_ids = set()
        self.aa_circles_as_images: bool = False
        self._aa_image_items: dict = {}  # canvas id -> dict with radius or shape, fill color and current image

    def _tags_to_tuple(self, tags) -> tuple:
        if not tags:
            return ()
        if isinstance(tags, str):
            return (tags,) if " " not in tags and "{" not in tags else tuple(self.tk.splitlist(tags))
        return tuple(str(tag) for tag in tags)

    _plain_tag_cache: dict = {}

    @classmethod
    def _is_plain_tag(cls, tag) -> bool:
        """ True for a normal tag name, False for item ids, 'all', 'current' and tag expressions """
        if type(tag) is not str:
            return False
        result = cls._plain_tag_cache.get(tag)
        if result is None:
            result = tag not in ("all", "current") and not tag.isdigit() and not any(character in tag for character in " &|!^()")
            if len(cls._plain_tag_cache) < 10000:
                cls._plain_tag_cache[tag] = result
        return result

    def _create(self, itemType, args, kw):
        canvas_id = super()._create(itemType, args, kw)
        tags = kw.get("tags")
        if tags is None and args and isinstance(args[-1], dict):
            tags = args[-1].get("tags")
        tags = self._tags_to_tuple(tags)
        self._id_tags[canvas_id] = tags
        for tag in tags:
            self._tag_ids.setdefault(tag, []).append(canvas_id)
        return canvas_id

    def _rebuild_tag_registry(self):
        self._tag_ids, self._id_tags = {}, {}
        for canvas_id in super().find_all():
            tags = super().gettags(canvas_id)
            self._id_tags[canvas_id] = tags
            for tag in tags:
                self._tag_ids.setdefault(tag, []).append(canvas_id)
        self._tag_registry_valid = True

    def _ids_with_tag(self, tag_or_id) -> tuple:
        """ canvas ids of the items with this tag or id, from the tag registry when possible """
        if self._is_plain_tag(tag_or_id):
            if not self._tag_registry_valid:
                self._rebuild_tag_registry()
            return tuple(self._tag_ids.get(tag_or_id, ()))
        return super().find_withtag(tag_or_id)

    def tag_exists(self, tag_or_id) -> bool:
        """ like bool(find_withtag(tag_or_id)), but without a Tcl call for normal tags """
        return len(self._ids_with_tag(tag_or_id)) > 0

    def addtag(self, *args):
        super().addtag(*args)
        self._tag_registry_valid = False

    def dtag(self, *args):
        super().dtag(*args)
        self._tag_registry_valid = False

    def itemconfigure(self, tagOrId, cnf=None, **kw):
        if "tags" in kw or (isinstance(cnf, dict) and "tags" in cnf):
            self._tag_registry_valid = False
        return super().itemconfigure(tagOrId, cnf, **kw)

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
            if angle != 0:
                return 0  # the rotated second circle of the font method is not needed for images, so no item is created
            circle_1 = self.create_image(x_pos, y_pos, anchor=anchor, tags=self._tags_to_tuple(tags) + ("ctk_aa_circle_font_element", "ctk_aa_image"))
            self._aa_circle_canvas_ids.add(circle_1)
            self._aa_image_items[circle_1] = {"radius": radius, "fill": fill, "image": None, "empty": False}
            self._update_aa_image(circle_1)
            return circle_1

        # create a circle with a font element
        circle_1 = self.create_text(x_pos, y_pos, text=self._get_char_from_radius(radius), anchor=anchor, fill=fill,
                                    font=("CustomTkinter_shapes_font", -radius * 2), tags=self._tags_to_tuple(tags) + ("ctk_aa_circle_font_element",),
                                    angle=angle)
        self._aa_circle_canvas_ids.add(circle_1)

        return circle_1

    def coords(self, tag_or_id, *args) -> List[float]:

        aa_circle_ids = self._ids_with_tag(tag_or_id) if type(tag_or_id) == str and self._aa_circle_canvas_ids else ()
        if aa_circle_ids and aa_circle_ids[0] in self._aa_circle_canvas_ids:
            coords_id = aa_circle_ids[0]  # take the first item with the given tag
            coords = super().coords(coords_id, *args[:2])

            if len(args) == 3:
                self._set_aa_circle_radius(coords_id, args[2])

        elif type(tag_or_id) == int and tag_or_id in self._aa_circle_canvas_ids:
            coords = super().coords(tag_or_id, *args[:2])

            if len(args) == 3:
                self._set_aa_circle_radius(tag_or_id, args[2])

        elif args:
            # skip the Tcl call if the coordinates of the item didn't change or no item has this tag
            ids = self._ids_with_tag(tag_or_id) if type(tag_or_id) != int else (tag_or_id,)
            if not ids and self._is_plain_tag(tag_or_id):
                return []
            if len(ids) == 1:
                if self._coords_cache.get(ids[0]) == args:
                    return []
                self._coords_cache[ids[0]] = args
            coords = super().coords(tag_or_id, *args)

        else:
            coords = super().coords(tag_or_id, *args)

        return coords

    def move(self, *args):
        self._coords_cache.clear()
        return super().move(*args)

    def moveto(self, *args, **kwargs):
        self._coords_cache.clear()
        return super().moveto(*args, **kwargs)

    def scale(self, *args):
        self._coords_cache.clear()
        return super().scale(*args)

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
        canvas_id = self.create_image(0, 0, anchor=tkinter.NW, tags=self._tags_to_tuple(tags) + ("ctk_aa_image",))
        self._aa_image_items[canvas_id] = {"shape": None, "fill": fill, "image": None, "empty": False}
        self.set_aa_shape(canvas_id, kind, x_pos, y_pos, size, line_width)
        return canvas_id

    def set_aa_shape(self, tag_or_id: Union[str, int], kind: str, x_pos: float, y_pos: float, size: float, line_width: float):
        """ moves and resizes a shape created with create_aa_shape() """
        for canvas_id in self._ids_with_tag(tag_or_id):
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
        deleted_any = False
        for tag_or_id in args:
            for canvas_id in self._ids_with_tag(tag_or_id):
                deleted_any = True
                self._aa_image_items.pop(canvas_id, None)
                self._aa_circle_canvas_ids.discard(canvas_id)
                self._coords_cache.pop(canvas_id, None)
                for tag in self._id_tags.pop(canvas_id, ()):
                    ids = self._tag_ids.get(tag)
                    if ids is not None:
                        if canvas_id in ids:
                            ids.remove(canvas_id)
                        if not ids:
                            del self._tag_ids[tag]
        if deleted_any or not all(self._is_plain_tag(tag_or_id) for tag_or_id in args):
            super().delete(*args)

    def itemconfig(self, tag_or_id, *args, **kwargs):
        if "tags" in kwargs:
            self._tag_registry_valid = False
        configure_ids = self._ids_with_tag(tag_or_id) if type(tag_or_id) != int else (tag_or_id,)
        if not configure_ids:
            return

        special_ids = [canvas_id for canvas_id in configure_ids if canvas_id in self._aa_circle_canvas_ids or canvas_id in self._aa_image_items]
        if not special_ids:
            super().itemconfigure(tag_or_id, *args, **kwargs)  # one Tcl call for all items
            return

        kwargs_except_outline = kwargs.copy()
        if "outline" in kwargs_except_outline:
            del kwargs_except_outline["outline"]
        for canvas_id in special_ids:
            if canvas_id in self._aa_image_items:
                self._itemconfig_aa_image(canvas_id, kwargs)
            else:
                super().itemconfigure(canvas_id, *args, **kwargs_except_outline)  # font shapes

        if len(special_ids) < len(configure_ids):  # normal items
            if self._is_plain_tag(tag_or_id):
                super().itemconfigure(f"{tag_or_id}&&!ctk_aa_circle_font_element&&!ctk_aa_image", *args, **kwargs)
            else:
                for canvas_id in configure_ids:
                    if canvas_id not in self._aa_circle_canvas_ids and canvas_id not in self._aa_image_items:
                        super().itemconfigure(canvas_id, *args, **kwargs)
