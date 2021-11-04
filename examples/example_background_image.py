import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import os

customtkinter.set_appearance_mode("System")  # Other: "Light", "Dark"

PATH = os.path.dirname(os.path.realpath(__file__))


class App(tkinter.Tk):

    APP_NAME = "CustomTkinter complex example"
    WIDTH = 900
    HEIGHT = 600

    def __init__(self, *args, **kwargs):
        customtkinter.enable_macos_darkmode()

        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)
        self.maxsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.image = Image.open(PATH + "/test_images/bg_gradient.jpg").resize((self.WIDTH, self.HEIGHT))
        self.photo = ImageTk.PhotoImage(self.image)

        self.image_label = tkinter.Label(master=self, image=self.photo)
        self.image_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.frame = customtkinter.CTkFrame(master=self,
                                            width=300,
                                            height=App.HEIGHT,
                                            corner_radius=0)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.button_1 = customtkinter.CTkButton(master=self.frame, text="button 1",
                                                corner_radius=10, command=self.button_event, width=200)
        self.button_1.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.button_2 = customtkinter.CTkButton(master=self.frame, text="button 2",
                                                corner_radius=10, command=self.button_event, width=200)
        self.button_2.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    def button_event(self):
        print("Button pressed")

    def on_closing(self, event=0):
        customtkinter.disable_macos_darkmode()
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
