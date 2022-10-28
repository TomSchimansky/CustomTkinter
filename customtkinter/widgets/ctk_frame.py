from typing import Union, Tuple, List

from .core_rendering.ctk_canvas import CTkCanvas
from ..theme_manager import ThemeManager
from .core_rendering.draw_engine import DrawEngine
from .core_widget_classes.widget_base_class import CTkBaseClass


class CTkFrame(CTkBaseClass):
    """
    Frame with rounded corners and border.
    Default foreground colors are set according to theme.
    To make the frame transparent set fg_color=None.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 master: any = None,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Union[int, str] = "default_theme",
                 border_width: Union[int, str] = "default_theme",

                 bg_color: Union[str, Tuple[str, str], None] = None,
                 fg_color: Union[str, Tuple[str, str], None] = "default_theme",
                 border_color: Union[str, Tuple[str, str]] = "default_theme",
                 background_corner_colors: Tuple[Union[str, Tuple[str, str]]] = None,

                 overwrite_preferred_drawing_method: str = None,
                 **kwargs):

        # transfer basic functionality (_bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height, **kwargs)

        # color
        self._border_color = ThemeManager.theme["color"]["frame_border"] if border_color == "default_theme" else border_color

        # determine fg_color of frame
        if fg_color == "default_theme":
            if isinstance(self.master, CTkFrame):
                if self.master._fg_color == ThemeManager.theme["color"]["frame_low"]:
                    self._fg_color = ThemeManager.theme["color"]["frame_high"]
                else:
                    self._fg_color = ThemeManager.theme["color"]["frame_low"]
            else:
                self._fg_color = ThemeManager.theme["color"]["frame_low"]
        else:
            self._fg_color = fg_color

        self._background_corner_colors = background_corner_colors  # rendering options for DrawEngine

        # shape
        self._corner_radius = ThemeManager.theme["shape"]["frame_corner_radius"] if corner_radius == "default_theme" else corner_radius
        self._border_width = ThemeManager.theme["shape"]["frame_border_width"] if border_width == "default_theme" else border_width

        self._canvas = CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._current_width),
                                 height=self._apply_widget_scaling(self._current_height))
        self._canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))
        self._draw_engine = DrawEngine(self._canvas)
        self._overwrite_preferred_drawing_method = overwrite_preferred_drawing_method

        self._draw(no_color_updates=True)

    def winfo_children(self) -> List[any]:
        """
        winfo_children of CTkFrame without self.canvas widget,
        because it's not a child but part of the CTkFrame itself
        """

        child_widgets = super().winfo_children()
        try:
            child_widgets.remove(self._canvas)
            return child_widgets
        except ValueError:
            return child_widgets

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width), height=self._apply_widget_scaling(self._desired_height))
        self._draw()

    def _set_dimensions(self, width=None, height=None):
        super()._set_dimensions(width, height)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw()

    def _draw(self, no_color_updates=False):
        if not self._canvas.winfo_exists():
            return

        if self._background_corner_colors is not None:
            self._draw_engine.draw_background_corners(self._apply_widget_scaling(self._current_width),
                                                      self._apply_widget_scaling(self._current_height))
            self._canvas.itemconfig("background_corner_top_left", fill=self._apply_appearance_mode(self._background_corner_colors[0]))
            self._canvas.itemconfig("background_corner_top_right", fill=self._apply_appearance_mode(self._background_corner_colors[1]))
            self._canvas.itemconfig("background_corner_bottom_right", fill=self._apply_appearance_mode(self._background_corner_colors[2]))
            self._canvas.itemconfig("background_corner_bottom_left", fill=self._apply_appearance_mode(self._background_corner_colors[3]))
        else:
            self._canvas.delete("background_parts")

        requires_recoloring = self._draw_engine.draw_rounded_rect_with_border(self._apply_widget_scaling(self._current_width),
                                                                              self._apply_widget_scaling(self._current_height),
                                                                              self._apply_widget_scaling(self._corner_radius),
                                                                              self._apply_widget_scaling(self._border_width),
                                                                              overwrite_preferred_drawing_method=self._overwrite_preferred_drawing_method)

        if no_color_updates is False or requires_recoloring:
            if self._fg_color is None:
                self._canvas.itemconfig("inner_parts",
                                        fill=self._apply_appearance_mode(self._bg_color),
                                        outline=self._apply_appearance_mode(self._bg_color))
            else:
                self._canvas.itemconfig("inner_parts",
                                        fill=self._apply_appearance_mode(self._fg_color),
                                        outline=self._apply_appearance_mode(self._fg_color))

            self._canvas.itemconfig("border_parts",
                                    fill=self._apply_appearance_mode(self._border_color),
                                    outline=self._apply_appearance_mode(self._border_color))
            self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))

        # self._canvas.tag_lower("inner_parts")  # maybe unnecessary, I don't know ???
        # self._canvas.tag_lower("border_parts")

    def configure(self, require_redraw=False, **kwargs):
        if "fg_color" in kwargs:
            self._fg_color = kwargs.pop("fg_color")
            require_redraw = True

            # check if CTk widgets are children of the frame and change their bg_color to new frame fg_color
            for child in self.winfo_children():
                if isinstance(child, CTkBaseClass):
                    child.configure(bg_color=self._fg_color)

        if "bg_color" in kwargs:
            # pass bg_color change to children if fg_color is None
            if self._fg_color is None:
                for child in self.winfo_children():
                    if isinstance(child, CTkBaseClass):
                        child.configure(bg_color=self._fg_color)

        if "border_color" in kwargs:
            self._border_color = kwargs.pop("border_color")
            require_redraw = True

        if "background_corner_colors" in kwargs:
            self._background_corner_colors = kwargs.pop("background_corner_colors")
            require_redraw = True

        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")
            require_redraw = True

        if "border_width" in kwargs:
            self._border_width = kwargs.pop("border_width")
            require_redraw = True

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "corner_radius":
            return self._corner_radius
        elif attribute_name == "border_width":
            return self._border_width

        elif attribute_name == "fg_color":
            return self._fg_color
        elif attribute_name == "border_color":
            return self._border_color
        elif attribute_name == "background_corner_colors":
            return self._background_corner_colors

        else:
            return super().cget(attribute_name)

    def bind(self, sequence=None, command=None, add=None):
        """ called on the tkinter.Canvas """
        return self._canvas.bind(sequence, command, add)

    def unbind(self, sequence, funcid=None):
        """ called on the tkinter.Canvas """
        return self._canvas.unbind(sequence, funcid)
