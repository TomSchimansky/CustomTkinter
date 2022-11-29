import sys

from .ctk_canvas import CTkCanvas
from .draw_engine import DrawEngine

# determine draw method based on current platform
if sys.platform == "darwin":
    DrawEngine.preferred_drawing_method = "polygon_shapes"
else:
    DrawEngine.preferred_drawing_method = "font_shapes"
