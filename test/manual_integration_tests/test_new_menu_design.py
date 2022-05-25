import customtkinter
import tkinter
import sys


class CTkMenu(tkinter.Toplevel):
    def __init__(self, master, x, y, options):
        super().__init__()

        self.overrideredirect(True)
        self.geometry(f"120x{len(options) * (25 + 3) + 3}+{x}+{y}")

        if sys.platform.startswith("darwin"):
            self.overrideredirect(False)
            self.wm_attributes("-transparent", True)  # turn off shadow
            self.config(bg='systemTransparent')  # transparent bg
            self.frame = customtkinter.CTkFrame(self, border_width=0, width=120, corner_radius=6, border_color="gray4", fg_color="#333740")
        elif sys.platform.startswith("win"):
            self.configure(bg="#FFFFF1")
            self.wm_attributes("-transparent", "#FFFFF1")
            self.focus()
            self.frame = customtkinter.CTkFrame(self, border_width=0, width=120, corner_radius=6, border_color="gray4", fg_color="#333740",
                                                overwrite_preferred_drawing_method="circle_shapes")
        else:
            self.configure(bg="#FFFFF1")
            self.wm_attributes("-transparent", "#FFFFF1")
            self.frame = customtkinter.CTkFrame(self, border_width=0, width=120, corner_radius=6, border_color="gray4", fg_color="#333740",
                                                overwrite_preferred_drawing_method="circle_shapes")

        self.frame.grid(row=0, column=0, sticky="nsew", rowspan=len(options) + 1, columnspan=1, ipadx=0, ipady=0)

        self.frame.grid_rowconfigure(len(options) + 1, minsize=3)
        self.frame.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.buttons = []
        for index, option in enumerate(options):
            button = customtkinter.CTkButton(self.frame, text=option, height=25, width=108, fg_color="#333740", text_color="gray74",
                                             hover_color="gray28", corner_radius=4, command=self.button_click)
            button.text_label.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="w")
            button.grid(row=index, column=0, padx=(3, 3), pady=(3, 0), columnspan=1, rowspan=1, sticky="ew")
            self.buttons.append(button)

        self.bind("<FocusOut>", self.focus_loss_event)
        self.frame.canvas.bind("<Button-1>", self.focus_loss_event)

    def focus_loss_event(self, event):
        print("focus loss")
        self.destroy()
        # self.update()

    def button_click(self):
        print("button press")
        self.destroy()
        # self.update()


app = customtkinter.CTk()
app.geometry("600x500")


def open_menu():
    menu = CTkMenu(app, button.winfo_rootx(), button.winfo_rooty() + button.winfo_height() + 4, ["Option 1", "Option 2", "Point 3"])

button = customtkinter.CTkButton(command=open_menu, height=30, corner_radius=6)
button.pack(pady=20)

button_2 = customtkinter.CTkButton(command=open_menu, height=30, corner_radius=6)
button_2.pack(pady=60)

app.mainloop()
