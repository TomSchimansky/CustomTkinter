import customtkinter
import tkinter.ttk as ttk

app = customtkinter.CTk()

tabview = customtkinter._CTkTabview(app)
tabview.pack(pady=20, padx=20)

tabview.create_tab(identifier="tab1", text="Tab 1")
tabview.select_tab("tab1")


switch = customtkinter.CTkSwitch(app, text="Darkmode", onvalue="dark", offvalue="light",
                                 command=lambda: customtkinter.set_appearance_mode(switch.get()))
switch.pack(padx=20, pady=20)
app.mainloop()
