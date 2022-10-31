import customtkinter
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))


app = customtkinter.CTk()

switch_1 = customtkinter.CTkSwitch(app, text="darkmode", command=lambda: customtkinter.set_appearance_mode("dark" if switch_1.get() == 1 else "light"))
switch_1.pack(padx=20, pady=20)

image_1 = customtkinter.CTkImage(light_image=Image.open(PATH + "/test_images/add_folder_dark.png"),
                                 dark_image=Image.open(PATH + "/test_images/add_folder_light.png"),
                                 size=(30, 50))
image_1.configure(dark_image=Image.open(PATH + "/test_images/add_folder_light.png"))

button_1 = customtkinter.CTkButton(app, image=image_1)
button_1.pack(padx=20, pady=20)

app.mainloop()

