from typing import Union, Optional
from tkinter import filedialog


class CTkFileDialog:
    """
    Dialog to open a file dialog and return the selected file path.
    """

    def __init__(
        self,
        master=None,
        title: str = "CTkFileDialog",
        filetypes: Optional[list] = None
    ):
        self.master = master
        self._title = title
        self._filetypes = filetypes if filetypes else [("Text files", "*.txt"), ("All files", "*.*")]
        self._file_path: Union[str, None] = None

    def open_file_dialog(self) -> str:
        """
        Open the file dialog and return the selected file path.
        
        Returns:
            str: Selected file path.
        """
        self._file_path = filedialog.askopenfilename(title=self._title, filetypes=self._filetypes)
        return self._file_path