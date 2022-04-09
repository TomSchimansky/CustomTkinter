import tkinter
import tkinter.ttk as ttk
import customtkinter

root_tk = customtkinter.CTk()
root_tk.geometry("1400x480")
root_tk.title("CustomTkinter TTk Compatibility Test")

root_tk.grid_rowconfigure(0, weight=1)
root_tk.grid_columnconfigure((0, 1, 2, 3, 5), weight=1)


button_0 = customtkinter.CTkButton(root_tk)
button_0.grid(padx=20, pady=20, row=0, column=0)

frame_1 = tkinter.Frame(master=root_tk)
frame_1.grid(padx=20, pady=20, row=0, column=1, sticky="nsew")
button_1 = customtkinter.CTkButton(frame_1, text="tkinter.Frame")
button_1.pack(pady=20, padx=20)

frame_2 = tkinter.LabelFrame(master=root_tk, text="Tkinter LabelFrame")
frame_2.grid(padx=20, pady=20, row=0, column=2, sticky="nsew")
button_2 = customtkinter.CTkButton(frame_2, text="tkinter.LabelFrame")
button_2.pack(pady=20, padx=20)

frame_3 = ttk.Frame(master=root_tk)
frame_3.grid(padx=20, pady=20, row=0, column=3, sticky="nsew")
button_3 = customtkinter.CTkButton(frame_3, text="ttk.Frame")
button_3.pack(pady=20, padx=20)

frame_4 = ttk.LabelFrame(master=root_tk, text="TTk LabelFrame")
frame_4.grid(padx=20, pady=20, row=0, column=4, sticky="nsew")
button_4 = customtkinter.CTkButton(frame_4)
button_4.pack(pady=20, padx=20)

frame_5 = ttk.Notebook(master=root_tk)
frame_5.grid(padx=20, pady=20, row=0, column=5, sticky="nsew")
button_5 = customtkinter.CTkButton(frame_5, text="ttk.Notebook")
button_5.pack(pady=20, padx=20)

ttk_style = ttk.Style()
ttk_style.configure(frame_3.winfo_class(), background='red')

root_tk.mainloop()
