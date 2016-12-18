__author__ = 'tapon'
from Tkinter import *
import ttk
from gui_interfaces.gui_settings import *
from controller.read_nodeB_input import *
import os
from tkMessageBox import *

class Demo(Frame):
    def __init__(self, parent=None, **args):
        Frame.__init__(self, parent, args)
        self.config()
        self.pack()
        self.var_db_update = IntVar()
        self.var_adj_type = StringVar()
        self.title = ["NodeB", "WCEL"]
        self.option_array = ['adjg', 'u_adjg']
        self.var_adj_type.set('adjg')
        for title, option in zip(self.title, self.option_array):

            x = ttk.Radiobutton(self,
                        text=title,
                        variable=self.var_adj_type,
                        value = option
                        )
            x.pack(side=TOP, anchor=NW, pady=(2, 0))






def askopenfile(var_input_filename):
    from tkFileDialog import askopenfilename
    filename = askopenfilename(initialdir=entry_local_working_dir.get())
    var_input_filename.set(filename)


def make():

    aInput = ReadNodeBInput(var_input_filename.get())
    aInput.open_file()
    aInput.read_ipnb()
    aInput.read_template()
    aInput.read_wcel()
    aInput.read_wbts()
    a = showinfo("Info", "Plan Generated")
    if a == "ok":
        os.startfile(entry_local_working_dir.get())
    pass




container_node_b_create = Frame()
Label(container_node_b_create, text="Node B Creation", fg="#005500", bg="#EEFFAA", height="2", font=(14)).pack()
frame_background = PhotoImage(file=os.getcwd()+'\\resources\\images\\banner.gif')
container_node_b_create.image = frame_background
frame1 = Frame(container_node_b_create)
frame1['borderwidth'] = 2
frame1['relief'] = 'groove'
frame1.pack(side=TOP, fill=X, padx=(5, 5), pady=(5, 5))
var_input_filename = StringVar()
var_input_filename.set(entry_local_working_dir.get()+'NodeBCrTemp.xlsx')
label_file_choose = ttk.Label(frame1, textvariable=var_input_filename).pack(side=LEFT, anchor=NW, fill=Y)
browse_button = ttk.Button(frame1, text='Browse', command = lambda : askopenfile(var_input_filename))
browse_button.pack(side=TOP, anchor=NE)

frame2 = ttk.Frame(container_node_b_create)
part = Demo(frame2)
part.pack(fill=X)
part.var_adj_type.set('adjg')
frame2.pack(side=TOP, fill=X, padx=(5, 5), pady=(5, 5))

make_button = ttk.Button(container_node_b_create, text="Create", command=lambda :make()).pack()

