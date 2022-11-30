import customtkinter
from PIL import Image, ImageTk
import os

# load images
file_path = os.path.dirname(os.path.realpath(__file__))
image_1 = customtkinter.CTkImage(light_image=Image.open(file_path + "/test_images/add_folder_dark.png"),
                                 dark_image=Image.open(file_path + "/test_images/add_folder_light.png"),
                                 size=(30, 30))
image_1.configure(dark_image=Image.open(file_path + "/test_images/add_folder_light.png"))
image_2 = customtkinter.CTkImage(light_image=Image.open(file_path + "/test_images/bg_gradient.jpg"),
                                 size=(30, 50))

app = customtkinter.CTk()
app.geometry("500x900")

mode_switch = customtkinter.CTkSwitch(app, text="darkmode",
                                      command=lambda: customtkinter.set_appearance_mode("dark" if mode_switch.get() == 1 else "light"))
mode_switch.pack(padx=20, pady=20)

scaling_button = customtkinter.CTkSegmentedButton(app, values=[0.8, 0.9, 1.0, 1.1, 1.2, 1.5, 2.0],
                                                  command=lambda v: customtkinter.set_widget_scaling(v))
scaling_button.pack(padx=20, pady=20)

button_1 = customtkinter.CTkButton(app, image=image_1)
button_1.pack(padx=20, pady=20)

button_1 = customtkinter.CTkButton(app, image=image_1, anchor="nw", compound="right", height=50, corner_radius=4)
button_1.pack(padx=20, pady=20)

label_1 = customtkinter.CTkLabel(app, text="", image=image_2, compound="right", fg_color="green", width=0)
label_1.pack(padx=20, pady=20)
label_1.configure(image=image_1)

label_2 = customtkinter.CTkLabel(app, text="text", image=image_2, compound="right", fg_color="red", width=0, corner_radius=10)
label_2.pack(padx=20, pady=20)

label_3 = customtkinter.CTkLabel(app, image=ImageTk.PhotoImage(Image.open(file_path + "/test_images/bg_gradient.jpg").resize((300, 100))),
                                 text="", compound="right", fg_color="green", width=0)
label_3.pack(padx=20, pady=20)

app.mainloop()

