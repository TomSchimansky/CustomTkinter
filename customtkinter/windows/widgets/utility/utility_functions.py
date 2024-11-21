
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


def get_root_window(self):
    widget = self
    while widget.master is not None:
        widget = widget.master
    return widget


def handle_root_click(widget, event, specific_widget=None):
    """
    Handle a click event on the root window for a given widget.

    :param widget: The widget to check the click event for.
    :param event: The click event.
    :param specific_widget: An optional specific widget within the main widget to check for focus.
    """
    def get_root_window(w):
        """Find the root window of the widget."""
        while w.master is not None:
            w = w.master
        return w

    def is_click_inside(w, evt):
        """Check if the click event occurred inside the widget's area."""
        x1, y1, x2, y2 = w.winfo_rootx(), w.winfo_rooty(), w.winfo_rootx() + w.winfo_width(), w.winfo_rooty() + w.winfo_height()
        return x1 <= evt.x_root <= x2 and y1 <= evt.y_root <= y2

    try:
        root_window = get_root_window(widget)
        focus_widget = specific_widget if specific_widget else widget

        if not is_click_inside(widget, event) and root_window.focus_get() == focus_widget:
            root_window.focus_set()
    except Exception as e:
        print(f"Error in handle_root_click: {e}")
