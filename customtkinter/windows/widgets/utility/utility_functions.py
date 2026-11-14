import sys
import tkinter
from typing import Tuple


def pop_from_dict_by_set(dictionary: dict, valid_keys: set) -> dict:
    """ remove and create new dict with key value pairs of dictionary, where key is in valid_keys """
    new_dictionary = {}

    for key in list(dictionary.keys()):
        if key in valid_keys:
            new_dictionary[key] = dictionary.pop(key)

    return new_dictionary


def check_kwargs_empty(kwargs_dict, raise_error=False) -> bool:
    """ returns True if kwargs are empty, False otherwise, raises error if not empty """

    if len(kwargs_dict) > 0:
        if raise_error:
            raise ValueError(f"{list(kwargs_dict.keys())} are not supported arguments. Look at the documentation for supported arguments.")
        else:
            return True
    else:
        return False


# Tk 8.7 and newer send <MouseWheel> for the mouse wheel on Linux (X11), older versions send <Button-4> and <Button-5>.
# Tk 9 sends <TouchpadScroll> instead of <MouseWheel> for two-finger scrolling on Windows and macOS.
WHEEL_USES_BUTTON_EVENTS = sys.platform.startswith("linux") and tkinter.TkVersion < 8.7
HAS_TOUCHPAD_SCROLL_EVENT = tkinter.TkVersion >= 9.0 and not sys.platform.startswith("linux")


def wheel_event_steps(event) -> int:
    """ returns the number of wheel steps of a <MouseWheel> or <Button-4>/<Button-5> event, positive is upwards """
    if event.num == 4:
        return 1
    if event.num == 5:
        return -1
    if sys.platform.startswith("linux") or sys.platform.startswith("win"):
        # one step of the wheel has a delta of 120, high resolution wheels send smaller values
        steps = int(event.delta / 120)
        return steps if steps != 0 else (1 if event.delta > 0 else -1)
    return event.delta  # macOS: one step has a delta of 1


def touchpad_scroll_deltas(event) -> Tuple[int, int]:
    """ unpacks the x and y delta of a <TouchpadScroll> event (two signed 16 bit values) """
    def signed_16(value):
        return value - 0x10000 if value & 0x8000 else value
    return signed_16((event.delta >> 16) & 0xffff), signed_16(event.delta & 0xffff)
