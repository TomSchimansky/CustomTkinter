import tkinter
import customtkinter

# test with scaling
# customtkinter.set_widget_scaling(2)
# customtkinter.set_window_scaling(2)
# customtkinter.set_spacing_scaling(2)

customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.title("test_scrollbar.py")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure((0, 2), weight=1)

tk_textbox = tkinter.Text(app, highlightthickness=0, padx=5, pady=5)
tk_textbox.grid(row=0, column=0, sticky="nsew")
ctk_textbox_scrollbar = customtkinter.CTkScrollbar(app, command=tk_textbox.yview)
ctk_textbox_scrollbar.grid(row=0, column=1, padx=0, sticky="ns")
tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

frame_1 = customtkinter.CTkFrame(app)
frame_1.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
frame_1.grid_rowconfigure((0, 1), weight=1)
frame_1.grid_columnconfigure((0, ), weight=1)
tk_textbox_1 = tkinter.Text(frame_1, highlightthickness=0, padx=5, pady=5)
tk_textbox_1.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)
ctk_textbox_scrollbar_1 = customtkinter.CTkScrollbar(frame_1, command=tk_textbox_1.yview)
ctk_textbox_scrollbar_1.grid(row=0, column=1, sticky="ns", padx=(0, 5), pady=5)
tk_textbox_1.configure(yscrollcommand=ctk_textbox_scrollbar_1.set)
ctk_textbox_scrollbar_1.configure(scrollbar_color="red", scrollbar_hover_color="darkred",
                                  border_spacing=0, width=12, fg_color="green", corner_radius=4)

frame_2 = customtkinter.CTkFrame(frame_1)
frame_2.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
frame_2.grid_rowconfigure((0, ), weight=1)
frame_2.grid_columnconfigure((0, ), weight=1)
tk_textbox_2 = tkinter.Text(frame_2, highlightthickness=0, padx=5, pady=5, wrap="none")
tk_textbox_2.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)
ctk_textbox_scrollbar_2 = customtkinter.CTkScrollbar(frame_2, command=tk_textbox_2.yview)
ctk_textbox_scrollbar_2.grid(row=0, column=1, sticky="ns", padx=(0, 5), pady=5)
ctk_textbox_scrollbar_2_horizontal = customtkinter.CTkScrollbar(frame_2, command=tk_textbox_2.xview, orientation="horizontal")
ctk_textbox_scrollbar_2_horizontal.grid(row=1, column=0, sticky="ew", padx=(5, 0), pady=(0, 5))
tk_textbox_2.configure(yscrollcommand=ctk_textbox_scrollbar_2.set, xscrollcommand=ctk_textbox_scrollbar_2_horizontal.set)

tk_textbox.configure(font=(customtkinter.ThemeManager.theme["text"]["font"], customtkinter.ThemeManager.theme["text"]["size"]))
tk_textbox_1.configure(font=(customtkinter.ThemeManager.theme["text"]["font"], customtkinter.ThemeManager.theme["text"]["size"]))
tk_textbox_2.configure(font=(customtkinter.ThemeManager.theme["text"]["font"], customtkinter.ThemeManager.theme["text"]["size"]))

tk_textbox.insert("insert", "\n".join([str(i) for i in range(100)]))
tk_textbox_1.insert("insert", "\n".join([str(i) for i in range(1000)]))
tk_textbox_2.insert("insert", "\n".join([str(i) + " - "*30 for i in range(10000)]))

app.mainloop()
