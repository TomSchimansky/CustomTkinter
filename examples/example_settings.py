import os
import tkinter  
import tkinter.messagebox 
import customtkinter # pip install customtkinter
import configparser # pip install configparser
import base64 # pip install base64

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter save settings example")
        self.geometry('1100x580')

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Settings", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Save Settings", command=self.save_setting)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Load Settings", command=self.load_setting)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # Custom save settings

        self.sidebar_save_as_label1 = customtkinter.CTkLabel(self.sidebar_frame, text=" ", anchor="s")
        self.sidebar_save_as_label1.grid(row=3, column=0, padx=20, pady=(10, 0))

        self.sidebar_save_as_label = customtkinter.CTkLabel(self.sidebar_frame, text="Save Settings as:", anchor="s")
        self.sidebar_save_as_label.grid(row=4, column=0, padx=20, pady=(10, 0))

        self.sidebar_settings_name = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Name" )
        self.sidebar_settings_name.grid(row=5, column=0, padx=(20, 0), pady=(20, 20))        

        self.sidebar_save_as_button = customtkinter.CTkButton(self.sidebar_frame, text="Save as", command=self.save_as )
        self.sidebar_save_as_button.grid(row=6, column=0, padx=20, pady=10)

        self.sidebar_save_as_label = customtkinter.CTkLabel(self.sidebar_frame, text="Load Settings", anchor="s")
        self.sidebar_save_as_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.optionmenu_load_settings = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,values=self.find_ini_files(), command=self.load_setting)
        self.optionmenu_load_settings.grid(row=8, column=0, padx=20, pady=(20, 10))


        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))


        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="Option 1", variable=self.radio_var, value=1)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="Option 2", variable=self.radio_var, value=2)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="Option 3", variable=self.radio_var, value=3)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Checkbox_1")
        self.checkbox_1.grid(row=1, column=0, pady=(20, 10), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Checkbox_2")
        self.checkbox_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        self.switch_1 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, text="switch_1", command=lambda: print("switch 1 toggle"))
        self.switch_1.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        self.switch_2 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, text="switch_2",)
        self.switch_2.grid(row=4, column=0, pady=(10, 20), padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")

        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # set default values        
        self.checkbox_1.select()
        self.switch_1.select()
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 2)
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

    def find_ini_files(self):
        cwd = os.getcwd()
        files = os.listdir(cwd)
        ini_files = [f for f in files if f.endswith(".ini")]
        return [f.rsplit(".", 1)[0] for f in ini_files]

    def filter_filename(self, string):
        safe_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-")
        return "".join([c for c in string if c in safe_chars])

    def save_as(self):
        print("save as + " + self.sidebar_settings_name.get())    
        self.save_setting(self.filter_filename(self.sidebar_settings_name.get()) or "") 
        self.optionmenu_load_settings.configure(values=self.find_ini_files())                     


    # save all gui elements into an ini file
    def save_setting(self, settings_name="settings"):        
        config = configparser.ConfigParser()

        config[settings_name] = {
            "textbox": base64.b64encode(self.textbox.get("1.0", "end").encode("utf-8")).decode("utf-8"),
            "entry": self.entry.get(),
            "radio": self.radio_var.get(),
            "checkbox_1": self.checkbox_1.get(),
            "checkbox_2": self.checkbox_2.get(),
            "switch_1": self.switch_1.get(),
            "switch_2": self.switch_2.get(),
            "optionmenu_1": self.optionmenu_1.get(),
            "combobox_1": self.combobox_1.get(),
            "seg_button_1": self.seg_button_1.get(),
            "slider_1": self.slider_1.get(),
            "slider_2": self.slider_1.get()
        }
        with open(settings_name+".ini", "w") as configfile:
            config.write(configfile)

    # load all gui elements from an ini file
    def load_setting(self, settings_name="settings"):

        self.sidebar_settings_name.delete(0, "end")
        self.sidebar_settings_name.insert(0, settings_name)
        
        try:
            config = configparser.ConfigParser()
            config.read(settings_name+".ini")

            self.textbox.delete("1.0", "end")
            self.textbox.insert("0.0", base64.b64decode(config[settings_name]["textbox"]).decode("utf-8"))

            self.entry.delete(0, "end")
            self.entry.insert(0, config[settings_name]["entry"])
            self.radio_var.set(config[settings_name]["radio"])

            self.checkbox_1.select() if int(config[settings_name]["checkbox_1"]) else self.checkbox_1.deselect()
            self.checkbox_2.select() if int(config[settings_name]["checkbox_2"]) else self.checkbox_2.deselect()

            self.switch_1.select() if int(config[settings_name]["switch_1"]) else self.switch_1.deselect()
            self.switch_2.select() if int(config[settings_name]["switch_2"]) else self.switch_2.deselect()

            self.optionmenu_1.set(config[settings_name]["optionmenu_1"])
            self.combobox_1.set(config[settings_name]["combobox_1"])

            self.seg_button_1.set(config[settings_name]["seg_button_1"])

            self.slider_1.set(float(config[settings_name]["slider_1"]))
            self.slider_2.set(float(config[settings_name]["slider_2"]))
        except Exception as e:
            print("Error on reading settings.ini. Maybe save it first." + str(e))
            pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
