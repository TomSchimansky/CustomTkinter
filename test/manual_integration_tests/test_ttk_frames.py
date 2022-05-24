import tkinter
import tkinter.ttk as ttk
import customtkinter

customtkinter.set_appearance_mode("light")

app = customtkinter.CTk()
app.geometry("1400x480")
app.title("CustomTkinter TTk Compatibility Test")

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure((0, 1, 2, 3, 5, 6), weight=1)


button_0 = customtkinter.CTkButton(app)
button_0.grid(padx=20, pady=20, row=0, column=0)

frame_1 = tkinter.Frame(master=app)
frame_1.grid(padx=20, pady=20, row=0, column=1, sticky="nsew")
button_1 = customtkinter.CTkButton(frame_1, text="tkinter.Frame")
button_1.pack(pady=20, padx=20)

frame_2 = tkinter.LabelFrame(master=app, text="Tkinter LabelFrame")
frame_2.grid(padx=20, pady=20, row=0, column=2, sticky="nsew")
button_2 = customtkinter.CTkButton(frame_2, text="tkinter.LabelFrame")
button_2.pack(pady=20, padx=20)

frame_3 = customtkinter.CTkFrame(master=app)
frame_3.grid(padx=20, pady=20, row=0, column=3, sticky="nsew")
label_3 = customtkinter.CTkLabel(master=frame_3, text="CTkFrame Label", fg_color=("gray95", "gray15"))
label_3.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky="ew")
button_3 = customtkinter.CTkButton(frame_3, text="CTkFrame")
button_3.grid(row=1, column=0, padx=20)
frame_3.grid_rowconfigure(1, weight=1)
frame_3.grid_columnconfigure((0, ), weight=1)

frame_4 = ttk.Frame(master=app)
frame_4.grid(padx=20, pady=20, row=0, column=4, sticky="nsew")
button_4 = customtkinter.CTkButton(frame_4, text="ttk.Frame")
button_4.pack(pady=20, padx=20)

frame_5 = ttk.LabelFrame(master=app, text="TTk LabelFrame")
frame_5.grid(padx=20, pady=20, row=0, column=5, sticky="nsew")
button_5 = customtkinter.CTkButton(frame_5)
button_5.pack(pady=20, padx=20)

frame_6 = ttk.Notebook(master=app)
frame_6.grid(padx=20, pady=20, row=0, column=6, sticky="nsew")
button_6 = customtkinter.CTkButton(frame_6, text="ttk.Notebook")
button_6.pack(pady=20, padx=20)

ttk_style = ttk.Style()
ttk_style.configure(frame_3.winfo_class(), background='red')

app.mainloop()
