import tkinter
import customtkinter  # <- import the CustomTkinter module
from PIL import Image, ImageTk  # <- import PIL for the images
import os

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window (you can also use normal tkinter.Tk window)
root_tk.geometry("450x260")
root_tk.title("CustomTkinter button images")


def button_function():
    print("button pressed")


# load images as PhotoImage
settings_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/settings.png").resize((30, 30)))
bell_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/bell.png").resize((30, 30)))

add_folder_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/add-folder.png").resize((30, 30), Image.ANTIALIAS))
add_list_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/add-list.png").resize((30, 30), Image.ANTIALIAS))
add_user_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/add-user.png").resize((30, 30), Image.ANTIALIAS))
chat_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/chat.png").resize((30, 30), Image.ANTIALIAS))
home_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/home.png").resize((30, 30), Image.ANTIALIAS))

frame_1 = customtkinter.CTkFrame(master=root_tk, width=250, height=240, corner_radius=15)
frame_1.pack(padx=20, pady=20, side="left")

button_1 = customtkinter.CTkButton(master=frame_1, image=add_folder_image, text="Add Folder", width=190, height=50,
                                   corner_radius=10, compound="right", command=button_function)
button_1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

button_2 = customtkinter.CTkButton(master=frame_1, image=add_list_image, text="Add Item", width=190, height=50,
                                   corner_radius=10, compound="right", fg_color="#D35B58", hover_color="#C77C78",
                                   command=button_function)
button_2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

button_3 = customtkinter.CTkButton(master=frame_1, image=chat_image, text="", width=50, height=50,
                                   corner_radius=10, fg_color="gray40", hover_color="gray35", command=button_function)
button_3.place(relx=0.35, rely=0.8, anchor=tkinter.CENTER)

button_4 = customtkinter.CTkButton(master=frame_1, image=home_image, text="", width=50, height=50,
                                   corner_radius=10, fg_color="gray40", hover_color="gray35", command=button_function)
button_4.place(relx=0.65, rely=0.8, anchor=tkinter.CENTER)

button_5 = customtkinter.CTkButton(master=root_tk, image=add_user_image, text="Add User", width=130, height=90, border_width=4,
                                   corner_radius=10, compound="bottom", border_color="#D35B58", fg_color=("gray80", "gray25"), hover_color="#C77C78",
                                   command=button_function)
button_5.pack(padx=20, pady=20, side="right")

root_tk.mainloop()