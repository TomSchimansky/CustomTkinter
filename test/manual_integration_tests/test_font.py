import customtkinter


app = customtkinter.CTk()
app.geometry("1200x1000")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure((0, 1), weight=1)

frame_1 = customtkinter.CTkFrame(app)
frame_1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
frame_2 = customtkinter.CTkFrame(app)
frame_2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

def set_scaling(scaling):
    customtkinter.set_widget_scaling(scaling)
    customtkinter.set_spacing_scaling(scaling)

scaling_button = customtkinter._CTkSegmentedButton(frame_1, values=[0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 2.0], command=set_scaling)
scaling_button.pack(pady=(2, 10))

b = customtkinter.CTkButton(frame_1, text="single name", font=("Times", ))
b.pack(pady=2)
b = customtkinter.CTkButton(frame_1, text="name with size", font=("Times", 18))
b.pack(pady=2)
b = customtkinter.CTkButton(frame_1, text="name with negative size", font=("Times", -18))
b.pack(pady=2)
b = customtkinter.CTkButton(frame_1, text="extra keywords", font=("Times", -18, "bold italic underline overstrike"))
b.pack(pady=2)

b = customtkinter.CTkButton(frame_1, text="object default")
b.pack(pady=(10, 2))
b = customtkinter.CTkButton(frame_1, text="object single name", font=customtkinter._CTkFont("Times"))
b.pack(pady=2)
b = customtkinter.CTkButton(frame_1, text="object with name and size", font=customtkinter._CTkFont("Times", 18))
b.pack(pady=2)
b = customtkinter.CTkButton(frame_1, text="object with name and negative size", font=customtkinter._CTkFont("Times", -18))
b.pack(pady=2)
b = customtkinter.CTkButton(frame_1, text="object with extra keywords",
                            font=customtkinter._CTkFont("Times", -18, weight="bold", slant="italic", underline=True, overstrike=True))
b.pack(pady=2)

b1 = customtkinter.CTkButton(frame_1, text="object default modified")
b1.pack(pady=(10, 2))
b1.cget("font").configure(size=9)
print("test_font.py:", b1.cget("font").cget("size"), b1.cget("font").cget("family"))

b2 = customtkinter.CTkButton(frame_1, text="object default overridden")
b2.pack(pady=10)
b2.configure(font=customtkinter._CTkFont(family="Times"))

label_font = customtkinter._CTkFont(size=5)
for i in range(30):
    l = customtkinter.CTkLabel(frame_2, font=label_font, height=0)
    l.grid(row=i, column=0, pady=1)
    b = customtkinter.CTkButton(frame_2, font=label_font, height=5)
    b.grid(row=i, column=1, pady=1)
    c = customtkinter.CTkCheckBox(frame_2, font=label_font)
    c.grid(row=i, column=2, pady=1)
    c = customtkinter.CTkComboBox(frame_2, font=label_font, height=15)
    c.grid(row=i, column=3, pady=1)
    e = customtkinter.CTkEntry(frame_2, font=label_font, height=15, placeholder_text="testtest")
    e.grid(row=i, column=4, pady=1)
frame_2.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

app.after(1500, lambda: label_font.configure(size=10))
# app.after(1500, lambda: l.configure(text="dshgfldjskhfjdslafhdjsgkkjdaslö"))
app.mainloop()
