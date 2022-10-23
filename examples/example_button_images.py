import PIL.ImageTk

import customtkinter
import tkinter
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

        def _pyimagingtkcall(command, photo, id):
            tk = photo.tk
            try:
                tk.call(command, photo, id)
            except tkinter.TclError:
                print("_pyimagingtkcall error")

        class PhotoImage:
            def __init__(self, image=None, size=None, **kw):
                if hasattr(image, "mode") and hasattr(image, "size"):
                    # got an image instead of a mode
                    mode = image.mode
                    if mode == "P":
                        # palette mapped data
                        image.apply_transparency()
                        image.load()
                        try:
                            mode = image.palette.mode
                        except AttributeError:
                            mode = "RGB"  # default
                    size = image.size
                    kw["width"], kw["height"] = size
                else:
                    mode = image
                    image = None

                if mode not in ["1", "L", "RGB", "RGBA"]:
                    mode = Image.getmodebase(mode)

                self.__mode = mode
                self.__size = size
                self.__photo = tkinter.PhotoImage(**kw)
                self.tk = self.__photo.tk
                if image:
                    self.paste(image)

            def __del__(self):
                name = self.__photo.name
                self.__photo.name = None
                try:
                    self.__photo.tk.call("image", "delete", name)
                except Exception:
                    pass  # ignore internal errors

            def __str__(self):
                return str(self.__photo)

            def width(self):
                return self.__size[0]

            def height(self):
                return self.__size[1]

            def paste(self, im, box=None):
                if box is not None:
                    deprecate("The box parameter", 10, None)

                # convert to blittable
                im.load()
                image = im.im
                if image.isblock() and im.mode == self.__mode:
                    block = image
                else:
                    block = image.new_block(self.__mode, im.size)
                    image.convert2(block, image)  # convert directly between buffers
                _pyimagingtkcall("PyImagingPhoto", self.__photo, block.id)

        pil_img = Image.open(PATH + "/test_images/add-folder.png").resize((10, 10))
        image = PhotoImage(pil_img)

        self.button_1 = customtkinter.CTkButton(master=self.frame_1, image=image, text="Add Folder", height=32,
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

        self.scaling_button = customtkinter.CTkSegmentedButton(self, values=[0.8, 0.9, 1.0, 1.1, 1.2, 1.5],
                                                               command=lambda v: customtkinter.set_widget_scaling(v))
        self.scaling_button.grid(row=1, column=0, pady=(0, 20))
        self.mode_switch = customtkinter.CTkSwitch(self, text="darkmode", onvalue="dark", offvalue="light",
                                                   command=lambda: customtkinter.set_appearance_mode(self.mode_switch.get()))
        self.mode_switch.grid(row=1, column=1, pady=(0, 20))

    def load_image(self, path, image_size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

    def button_function(self):
        print("button pressed")


if __name__ == "__main__":
    app = App()
    app.mainloop()
