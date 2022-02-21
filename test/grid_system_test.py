import tkinter
import customtkinter  # <- import the CustomTkinter module
from PIL import Image, ImageTk  # <- import PIL for the images
import os

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.set_appearance_mode("System")  # Other: "Dark", "Light"

root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window (you can also use normal tkinter.Tk window)
root_tk.geometry("400x600")
root_tk.title("CustomTkinter Test")


def button_function():
    print("button pressed")


# load images as PhotoImage
settings_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/settings.png").resize((40, 40)))
bell_image     = ImageTk.PhotoImage(Image.open(PATH + "/test_images/bell.png").resize((40, 40)))

frame_1 = customtkinter.CTkFrame(master=root_tk, width=300, height=350)
frame_1.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor=tkinter.CENTER)

# button with bell-image and standard compound ("left")
button_2 = customtkinter.CTkButton(master=frame_1, height=60,
                                   corner_radius=10, command=button_function)
button_2.place(relx=0.5, rely=0.3, relwidth=0.5, anchor=tkinter.CENTER)
button_2.configure(image=bell_image)
button_2.configure(image=settings_image, text="new text")

# button with settings-image and compound="right"
button_3 = customtkinter.CTkButton(master=frame_1, text="large button 3", compound="right",
                                   command=button_function, height=30, corner_radius=8)
button_3.place(relx=0.5, rely=0.5, relwidth=0.6, anchor=tkinter.CENTER)

entry_1 = customtkinter.CTkEntry(frame_1)
entry_1.pack(fill="x", pady=10, padx=10)
entry_1.configure(corner_radius=15)

label_1 = customtkinter.CTkLabel(frame_1, text="auto size label")
label_1.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER, relwidth=0.5, relheight=0.08)

entry_2 = customtkinter.CTkEntry(frame_1, corner_radius=6, height=30, width=90, justify='center')
entry_2.place(relx=0.5, anchor=tkinter.CENTER, rely=0.15)

root_tk.mainloop()
