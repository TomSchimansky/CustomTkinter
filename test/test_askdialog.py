from tkinter.constants import CENTER, LEFT
import tkinter
import tkinter.messagebox
from tkinter import filedialog as fd
import customtkinter  # <- import the CustomTkinter module
import os


class App(customtkinter.CTk):

    customtkinter.set_appearance_mode("dark")
    APP_NAME = "Bulk Barcode Generator"
    WIDTH = 600
    HEIGHT = 450

    MAIN_COLOR = "#5ea886"
    MAIN_COLOR_DARK = "#2D5862"
    MAIN_HOVER = "#05f4b7"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # ============ create two CTkFrames ============

        #1
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                width=220,
                                                height=App.HEIGHT-40,
                                                corner_radius=5)
        self.frame_left.place(relx=0.38, rely=0.5, anchor=tkinter.E)

        #2
        self.frame_right = customtkinter.CTkFrame(master=self,
                                                width=350,
                                                height=App.HEIGHT-40,
                                                corner_radius=5)
        self.frame_right.place(relx=0.40, rely=0.5, anchor=tkinter.W)

#        # ============ frame_right ============

        self.button_output = customtkinter.CTkButton(master=self.frame_right, border_color=App.MAIN_COLOR,
                                                fg_color=None, hover_color=App.MAIN_HOVER,
                                                height=28, text="Output Folder", command=self.button_outputFunc,
                                                border_width=3, corner_radius=10, text_font=('Calibri',12))
        self.button_output.place(relx=0.05, rely=0.06, anchor=tkinter.NW)
        self.entry_output = customtkinter.CTkEntry(master=self.frame_right, width=320, height=38, corner_radius=5)
        self.entry_output.place(relx=0.05, rely=0.18, anchor=tkinter.NW)


    def button_outputFunc(self):
        self.entry_output.delete(0, 'end')
        filename = fd.askdirectory()
        self.entry_output.insert(0,str(filename))
        pass

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()




if __name__ == "__main__":
    app = App()
    app.start()