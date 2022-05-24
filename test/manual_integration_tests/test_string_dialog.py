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


def button_click_event():
    dialog = customtkinter.CTkInputDialog(master=None, text="Type in a number:", title="Test")
    print("Number:", dialog.get_input())


button = customtkinter.CTkButton(app, text="Open Dialog", command=button_click_event)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
c1 = customtkinter.CTkCheckBox(app, text="dark mode", command=change_mode)
c1.place(relx=0.5, rely=0.8, anchor=customtkinter.CENTER)

app.mainloop()
