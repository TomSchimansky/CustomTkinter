import tkinter
import customtkinter

app = customtkinter.CTk()
app.title('test_optionmenu.py')
app.geometry('400x300')


def select_callback(choice):
    choice = variable.get()
    print("display_selected", choice)


countries = ['Bahamas', 'Canada', 'Cuba', 'United States']

variable = tkinter.StringVar()
variable.set("test")

optionmenu_tk = tkinter.OptionMenu(app, variable, *countries, command=select_callback)
optionmenu_tk.pack(pady=10, padx=10)

optionmenu_1 = customtkinter.CTkOptionMenu(app, variable=variable, values=countries, command=select_callback)
optionmenu_1.pack(pady=10, padx=10)

app.mainloop()
