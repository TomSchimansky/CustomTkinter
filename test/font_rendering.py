import tkinter

app = tkinter.Tk()
app.geometry("600x500")


canvas = tkinter.Canvas(master=app, highlightthickness=0, bg="gray30")
canvas.pack(expand=True, fill="both")

text_1 = canvas.create_text(100, 100, text="⬤", font=('Helvetica','2','bold'))
text_2 = canvas.create_text(100, 200, text="⬤", font=('Helvetica','4','bold'))
text_3 = canvas.create_text(100, 300, text="⬤", font=('Helvetica','6','bold'))
text_4 = canvas.create_text(100, 400, text="⬤", font=('Helvetica',8,'bold'))
text_4 = canvas.create_text(400, 400, text="⬤", font=('Helvetica',80,'bold'))

app.mainloop()