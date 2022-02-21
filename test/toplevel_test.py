import tkinter
import customtkinter
import time

customtkinter.set_appearance_mode("light")


class ExampleApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self.title("main CTk window")
        time.sleep(0.5)
        self.resizable(False, False)

        self.b1 = customtkinter.CTkButton(self, text="Add another window", command=self.newWindow)
        self.b1.pack(side="top", padx=40, pady=40)
        self.c1 = customtkinter.CTkCheckBox(self, text="dark mode", command=self.change_mode)
        self.c1.pack()
        self.count = 0

    def change_mode(self):
        if self.c1.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def newWindow(self):
        self.count += 1

        window = customtkinter.CTkToplevel(self)
        window.configure(bg=("lime", "darkgreen"))
        window.title("CTkToplevel window")
        window.geometry("400x200")
        window.resizable(False, False)

        label = customtkinter.CTkLabel(window, text=f"This is CTkToplevel window number {self.count}")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)


if __name__ == "__main__":
    root = ExampleApp()
    time.sleep(0.5)
    root.mainloop()
