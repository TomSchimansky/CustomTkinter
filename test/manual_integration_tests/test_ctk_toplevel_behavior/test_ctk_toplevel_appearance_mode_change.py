import customtkinter
import sys

customtkinter.set_appearance_mode("dark")


app = customtkinter.CTk()
app.geometry("400x400+300+300")

toplevel = customtkinter.CTkToplevel(app)
toplevel.geometry("350x240+800+300")


def change_appearance_mode():
    # test appearance mode change while withdrawn
    app.after(500, toplevel.withdraw)
    app.after(1500, lambda: customtkinter.set_appearance_mode("light"))
    app.after(2500, toplevel.deiconify)

    # test appearance mode change while iconified
    app.after(3500, toplevel.iconify)
    app.after(4500, lambda: customtkinter.set_appearance_mode("dark"))
    app.after(5500, toplevel.deiconify)

    if sys.platform.startswith("win"):
        # test appearance mode change while zoomed
        app.after(6500, lambda: toplevel.state("zoomed"))
        app.after(7500, lambda: customtkinter.set_appearance_mode("light"))
        app.after(8500, lambda: toplevel.state("normal"))


button_1 = customtkinter.CTkButton(app, text="start test", command=change_appearance_mode)
button_1.pack(pady=20, padx=20)

app.mainloop()
