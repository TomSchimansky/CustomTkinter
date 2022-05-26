from tkinter import *
import customtkinter

ws = Tk()
ws.title('PythonGuides')
ws.geometry('400x300')
ws.config(bg='#F2B90C')

def display_selected(choice):
    choice = variable.get()
    print(choice)

countries = ['Bahamas','Canada', 'Cuba','United States']

# setting variable for Integers
variable = StringVar()
variable.set("test")

# creating widget
dropdown = OptionMenu(
    ws,
    variable,
    *countries,
    command=display_selected
)

# positioning widget
dropdown.pack(pady=10, padx=10)

optionmenu_1 = customtkinter.CTkOptionMenu(master=ws, values=["option 1", "option 2", "number 42"])
optionmenu_1.pack(pady=10, padx=10)

# infinite loop
ws.mainloop()
