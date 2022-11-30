import customtkinter

#customtkinter.set_widget_scaling(0.9)
#customtkinter.set_window_scaling(0.9)

customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.title("test_scrollbar.py")
app.geometry("800x1200")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

textbox_1 = customtkinter.CTkTextbox(app, fg_color=None, corner_radius=0, border_spacing=0)
textbox_1.grid(row=0, column=0, sticky="nsew")
textbox_1.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

frame_1 = customtkinter.CTkFrame(app, corner_radius=0)
frame_1.grid(row=0, column=1, sticky="nsew")
frame_1.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
frame_1.grid_columnconfigure(0, weight=1)

textbox_2 = customtkinter.CTkTextbox(frame_1, wrap="none")
textbox_2.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
textbox_2.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_2 = customtkinter.CTkTextbox(frame_1, wrap="none", corner_radius=30)
textbox_2.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
textbox_2.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_2 = customtkinter.CTkTextbox(frame_1, wrap="none", corner_radius=0, border_width=30)
textbox_2.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
textbox_2.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_2 = customtkinter.CTkTextbox(frame_1, wrap="none", corner_radius=60, border_width=15)
                                     #fg_color="blue", scrollbar_color="yellow", text_color="red")
textbox_2.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)
textbox_2.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_2 = customtkinter.CTkTextbox(frame_1, wrap="none", corner_radius=0, border_width=0)
textbox_2.grid(row=4, column=0, sticky="nsew", padx=20, pady=20)
textbox_2.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

frame_2 = customtkinter.CTkFrame(app, corner_radius=0, fg_color=None)
frame_2.grid(row=0, column=2, sticky="nsew")
frame_2.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
frame_2.grid_columnconfigure(0, weight=1)

textbox_3 = customtkinter.CTkTextbox(frame_2)
textbox_3.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
textbox_3.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_3 = customtkinter.CTkTextbox(frame_2, corner_radius=30)
textbox_3.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
textbox_3.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_3 = customtkinter.CTkTextbox(frame_2, corner_radius=0, border_width=30)
textbox_3.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
textbox_3.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_3 = customtkinter.CTkTextbox(frame_2, corner_radius=60, border_width=15)
textbox_3.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)
textbox_3.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_3 = customtkinter.CTkTextbox(frame_2, corner_radius=0, border_width=0, border_spacing=20)
textbox_3.grid(row=4, column=0, sticky="nsew", padx=20, pady=20)
textbox_3.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

frame_3 = customtkinter.CTkFrame(app, corner_radius=0, fg_color=None)
frame_3.grid(row=0, column=3, sticky="nsew")
frame_3.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
frame_3.grid_columnconfigure(0, weight=1)

textbox_3 = customtkinter.CTkTextbox(frame_3, activate_scrollbars=False)
textbox_3.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
textbox_3.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_3 = customtkinter.CTkTextbox(frame_3, corner_radius=10, border_width=2, activate_scrollbars=False)
textbox_3.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
textbox_3.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_3 = customtkinter.CTkTextbox(frame_3, corner_radius=0, border_width=2, activate_scrollbars=False)
textbox_3.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
textbox_3.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_3 = customtkinter.CTkTextbox(frame_3, corner_radius=0, border_width=2, activate_scrollbars=False)
textbox_3.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)
textbox_3.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_3 = customtkinter.CTkTextbox(frame_3, corner_radius=0, border_width=0, activate_scrollbars=False, border_spacing=10)
textbox_3.grid(row=4, column=0, sticky="nsew", padx=20, pady=20)
textbox_3.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

textbox_4 = customtkinter.CTkTextbox(app, fg_color=None, corner_radius=0)
textbox_4.grid(row=0, column=4, sticky="nsew")
textbox_4.insert("0.0", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
scrollbar4 = customtkinter.CTkScrollbar(app, command=textbox_4.yview)
scrollbar4.grid(row=0, column=5, sticky="nsew")
textbox_4.configure(yscrollcommand=scrollbar4.set)

# app.after(3000, lambda: customtkinter.set_appearance_mode("light"))
app.mainloop()
