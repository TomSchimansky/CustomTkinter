import tkinter
import customtkinter


class ExampleApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("500x400")

        self.button_1 = customtkinter.CTkButton(self, text="Create CTkToplevel", command=self.create_toplevel)
        self.button_1.pack(side="top", padx=40, pady=40)

    def create_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("400x200")

        label = customtkinter.CTkLabel(window, text="CTkToplevel window")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)


app = ExampleApp()
app.mainloop()