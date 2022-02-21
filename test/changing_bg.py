import tkinter
import customtkinter  # <- import the CustomTkinter module

root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window (you can also use normal tkinter.Tk window)
#root_tk = tkinter.Tk()
root_tk.geometry("400x300")
root_tk.title("CustomTkinter Test")

customtkinter.set_appearance_mode("System")  # Other: "Dark", "Light"


def rgb2hex(rgb_color: tuple) -> str:
    return "#{:02x}{:02x}{:02x}".format(round(rgb_color[0]), round(rgb_color[1]), round(rgb_color[2]))


def slider_function(value):
    progressbar_1.set(value)
    col_1 = rgb2hex((100, 50, value * 250))
    col_2 = rgb2hex((100, value * 250, 100))
    root_tk.config(bg=col_1)
    #root_tk["background"] = (col_1, col_2)
    #frame_1["bg_color"] = col_1
    frame_1.configure(fg_color=col_2)
    #frame_1.configure(fg_color=bg_col)


frame_1 = customtkinter.CTkFrame(master=root_tk, width=300, height=200, corner_radius=15)
frame_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

label_1 = customtkinter.CTkLabel(master=frame_1)
label_1.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
progressbar_1.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

button_1 = customtkinter.CTkButton(master=frame_1, corner_radius=10)
button_1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
button_1.configure(state="disabled")

slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_function, from_=0, to=1, progress_color="gray20")
slider_1.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
#slider_1.set(1.5)

entry_1 = customtkinter.CTkEntry(master=frame_1)
entry_1.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

checkbox_1 = customtkinter.CTkCheckBox(master=root_tk)
checkbox_1.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

#frame_1.config(bg_color="red")

root_tk.mainloop()
