from typing import Union
from tkinter import filedialog


class CTkPathDialog:
    """
    Dialog to open a directory dialog and return the selected directory path.
    """

    def __init__(
        self,
        master=None,
        title: str = "CTkPathDialog"
    ):
        self.master = master
        self._title = title
        self._path: Union[str, None] = None

    def open_path_dialog(self) -> str:
        """
        Open the directory dialog and return the selected directory path.

        Returns:
            str: Selected directory path.
        """
        self._path = filedialog.askdirectory(title=self._title)
        return self._path
