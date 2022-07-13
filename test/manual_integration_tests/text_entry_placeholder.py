import customtkinter

app = customtkinter.CTk()  # create CTk window like you do with the Tk window (you can also use normal tkinter.Tk window)
app.geometry("400x400")
app.title("test_entry_placeholder.py")

str_var = customtkinter.StringVar(value="test")

entry_1 = customtkinter.CTkEntry(app, placeholder_text="placeholder", textvariable=str_var)
entry_1.pack(pady=20)

entry_2 = customtkinter.CTkEntry(app, placeholder_text="placeholder", textvariable=str_var)
entry_2.pack(pady=20)
entry_2.insert(0, "sdfjk ")
entry_2.delete(0, 2)

entry_3 = customtkinter.CTkEntry(app, placeholder_text="placeholder")
entry_3.pack(pady=(40, 20))
entry_3.insert(0, "sdfjk")
entry_3.delete(0, "end")

entry_4 = customtkinter.CTkEntry(app, placeholder_text="password", show="*")
entry_4.pack(pady=(20, 20))
entry_4.insert(0, "sdfjk")
entry_4.delete(0, 2)

app.mainloop()
