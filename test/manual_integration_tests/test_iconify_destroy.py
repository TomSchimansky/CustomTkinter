import customtkinter

app = customtkinter.CTk()
app.geometry("400x240")

app.withdraw()
app.after(1000, app.deiconify)


def button_function():
    top = customtkinter.CTkToplevel(app)
    top.withdraw()

    app.after(1000, top.deiconify)  # show toplevel
    app.after(2000, top.iconify)  # hide toplevel
    app.after(2500, top.deiconify)  # show toplevel
    app.after(3500, app.iconify)  # hide app
    app.after(4000, app.deiconify)  # show app
    app.after(5000, app.destroy)  # destroy everything


button = customtkinter.CTkButton(app, command=button_function)
button.pack(pady=20, padx=20)

app.mainloop()
