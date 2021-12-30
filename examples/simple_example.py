import tkinter
import customtkinter  # <- import the CustomTkinter module

customtkinter.enable_macos_darkmode()

root_tk = tkinter.Tk()  # create the Tk window like you normally do
root_tk.geometry("400x300")
root_tk.title("CustomTkinter Test")

customtkinter.set_appearance_mode("System")  # Other: "Dark", "Light"


def button_function():
    print("Button click")


def slider_function(value):
    progressbar_1.set(value)


def check_box_function():
    print("checkbox_1:", checkbox_1.get())


frame_1 = customtkinter.CTkFrame(master=root_tk, width=300, height=260, corner_radius=15)
frame_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

label_1 = customtkinter.CTkLabel(master=frame_1)
label_1.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
progressbar_1.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=10, command=button_function)
button_1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
# button_1.configure(state="disabled")

slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_function, from_=0, to=1, progress_color="gray20")
slider_1.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
slider_1.set(1.5)

entry_1 = customtkinter.CTkEntry(master=frame_1)
entry_1.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

checkbox_1 = customtkinter.CTkCheckBox(master=frame_1, command=check_box_function)
checkbox_1.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

root_tk.mainloop()
customtkinter.disable_macos_darkmode()
