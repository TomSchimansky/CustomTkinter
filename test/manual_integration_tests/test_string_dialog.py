import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x300")
app.title("CTkDialog Test")


def change_mode():
    if c1.get() == 0:
        customtkinter.set_appearance_mode("light")
    else:
        customtkinter.set_appearance_mode("dark")


def button_1_click_event():
    dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
    print("Number:", dialog.get_input())


def button_2_click_event():
    dialog = customtkinter.CTkInputDialog(text="long text "*100, title="Test")
    print("Number:", dialog.get_input())


button_1 = customtkinter.CTkButton(app, text="Open Dialog", command=button_1_click_event)
button_1.pack(pady=20)
button_2 = customtkinter.CTkButton(app, text="Open Dialog", command=button_2_click_event)
button_2.pack(pady=20)
c1 = customtkinter.CTkCheckBox(app, text="dark mode", command=change_mode)
c1.pack(pady=20)

app.mainloop()
