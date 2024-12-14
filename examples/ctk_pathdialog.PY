import customtkinter
from customtkinter.windows.ctk_path_dialog import CTkPathDialog

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter Dialog Example")
        self.geometry("400x300")

        self.label_path = customtkinter.CTkLabel(self, text="Select a directory:")
        self.label_path.pack(pady=10)

        self.button_path = customtkinter.CTkButton(self, text="Open directory", command=self.open_path_dialog)
        self.button_path.pack(pady=10)

        self.path_label = customtkinter.CTkLabel(self, text="")
        self.path_label.pack(pady=10)

    def open_path_dialog(self):
        dialog = CTkPathDialog(self)
        path = dialog.open_path_dialog()
        if path:
            self.path_label.configure(text=f"Directory selected: {path}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
