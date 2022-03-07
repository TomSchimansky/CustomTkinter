import customtkinter
import tkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x300")
app.title("CTkDialog Test")


def change_mode():
    if customtkinter.get_appearance_mode().lower() == "dark":
        customtkinter.set_appearance_mode("light")
    elif customtkinter.get_appearance_mode().lower() == "light":
        customtkinter.set_appearance_mode("dark")


def button_click_event():
    dialog = customtkinter.CTkInputDialog(master=None, text="Type in a number:", title="Test")
    print("Number:", dialog.get_input())


button = customtkinter.CTkButton(app, text="Open Dialog", command=button_click_event)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
c1 = customtkinter.CTkCheckBox(app, text="dark mode", command=change_mode)
c1.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

app.mainloop()