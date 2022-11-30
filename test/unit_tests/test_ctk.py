import time
import customtkinter


class TestCTk():
    def __init__(self):
        self.root_ctk = customtkinter.CTk()
        self.root_ctk.title("TestCTk")

    def clean(self):
        self.root_ctk.quit()
        self.root_ctk.withdraw()

    def main(self):
        self.execute_tests()
        self.root_ctk.mainloop()

    def execute_tests(self):
        print("\nTestCTk started:")
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
        self.root_ctk.geometry("100x200+200+300")
        assert self.root_ctk.current_width == 100 and self.root_ctk.current_height == 200

        self.root_ctk.minsize(300, 400)
        assert self.root_ctk.current_width == 300 and self.root_ctk.current_height == 400
        assert self.root_ctk.min_width == 300 and self.root_ctk.min_height == 400

        self.root_ctk.maxsize(400, 500)
        self.root_ctk.geometry("600x600")
        assert self.root_ctk.current_width == 400 and self.root_ctk.current_height == 500
        assert self.root_ctk.max_width == 400 and self.root_ctk.max_height == 500

        self.root_ctk.maxsize(1000, 1000)
        self.root_ctk.geometry("300x400")
        self.root_ctk.resizable(False, False)
        self.root_ctk.geometry("500x600")
        assert self.root_ctk.current_width == 500 and self.root_ctk.current_height == 600
        print("successful")

    def test_scaling(self):
        print(" -> test_scaling: ", end="")

        customtkinter.ScalingTracker.set_window_scaling(1.5)
        self.root_ctk.geometry("300x400")
        assert self.root_ctk._current_width == 300 and self.root_ctk._current_height == 400
        assert self.root_ctk.window_scaling == 1.5 * customtkinter.ScalingTracker.get_window_dpi_scaling(self.root_ctk)

        self.root_ctk.maxsize(400, 500)
        self.root_ctk.geometry("500x500")
        assert self.root_ctk._current_width == 400 and self.root_ctk._current_height == 500

        customtkinter.ScalingTracker.set_window_scaling(1)
        assert self.root_ctk._current_width == 400 and self.root_ctk._current_height == 500
        print("successful")

    def test_configure(self):
        print(" -> test_configure: ", end="")
        self.root_ctk.configure(bg="white")
        assert self.root_ctk.cget("fg_color") == "white"

        self.root_ctk.configure(background="red")
        assert self.root_ctk.cget("fg_color") == "red"
        assert self.root_ctk.cget("bg") == "red"

        self.root_ctk.config(fg_color=("green", "#FFFFFF"))
        assert self.root_ctk.cget("fg_color") == ("green", "#FFFFFF")
        print("successful")

    def test_appearance_mode(self):
        print(" -> test_appearance_mode: ", end="")
        customtkinter.set_appearance_mode("light")
        self.root_ctk.config(fg_color=("green", "#FFFFFF"))
        assert self.root_ctk.cget("bg") == "green"

        customtkinter.set_appearance_mode("dark")
        assert self.root_ctk.cget("bg") == "#FFFFFF"
        print("successful")

    def test_iconify(self):
        print(" -> test_iconify: ", end="")
        self.root_ctk.iconify()
        self.root_ctk.after(100, self.root_ctk.deiconify)
        print("successful")


if __name__ == "__main__":
    TestCTk().main()
