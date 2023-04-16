import tkinter as tk
import customtkinter as ctk

window = ctk.CTk()

ctk.CTkLabel(window, text='Flat', padx=10).pack()
ctk.CTkLabel(window, text='Sunken', relief='sunken', borderwidth=5, padx=10).pack()
ctk.CTkLabel(window, text='Raised', relief='raised', borderwidth=5, padx=10).pack()
ctk.CTkLabel(window, text='Groove', relief='groove', borderwidth=5, padx=10).pack()
ctk.CTkLabel(window, text='Ridge', relief='ridge', borderwidth=5, padx=10).pack()

ctk.CTkLabel(window, text="bd", relief='raised', bd=5, padx=10).pack()
ctk.CTkLabel(window, text="both", relief='raised', bd=5, borderwidth=1, padx=10).pack()
ctk.CTkLabel(window, text="both flipped", relief='raised', borderwidth=1, bd=5, padx=10).pack()

configure = ctk.CTkLabel(window, text="configured", relief='raised', bd=5, padx=10)
configure.configure(borderwidth=1)
configure.pack()

window.mainloop()
