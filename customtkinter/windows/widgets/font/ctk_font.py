from tkinter.font import Font
import copy
from typing import List, Callable, Tuple, Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from ..theme import ThemeManager


class CTkFont(Font):
    """
    Font object with size in pixel, independent of scaling.
    To get scaled tuple representation use create_scaled_tuple() method.

    family	The font family name as a string.
    size	The font height as an integer in pixel.
    weight	'bold' for boldface, 'normal' for regular weight.
    slant	'italic' for italic, 'roman' for unslanted.
    underline	1 for underlined text, 0 for normal.
    overstrike	1 for overstruck text, 0 for normal.

    Tkinter Font: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/fonts.html
    """

    def __init__(self,
                 family: Optional[str] = None,
                 size: Optional[int] = None,
                 weight: Literal["normal", "bold"] = None,
                 slant: Literal["italic", "roman"] = "roman",
                 underline: bool = False,
                 overstrike: bool = False):

        self._size_configure_callback_list: List[Callable] = []

        self._size = ThemeManager.theme["CTkFont"]["size"] if size is None else size

        super().__init__(family=ThemeManager.theme["CTkFont"]["family"] if family is None else family,
                         size=-abs(self._size),
                         weight=ThemeManager.theme["CTkFont"]["weight"] if weight is None else weight,
                         slant=slant,
                         underline=underline,
                         overstrike=overstrike)

        self._family = super().cget("family")
        self._tuple_style_string = f"{super().cget('weight')} {slant} {'underline' if underline else ''} {'overstrike' if overstrike else ''}"

    def add_size_configure_callback(self, callback: Callable):
        """ add function, that gets called when font got configured """
        self._size_configure_callback_list.append(callback)

    def remove_size_configure_callback(self, callback: Callable):
        """ remove function, that gets called when font got configured """
        try:
            self._size_configure_callback_list.remove(callback)
        except ValueError:
            pass

    def create_scaled_tuple(self, font_scaling: float) -> Tuple[str, int, str]:
        """ return scaled tuple representation of font in the form (family: str, size: int, style: str)"""
        return self._family, round(-abs(self._size) * font_scaling), self._tuple_style_string

    def config(self, *args, **kwargs):
        raise AttributeError("'config' is not implemented for CTk widgets. For consistency, always use 'configure' instead.")

    def configure(self, **kwargs):
        if "size" in kwargs:
            self._size = kwargs.pop("size")
            super().configure(size=-abs(self._size))

        if "family" in kwargs:
            super().configure(family=kwargs.pop("family"))
            self._family = super().cget("family")

        super().configure(**kwargs)

        # update style string for create_scaled_tuple() method
        self._tuple_style_string = f"{super().cget('weight')} {super().cget('slant')} {'underline' if super().cget('underline') else ''} {'overstrike' if super().cget('overstrike') else ''}"

        # call all functions registered with add_size_configure_callback()
        for callback in self._size_configure_callback_list:
            callback()

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "size":
            return self._size
        if attribute_name == "family":
            return self._family
        else:
            return super().cget(attribute_name)

    def copy(self) -> "CTkFont":
        return copy.deepcopy(self)
