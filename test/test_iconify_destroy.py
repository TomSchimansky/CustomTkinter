import tkinter
import customtkinter

root_tk = customtkinter.CTk()
root_tk.geometry("400x240")

def button_function():
    root_tk.iconify()
    root_tk.after(1000, root_tk.deiconify)
    root_tk.after(2000, root_tk.destroy)

frame = tkinter.Frame()
frame.pack(padx=10, pady=10, expand=True, fill="both")

button = customtkinter.CTkButton(frame, command=button_function)
button.pack(pady=20, padx=20)

root_tk.mainloop()