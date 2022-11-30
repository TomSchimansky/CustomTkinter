import customtkinter

app = customtkinter.CTk()
app.geometry("800x900")

tabview_1 = customtkinter.CTkTabview(app)
tabview_1.pack(padx=20, pady=20)

tab_1 = tabview_1.add("tab 1")
tabview_1.insert(0, "tab 2")

tabview_1.add("tab 42")
tabview_1.set("tab 42")
tabview_1.delete("tab 42")
tabview_1.insert(0, "tab 42")
tabview_1.delete("tab 42")
tabview_1.insert(1, "tab 42")
tabview_1.delete("tab 42")

tabview_1.move(0, "tab 2")

b2 = customtkinter.CTkButton(master=tabview_1.tab("tab 2"), text="button tab 2")
b2.pack()

# tabview_1.tab("tab 2").configure(fg_color="red")
tabview_1.configure(state="normal")
# tabview_1.delete("tab 1")

for i in range(10):
    for j in range(30):
        button = customtkinter.CTkButton(tabview_1.tab("tab 1"), height=10, width=30, font=customtkinter.CTkFont(size=8))
        button.grid(row=j, column=i, padx=2, pady=2)

app.mainloop()
