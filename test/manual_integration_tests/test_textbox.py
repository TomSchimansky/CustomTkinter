import customtkinter

#customtkinter.set_widget_scaling(2)
#customtkinter.set_window_scaling(2)
#customtkinter.set_spacing_scaling(2)

customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.title("test_scrollbar.py")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure((0, 1), weight=1)

textbox_1 = customtkinter.CTkScrolledTextbox(app, fg_color=None, corner_radius=0)
textbox_1.grid(row=0, column=0, sticky="nsew")
textbox_1.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

frame_1 = customtkinter.CTkFrame(app, corner_radius=0)
frame_1.grid(row=0, column=1, sticky="nsew")
frame_1.grid_rowconfigure((0, 1), weight=1)
frame_1.grid_columnconfigure(0, weight=1)

textbox_2 = customtkinter.CTkScrolledTextbox(frame_1, wrap="none")
textbox_2.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
textbox_2.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)


app.mainloop()
