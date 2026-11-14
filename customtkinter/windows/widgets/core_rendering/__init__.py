import sys

from .ctk_canvas import CTkCanvas
from .draw_engine import DrawEngine

CTkCanvas.init_font_character_mapping()

# determine draw method based on current platform
if sys.platform == "darwin":
    DrawEngine.preferred_drawing_method = "polygon_shapes"  # Tk on macOS draws antialiased polygons
elif sys.platform.startswith("linux"):
    DrawEngine.preferred_drawing_method = "image_shapes"  # works with every Tk build, also without Xft
else:
    DrawEngine.preferred_drawing_method = "font_shapes"
