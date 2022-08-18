import customtkinter

app = customtkinter.CTk()
app.geometry("400x240")

app.iconify()
app.after(1000, app.deiconify)


def button_function():
    top = customtkinter.CTkToplevel(app)
    top.iconify()

    app.after(1500, top.deiconify)  # show toplevel
    app.after(2000, top.iconify)  # hide toplevel
    app.after(2500, top.deiconify)  # show toplevel
    app.after(3500, app.iconify)  # hide app
    app.after(4000, app.deiconify)  # show app
    app.after(4500, top.lift)  # show app


button = customtkinter.CTkButton(app, command=button_function)
button.pack(pady=20, padx=20)

app.mainloop()
