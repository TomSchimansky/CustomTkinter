import tkinter
import customtkinter

TEST_CONFIGURE = True
TEST_REMOVING = False

app = customtkinter.CTk()  # create CTk window like you do with the Tk window (you can also use normal tkinter.Tk window)
app.geometry("400x900")
app.title("Tkinter Variable Test")

def checkbox_event():
    print("checkbox_event")

txt_var = tkinter.StringVar(value="")
entry_1 = customtkinter.CTkEntry(app, width=200, textvariable=txt_var, placeholder_text="placeholder")
entry_1.pack(pady=15)
txt_var.set("new text test")
if TEST_CONFIGURE: entry_1.configure(textvariable=txt_var)
if TEST_REMOVING: entry_1.configure(textvariable="")
#entry_1.delete(0, "end")
#entry_1.insert(0, "sadsad")

label_1 = customtkinter.CTkLabel(app, width=200, textvariable=txt_var)
label_1.pack(pady=15)
if TEST_CONFIGURE: label_1.configure(textvariable=txt_var)
if TEST_REMOVING: label_1.configure(textvariable="")

button_1 = customtkinter.CTkButton(app, width=200, textvariable=txt_var)
button_1.pack(pady=15)
int_var = tkinter.IntVar(value=10)
if TEST_CONFIGURE: button_1.configure(textvariable=int_var)
if TEST_REMOVING: button_1.configure(textvariable="")

slider_1 = customtkinter.CTkSlider(app, width=200, from_=0, to=3, variable=int_var)
slider_1.pack(pady=15)
if TEST_CONFIGURE: slider_1.configure(variable=int_var)
if TEST_REMOVING: slider_1.configure(variable="")
int_var.set(2)

slider_2 = customtkinter.CTkSlider(app, width=200, from_=0, to=3, variable=int_var)
slider_2.pack(pady=15)
if TEST_CONFIGURE: slider_2.configure(variable=int_var)
if TEST_REMOVING: slider_2.configure(variable="")

label_2 = customtkinter.CTkLabel(app, width=200, textvariable=int_var)
label_2.pack(pady=15)

progress_1 = customtkinter.CTkProgressBar(app, width=200, variable=int_var)
progress_1.pack(pady=15)
if TEST_CONFIGURE: progress_1.configure(variable=int_var)
if TEST_REMOVING: progress_1.configure(variable="")

check_var = tkinter.StringVar(value="on")
check_1 = customtkinter.CTkCheckBox(app, text="check 1", variable=check_var, onvalue="on", offvalue="off", textvariable=txt_var,
                                    command=checkbox_event)
check_1.pack(pady=15)
if TEST_CONFIGURE: check_1.configure(variable=check_var)
if TEST_REMOVING: check_1.configure(variable="")

print("check 1 created")

check_2 = customtkinter.CTkCheckBox(app, text="check 2", variable=check_var, onvalue="on", offvalue="off")
check_2.pack(pady=15)
if TEST_CONFIGURE: check_2.configure(variable=check_var)
if TEST_REMOVING: check_2.configure(variable="")

label_3 = customtkinter.CTkLabel(app, width=200, textvariable=check_var)
label_3.pack(pady=15)
label_3.configure(textvariable=check_var)

def switch_event():
    print("switch event")

s_var = tkinter.StringVar(value="on")
switch_1 = customtkinter.CTkSwitch(master=app, variable=s_var, textvariable=s_var, onvalue="on", offvalue="off", command=switch_event)
switch_1.pack(pady=20, padx=10)
switch_2 = customtkinter.CTkSwitch(master=app, variable=s_var, textvariable=s_var, onvalue="on", offvalue="off")
switch_2.pack(pady=20, padx=10)

optionmenu_var = tkinter.StringVar(value="test")
optionmenu_1 = customtkinter.CTkOptionMenu(master=app, variable=None, values=["Option 1", "Option 2", "Option 3"])
optionmenu_1.pack(pady=20, padx=10)
optionmenu_1.configure(variable=optionmenu_var)
combobox_1 = customtkinter.CTkComboBox(master=app, values=["Option 1", "Option 2", "Option 3"])
combobox_1.pack(pady=20, padx=10)
combobox_1.configure(variable=optionmenu_var)

radio_1 = customtkinter.CTkRadioButton(app, textvariable=txt_var)
radio_1.pack(pady=20, padx=10)

app.mainloop()
