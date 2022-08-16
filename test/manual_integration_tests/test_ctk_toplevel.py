import customtkinter


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, closing_event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.geometry("500x300")
        self.closing_event = closing_event

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

    def closing(self):
        self.destroy()
        if self.closing_event is not None:
            self.closing_event()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")

        self.button_1 = customtkinter.CTkButton(self, text="Open CTkToplevel", command=self.open_toplevel)
        self.button_1.pack(side="top", padx=40, pady=40)

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None:  # create toplevel window only if not already open
            self.toplevel_window = ToplevelWindow(self, closing_event=self.toplevel_close_event)

    def toplevel_close_event(self):
        self.toplevel_window = None


if __name__ == "__main__":
    app = App()
    app.mainloop()
