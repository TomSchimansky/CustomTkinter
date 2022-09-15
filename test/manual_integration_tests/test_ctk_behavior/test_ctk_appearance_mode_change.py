import customtkinter
import sys

customtkinter.set_appearance_mode("dark")


app = customtkinter.CTk()
app.geometry("400x240")


def change_appearance_mode():
    # test appearance mode change while withdrawn
    app.after(500, app.withdraw)
    app.after(1500, lambda: customtkinter.set_appearance_mode("light"))
    app.after(2500, app.deiconify)

    # test appearance mode change while iconified
    app.after(3500, app.iconify)
    app.after(4500, lambda: customtkinter.set_appearance_mode("dark"))
    app.after(5500, app.deiconify)

    if sys.platform.startswith("win"):
        # test appearance mode change while zoomed
        app.after(6500, lambda: app.state("zoomed"))
        app.after(7500, lambda: customtkinter.set_appearance_mode("light"))
        app.after(8500, lambda: app.state("normal"))


button_1 = customtkinter.CTkButton(app, text="start test", command=change_appearance_mode)
button_1.pack(pady=20, padx=20)

app.mainloop()
