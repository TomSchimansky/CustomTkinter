import customtkinter

customtkinter.set_window_scaling(1.3)

app = customtkinter.CTk()
app.geometry("300x300")
app.geometry("-100-100")
app.geometry("+-100+-100")
app.geometry("+100+100")
app.geometry("300x300-100-100")
app.geometry("300x300+-100+-100")
app.geometry("300x300+100+100")

app.geometry("400x400")
app.geometry("+400+400")
app.update()
print(app.geometry())
assert app.geometry() == "400x400+400+400"

toplevel = customtkinter.CTkToplevel(app)
toplevel.geometry("300x300")
toplevel.geometry("-100-100")
toplevel.geometry("+-100+-100")
toplevel.geometry("+100+100")
toplevel.geometry("300x300-100-100")
toplevel.geometry("300x300+-100+-100")
toplevel.geometry("300x300+100+100")

toplevel.geometry("300x300")
toplevel.geometry("+500+500")
toplevel.update()
print(toplevel.geometry())
assert toplevel.geometry() == "300x300+500+500"

app.mainloop()
