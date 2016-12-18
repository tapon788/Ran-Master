from Tkinter import *#Tk, Frame, BOTH

import Tkinter
from PIL import Image, ImageTk
import os
class Example(Frame):

   def __init__(self, parent):
      Frame.__init__(self, parent)
      self.parent = parent
      self.initUI()

   def initUI(self):

      self.parent.title("PISE")
      self.pack(fill=BOTH, expand=1)

root = Tk()
root.geometry("1111x675+300+300")
app = Example(root)

im = Image.open('C:\\Python27\\Adjacency\\resources\\images\\banner.gif')
tkimage = ImageTk.PhotoImage(im)
Tkinter.Label(root, image= tkimage).pack()

custName = StringVar(None)
yourName = Entry(app, textvariable=custName)
yourName.pack()

relStatus = StringVar()
relStatus.set(None)

labelText = StringVar()
labelText.set('Accuracy Level')
label1 = Label(app, textvariable=labelText, height=2)
label1.pack()

radio1 = Radiobutton(app, text='100%', value='1', variable = relStatus, ).pack()
radio2 = Radiobutton(app, text='50%', value='5', variable = relStatus, ).pack()

root.mainloop()