import customtkinter

app = customtkinter.CTk()

tabview_1 = customtkinter._CTkTabview(app)
tabview_1.pack(padx=20, pady=20)
tabview_1.add("tab 1")
tabview_1.insert(0, "tab 0 g |ß$§")

app.update()

tabview_1._segmented_button._buttons_dict["tab 0 g |ß$§"]._text_label.configure(padx=0, pady=0, bd=0)
tabview_1._segmented_button._buttons_dict["tab 0 g |ß$§"]._text_label.configure(bg="red")
app.mainloop()
