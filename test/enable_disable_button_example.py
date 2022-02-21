import tkinter
import customtkinter  # <- import the CustomTkinter module

customtkinter.set_appearance_mode("System")  # Other: "Dark", "Light"

root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window (you can also use normal tkinter.Tk window)
root_tk.geometry("400x240")
root_tk.title("CustomTkinter Test")


def change_button_2_state():
    if button_2.state == tkinter.NORMAL:
        button_2.configure(state=tkinter.DISABLED)
    elif button_2.state == tkinter.DISABLED:
        button_2.configure(state=tkinter.NORMAL)


def button_2_click():
    print("button_2 clicked")


frame_1 = customtkinter.CTkFrame(master=root_tk, width=300, height=200, corner_radius=15)
frame_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

button_1 = customtkinter.CTkButton(master=frame_1, text="Disable/Enable Button_2",
                                   corner_radius=10, command=change_button_2_state, width=200)
button_1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

button_2 = customtkinter.CTkButton(master=frame_1, text="Button_2",
                                   corner_radius=10, command=button_2_click)
button_2.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

root_tk.mainloop()
