import customtkinter
from customtkinter.windows.ctk_file_dialog import CTkFileDialog
from customtkinter.windows.ctk_path_dialog import CTkPathDialog

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter Dialog Example")
        self.geometry("400x300")

        self.label_file = customtkinter.CTkLabel(self, text="Seleccione un archivo:")
        self.label_file.pack(pady=10)

        self.button_file = customtkinter.CTkButton(self, text="Abrir archivo", command=self.open_file_dialog)
        self.button_file.pack(pady=10)

        self.filepath_label = customtkinter.CTkLabel(self, text="")
        self.filepath_label.pack(pady=10)

        self.label_path = customtkinter.CTkLabel(self, text="Seleccione un directorio:")
        self.label_path.pack(pady=10)

        self.button_path = customtkinter.CTkButton(self, text="Abrir directorio", command=self.open_path_dialog)
        self.button_path.pack(pady=10)

        self.path_label = customtkinter.CTkLabel(self, text="")
        self.path_label.pack(pady=10)

    def open_file_dialog(self):
        dialog = CTkFileDialog(self)
        filepath = dialog.open_file_dialog()
        if filepath:
            self.filepath_label.configure(text=f"Archivo seleccionado: {filepath}")

    def open_path_dialog(self):
        dialog = CTkPathDialog(self)
        path = dialog.open_path_dialog()
        if path:
            self.path_label.configure(text=f"Directorio seleccionado: {path}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
