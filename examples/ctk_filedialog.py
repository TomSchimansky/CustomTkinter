import customtkinter
from customtkinter.windows.ctk_file_dialog import CTkFileDialog

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter filedialog Example")
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Seleccione un archivo:")
        self.label.pack(pady=20)

        self.button = customtkinter.CTkButton(self, text="Abrir archivo", command=self.open_custom_file_dialog)
        self.button.pack(pady=20)

        self.filepath_label = customtkinter.CTkLabel(self, text="")
        self.filepath_label.pack(pady=20)

    def open_custom_file_dialog(self):
        dialog = CTkFileDialog(self)
        filepath = dialog.open_file_dialog()
        if filepath:
            self.filepath_label.configure(text=f"Archivo seleccionado: {filepath}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
