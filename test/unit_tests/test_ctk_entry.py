import customtkinter
import time

app = customtkinter.CTk()

entry_1 = customtkinter.CTkEntry(app, width=100, height=25)
entry_1.pack(padx=20, pady=20)
entry_2 = customtkinter.CTkEntry(app, width=100, height=25)
entry_2.pack(padx=20, pady=20)

txt_var = customtkinter.StringVar(value="test")

entry_1.configure(width=300,
                  height=35,
                  corner_radius=1000,
                  border_width=4,
                  bg_color="green",
                  fg_color=("red", "yellow"),
                  border_color="blue",
                  text_color=("brown", "green"),
                  placeholder_text_color="blue",
                  textvariable=txt_var,
                  placeholder_text="new_placholder",
                  font=("Times New Roman", -8, "bold"),
                  state="normal",
                  insertborderwidth=5,
                  insertwidth=10,
                  justify="right",
                  show="+")

assert entry_1.cget("width") == 300
assert entry_1.cget("height") == 35
assert entry_1.cget("corner_radius") == 1000
assert entry_1.cget("border_width") == 4
assert entry_1.cget("bg_color") == "green"
assert entry_1.cget("fg_color") == ("red", "yellow")
assert entry_1.cget("border_color") == "blue"
assert entry_1.cget("text_color") == ("brown", "green")
assert entry_1.cget("placeholder_text_color") == "blue"
assert entry_1.cget("textvariable") == txt_var
assert entry_1.cget("placeholder_text") == "new_placholder"
assert entry_1.cget("font") == ("Times New Roman", -8, "bold")
assert entry_1.cget("state") == "normal"
assert entry_1.cget("insertborderwidth") == 5
assert entry_1.cget("insertwidth") == 10
assert entry_1.cget("justify") == "right"
# assert entry_1.cget("show") == "+"  # somehow does not work, maybe a tkinter bug?

def test_textvariable():
    txt_var.set("test_2")
    print(entry_1.get())
    assert entry_1.get() == "test_2"

app.after(500, test_textvariable)
app.mainloop()
