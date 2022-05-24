import tkinter
import customtkinter


app = customtkinter.CTk()
app.geometry("400x800")
app.title("CustomTkinter Test")


def change_state(widget):
    if widget.state == tkinter.NORMAL:
        widget.configure(state=tkinter.DISABLED)
    elif widget.state == tkinter.DISABLED:
        widget.configure(state=tkinter.NORMAL)


def widget_click():
    print("widget clicked")


button_1 = customtkinter.CTkButton(master=app, text="button_1", command=widget_click)
button_1.pack(padx=20, pady=(20, 10))
button_2 = customtkinter.CTkButton(master=app, text="Disable/Enable button_1", command=lambda: change_state(button_1))
button_2.pack(padx=20, pady=(10, 20))

switch_1 = customtkinter.CTkSwitch(master=app, text="switch_1", command=widget_click)
switch_1.pack(padx=20, pady=(20, 10))
button_2 = customtkinter.CTkButton(master=app, text="Disable/Enable switch_1", command=lambda: change_state(switch_1))
button_2.pack(padx=20, pady=(10, 20))

entry_1 = customtkinter.CTkEntry(master=app, placeholder_text="entry_1")
entry_1.pack(padx=20, pady=(20, 10))
button_3 = customtkinter.CTkButton(master=app, text="Disable/Enable entry_1", command=lambda: change_state(entry_1))
button_3.pack(padx=20, pady=(10, 20))

checkbox_1 = customtkinter.CTkCheckBox(master=app, text="checkbox_1")
checkbox_1.pack(padx=20, pady=(20, 10))
button_4 = customtkinter.CTkButton(master=app, text="Disable/Enable checkbox_1", command=lambda: change_state(checkbox_1))
button_4.pack(padx=20, pady=(10, 20))

radiobutton_1 = customtkinter.CTkRadioButton(master=app, text="radiobutton_1")
radiobutton_1.pack(padx=20, pady=(20, 10))
button_5 = customtkinter.CTkButton(master=app, text="Disable/Enable entry_1", command=lambda: change_state(radiobutton_1))
button_5.pack(padx=20, pady=(10, 20))


app.mainloop()
