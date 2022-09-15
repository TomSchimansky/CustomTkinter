import customtkinter

customtkinter.set_appearance_mode("dark")


app = customtkinter.CTk()
app.geometry("400x240")


def change_appearance_mode():
    # test zoom with withdraw
    app.after(1000, lambda: app.state("zoomed"))
    app.after(2000, app.withdraw)
    app.after(3000, app.deiconify)
    app.after(4000, lambda: app.state("normal"))

    # test zoom with iconify
    app.after(5000, lambda: app.state("zoomed"))
    app.after(6000, app.iconify)
    app.after(7000, app.deiconify)
    app.after(8000, lambda: app.state("normal"))


button_1 = customtkinter.CTkButton(app, text="start test", command=change_appearance_mode)
button_1.pack(pady=20, padx=20)

app.mainloop()
