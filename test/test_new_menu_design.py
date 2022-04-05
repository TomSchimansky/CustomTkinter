import customtkinter
import tkinter

# customtkinter.set_appearance_mode("light")

root_tk = customtkinter.CTk()
root_tk.geometry("600x500")

menu = tkinter.Menu(tearoff=0, bd=0, relief=tkinter.FLAT, activeforeground="red")
menu.add_command(label="System")
menu.add_command(label="Light")
menu.add_command(label="Dark")


class CTkMenu(tkinter.Toplevel):
    def __init__(self, master, x, y, options):
        super().__init__(bg="black")
        super().overrideredirect(True)
        #self.wm_attributes("-transparentcolor", "black")
        super().geometry(f"120x{len(options) * (25 + 4) + 4}+{x}+{y}")
        super().lift()
        super().transient(master)
        self.resizable(False, False)
        super().focus_force()
        self.focus()

        self.frame = customtkinter.CTkFrame(self, border_width=0, width=120, corner_radius=10, border_color="gray4", fg_color="#333740")
        self.frame.grid(row=0, column=0, sticky="nsew", rowspan=len(options) + 2, columnspan=1)

        self.frame.grid_rowconfigure(0, minsize=2)
        self.frame.grid_rowconfigure(len(options) + 1, minsize=2)

        self.grid_columnconfigure(0, weight=1)

        self.buttons = []
        for index, option in enumerate(options):
            button = customtkinter.CTkButton(self.frame, height=25, width=108, fg_color="#333740", text_color="gray74", hover_color="#272A2E", corner_radius=8)
            button.text_label.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="w")
            button.grid(row=index + 1, column=0, padx=4, pady=2)
            self.buttons.append(button)

        # master.bind("<Configure>", self.window_drag())




def open_menu():
    menu = CTkMenu(root_tk, button.winfo_rootx(), button.winfo_rooty() + button.winfo_height() + 4, ["Option 1", "Option 2", "Point 3"])

button = customtkinter.CTkButton(command=open_menu, height=50)
button.pack(pady=20)

root_tk.mainloop()
