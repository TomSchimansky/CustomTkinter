import customtkinter


class TestCTkToplevel():
    def __init__(self):
        self.root_ctk = customtkinter.CTk()
        self.root_ctk.title("TestCTkToplevel")
        self.ctk_toplevel = customtkinter.CTkToplevel()
        self.ctk_toplevel.title("TestCTkToplevel")

    def clean(self):
        self.root_ctk.quit()
        self.ctk_toplevel.withdraw()
        self.root_ctk.withdraw()

    def main(self):
        self.execute_tests()
        self.root_ctk.mainloop()

    def execute_tests(self):
        print("\nTestCTkToplevel started:")
        start_time = 0

        self.root_ctk.after(start_time, self.test_geometry)
        start_time += 100

        self.root_ctk.after(start_time, self.test_scaling)
        start_time += 100

        self.root_ctk.after(start_time, self.test_configure)
        start_time += 100

        self.root_ctk.after(start_time, self.test_appearance_mode)
        start_time += 100

        self.root_ctk.after(start_time, self.test_iconify)
        start_time += 1500

        self.root_ctk.after(start_time, self.clean)

    def test_geometry(self):
        print(" -> test_geometry: ", end="")
        self.ctk_toplevel.geometry("200x300+200+300")
        assert self.ctk_toplevel.current_width == 200 and self.ctk_toplevel.current_height == 300

        self.ctk_toplevel.minsize(300, 400)
        assert self.ctk_toplevel.current_width == 300 and self.ctk_toplevel.current_height == 400
        assert self.ctk_toplevel.min_width == 300 and self.ctk_toplevel.min_height == 400

        self.ctk_toplevel.maxsize(400, 500)
        self.ctk_toplevel.geometry("600x600")
        assert self.ctk_toplevel.current_width == 400 and self.ctk_toplevel.current_height == 500
        assert self.ctk_toplevel.max_width == 400 and self.ctk_toplevel.max_height == 500

        self.ctk_toplevel.maxsize(1000, 1000)
        self.ctk_toplevel.geometry("300x400")
        self.ctk_toplevel.resizable(False, False)
        self.ctk_toplevel.geometry("500x600")
        assert self.ctk_toplevel.current_width == 500 and self.ctk_toplevel.current_height == 600
        print("successful")

    def test_scaling(self):
        print(" -> test_scaling: ", end="")

        customtkinter.ScalingTracker.set_window_scaling(1.5)
        self.ctk_toplevel.geometry("300x400")
        assert self.ctk_toplevel.current_width == 300 and self.ctk_toplevel.current_height == 400
        assert self.root_ctk.window_scaling == 1.5 * customtkinter.ScalingTracker.get_window_dpi_scaling(self.root_ctk)

        self.ctk_toplevel.maxsize(400, 500)
        self.ctk_toplevel.geometry("500x500")
        assert self.ctk_toplevel.current_width == 400 and self.ctk_toplevel.current_height == 500

        customtkinter.ScalingTracker.set_window_scaling(1)
        assert self.ctk_toplevel.current_width == 400 and self.ctk_toplevel.current_height == 500
        print("successful")

    def test_configure(self):
        print(" -> test_configure: ", end="")
        self.ctk_toplevel.configure(bg="white")
        assert self.ctk_toplevel.fg_color == "white"

        self.ctk_toplevel.configure(background="red")
        assert self.ctk_toplevel.fg_color == "red"
        assert self.ctk_toplevel.cget("bg") == "red"

        self.ctk_toplevel.config(fg_color=("green", "#FFFFFF"))
        assert self.ctk_toplevel.fg_color == ("green", "#FFFFFF")
        print("successful")

    def test_appearance_mode(self):
        print(" -> test_appearance_mode: ", end="")
        customtkinter.set_appearance_mode("light")
        self.ctk_toplevel.config(fg_color=("green", "#FFFFFF"))
        assert self.ctk_toplevel.cget("bg") == "green"

        customtkinter.set_appearance_mode("dark")
        assert self.ctk_toplevel.cget("bg") == "#FFFFFF"
        print("successful")

    def test_iconify(self):
        print(" -> test_iconify: ", end="")
        self.ctk_toplevel.iconify()
        self.ctk_toplevel.after(100, self.ctk_toplevel.deiconify)
        print("successful")


if __name__ == "__main__":
    TestCTkToplevel()
