from Tkinter import *
root = Tk()


frame = Frame(root, width=300, height=300)
frame.pack()

canvas = Canvas(frame, bg='#FFAABB', width=300, height=300, scrollregion=(0, 0, 500, 500))
l = Listbox(canvas)
for i in range(100):
    l.insert(END, str(i))
l.pack()
vbar = Scrollbar(frame, orient=VERTICAL)
vbar.pack(side=RIGHT, fill=Y)
vbar.config(command=l.yview)
canvas.config(width=300, height=300)
canvas.pack(side=LEFT,expand=True, fill=BOTH)
root.geometry('100x100')
root.mainloop()