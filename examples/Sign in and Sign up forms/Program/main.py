#https://github.com/Northstrix/customtkinter-sign-in-and-sign-up-forms
from customtkinter import *
from PIL import Image

def sign_in_window():
    global username_entry, password_entry
    app = CTk()
    app.geometry("600x403")
    app.resizable(0, 0)
    app.title("Sign in form")
    # Center the window on the screen
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    window_width = 600
    window_height = 403

    position_x = int((screen_width - window_width) / 2)
    position_y = int((screen_height - window_height) / 2)

    app.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    side_img_data = Image.open("./assets/signin.png")
    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 403))

    CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

    frame = CTkFrame(master=app, width=300, height=403, fg_color="#F3F9F9", corner_radius=0)
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    CTkLabel(master=frame, text="Shalom!", text_color="#26252A", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="Username:", text_color="#26252A", anchor="w", justify="left", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(26, 0), padx=(25, 0))
    username_entry = CTkEntry(master=frame, width=225, fg_color="#F3F9F9", border_color="#26252A", border_width=1, text_color="#26252A")
    username_entry.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="Password:", text_color="#26252A", anchor="w", justify="left", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    password_entry = CTkEntry(master=frame, width=225, fg_color="#F3F9F9", border_color="#26252A", border_width=1, text_color="#26252A", show="*")
    password_entry.pack(anchor="w", padx=(25, 0))

    CTkButton(master=frame, text="Sign in", fg_color="#222126", hover_color="#26e1e1", font=("Arial Bold", 12), text_color="#F3F9F9", width=225, command=lambda: sign_in_action(username_entry, password_entry, app)).pack(anchor="w", pady=(40, 0), padx=(25, 0))

    dnthal1 = CTkLabel(master=frame, text="Don't have an account?", text_color="#7E7E7E", font=("Arial Bold", 12))
    dnthal1.place(x=25, y=350)
    signuplabel = CTkLabel(master=frame, text="Sign Up", text_color="#26e1e1", font=("Arial Bold", 12, "underline"))
    signuplabel.place(x=162, y=350)
    signuplabel.bind("<Button-1>", lambda e: open_signup_form(app))
    signuplabel.bind("<Enter>", lambda e: e.widget.config(cursor="hand2"))
    signuplabel.bind("<Leave>", lambda e: e.widget.config(cursor=""))

    app.mainloop()

def print_sign_in_data(username_entry, password_entry, form):
    username = username_entry.get()
    password = password_entry.get()
    print(f"Username: {username}, Password: {password}")
    form.destroy()

def sign_in_action(username_entry, password_entry, form):
    print_sign_in_data(username_entry, password_entry, form)

def open_signup_form(root):
    signup_form = CTkToplevel(root)
    signup_form.geometry("600x403")
    signup_form.resizable(0, 0)
    signup_form.title("Sign up form")

    side_img_data = Image.open("./assets/signup.png")
    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 403))

    CTkLabel(master=signup_form, text="", image=side_img).pack(expand=True, side="left")

    frame = CTkFrame(master=signup_form, width=300, height=403, fg_color="#F3F9F9", corner_radius=0)
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    CTkLabel(master=frame, text="Sign Up", text_color="#26252A", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Create an account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="Username:", text_color="#26252A", anchor="w", justify="left", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
    username_entry_signup = CTkEntry(master=frame, width=225, fg_color="#F3F9F9", border_color="#26252A", border_width=1, text_color="#26252A")
    username_entry_signup.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="Password:", text_color="#26252A", anchor="w", justify="left", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
    password_entry_signup = CTkEntry(master=frame, width=225, fg_color="#F3F9F9", border_color="#26252A", border_width=1, text_color="#26252A", show="*")
    password_entry_signup.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="Confirm Password:", text_color="#26252A", anchor="w", justify="left", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
    confirm_password_entry_signup = CTkEntry(master=frame, width=225, fg_color="#F3F9F9", border_color="#26252A", border_width=1, text_color="#26252A", show="*")
    confirm_password_entry_signup.pack(anchor="w", padx=(25, 0))

    CTkButton(master=frame, text="Sign Up", fg_color="#222126", hover_color="#26e1e1", font=("Arial Bold", 12), text_color="#F3F9F9", width=225, command=lambda: check_passwords(username_entry_signup, password_entry_signup, confirm_password_entry_signup, signup_form)).pack(anchor="w", pady=(20, 0), padx=(25, 0))

def check_passwords(username_entry, password_entry, confirm_password_entry, form):
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if password == confirm_password:
        print(f"Username: {username}, Password: {password}")
        form.destroy()
    else:
        print("Passwords do not match")

if __name__ == "__main__":
    sign_in_window()