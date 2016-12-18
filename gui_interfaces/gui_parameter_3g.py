__author__ = 'tpaul'
__author__ = 'tpaul'

from Tkinter import *
import ttk

from controller.parameter import Paramchange
from controller.generate_plan import read_input
from gui_interfaces.gui_settings import *

def askopenfile(var_input_filename):
    from tkFileDialog import askopenfilename
    filename = askopenfilename(initialdir=entry_local_working_dir.get())
    var_input_filename.set(filename)

def make(in_output_type, in_sheet_index):
    if in_output_type== 'MML':

        pc = Paramchange()
        pc.readxl(var_input_filename.get(), in_sheet_index)
        pc.GuiMap()
        pc.IntGuiConv()
        pc.CmdMaker()
        commands = pc.CmdCombiner()
        pc.writer(commands)
    else:
        aReadInput = read_input(var_input_filename.get(), in_sheet_index)
        aReadInput.ReadExcel()
        aReadInput.main()
    pass

container_parameter_3g = Frame()
frame1 = Frame(container_parameter_3g)
frame1['borderwidth'] = 2
frame1['relief'] = 'groove'
frame1.pack(side=TOP, fill=X, padx=(5, 5), pady=(5, 5))
var_input_filename = StringVar()
var_input_filename.set(entry_local_working_dir.get()+'input_nsn.xlsx')
label_file_choose = ttk.Label(frame1, textvariable=var_input_filename).pack(side=LEFT, anchor=NW, fill=Y)
browse_button = ttk.Button(frame1, text='Browse', command = lambda : askopenfile(var_input_filename))
browse_button.pack(side=TOP, anchor=NE)

make_xml = ttk.Button(container_parameter_3g, text="Make XML", command=lambda : make('XML', 1)).pack()

