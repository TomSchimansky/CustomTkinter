import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("dark")


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("test filedialog")

        self.button_1 = customtkinter.CTkButton(master=self, text="askopenfile", command=lambda: print(customtkinter.filedialog.askopenfile()))
        self.button_1.pack(pady=10)
        self.button_2 = customtkinter.CTkButton(master=self, text="askopenfiles", command=lambda: print(customtkinter.filedialog.askopenfiles()))
        self.button_2.pack(pady=10)
        self.button_3 = customtkinter.CTkButton(master=self, text="askdirectory", command=lambda: print(customtkinter.filedialog.askdirectory()))
        self.button_3.pack(pady=10)
        self.button_4 = customtkinter.CTkButton(master=self, text="asksaveasfile", command=lambda: print(customtkinter.filedialog.asksaveasfile()))
        self.button_4.pack(pady=10)
        self.button_5 = customtkinter.CTkButton(master=self, text="askopenfilename", command=lambda: print(customtkinter.filedialog.askopenfilename()))
        self.button_5.pack(pady=10)
        self.button_6 = customtkinter.CTkButton(master=self, text="askopenfilenames", command=lambda: print(customtkinter.filedialog.askopenfilenames()))
        self.button_6.pack(pady=10)
        self.button_7 = customtkinter.CTkButton(master=self, text="asksaveasfilename", command=lambda: print(customtkinter.filedialog.asksaveasfilename()))
        self.button_7.pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
