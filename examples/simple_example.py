import tkinter
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x480")
app.title("CustomTkinter simple_example.py")


def button_function():
    print("Button click", label_1.text_label.cget("text"))


def slider_function(value):
    progressbar_1.set(value)


def check_box_function():
    print("checkbox_1:", checkbox_1.get())


y_padding = 13

frame_1 = customtkinter.CTkFrame(master=app, corner_radius=15)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT)
label_1.pack(pady=y_padding, padx=10)

progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
progressbar_1.pack(pady=y_padding, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=8, command=button_function)
button_1.pack(pady=y_padding, padx=10)

slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_function, from_=0, to=1)
slider_1.pack(pady=y_padding, padx=10)
slider_1.set(0.5)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="CTkEntry")
entry_1.pack(pady=y_padding, padx=10)

checkbox_1 = customtkinter.CTkCheckBox(master=frame_1, command=check_box_function)
checkbox_1.pack(pady=y_padding, padx=10)

radiobutton_var = tkinter.IntVar(value=1)

radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=1)
radiobutton_1.pack(pady=y_padding, padx=10)

radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=2)
radiobutton_2.pack(pady=y_padding, padx=10)

s_var = tkinter.StringVar(value="on")

switch_1 = customtkinter.CTkSwitch(master=frame_1)
switch_1.pack(pady=y_padding, padx=10)

app.mainloop()
