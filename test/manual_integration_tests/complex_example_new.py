import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{920}x{500}-100-100")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0, minsize=200)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", text_font=("Roboto", -16))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_callback)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_callback)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_callback)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 10), pady=(10, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(self, fg_color=None, border_width=2)
        self.main_button_1.grid(row=3, column=3, padx=(10, 20), pady=(10, 20), sticky="nsew")

        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(10, 20), pady=(20, 10), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create optionemnu and combobox frame
        self.optionemnu_combobox_frame = customtkinter.CTkFrame(self)
        self.optionemnu_combobox_frame.grid(row=0, column=2, padx=(10, 10), pady=(20, 10), sticky="nsew")
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.optionemnu_combobox_frame,
                                                        dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.combobox_1 = customtkinter.CTkComboBox(self.optionemnu_combobox_frame,
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.string_input_button = customtkinter.CTkButton(self.optionemnu_combobox_frame, text="Open CTkInputDialog",
                                                           command=self.open_input_dialog)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="ew")

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(10, 20), pady=(10, 10), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 10), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.switch_1 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame)
        self.switch_1.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        self.switch_2 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame)
        self.switch_2.grid(row=4, column=0, pady=(10, 20), padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color=None)
        self.slider_progressbar_frame.grid(row=1, column=1, columnspan=2, padx=(20, 10), pady=(10, 10), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(3, weight=1)
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame)
        self.slider_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=4, number_of_steps=4)
        self.slider_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_3 = customtkinter.CTkSlider(self.slider_progressbar_frame, orient="vertical")
        self.slider_3.grid(row=0, column=1, rowspan=4, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orient="vertical")
        self.progressbar_2.grid(row=0, column=2, rowspan=4, padx=(10, 20), pady=(10, 10), sticky="ns")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_2.configure(state="disabled")
        self.switch_2.configure(state="disabled")
        self.checkbox_1.select()
        self.switch_1.select()
        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.textbox.insert("1.0",
                            "CTkTextbox\n\nLorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.", )
        #self.textbox.tag_add("headline", "1.0", "1.end")
        #self.textbox.tag_config("headline", foreground="red")

    def open_input_dialog(self):
        dialog = customtkinter.CTkInputDialog(master=None, text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_spacing_scaling(new_scaling_float)
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_callback(self):
        print("sidebar_button click")

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
