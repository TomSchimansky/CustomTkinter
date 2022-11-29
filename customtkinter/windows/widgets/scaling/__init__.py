import sys

from .scaling_base_class import CTkScalingBaseClass
from .scaling_tracker import ScalingTracker

if sys.platform.startswith("win") and sys.getwindowsversion().build < 9000:  # No automatic scaling on Windows < 8.1
    ScalingTracker.deactivate_automatic_dpi_awareness = True
