import customtkinter

app = customtkinter.CTk()
app.geometry("400x240")


def button_function():

    top = customtkinter.CTkToplevel(app)

    app.after(1000, top.iconify)  # hide toplevel
    app.after(1500, top.deiconify)  # show toplevel
    app.after(2500, app.iconify)  # hide app
    app.after(3000, app.deiconify)  # show app
    app.after(4000, app.destroy)  # destroy everything


button = customtkinter.CTkButton(app, command=button_function)
button.pack(pady=20, padx=20)

app.mainloop()
