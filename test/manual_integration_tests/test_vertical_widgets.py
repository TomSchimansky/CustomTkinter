import customtkinter

root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window (you can also use normal tkinter.Tk window)
root_tk.geometry("400x650")
root_tk.title("test_vertical_widgets")

root_tk.grid_columnconfigure(0, weight=1)
root_tk.grid_rowconfigure((0, 1, 2, 3), weight=1)

progressbar_1 = customtkinter.CTkProgressBar(root_tk, orient="horizontal")
progressbar_1.grid(row=0, column=0, pady=20, padx=20)

progressbar_2 = customtkinter.CTkProgressBar(root_tk, orient="vertical")
progressbar_2.grid(row=1, column=0, pady=20, padx=20)

slider_1 = customtkinter.CTkSlider(root_tk, orient="horizontal", command=progressbar_1.set,
                                   button_corner_radius=3, button_length=20)
slider_1.grid(row=2, column=0, pady=20, padx=20)

slider_2 = customtkinter.CTkSlider(root_tk, orient="vertical", command=progressbar_2.set,
                                   button_corner_radius=3, button_length=20)
slider_2.grid(row=3, column=0, pady=20, padx=20)


root_tk.mainloop()
