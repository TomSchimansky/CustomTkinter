import tkinter
import time

from customtkinter.customtkinter_label import CTkLabel
from customtkinter.customtkinter_button import CTkButton
from customtkinter.customtkinter_entry import CTkEntry
from customtkinter.customtkinter_color_manager import CTkColorManager


class CTkDialog:
    def __init__(self,
                 master=None,
                 title="CTkDialog",
                 text="CTkDialog",
                 fg_color=CTkColorManager.MAIN,
                 hover_color=CTkColorManager.MAIN_HOVER):
        self.master = master

        self.user_input = None
        self.running = False

        self.height = len(text.split("\n"))*20 + 150
        self.fg_color = fg_color
        self.hover_color = hover_color

        self.top = tkinter.Toplevel()
        self.top.geometry("300x{}".format(self.height))
        self.top.resizable(False, False)
        self.top.title(title)

        self.label_frame = tkinter.Frame(master=self.top,
                                         width=300,
                                         height=self.height-100)
        self.label_frame.place(relx=0.5, rely=0, anchor=tkinter.N)

        self.button_and_entry_frame = tkinter.Frame(master=self.top,
                                                    width=300,
                                                    height=100)
        self.button_and_entry_frame.place(relx=0.5, rely=1, anchor=tkinter.S)

        self.myLabel = CTkLabel(master=self.label_frame,
                                text=text,
                                width=300,
                                height=self.height-100)
        self.myLabel.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.entry = CTkEntry(master=self.button_and_entry_frame,
                              width=180)
        self.entry.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.ok_button = CTkButton(master=self.button_and_entry_frame,
                                   text='Ok',
                                   command=self.ok_event,
                                   fg_color=self.fg_color,
                                   hover_color=self.hover_color)
        self.ok_button.place(relx=0.25, rely=0.75, anchor=tkinter.CENTER)

        self.cancel_button = CTkButton(master=self.button_and_entry_frame,
                                       text='Cancel',
                                       command=self.cancel_event,
                                       fg_color=self.fg_color,
                                       hover_color=self.hover_color)
        self.cancel_button.place(relx=0.75, rely=0.75, anchor=tkinter.CENTER)

    def ok_event(self):
        self.user_input = self.entry.get()
        self.running = False

    def cancel_event(self):
        self.running = False

    def get_input(self):
        self.running = True

        while self.running:
            self.top.update()
            time.sleep(0.01)

        time.sleep(0.05)
        self.top.destroy()
        return self.user_input


if __name__ == "__main__":
    import customtkinter
    customtkinter.enable_macos_darkmode()
    customtkinter.set_appearance_mode("System")

    app = tkinter.Tk()
    app.title("CTkDialog Test")

    def button_click_event():
        dialog = CTkDialog(master=None, text="Type in a number:", title="Test", fg_color="green", hover_color="darkgreen")
        print("Number:", dialog.get_input())

    button = CTkButton(master=app, text="Open Dialog", command=button_click_event)
    button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    app.mainloop()
    customtkinter.disable_macos_darkmode()
