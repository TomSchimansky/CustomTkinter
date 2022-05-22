import tkinter
import customtkinter
from PIL import Image, ImageTk  # <- import PIL for the images
import os

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()  # create CTk window like you do with the Tk window (you can also use normal tkinter.Tk window)
app.geometry("450x260")
app.title("CustomTkinter example_button_images.py")


def button_function():
    print("button pressed")


# load images as PhotoImage
image_size = 20

settings_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/settings.png").resize((image_size, image_size)))
bell_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/bell.png").resize((image_size, image_size)))

add_folder_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/add-folder.png").resize((image_size, image_size), Image.ANTIALIAS))
add_list_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/add-list.png").resize((image_size, image_size), Image.ANTIALIAS))
add_user_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/add-user.png").resize((image_size, image_size), Image.ANTIALIAS))
chat_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/chat.png").resize((image_size, image_size), Image.ANTIALIAS))
home_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/home.png").resize((image_size, image_size), Image.ANTIALIAS))

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1, minsize=200)

frame_1 = customtkinter.CTkFrame(master=app, width=250, height=240, corner_radius=15)
frame_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

frame_1.grid_columnconfigure(0, weight=1)
frame_1.grid_columnconfigure(1, weight=1)
frame_1.grid_rowconfigure(0, minsize=10)  # add empty row for spacing

button_1 = customtkinter.CTkButton(master=frame_1, image=add_folder_image, text="Add Folder", width=190, height=40,
                                   compound="right", command=button_function)
button_1.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

button_2 = customtkinter.CTkButton(master=frame_1, image=add_list_image, text="Add Item", width=190, height=40,
                                   compound="right", fg_color="#D35B58", hover_color="#C77C78",
                                   command=button_function)
button_2.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

button_3 = customtkinter.CTkButton(master=frame_1, image=chat_image, text="", width=50, height=50,
                                   corner_radius=10, fg_color="gray40", hover_color="gray25", command=button_function)
button_3.grid(row=3, column=0, columnspan=1, padx=20, pady=10, sticky="w")

button_4 = customtkinter.CTkButton(master=frame_1, image=home_image, text="", width=50, height=50,
                                   corner_radius=10, fg_color="gray40", hover_color="gray25", command=button_function)
button_4.grid(row=3, column=1, columnspan=1, padx=20, pady=10, sticky="e")

button_5 = customtkinter.CTkButton(master=app, image=add_user_image, text="Add User", width=130, height=70, border_width=3,
                                   corner_radius=10, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"), hover_color="#C77C78",
                                   command=button_function)
button_5.grid(row=0, column=1, padx=20, pady=20)

app.mainloop()
