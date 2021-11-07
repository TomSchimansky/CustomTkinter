import tkinter
import customtkinter  # <- import the CustomTkinter module
from PIL import Image, ImageTk  # <- import PIL for the images
import os

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.enable_macos_darkmode()
customtkinter.set_appearance_mode("System")  # Other: "Dark", "Light"

root_tk = tkinter.Tk()  # create the Tk window like you normally do
root_tk.geometry("400x400")
root_tk.title("CustomTkinter Test")


def button_function():
    print("button pressed")


# load images as PhotoImage
settings_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/settings.png").resize((40, 40)))
bell_image     = ImageTk.PhotoImage(Image.open(PATH + "/test_images/bell.png").resize((40, 40)))

frame_1 = customtkinter.CTkFrame(master=root_tk, width=300, height=350, corner_radius=15)
frame_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# button with settings-image and no text
button_1 = customtkinter.CTkButton(master=frame_1, image=bell_image, text="", width=60, height=60,
                                   corner_radius=10, command=button_function)
button_1.place(relx=0.1, rely=0.2, anchor=tkinter.W)

# button with bell-image and standard compound ("left")
button_2 = customtkinter.CTkButton(master=frame_1, image=bell_image, width=60, height=60,
                                   corner_radius=10, command=button_function)
button_2.place(relx=0.9, rely=0.2, anchor=tkinter.E)

# button with bell-image and compound="bottom"
button_3 = customtkinter.CTkButton(master=frame_1, image=bell_image, text="bell_image", compound="bottom",
                                   command=button_function, height=100)
button_3.place(relx=0.5, rely=0.55, relwidth=0.5, anchor=tkinter.CENTER)

# button with settings-image and compound="right"
button_4 = customtkinter.CTkButton(master=frame_1, image=settings_image, text="bell_image", compound="right",
                                   command=button_function, height=60)
button_4.place(relx=0.5, rely=0.85, relwidth=0.5, anchor=tkinter.CENTER)
button_4.configure(text=None)


root_tk.mainloop()
customtkinter.disable_macos_darkmode()
