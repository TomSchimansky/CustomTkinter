import tkinter
import tkinter.messagebox
import customtkinter
import sys

# Set dark appearance mode:
customtkinter.set_appearance_mode("Dark")  # Other: "Light", "System"


class App(tkinter.Tk):

    APP_NAME = "CustomTkinter complex example"
    WIDTH = 700
    HEIGHT = 500

    MAIN_COLOR = "#5EA880"
    MAIN_COLOR_DARK = "#2D5862"
    MAIN_HOVER = "#458577"

    def __init__(self, *args, **kwargs):
        customtkinter.enable_macos_darkmode()

        tkinter.Tk.__init__(self, *args, **kwargs)

        if "win" in sys.platform:
            if customtkinter.get_appearance_mode() == "Dark":
                self.configure(bg="gray20")  # set window background to dark color

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        # ============ create two CTkFrames ============

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=200,
                                                 height=App.HEIGHT-40,
                                                 corner_radius=0)
        self.frame_left.place(relx=0.32, rely=0.5, anchor=tkinter.E)

        self.frame_right = customtkinter.CTkFrame(master=self,
                                                  width=420,
                                                  height=App.HEIGHT-40,
                                                  corner_radius=0)
        self.frame_right.place(relx=0.365, rely=0.5, anchor=tkinter.W)

        # ============ frame_left ============

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                border_color=App.MAIN_COLOR,
                                                fg_color=None,
                                                hover_color=App.MAIN_HOVER,
                                                text="CTkButton",
                                                command=self.button_event,
                                                border_width=2,
                                                corner_radius=0)
        self.button_1.place(relx=0.5, y=50, anchor=tkinter.CENTER)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                border_color=App.MAIN_COLOR,
                                                fg_color=None,
                                                hover_color=App.MAIN_HOVER,
                                                text="CTkButton",
                                                command=self.button_event,
                                                border_width=2,
                                                corner_radius=0)
        self.button_2.place(relx=0.5, y=100, anchor=tkinter.CENTER)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                border_color=App.MAIN_COLOR,
                                                fg_color=None,
                                                hover_color=App.MAIN_HOVER,
                                                text="CTkButton",
                                                command=self.button_event,
                                                border_width=2,
                                                corner_radius=0)
        self.button_3.place(relx=0.5, y=150, anchor=tkinter.CENTER)

        # ============ frame_right ============

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right,
                                                 width=380,
                                                 height=200,
                                                 corner_radius=0)
        self.frame_info.place(relx=0.5, y=20, anchor=tkinter.N)

        # ============ frame_right -> frame_info ============

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="CTkLabel: Lorem ipsum dolor sit,\n" +
                                                        "amet consetetur sadipscing elitr,\n" +
                                                        "sed diam nonumy eirmod tempor\n" +
                                                        "invidunt ut labore",
                                                   width=250,
                                                   height=100,
                                                   corner_radius=0,
                                                   fg_color=("white", "gray20"),
                                                   text_color=App.MAIN_COLOR,
                                                   justify=tkinter.LEFT)
        self.label_info_1.place(relx=0.5, rely=0.15, anchor=tkinter.N)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info,
                                                        progress_color=App.MAIN_COLOR,
                                                        width=250,
                                                        height=15,
                                                        border_width=0)
        self.progressbar.place(relx=0.5, rely=0.85, anchor=tkinter.S)
        self.progressbar.set(0.65)

        # ============ frame_right <- ============

        self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
                                                button_color=App.MAIN_COLOR,
                                                button_hover_color=App.MAIN_HOVER,
                                               width=160,
                                               height=16,
                                               border_width=5.5,
                                               command=self.progressbar.set)
        self.slider_1.place(x=20, rely=0.6, anchor=tkinter.W)
        self.slider_1.set(0.3)

        self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
                                                button_color=App.MAIN_COLOR,
                                                button_hover_color=App.MAIN_HOVER,
                                               width=160,
                                               height=16,
                                               border_width=5.5,
                                               command=self.progressbar.set)
        self.slider_2.place(x=20, rely=0.7, anchor=tkinter.W)
        self.slider_2.set(0.7)

        self.label_info_2 = customtkinter.CTkLabel(master=self.frame_right,
                                                   text="CTkLabel: Lorem ipsum",
                                                   width=180,
                                                   height=20,
                                                   justify=tkinter.CENTER)
        self.label_info_2.place(x=310, rely=0.6, anchor=tkinter.CENTER)

        self.button_4 = customtkinter.CTkButton(master=self.frame_right,
                                                border_color=App.MAIN_COLOR,
                                                fg_color=None,
                                                hover_color=App.MAIN_HOVER,
                                                height=28,
                                                text="CTkButton",
                                                command=self.button_event,
                                                border_width=2,
                                                corner_radius=0)
        self.button_4.place(x=310, rely=0.7, anchor=tkinter.CENTER)

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            height=28,
                                            corner_radius=0)
        self.entry.place(relx=0.33, rely=0.92, anchor=tkinter.CENTER)
        self.entry.insert(0, "CTkEntry")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                border_color=App.MAIN_COLOR,
                                                fg_color=None,
                                                hover_color=App.MAIN_HOVER,
                                                height=28,
                                                text="CTkButton",
                                                command=self.button_event,
                                                border_width=2,
                                                corner_radius=0)
        self.button_5.place(relx=0.66, rely=0.92, anchor=tkinter.CENTER)

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
