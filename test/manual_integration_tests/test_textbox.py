import customtkinter

app = customtkinter.CTk()
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

textbox = customtkinter.CTkTextbox(app)
textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


app.mainloop()
