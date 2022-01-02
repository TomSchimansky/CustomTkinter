import tkinter as tk
import customtkinter as ctk

root = tk.Tk()

btn = ctk.CTkButton(master=root, text="EXIT", command=root.destroy).pack()

root.mainloop()