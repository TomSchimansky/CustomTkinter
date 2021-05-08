import tkinter
import customtkinter  # <- import the CustomTkinter module
from PIL import Image, ImageTk  # <- import PIL for the images

customtkinter.enable_macos_darkmode()
customtkinter.set_appearance_mode("System")  # Other: "Dark", "Light"

root_tk = tkinter.Tk()  # create the Tk window like you normally do
root_tk.geometry("400x240")
root_tk.title("CustomTkinter Test")


def button_function():
    print("button pressed")


# load images as PhotoImage
settings_image = ImageTk.PhotoImage(Image.open("test_images/settings.png").resize((40, 40)))
bell_image     = ImageTk.PhotoImage(Image.open("test_images/bell.png").resize((40, 40)))

frame_1 = customtkinter.CTkFrame(master=root_tk, width=300, height=200, corner_radius=15)
frame_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# button with settings-image
button_1 = customtkinter.CTkButton(master=frame_1, image=settings_image, width=60, height=60,
                                   corner_radius=10, command=button_function)
button_1.place(relx=0.33, rely=0.5, anchor=tkinter.CENTER)

# button with bell-image
button_2 = customtkinter.CTkButton(master=frame_1, image=bell_image, width=60, height=60,
                                   corner_radius=10, command=button_function)
button_2.place(relx=0.66, rely=0.5, anchor=tkinter.CENTER)

root_tk.mainloop()
customtkinter.disable_macos_darkmode()
