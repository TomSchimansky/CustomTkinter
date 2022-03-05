import customtkinter
import tkinter

customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.geometry("600x1000")

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)
app.grid_columnconfigure(3, weight=1)

f1 = customtkinter.CTkFrame(app, fg_color="gray10", corner_radius=0)
f1.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew")
f1.grid_columnconfigure(0, weight=1)

f2 = customtkinter.CTkFrame(app, fg_color="gray10", corner_radius=0)
f2.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nsew")
f2.grid_columnconfigure(0, weight=1)

f3 = customtkinter.CTkFrame(app, fg_color="gray85", corner_radius=0)
f3.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="nsew")
f3.grid_columnconfigure(0, weight=1)

f4 = customtkinter.CTkFrame(app, fg_color="gray90", corner_radius=0)
f4.grid(row=0, column=3, rowspan=1, columnspan=1, sticky="nsew")
f4.grid_columnconfigure(0, weight=1)

for i in range(0, 21, 1):
    b = customtkinter.CTkButton(f1, corner_radius=i, height=34, border_width=2, text=f"{i} {i-2}",
                                border_color="white", fg_color=None, text_color="white")
    b.grid(row=i, column=0, pady=5, padx=15, sticky="nsew")

    b = customtkinter.CTkButton(f2, corner_radius=i, height=34, border_width=0, text=f"{i}",
                                fg_color="#228da8")
    b.grid(row=i, column=0, pady=5, padx=15, sticky="nsew")

    b = customtkinter.CTkButton(f3, corner_radius=i, height=34, border_width=2, text=f"{i} {i-2}",
                                fg_color=None, border_color="gray20", text_color="black")
    b.grid(row=i, column=0, pady=5, padx=15, sticky="nsew")

    b = customtkinter.CTkButton(f4, corner_radius=i, height=34, border_width=0, text=f"{i}",
                                border_color="gray10", fg_color="#228da8")
    b.grid(row=i, column=0, pady=5, padx=15, sticky="nsew")

customtkinter.CTkSettings.print_settings()
app.mainloop()