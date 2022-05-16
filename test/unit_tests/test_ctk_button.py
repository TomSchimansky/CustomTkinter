import time
import customtkinter


class TestCTkButton():
    def __init__(self):
        self.root_ctk = customtkinter.CTk()
        self.ctk_button = customtkinter.CTkButton(self.root_ctk)
        self.ctk_button.pack(padx=20, pady=20)
        self.root_ctk.title(self.__class__.__name__)

    def clean(self):
        self.root_ctk.quit()
        self.root_ctk.withdraw()

    def main(self):
        self.execute_tests()
        self.root_ctk.mainloop()

    def execute_tests(self):
        print(f"\n{self.__class__.__name__} started:")

        start_time = 0

        self.root_ctk.after(start_time, self.test_iconify)
        start_time += 1500

        self.root_ctk.after(start_time, self.clean)

    def test_iconify(self):
        print(" -> test_iconify: ", end="")
        self.root_ctk.iconify()
        self.root_ctk.after(100, self.root_ctk.deiconify)
        print("successful")


if __name__ == "__main__":
    TestCTkButton().main()
