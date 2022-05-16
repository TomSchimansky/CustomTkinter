import tkinter
import customtkinter

root_tk = customtkinter.CTk()
root_tk.geometry("400x240")


def button_function():

    top = customtkinter.CTkToplevel(root_tk)

    root_tk.after(1000, top.iconify)  # hide toplevel
    root_tk.after(1500, top.deiconify)  # show toplevel
    root_tk.after(2500, root_tk.iconify)  # hide root_tk
    root_tk.after(3000, root_tk.deiconify)  # show root_tk
    root_tk.after(4000, root_tk.destroy)  # destroy everything


button = customtkinter.CTkButton(root_tk, command=button_function)
button.pack(pady=20, padx=20)

root_tk.mainloop()