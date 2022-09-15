import customtkinter

customtkinter.set_window_scaling(1.3)

app = customtkinter.CTk()
toplevel = customtkinter.CTkToplevel(app)


app.after(1000, lambda: app.geometry("300x300"))
app.after(2000, lambda: app.geometry("-100-100"))
app.after(3000, lambda: app.geometry("+-100+-100"))
app.after(4000, lambda: app.geometry("+100+100"))
app.after(5000, lambda: app.geometry("300x300-100-100"))
app.after(6000, lambda: app.geometry("300x300+-100+-100"))
app.after(7000, lambda: app.geometry("300x300+100+100"))

app.after(8000, lambda: app.geometry("400x400"))
app.after(9000, lambda: app.geometry("+400+400"))


app.after(10000, lambda: toplevel.geometry("300x300"))
app.after(11000, lambda: toplevel.geometry("-100-100"))
app.after(12000, lambda: toplevel.geometry("+-100+-100"))
app.after(13000, lambda: toplevel.geometry("+100+100"))
app.after(14000, lambda: toplevel.geometry("300x300-100-100"))
app.after(15000, lambda: toplevel.geometry("300x300+-100+-100"))
app.after(16000, lambda: toplevel.geometry("300x300+100+100"))

app.after(17000, lambda: toplevel.geometry("300x300"))
app.after(18000, lambda: toplevel.geometry("+500+500"))


app.after(19000, lambda: print("app:", app.geometry()))
app.after(19000, lambda: print("toplevel:", toplevel.geometry()))


app.mainloop()
