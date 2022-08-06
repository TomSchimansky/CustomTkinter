import customtkinter
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("450x260")
        self.title("CustomTkinter example_button_images.py")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=200)

        self.frame_1 = customtkinter.CTkFrame(master=self, width=250, height=240, corner_radius=15)
        self.frame_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_1.grid_columnconfigure(0, weight=1)
        self.frame_1.grid_columnconfigure(1, weight=1)

        self.settings_image = self.load_image("/test_images/settings.png", 20)
        self.bell_image = self.load_image("/test_images/bell.png", 20)
        self.add_folder_image = self.load_image("/test_images/add-folder.png", 20)
        self.add_list_image = self.load_image("/test_images/add-folder.png", 20)
        self.add_user_image = self.load_image("/test_images/add-user.png", 20)
        self.chat_image = self.load_image("/test_images/chat.png", 20)
        self.home_image = self.load_image("/test_images/home.png", 20)

        self.button_1 = customtkinter.CTkButton(master=self.frame_1, image=self.add_folder_image, text="Add Folder", height=32,
                                                compound="right", command=self.button_function)
        self.button_1.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")

        self.button_2 = customtkinter.CTkButton(master=self.frame_1, image=self.add_list_image, text="Add Item", height=32,
                                                compound="right", fg_color="#D35B58", hover_color="#C77C78",
                                                command=self.button_function)
        self.button_2.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        self.button_3 = customtkinter.CTkButton(master=self.frame_1, image=self.chat_image, text="", width=40, height=40,
                                                corner_radius=10, fg_color="gray40", hover_color="gray25",
                                                command=self.button_function)
        self.button_3.grid(row=3, column=0, columnspan=1, padx=20, pady=10, sticky="w")

        self.button_4 = customtkinter.CTkButton(master=self.frame_1, image=self.home_image, text="", width=40, height=40,
                                                corner_radius=10, fg_color="gray40", hover_color="gray25",
                                                command=self.button_function)
        self.button_4.grid(row=3, column=1, columnspan=1, padx=20, pady=10, sticky="e")

        self.button_5 = customtkinter.CTkButton(master=self, image=self.add_user_image, text="Add User", width=130, height=60, border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#D35B58", fg_color=("gray84", "gray25"),
                                                hover_color="#C77C78", command=self.button_function)
        self.button_5.grid(row=0, column=1, padx=20, pady=20)

    def load_image(self, path, image_size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

    def button_function(self):
        print("button pressed")


if __name__ == "__main__":
    app = App()
    app.mainloop()
