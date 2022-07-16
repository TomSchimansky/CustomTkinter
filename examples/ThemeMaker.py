import tkinter
import customtkinter
from tkinter.colorchooser import askcolor
from tkinter import filedialog, messagebox
import json

#Main Window
WIDTH = 390
HEIGHT = 350
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
self=customtkinter.CTk()
self.title("CustomTkinter ThemeMaker")
self.geometry(f"{WIDTH}x{HEIGHT}")
self.resizable(width=False, height=False)

null=None #Default is null

#Main Body of the json file
json_data={
    "color": {
        'window_bg_color': [null, null],
        'frame_border': [null, null],
        'frame_low': [null, null],
        'frame_high': [null, null],
        'button': [null, null],
        'button_hover': [null, null],
        'button_border': [null, null],
        'checkbox_border': [null, null],
        'checkmark': [null, null],
        'entry': [null, null],
        'entry_border': [null, null],
        'entry_placeholder_text': [null, null],
        'label': [null, null],
        'text': [null, null],
        'text_disabled': [null, null],
        'text_button_disabled': [null, null],
        'progressbar': [null, null],
        'progressbar_progress': [null, null],
        'progressbar_border': [null, null],
        'slider': [null, null],
        'slider_progress': [null, null],
        'slider_button': [null, null],
        'slider_button_hover': [null, null],
        'switch': [null, null],
        'switch_progress': [null, null],
        'switch_button': [null, null],
        'switch_button_hover': [null, null],
        'optionmenu_button': [null, null],
        'optionmenu_button_hover': [null, null],
        'combobox_border': [null, null],
        'combobox_button_hover': [null, null],
        'dropdown_color': [null, null],
        'dropdown_text': [null, null],
        'dropdown_hover': [null, null],
        'scrollbar_button': [null, null],
        'scrollbar_button_hover': [null, null]
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


#list of widgets
Widgets=['Window', 'Frame', 'Button', 'CheckBox', 'Entry', 'Label', 'Text', 'ProgressBar', 'Slider',
         'Switch', 'Menu + Dropdown', 'Scrollbar']

#List containing menu content
list0=['window_bg_color']
list1=['frame_border', 'frame_low', 'frame_high']
list2=['button','button_hover','button_border']
list3=['checkbox_border','checkmark']
list4=['entry','entry_border','entry_placeholder_text']
list5=['label']
list6=['text','text_disabled','text_button_disabled']
list7=['progressbar','progressbar_progress','progressbar_border']
list8=['slider','slider_progress','slider_button','slider_button_hover']
list9=['switch','switch_progress','switch_button','switch_button_hover']
list10=['optionmenu_button','optionmenu_button_hover','combobox_border','combobox_button_hover',
        'dropdown_color','dropdown_hover','dropdown_text']
list11=['scrollbar_button','scrollbar_button_hover']

#Function for changing the values of menu
def changemenu():
    if current=='Window':
        menu.configure(values=list0)
        menu.set(list0[0])
    elif current=='Frame':
        menu.configure(values=list1)
        menu.set(list1[0])
    elif current=='Button':
        menu.configure(values=list2)
        menu.set(list2[0])
    elif current=='CheckBox':
        menu.configure(values=list3)
        menu.set(list3[0])
    elif current=='Entry':
        menu.configure(values=list4)
        menu.set(list4[0])
    elif current=='Label':
        menu.configure(values=list5)
        menu.set(list5[0])
    elif current=='Text':
        menu.configure(values=list6)
        menu.set(list6[0])
    elif current=='ProgressBar':
        menu.configure(values=list7)
        menu.set(list7[0])
    elif current=='Slider':
        menu.configure(values=list8)
        menu.set(list8[0])
    elif current=='Switch':
        menu.configure(values=list9)
        menu.set(list9[0])
    elif current=='Menu + Dropdown':
        menu.configure(values=list10)
        menu.set(list10[0])
    elif current=='Scrollbar':
        menu.configure(values=list11)
        menu.set(list11[0])
        
def ChangeModeRight():
    global current
    Widgets.append(Widgets.pop(0))
    current=Widgets[0]
    widget_type.configure(text=current)
    changemenu()
def ChangeModeLeft():
    global current
    Widgets.insert(0, Widgets.pop())
    current=Widgets[0]
    widget_type.configure(text=current)
    changemenu()
    
current=Widgets[0]

def update(value):
    for i in json_data["color"]:
        if i==menu.get():
            if (json_data["color"][i])[0]!=null:
                button_light.configure(fg_color=(json_data["color"][i])[0])
            else:
                button_light.configure(fg_color=None)
            if (json_data["color"][i])[1]!=null:    
                button_dark.configure(fg_color=(json_data["color"][i])[1])
            else:
                button_dark.configure(fg_color=None)
                
#Porgram widgets
frame_info = customtkinter.CTkFrame(master=self, width=350, height=60)
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

menu=customtkinter.CTkOptionMenu(master=self,width=350,fg_color=("white", "gray38"), button_color=("white", "gray38"),
                                 button_hover_color=None,
                                 height=30, values=list0, command=update)
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
                
button_light = customtkinter.CTkButton(master=self, height=100, width=170, corner_radius=10, border_color="white",
                                       fg_color=None, border_width=2, text="Light", hover_color=None, command=changecolor)
button_light.place(x=20,y=150)

button_dark = customtkinter.CTkButton(master=self, height=100, width=170, corner_radius=10, border_color="white",
                                       fg_color=None, border_width=2, text="Dark", hover_color=None, command=changecolor2)
button_dark.place(x=200,y=150)

#Export the json file
def savethis():
    dialog=customtkinter.CTkInputDialog(master=self, text="Enter your theme name:", title="Save Theme")
    try:
        themename=dialog.get_input()+".json"
        outfile=open(themename,"w")
        json.dump(json_data, outfile, indent=2)
        outfile.close()
        tkinter.messagebox.showinfo("Exported!","Theme exported successfully!")
    except:
        pass

#Load external json file  
def loadthis():
    global json_data
    openjson=tkinter.filedialog.askopenfilename(filetypes =[('json', ['*.json']),('All Files', '*.*')])
    if openjson:
        f=open(openjson)
        json_data=json.load(f)
        f.close()
    update(menu.get())

#Reset current colors to null
def resetthis():
    for i in json_data["color"]:
        if i==menu.get():
            json_data["color"][i][0]=null
            button_light.configure(fg_color=None)
            json_data["color"][i][1]=null
            button_dark.configure(fg_color=None)
            
button_load= customtkinter.CTkButton(master=self, height=40, width=110, text="Load Theme",  command=loadthis)
button_load.place(x=20,y=280)

button_export = customtkinter.CTkButton(master=self, height=40, width=110, text="Export Theme",  command=savethis)
button_export.place(x=140,y=280)

button_reset=customtkinter.CTkButton(master=self, height=40, width=110, text="Reset",  command=resetthis)
button_reset.place(x=260,y=280)

self.mainloop()
