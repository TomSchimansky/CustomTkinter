import os
import sys
import tempfile
import atexit

from .ctk_font import CTkFont
from .font_manager import FontManager
from .fonts import Font

# import DrawEngine to set preferred_drawing_method if loading shapes font fails
from ..core_rendering import DrawEngine

FontManager.init_font_manager()

# load Roboto fonts (used on Windows/Linux)
#customtkinter_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
with tempfile.TemporaryFile(suffix=".ttf") as f:
    f.write(Font("Roboto-Regular.ttf"))
    f.close()
    FontManager.load_font(f.name)
with tempfile.TemporaryFile(suffix=".ttf") as f:
    f.write(Font("Roboto-Medium.ttf"))
    f.close()
    FontManager.load_font(f.name)
font_to_delete = ""
# load font necessary for rendering the widgets (used on Windows/Linux)
with tempfile.TemporaryFile(suffix=".otf", delete=False) as f:
    f.write(Font("CustomTkinter_shapes_font.otf"))
    f.close()
    font_to_delete = f.name
    if FontManager.load_font(f.name) is False:
        # change draw method if font loading failed
        if DrawEngine.preferred_drawing_method == "font_shapes":
            sys.stderr.write("customtkinter.windows.widgets.font warning: " +
                            "Preferred drawing method 'font_shapes' can not be used because the font file could not be loaded.\n" +
                            "Using 'circle_shapes' instead. The rendering quality will be bad!\n")
            DrawEngine.preferred_drawing_method = "circle_shapes"

def exit_handler():
    try:
        os.unlink(font_to_delete)
    except:
        pass

atexit.register(exit_handler)