from tkinter import *
import customtkinter

ws = customtkinter.CTk()
ws.title('PythonGuides')
ws.geometry('400x300')

def display_selected(choice):
    choice = variable.get()
    print("display_selected", choice)

countries = ['Bahamas','Canada', 'Cuba','United States']

# setting variable for Integers
variable = StringVar()
variable.set("test")

# creating widget
optionmenu_tk = OptionMenu(ws, variable, *countries, command=display_selected)
optionmenu_tk.pack(pady=10, padx=10)

optionmenu_1 = customtkinter.CTkOptionMenu(master=ws, variable=variable, values=countries, command=display_selected)
optionmenu_1.pack(pady=10, padx=10)

# infinite loop
ws.mainloop()
