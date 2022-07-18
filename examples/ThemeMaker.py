import tkinter
import customtkinter
from tkinter.colorchooser import askcolor
from tkinter import filedialog, messagebox
import json
    
WIDTH = 390
HEIGHT = 350

#Main Window
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
root_tk=customtkinter.CTk()
root_tk.title("CustomTkinter ThemeMaker")
root_tk.geometry(f"{WIDTH}x{HEIGHT}")
root_tk.resizable(width=False, height=False)

#Main Body of the json file
json_data={
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


#widgets
Widgets={'Window':['window_bg_color'],
         'Frame':['frame_border', 'frame_low', 'frame_high'],
         'Button':['button','button_hover','button_border'],
         'CheckBox':['checkbox_border','checkmark'],
         'Entry':['entry','entry_border','entry_placeholder_text'],
         'Label':['label'], 'Text':['text','text_disabled','text_button_disabled'],
         'ProgressBar':['progressbar','progressbar_progress','progressbar_border'],
         'Slider':['slider','slider_progress','slider_button','slider_button_hover'],
         'Switch':['switch','switch_progress','switch_button','switch_button_hover'],
         'Menu + Dropdown':['optionmenu_button','optionmenu_button_hover','combobox_border','combobox_button_hover','dropdown_color','dropdown_hover','dropdown_text'],
         'Scrollbar':['scrollbar_button','scrollbar_button_hover']}

widgetlist=[key for key in Widgets]

#Function for changing the values of menu
def changemenu():
    global current
    menu.configure(values=Widgets[current])
    menu.set(Widgets[current][0])
def ChangeModeRight():
    global current
    widgetlist.append(widgetlist.pop(0))
    current=widgetlist[0]
    widget_type.configure(text=current)
    changemenu()
def ChangeModeLeft():
    global current
    widgetlist.insert(0, widgetlist.pop())
    current=widgetlist[0]
    widget_type.configure(text=current)
    changemenu()

current=widgetlist[0]

def update(value):
    for i in json_data["color"]:
        if i==menu.get():
            if (json_data["color"][i])[0]!=None:
                button_light.configure(fg_color=(json_data["color"][i])[0])
            else:
                button_light.configure(fg_color=None)
            if (json_data["color"][i])[1]!=None:    
                button_dark.configure(fg_color=(json_data["color"][i])[1])
            else:
                button_dark.configure(fg_color=None)
                
#Program widgets
frame_info = customtkinter.CTkFrame(master=root_tk, width=350, height=60)
frame_info.place(x=20,y=20)

widget_type = customtkinter.CTkLabel(master=frame_info,text=current, corner_radius=10, width=200, height=23,
                                     fg_color=("white", "gray38"))
widget_type.place(x=75,y=20)

left_button= customtkinter.CTkButton(master=frame_info, text="<--", width=20, height=20, corner_radius=10,
                                     fg_color=("white", "gray38"), command=ChangeModeLeft)
left_button.place(x=20,y=20)

right_button = customtkinter.CTkButton(master=frame_info, text="-->", width=20, height=20, corner_radius=10,
                                       fg_color=("white", "gray38"), command=ChangeModeRight)
right_button.place(x=290,y=20)

menu=customtkinter.CTkOptionMenu(master=root_tk,width=350,fg_color=("white", "gray38"), button_color=("white", "gray38"),
                                 button_hover_color=None,
                                 height=30, values=list(Widgets.items())[0][1],command=update)
menu.place(x=20,y=100)

#Color chooser
def changecolor():
    color1=askcolor(title="Choose color for "+menu.get()+" (Light)")[1]
    if color1!=None:
        button_light.configure(fg_color=color1)
        for i in json_data["color"]:
            if i==menu.get():
                (json_data["color"][i])[0]=color1
def changecolor2():
    color2=askcolor(title="Choose color for "+menu.get()+" (Dark)")[1]
    if color2!=None:
        button_dark.configure(fg_color=color2)
        for i in json_data["color"]:
            if i==menu.get():
                (json_data["color"][i])[1]=color2
                
button_light = customtkinter.CTkButton(master=root_tk, height=100, width=170, corner_radius=10, border_color="white",
                                       fg_color=None, border_width=2, text="Light", hover_color=None, command=changecolor)
button_light.place(x=20,y=150)

button_dark = customtkinter.CTkButton(master=root_tk, height=100, width=170, corner_radius=10, border_color="white",
                                       fg_color=None, border_width=2, text="Dark", hover_color=None, command=changecolor2)
button_dark.place(x=200,y=150)

#Export json file
def save():
    dialog=customtkinter.CTkInputDialog(master=root_tk, text="Enter your theme name:", title="Save Theme")
    try:
        themename=dialog.get_input()+".json"
        outfile=open(themename,"w")
        json.dump(json_data, outfile, indent=2)
        outfile.close()
        tkinter.messagebox.showinfo("Exported!","Theme exported successfully!")
    except:
        if dialog.get_input()!=None:
            tkinter.messagebox.showerror("Error!","Something went wrong!")
            
#Load external json file
def load():
    global json_data
    openjson=tkinter.filedialog.askopenfilename(filetypes =[('json', ['*.json']),('All Files', '*.*')])
    try:
        if openjson:
            f=open(openjson)
            json_data=json.load(f)
            f.close()
        update(menu.get())
    except:
        tkinter.messagebox.showerror("Error!","Unable to import theme!")

#Reset current colors to None
def reset():
    for i in json_data["color"]:
        if i==menu.get():
            json_data["color"][i][0]=None
            button_light.configure(fg_color=None)
            json_data["color"][i][1]=None
            button_dark.configure(fg_color=None)
            
button_load= customtkinter.CTkButton(master=root_tk, height=40, width=110, text="Load Theme",  command=load)
button_load.place(x=20,y=280)

button_export = customtkinter.CTkButton(master=root_tk, height=40, width=110, text="Export Theme",  command=save)
button_export.place(x=140,y=280)

button_reset=customtkinter.CTkButton(master=root_tk, height=40, width=110, text="Reset",  command=reset)
button_reset.place(x=260,y=280)

root_tk.mainloop()
