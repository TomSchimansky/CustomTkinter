import customtkinter

app = customtkinter.CTk()

tabview_1 = customtkinter._CTkTabview(app, state="disabled")
tabview_1.pack(padx=20, pady=20)

tab_1 = tabview_1.add("tab 2")
tabview_1.insert(0, "tab 1")

tabview_1.add("tab 42")
tabview_1.set("tab 42")
tabview_1.delete("tab 42")
tabview_1.insert(0, "tab 42")
tabview_1.delete("tab 42")
tabview_1.insert(1, "tab 42")
tabview_1.delete("tab 42")

#b1 = customtkinter.CTkButton(master=tab_1, text="button tab 1")
#b1.pack(pady=20)
b2 = customtkinter.CTkButton(master=tabview_1.tab("tab 2"), text="button tab 2")
b2.pack()

tabview_1.tab("tab 2").configure(fg_color="red")
# tabview_1.delete("tab 1")

app.mainloop()
