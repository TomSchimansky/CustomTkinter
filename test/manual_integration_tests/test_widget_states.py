import tkinter
import customtkinter


root_tk = customtkinter.CTk()
root_tk.geometry("400x800")
root_tk.title("CustomTkinter Test")


def change_state(widget):
    if widget.state == tkinter.NORMAL:
        widget.configure(state=tkinter.DISABLED)
    elif widget.state == tkinter.DISABLED:
        widget.configure(state=tkinter.NORMAL)


def widget_click():
    print("widget clicked")


button_1 = customtkinter.CTkButton(master=root_tk, text="button_1", command=widget_click)
button_1.pack(padx=20, pady=(20, 10))
button_2 = customtkinter.CTkButton(master=root_tk, text="Disable/Enable button_1", command=lambda: change_state(button_1))
button_2.pack(padx=20, pady=(10, 20))

switch_1 = customtkinter.CTkSwitch(master=root_tk, text="switch_1", command=widget_click)
switch_1.pack(padx=20, pady=(20, 10))
button_2 = customtkinter.CTkButton(master=root_tk, text="Disable/Enable switch_1", command=lambda: change_state(switch_1))
button_2.pack(padx=20, pady=(10, 20))

entry_1 = customtkinter.CTkEntry(master=root_tk, placeholder_text="entry_1")
entry_1.pack(padx=20, pady=(20, 10))
button_3 = customtkinter.CTkButton(master=root_tk, text="Disable/Enable entry_1", command=lambda: change_state(entry_1))
button_3.pack(padx=20, pady=(10, 20))

checkbox_1 = customtkinter.CTkCheckBox(master=root_tk, text="checkbox_1")
checkbox_1.pack(padx=20, pady=(20, 10))
button_4 = customtkinter.CTkButton(master=root_tk, text="Disable/Enable checkbox_1", command=lambda: change_state(checkbox_1))
button_4.pack(padx=20, pady=(10, 20))

radiobutton_1 = customtkinter.CTkRadioButton(master=root_tk, text="radiobutton_1")
radiobutton_1.pack(padx=20, pady=(20, 10))
button_5 = customtkinter.CTkButton(master=root_tk, text="Disable/Enable entry_1", command=lambda: change_state(radiobutton_1))
button_5.pack(padx=20, pady=(10, 20))


root_tk.mainloop()
