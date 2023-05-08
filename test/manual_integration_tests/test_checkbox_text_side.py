import customtkinter as ctk


def flip():
    if not flipping.get():
        changing.configure(text_side='left')
    else:
        changing.configure(text_side='right')


window = ctk.CTk()
window.geometry('150x150')

ctk.CTkCheckBox(window).pack()
ctk.CTkCheckBox(window, text_side='right').pack()
changing = ctk.CTkCheckBox(window, text_side='left')
changing.pack()
flipping = ctk.CTkCheckBox(window, text='', width=24, command=flip)
flipping.pack()

window.mainloop()
