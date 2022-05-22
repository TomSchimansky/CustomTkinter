import tkinter
import customtkinter


root_tk = customtkinter.CTk()
root_tk.geometry("400x240")
root_tk.title("CustomTkinter Test")


def change_state(widget):
    if widget.state == tkinter.NORMAL:
        widget.configure(state=tkinter.DISABLED)
    elif widget.state == tkinter.DISABLED:
        widget.configure(state=tkinter.NORMAL)


def button_2_click():
    print("button_2 clicked")


button_1 = customtkinter.CTkButton(master=root_tk, text="button_1", command=button_2_click)
button_1.pack(padx=20, pady=10)
button_2 = customtkinter.CTkButton(master=root_tk, text="Disable/Enable button_1", command=lambda: change_state(button_1))
button_2.pack(padx=20, pady=10)

switch_1 = customtkinter.CTkSwitch(master=root_tk, text="switch_1", command=button_2_click)
switch_1.pack(padx=20, pady=10)
switch_2 = customtkinter.CTkSwitch(master=root_tk, text="Disable/Enable switch_1", command=lambda: change_state(switch_1))
switch_2.pack(padx=20, pady=10)

root_tk.mainloop()
