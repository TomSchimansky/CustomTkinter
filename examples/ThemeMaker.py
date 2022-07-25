import tkinter
import customtkinter
from tkinter.colorchooser import askcolor
from tkinter import filedialog, messagebox
import json

"""
Quick Guide:

This program can be used to create custom themes for customtkinter.
You can easily create and edit themes for your applications.

Customtkinter themefiles are .json files that can be used with customtkinter using the 'customtkinter.set_default_color_theme(theme_file)' method.
Example: customtkinter.set_default_color_theme("Path/my_theme.json")

A customtkinter theme has one dark and one light color attribute for each widget type and you have to choose the 2 colors for each widget type.
(You can switch between them with the 'set_appearance_mode' method)

Currently it is not possible to switch between themes, so only appearance_mode can be changed.

Default color is null/None which has no color, leaving a widget with null value will give you a blank widget.
But it's also recommened to leave the label color as None.

Note that some parameters are interlinked like the main entry color and combobox's entry color (which is not directly available in the contents).

Other values can also be changed in the json_data manually.
"""

class App(customtkinter.CTk):
    
    #--------------------Main Structure of the Theme File--------------------#
    
    json_data = {
        "color": {
            'window_bg_color': [None, None],
            'frame_border': [None, None],
            'frame_low': [None, None],
            'frame_high': [None, None],
            'button': [None, None],
            'button_hover': [None, None],
            'button_border': [None, None],
            'checkbox_border': [None, None],
            'checkmark': [None, None],
            'entry': [None, None],
            'entry_border': [None, None],
            'entry_placeholder_text': [None, None],
            'label': [None, None],
            'text': [None, None],
            'text_disabled': [None, None],
            'text_button_disabled': [None, None],
            'progressbar': [None, None],
            'progressbar_progress': [None, None],
            'progressbar_border': [None, None],
            'slider': [None, None],
            'slider_progress': [None, None],
            'slider_button': [None, None],
            'slider_button_hover': [None, None],
            'switch': [None, None],
            'switch_progress': [None, None],
            'switch_button': [None, None],
            'switch_button_hover': [None, None],
            'optionmenu_button': [None, None],
            'optionmenu_button_hover': [None, None],
            'combobox_border': [None, None],
            'combobox_button_hover': [None, None],
            'dropdown_color': [None, None],
            'dropdown_text': [None, None],
            'dropdown_hover': [None, None],
            'scrollbar_button': [None, None],
            'scrollbar_button_hover': [None, None]
        },
        "text": {
        "macOS": {
            "font": "SF Display",
            "size": -13
            },
        "Windows": {
            "font": "Roboto",
            "size": -13
        },
        "Linux": {
            "font": "Roboto",
            "size": -13
            }
        },
        "shape": {
            "button_corner_radius": 8,
            "button_border_width": 0,
            "checkbox_corner_radius": 7,
            "checkbox_border_width": 3,
            "radiobutton_corner_radius": 1000,
            "radiobutton_border_width_unchecked": 3,
            "radiobutton_border_width_checked": 6,
            "entry_border_width": 2,
            "frame_corner_radius": 10,
            "frame_border_width": 0,
            "label_corner_radius": 0,
            "progressbar_border_width": 0,
            "progressbar_corner_radius": 1000,
            "slider_border_width": 6,
            "slider_corner_radius": 8,
            "slider_button_length": 0,
            "slider_button_corner_radius": 1000,
            "switch_border_width": 3,
            "switch_corner_radius": 1000,
            "switch_button_corner_radius": 1000,
            "switch_button_length": 0,
            "scrollbar_corner_radius": 1000,
            "scrollbar_border_spacing": 4
        }
    }

    #--------------------Widget Type and Content--------------------#
    
    widgets = {'Window':['window_bg_color'],
             'Frame':['frame_border', 'frame_low', 'frame_high'],
             'Button':['button','button_hover','button_border'],
             'CheckBox':['checkbox_border','checkmark'],
             'Entry':['entry','entry_border','entry_placeholder_text'],
             'Label':['label'], 'Text':['text','text_disabled','text_button_disabled'],
             'ProgressBar':['progressbar','progressbar_progress','progressbar_border'],
             'Slider':['slider','slider_progress','slider_button','slider_button_hover'],
             'Switch':['switch','switch_progress','switch_button','switch_button_hover'],
             'Menu + Dropdown':['optionmenu_button','optionmenu_button_hover','combobox_border',
                                'combobox_button_hover','dropdown_color','dropdown_hover','dropdown_text'],
             'Scrollbar':['scrollbar_button','scrollbar_button_hover']}

    widgetlist = [key for key in widgets] #This is a dynamic list of all the widget type
    current = widgetlist[0] #This is the current widget type selected


    def __init__(self):
        
        #--------------------Main root Window--------------------#
        
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")
        self.main = customtkinter.CTk()
        self.main.title("CustomTkinter ThemeMaker")
        self.main.geometry("450x400")
        self.main.grid_columnconfigure((0,1,2,3,4,5), weight=1)
        self.main.grid_rowconfigure(2, weight=1)
        
        self.frame_info = customtkinter.CTkFrame(master=self.main, height=80)
        self.frame_info.grid(row=0, column=0, columnspan=6, sticky="nswe", padx=20, pady=20)
        self.frame_info.grid_columnconfigure(0, weight=1)

        self.widget_type = customtkinter.CTkLabel(master=self.frame_info, text=self.current, corner_radius=10, width=200, height=20,
                                        fg_color=("white", "gray38"))
        self.widget_type.grid(row=0, column=0, sticky="nswe", padx=80, pady=20)

        self.left_button = customtkinter.CTkButton(master=self.frame_info, text="<", width=20, height=20, corner_radius=10,
                                        fg_color=("white", "gray38"), command=self.change_mode_left)
        self.left_button.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)

        self.right_button = customtkinter.CTkButton(master=self.frame_info, text=">", width=20, height=20, corner_radius=10,
                                        fg_color=("white", "gray38"), command=self.change_mode_right)
        self.right_button.grid(row=0, column=0, sticky="nse", padx=20, pady=20)

        self.menu = customtkinter.CTkOptionMenu(master=self.main, fg_color=("white", "gray38"), button_color=("white", "gray38"),
                                        button_hover_color=None, height=30, values=list(self.widgets.items())[0][1], command=self.update)   
        self.menu.grid(row=1, column=0, columnspan=6, sticky="nswe", padx=20)

        self.button_light = customtkinter.CTkButton(master=self.main, height=100, width=200, corner_radius=10, border_color="white",
                                        fg_color=None, border_width=2, text="Light", hover_color=None, command=self.change_color_light)
        self.button_light.grid(row=2, column=0, sticky="nswe", columnspan=3, padx=(20,5), pady=20)
    
        self.button_dark = customtkinter.CTkButton(master=self.main, height=100, width=200, corner_radius=10, border_color="white",
                                        fg_color=None, border_width=2, text="Dark", hover_color=None, command=self.change_color_dark)
        self.button_dark.grid(row=2, column=3, sticky="nswe", columnspan=3, padx=(5,20), pady=20)

        self.button_load = customtkinter.CTkButton(master=self.main, height=40, width=110, text="Load Theme", command=self.load)
        self.button_load.grid(row=3, column=0,  columnspan=2, sticky="nswe", padx=(20,5), pady=(0,20))

        self.button_export = customtkinter.CTkButton(master=self.main, height=40, width=110, text="Save Theme", command=self.save)
        self.button_export.grid(row=3, column=2,  columnspan=2, sticky="nswe", padx=(5,5), pady=(0,20))
    
        self.button_reset = customtkinter.CTkButton(master=self.main, height=40, width=110, text="Reset", command=self.reset)
        self.button_reset.grid(row=3, column=4,  columnspan=2, sticky="nswe", padx=(5,20), pady=(0,20))
        
        self.main.mainloop()


    #--------------------class App Functions--------------------#

    #Function for changing current widget type wih right button
    def change_mode_right(self):
        self.widgetlist.append(self.widgetlist.pop(0))
        self.current = App.widgetlist[0]
        self.widget_type.configure(text=self.current)
        self.menu.configure(values=self.widgets[self.current])
        self.menu.set(self.widgets[self.current][0])

    #Function for changing current widget type with left button  
    def change_mode_left(self):
        self.widgetlist.insert(0, self.widgetlist.pop())
        self.current = self.widgetlist[0]
        self.widget_type.configure(text=self.current)
        self.menu.configure(values=self.widgets[self.current])
        self.menu.set(self.widgets[self.current][0])
        
    #Function for updating the contents and their colors
    def update(self, value):
        for i in self.json_data["color"]:
            if i==self.menu.get():
                if (self.json_data["color"][i])[0] is not None:
                    self.button_light.configure(fg_color=(self.json_data["color"][i])[0])
                else:
                    self.button_light.configure(fg_color=None)
                if (self.json_data["color"][i])[1] is not None:    
                    self.button_dark.configure(fg_color=(self.json_data["color"][i])[1])
                else:
                    self.button_dark.configure(fg_color=None)
                    
    #Function for choosing the color for Light mode of the theme
    def change_color_light(self):
        color1 = askcolor(title="Choose color for "+self.menu.get()+" (Light)", initialcolor=self.button_light.fg_color)[1]
        if color1 is not None:
            self.button_light.configure(fg_color=color1)
            for i in self.json_data["color"]:
                if i==self.menu.get():
                    (self.json_data["color"][i])[0] = color1
                    
    #Function for choosing the color for Dark mode of the theme                
    def change_color_dark(self):
        color2 = askcolor(title="Choose color for "+self.menu.get()+" (Dark)", initialcolor=self.button_dark.fg_color)[1]
        if color2 is not None:
            self.button_dark.configure(fg_color=color2)
            for i in self.json_data["color"]:
                if i==self.menu.get():
                    (self.json_data["color"][i])[1] = color2

    #Function for exporting the theme file         
    def save(self):
        save_file = tkinter.filedialog.asksaveasfilename(initialfile="Untitled.json", filetypes=[('json', ['*.json']),('All Files', '*.*')], defaultextension=".json")
        try:
            if save_file:
                with open(save_file, "w") as f:
                    json.dump(self.json_data, f, indent=2)
                    f.close()
                tkinter.messagebox.showinfo("Exported!","Theme saved successfully!")
        except:
            tkinter.messagebox.showerror("Error!","Something went wrong!")
            
    #Function for loading the theme file            
    def load(self):
        global json_data
        open_json = tkinter.filedialog.askopenfilename(filetypes=[('json', ['*.json']),('All Files', '*.*')])
        try:
            if open_json:
                with open(open_json) as f:
                    self.json_data = json.load(f)
                    f.close()
            self.update(self.menu.get())
        except:
            tkinter.messagebox.showerror("Error!","Unable to load the theme file!")
            
    #Function for resetting the current colors of the widget to null (default value)
    def reset(self):
        for i in self.json_data["color"]:
            if i==self.menu.get():
                self.json_data["color"][i][0] = None
                self.button_light.configure(fg_color=None)
                self.json_data["color"][i][1] = None
                self.button_dark.configure(fg_color=None)
            

if __name__ == "__main__":
    app = App()
