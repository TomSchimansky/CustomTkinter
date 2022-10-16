from tkinter.font import Font
import copy
import sys

from ..scaling_tracker import ScalingTracker
from ..theme_manager import ThemeManager


class CTkFont(Font):
    """
    Font object with size in pixel independent of scaling.
    """
    def __init__(self,
                 family: str = "default_theme",
                 size: int = "default_theme",
                 weight: str = "normal",
                 slant: str = "roman",
                 underline: bool = False,
                 overstrike: bool = False):

        # unscaled font size in px
        self._size = ThemeManager.theme["text"]["size"] if size == "default_theme" else size

        if self._size < 0:
            sys.stderr.write(f"Warning: size {self._size} of CTkFont don't has to be negative, it's measured in pixel by default\n")

        super().__init__(family=ThemeManager.theme["text"]["font"] if family == "default_theme" else family,
                         size=self._size,
                         weight=weight,
                         slant=slant,
                         underline=underline,
                         overstrike=overstrike)

    def _set_scaling(self, new_widget_scaling, new_spacing_scaling, new_window_scaling):
        self._widget_scaling = new_widget_scaling
        super().configure(size=round(self._apply_widget_scaling(self._size)))

    def _apply_widget_scaling(self, value: int) -> int:
        if isinstance(value, int):
            return round(value * self._widget_scaling)
        else:
            raise ValueError(f"CTkFont can not scale size of type {type(value)}, only int allowed")

    def _reverse_widget_scaling(self, value: int) -> int:
        if isinstance(value, int):
            return round(value / self._widget_scaling)
        else:
            raise ValueError(f"CTkFont can not scale size of type {type(value)}, only int allowed")

    def config(self, *args, **kwargs):
        raise AttributeError("'config' is not implemented for CTk widgets. For consistency, always use 'configure' instead.")

    def configure(self, **kwargs):
        if "size" in kwargs:
            self._size = kwargs.pop("size")
            super().configure(size=self._apply_widget_scaling(self._size))

        super().configure(**kwargs)

    def cget(self, attribute_name) -> any:
        if attribute_name == "size":
            return self._size
        else:
            super().cget(attribute_name)

    def copy(self) -> "CTkFont":
        return copy.deepcopy(self)

    def measure(self, text, displayof=None) -> int:
        """ measure width of text in px independent of scaling  """
        return self._reverse_widget_scaling(super().measure(text, displayof=displayof))

    def metrics(self, *options: any, **kw: any) -> dict:
        """ metrics of font, all values independent of scaling """
        metrics_dict = super().metrics(*options, **kw)

        if "ascent" in metrics_dict:
            metrics_dict["ascent"] = self._reverse_widget_scaling(metrics_dict["ascent"])
        if "descent" in metrics_dict:
            metrics_dict["descent"] = self._reverse_widget_scaling(metrics_dict["descent"])
        if "linespace" in metrics_dict:
            metrics_dict["linespace"] = self._reverse_widget_scaling(metrics_dict["linespace"])

        return metrics_dict

    def actual(self, option: any = None, displayof: any = None) -> dict:
        """ get back a dictionary of the font's actual attributes, which may differ from the ones you requested, size independent of scaling """
        actual_dict = super().actual(option, displayof)

        if "size" in actual_dict:
            actual_dict["size"] = self._reverse_widget_scaling(actual_dict["size"])

        return actual_dict

